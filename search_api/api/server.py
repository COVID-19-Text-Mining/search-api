import sentry_sdk
from fastapi import FastAPI
from search_api.database import CovidscholarDB
from starlette.responses import JSONResponse
from search_api.api.search import search_abstracts, get_all, k_most_recently_published, k_most_recently_submitted
from pprint import pprint

db = CovidscholarDB()
app = FastAPI()

# Sentry Error Logging
sentry_sdk.init(
    dsn="https://cc3f924ad01c4e1797438ad8ce49f32c@sentry.io/5172541"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/test/{test_string}")
async def test_api(test_string: str):
    return test_string


@app.post("/entries/")
async def entries(text: str = "", limit: int = 100, covid19_only: bool = False):
    abstracts = search_abstracts(text, limit=limit, collection="entries", covid19_only=covid19_only)
    return JSONResponse(abstracts)


@app.post("/search/")
async def search(text: str = "", limit: int = 100, covid19_only: bool = False):
    abstracts = search_abstracts(text, limit=limit, collection="google_form_submissions", covid19_only=covid19_only)
    return JSONResponse(abstracts)


@app.get("/submissions/")
async def get_all_submissions():
    return JSONResponse(get_all())

@app.get("/most_recent/")
async def get_most_recent():
    most_recent_papers = k_most_recently_submitted(20)
    return JSONResponse(most_recent_papers)

@app.get("/recent/")
async def get_most_recently_published():
    most_recent_papers = k_most_recently_published(20)
    return JSONResponse(most_recent_papers)

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
