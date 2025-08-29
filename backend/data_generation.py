import os
import time
from faker import Faker
from dotenv import load_dotenv
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

load_dotenv()

ES_HOST = f"http://localhost:{os.getenv('ES_PORT')}"
INDEX_NAME = f"{os.getenv('ES_INDEX')}"

NUMBER_OF_DOCUMENTS = 2500000   

es = Elasticsearch(ES_HOST)
fake = Faker()

def create_index():
    """Creates the Elasticsearch index with the simplified mapping."""
    if es.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists. Deleting it.")
        es.indices.delete(index=INDEX_NAME)

    mapping = {
      "mappings": {
        "properties": {
          "user_id": { "type": "keyword" },
          "name": { "type": "text" },
          "email": { "type": "keyword" },
          "country": { "type": "keyword" }
        }
      }
    }
    print(f"Creating index '{INDEX_NAME}' with the new mapping.")
    es.indices.create(index=INDEX_NAME, body=mapping)

def generate_data_stream():
    """
    Generator function to yield simplified fake documents.
    """
    print(f"Starting to generate {NUMBER_OF_DOCUMENTS} documents...")
    for i in range(NUMBER_OF_DOCUMENTS):
        if i > 0 and i % 50000 == 0:
            print(f"  Generated {i} documents...")
        
        yield {
            "_index": INDEX_NAME,
            "_source": {
                "user_id": fake.uuid4(),
                "name": fake.name(),
                "email": fake.email(),
                "country": fake.country()
            }
        }

if __name__ == "__main__":
    start_time = time.time()
    
    create_index()

    print("Ingesting data using bulk API...")
    try:
        successes, failures = bulk(es, generate_data_stream(), chunk_size=1000, request_timeout=200)
        print(f"Successfully ingested {successes} documents.")
        if failures:
            print(f"Failed to ingest {len(failures)} documents.")
    except Exception as e:
        print(f"An error occurred: {e}")

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds.")