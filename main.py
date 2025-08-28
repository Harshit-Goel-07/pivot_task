import json
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
from typing import Optional


# Create main FastAPI application.
app = FastAPI()

# Connect to Elasticsearch database.
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "users"

# This part allows your HTML/JavaScript frontend to make requests
# to this Python backend. It's a standard security feature.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API Endpoints ---

# This creates the "/search" URL for our API.
# It listens for POST requests.
# In main.py, replace your entire @app.post("/search") function with this block.

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

    size = 15  # Using 15 to match the frontend's resultsPerPage
    from_offset = (page - 1) * size

    # This is the search query we'll send to Elasticsearch.
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

    # Send the query to Elasticsearch and return the results.
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
            # Yield each user as a JSON string followed by a newline.
            yield json.dumps(user['_source']) + '\n'
        
        search_query['search_after'] = hits[-1]['sort']

    es.close_point_in_time(body={'id': pit_id})
# This creates the "/download" URL for our API.
@app.post("/download")
def handle_download_requests(query: Optional[str] = Body(None, embed=True)):
    """
    This function handles download requests. It streams all matching users
    back to the browser as a downloadable JSONL file.
    """
    print(f"Downloading results for: '{query}' as JSONL")
    
    return StreamingResponse(
        stream_all_users(query),
        media_type="application/x-ndjson",  # The official media type for JSON Lines
        headers={"Content-Disposition": "attachment; filename=user_results.jsonl"} # Changed file extension
    )