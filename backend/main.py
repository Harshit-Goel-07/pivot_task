import os
import json
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Body
from elasticsearch import Elasticsearch
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

es = Elasticsearch(f"http://localhost:{os.getenv('ES_PORT')}")
INDEX_NAME = f"{os.getenv('ES_INDEX')}"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/search")
def handle_search_requests(
    query: Optional[str] = Body(None, embed=True), 
    page: int = Body(1, embed=True)
):
    """
    This function handles search requests from the frontend.
    It searches for users in Elasticsearch and returns one page of results.
    """
    print(f"Searching for: '{query}' on page {page}")

    size = 15 
    from_offset = (page - 1) * size

    search_query = {
        "from": from_offset,
        "size": size,
        "query": {
            "multi_match": {
                "query": query if query else "",
                "fields": ["user_id", "name", "email", "country"],
                "fuzziness": "AUTO"
            }
        }
    }
    
    if not query:
        search_query["query"] = {"match_all": {}}

    response = es.search(index=INDEX_NAME, body=search_query)
    return {
        "total": response['hits']['total']['value'],
        "results": [hit['_source'] for hit in response['hits']['hits']]
    }


def stream_all_users(query: Optional[str]):
    """
    This is a helper for the download function. It gets ALL matching users
    from Elasticsearch and streams them as JSON Lines (one JSON object per line).
    """
    pit = es.open_point_in_time(index=INDEX_NAME, keep_alive="1m")
    pit_id = pit['id']

    search_query = {
        "size": 1000,
        "query": {"multi_match": {"query": query if query else "", "fields": ["user_id", "name", "email", "country"]}},
        "pit": {"id": pit_id, "keep_alive": "1m"},
        "sort": ["_doc"]
    }
    if not query:
        search_query["query"] = {"match_all": {}}

    while True:
        response = es.search(body=search_query)
        hits = response['hits']['hits']
        if not hits:
            break
        
        for user in hits:
            yield json.dumps(user['_source']) + '\n'
        
        search_query['search_after'] = hits[-1]['sort']

    es.close_point_in_time(body={'id': pit_id})

@app.post("/download")
def handle_download_requests(query: Optional[str] = Body(None, embed=True)):
    """
    This function handles download requests. It streams all matching users
    back to the browser as a downloadable JSONL file.
    """
    print(f"Downloading results for: '{query}' as JSONL")
    
    return StreamingResponse(
        stream_all_users(query),
        media_type="application/x-ndjson", 
        headers={"Content-Disposition": "attachment; filename=user_results.jsonl"} 
    )