import sentry_sdk
from fastapi import FastAPI
from search_api.database import CovidscholarDB
from starlette.responses import JSONResponse
from search_api.api.search import search_abstracts, get_all

db = CovidscholarDB()
app = FastAPI()

# Sentry Error Logging
sentry_sdk.init(
    dsn="https://230802b6ec5a4433b7c4c0bc74401665@sentry.io/1480752"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/test/{test_string}")
async def test_api(test_string: str):
    return test_string


@app.get("/entries/")
async def search_entries(title: str = "", abstract: str = ""):
    query_string = title
    if abstract != "":
        query_string += abstract
    result = [{k: str(v) for k, v in e.items() if k != "_id"} for e in
              db.entries.find({"$text": {"$search": query_string}})]
    return JSONResponse(result)


@app.post("/search/")
async def search(text: str = "", limit: int = 500):
    abstracts = search_abstracts(text, limit=limit)
    return JSONResponse(abstracts)


@app.get("/submissions/")
async def search():
    return JSONResponse(get_all())


# Entries collection format
"""
{
*"Title": string,
"Authors": {
[*"Name": string (preference for first initial last format),
"Affiliation": string,
"Email": string
]
}
*"Doi": string,
"Journal" string,
"Publication Date": Datetime.Datetime object,
"Abstract": string,
"Origin": string, source scraped from/added from,
"Last Updated: Datetime.Datetime object, timestamp of last update,
"Body Text": {
["Section Heading": string,
"Text": string
]
}
"Citations": list of dois,
"Link": use given if available, otherwise build from doi
"Category_human": string,
"Category_ML": string,
"Tags_human": list of strings,
"Tags_ML": list of strings,
"Relevance_human": string,
"Relevance_ML": string,
"Summary_human": string,
"Summary_ML": string

}
"""
