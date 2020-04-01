import pymongo
import os
from datetime import datetime

client = pymongo.MongoClient(host=os.getenv('COVID_HOST'),
                             username=os.getenv('COVID_USER'),
                             password=os.getenv('COVID_PASS'),
                             authSource=os.getenv('COVID_DB'))
db = client[os.getenv('COVID_DB')]


def search_abstracts(text, collection, limit=100, covid19_only=False):
    """
    Search on the abstracts collection

    Inputs:
            text (str): text to search. Searches both entities and text matches
            collection (str): name of collection on which to search
            limit (int): number of abstracts to return.

    Returns:
            Dict with keys:
                Exact Matches
                Partial Matches
                Calendar
    """

    # First get the exact text matches
    abstracts_exact, ids_exact = __search_exact(text, collection, limit, covid19_only)

    remaining_limit = limit - len(abstracts_exact)

    # If we don't have at least limit results, get partial matches
    if remaining_limit >= 1:
        abstracts_partial = __search_partial(
            text, collection, remaining_limit, ids_exact, covid19_only)
    else:
        abstracts_partial = []

    abstracts_exact = [{k: v for k, v in a.items() if
                        k not in ['_id', "_bt", "body_text", "PDF_gridfs_id", "pdf_location", "submission_email",
                                  "crossref_raw_result"]}
                       for a in abstracts_exact]
    for k in abstracts_exact:
        k["last_updated"] = k["last_updated"].strftime("%m/%d/%Y, %H:%M:%S")
        if 'publication_date' in k.keys() and k['publication_date'] is not None:
            k['publication_date'] = k['publication_date'].strftime("%m/%d/%Y, %H:%M:%S")

    abstracts_partial = [{k: v for k, v in a.items() if
                          k not in ['_id', "_bt", "body_text", "PDF_gridfs_id", "pdf_location", "submission_email",
                                    "crossref_raw_result"]}
                         for a in abstracts_partial]
    for k in abstracts_partial:
        k["last_updated"] = k["last_updated"].strftime("%m/%d/%Y, %H:%M:%S")
        if 'publication_date' in k.keys() and k['publication_date'] is not None:
            k['publication_date'] = k['publication_date'].strftime("%m/%d/%Y, %H:%M:%S")

    # Jam it all in a dict to hand over to the front end
    return_dict = dict()
    return_dict['full'] = abstracts_exact
    return_dict['partial'] = abstracts_partial
    return return_dict


def get_all():
    """
    Return all submissions.

    """
    entries = list(db.google_form_submissions.find({}))
    entries = [{k: v for k, v in a.items() if
                k not in ['_id', "last_updated", "PDF_gridfs_id", "pdf_location", "submission_email",
                          "crossref_raw_result"]}
               for a in entries]
    for e in entries:
        if 'publication_date' in e.keys():
            e['publication_date'] = e['publication_date'].strftime("%m/%d/%Y, %H:%M:%S")

    return entries


def k_most_recently_submitted(k):
    """
    Get the k most recent submissions through the google form
    """
    entries = list(db.google_form_submissions.find({}).sort("publication_date", -1).limit(k))

    entries = [{k: v for k, v in a.items() if
                k not in ['_id', "last_updated", "PDF_gridfs_id", "pdf_location", "submission_email",
                          "crossref_raw_result"]}
               for a in entries]
    for e in entries:
        if 'publication_date' in e.keys():
            e['publication_date'] = e['publication_date'].strftime("%m/%d/%Y")

    return entries


def k_most_recently_published(k, only_is_covid=True):
    """
    Get the k most recent submissions through the google form
    """

    needed_fields = ["abstract",
                     "title",
                     "authors",
                     "journal",
                     "publication_date",
                     "category_human",
                     "doi",
                     "is_covid19",
                     "similar_abstracts",
                     "link",
                     "keywords",
                     "keywords_ML",
                     "summary_human",
                     "summary_ML",
                     "has_year",
                     "has_month",
                     "has_day",
                     "similar_abstracts"
                     ]
    returned_fields = ["abstract",
                       "title",
                       "authors",
                       "journal",
                       "publication_date",
                       "doi",
                       "similar_abstracts",
                       "link",
                       "keywords",
                       "keywords_ML",
                       "summary_human",
                       "summary_ML",
                       "similar_abstracts"
                       ]
    projection = {field: 1 for field in needed_fields}

    if only_is_covid:
        query = {"is_covid19": True, "publication_date": {"$lt": datetime.now()}}
    else:
        query = {"publication_date": {"$lt": datetime.now()}}

    entries = list(db.entries.find(query, projection).sort("publication_date", -1).limit(k))
    for entry in entries:
        if "keywords_ML" not in entry or entry["keywords_ML"] is None:
            entry["keywords_ML"] = []

    entries = [{k: v for k, v in a.items() if k in returned_fields} for a in entries]

    for e in entries:
        if "has_day" in e and "has_year" in e and "has_month" in e and e["has_year"] is not None:
            day = "%d/" if e["has_day"] and e["has_month"] else ""
            month = "%m/" if e["has_month"] else ""
            year = "%Y"
            time_string = month + day + year
        else:
            time_string = "%m/%d/%Y"
        e['publication_date'] = e['publication_date'].strftime(time_string)
    return entries


def __search_exact(text, collection, limit, covid19_only=False):
    """
    Find exact matches for text search
    In order of priority, we perform;
    1) Exact entity match on text
    2) Exact phrase match on text
    Until at least (limit) abstracts are found
    Inputs:
            text (str): text to search. Searches both entities and text matches
            collection (str): name of collection to search over
            limit (int): number of abstracts to return.
            covid19_only (bool): whether to restrict only to those entries about covid19

    Returns:
            List of abstract dicts
    """
    abstracts = []
    # First try an exact entity match
    pipeline = []

    pipeline.append(
        {"$match": {"keywords": {"$regex": text, "$options": "imx"}}})

    if covid19_only:
        pipeline.append(
            {"$match": {"is_covid19": True}})

    pipeline.append({"$limit": limit})

    abstracts += [a for a in db[collection].aggregate(pipeline)]

    # See if we have at least limit results
    if len(abstracts) >= limit:
        return abstracts

    # Next try an exact phrase match on text fields
    pipeline = []

    pipeline.append({"$match": {'$text': {'$search': "\"{}\"".format(text)}}})

    if covid19_only:
        pipeline.append(
            {"$match": {"is_covid19": True}})

    pipeline.append({'$sort': {'score': {'$meta': "textScore"}}})

    pipeline.append({"$limit": limit})

    abstracts += [a for a in db[collection].aggregate(pipeline)]
    # Remove duplicates
    abstracts = [i for n, i in enumerate(abstracts) if str(i['_id']) not in [
        str(a['_id']) for a in abstracts[:n]]]
    # Keep a list of ids to make sure we dont find them again in partial matches
    ids = [a['_id'] for a in abstracts]
    # Clean '_id' key
    abstracts = [{k: v for k, v in a.items() if
                  k not in ['_id', "PDF_gridfs_id", "pdf_location", "submission_email", "crossref_raw_result"]}
                 for a in abstracts]
    return abstracts, ids


def __search_partial(text, collection, limit, ids_exact, covid19_only=False):
    """
    Find partial matches for text search
    Until at least (limit) abstracts are found
    Inputs:
            text (str): text to search. Searches both entities and text matches
            collection (str): name of collection to search over
            limit (int): number of abstracts to return.
            ids_exact (list): ids of exact matches
            covid19_only (bool): whether to restrict only to those entries about covid19

    Returns:
            List of abstract dicts
    """

    # Finally try a general search on text fields
    pipeline = []

    pipeline.append({"$match": {'$text': {'$search': text}}})

    if covid19_only:
        pipeline.append(
            {"$match": {"is_covid19": True}})

    pipeline.append({'$sort': {'score': {'$meta': "textScore"}}})

    pipeline.append({"$match": {"_id": {"$nin": ids_exact}}})

    pipeline.append({"$limit": limit})

    abstracts = [a for a in db[collection].aggregate(pipeline)]

    # clean '_id' key
    abstracts = [{k: v for k, v in a.items() if
                  k not in ['_id', "PDF_gridfs_id", "submission_email", "pdf_location", "crossref_raw_result"]}
                 for a in abstracts]

    return abstracts
