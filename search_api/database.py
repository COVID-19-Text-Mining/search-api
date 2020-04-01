from pymongo import MongoClient
from elasticsearch import Elasticsearch
import os
import certifi


class CovidscholarDB:
    """
    Main class for accessing the CovidScholar DB

    """

    def __init__(self):
        self._client = MongoClient(os.getenv("COVID_HOST"), username=os.getenv("COVID_USER"),
                             password=os.getenv("COVID_PASS"), authSource=os.getenv("COVID_DB"))
        self._mongo_db = self._client[os.getenv("COVID_DB")]
        self.entries = self._mongo_db.entries_corrupt
        self.submissions = self._mongo_db.google_form_submissions

        # self._elastic_db = Elasticsearch(hosts=[os.environ["COVID_ELASTIC_HOST"]],
        #                                  http_auth=(os.environ['COVID_ELASTIC_USER'],
        #                                             os.environ['COVID_ELASTIC_PASS']),
        #                                  use_ssl=True,
        #                                  ca_certs=certifi.where())


    def search_text(self, text, dois=(), limit=100):
        """
        Performs a text-based search on the abstracts in the Matscholar database.
        If a list of dois is provided, only documents with dois from that list
        are returned. Results are sorted in order of decreasing relevance.

        Args:
            text: (str) Text for natural language search on abstracts.
            dois: (list of str, optional) DOIs to search within.
            limit: (int) Max number of results to return. Default is 100.

        Returns:
            List of results. Dictionaries with dois and scores.

        """
        lim = limit
        if text is None:
            return None
        if limit is None or limit == 0:
            lim = 10000

        text_query = {"simple_query_string": {"query": text,
                                              "fields": ["title", "abstract"]}}
        query_dict = {"bool": {}}
        query_dict["bool"]["must"] = text_query
        if dois:
            doi_filter = {"terms": {"doi.keyword": dois}}
            query_dict["bool"]["filter"] = doi_filter
        query = {"query": query_dict, "_source": ["doi"]}
        hits = self._elastic_db.search(index="%s.entries".format(os.getenv("COVID_DB")),
                                       body=query, size=lim,
                                       request_timeout=30)["hits"]["hits"]
        hits = [{"doi": hit["_source"]["doi"],
                 "score": hit["_score"]}
                for hit in hits]
        return hits
