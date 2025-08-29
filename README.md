Elasticsearch Search and Download Application
This project is a full-stack application designed to efficiently handle, search, and export large datasets. It features a Python backend using FastAPI and a vanilla JavaScript frontend that interacts with an Elasticsearch database. The system can ingest approximately 600MB of simulated user data and provides a clean interface for filtering, viewing paginated results, and downloading the filtered data as a JSONL file.

Screenshot
Here is a screenshot of the final application interface:

Tech Stack
Backend:

Python 3

FastAPI (for the REST API)

Uvicorn (as the ASGI server)

Database / Search Engine:

Elasticsearch 8.x

Frontend:

HTML5

CSS3

Vanilla JavaScript

Data Simulation:

Faker Library

Environment:

Docker (for running Elasticsearch)

Key Features
Efficient Data Ingestion: A Python script generates and streams ~600MB (4.5 million records) of fake user data directly into Elasticsearch without saving a large file to disk.

Fast Full-Text Search: The backend leverages Elasticsearch's multi_match query to search across multiple fields (user_id, name, email, country).

Typo Tolerance: The search includes fuzziness to return relevant results even with minor spelling errors.

Paginated Results: The frontend displays results in a clean, paginated table to handle large query responses without overwhelming the user.

Streaming Downloads: Filtered results can be downloaded as a .jsonl file. The backend streams the data directly from Elasticsearch to the user, ensuring low memory usage on the server.

Setup and Installation
Follow these steps to get the project running on your local machine.

Prerequisites
Git

Python 3.10+

Docker Desktop

1. Clone the Repository
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME

2. Set Up the Backend
Create and activate a Python virtual environment.

# Create a virtual environment
python -m venv venv

# Activate it
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
# source venv/bin/activate

Install the required Python packages.

pip install -r requirements.txt

(Note: You will need to create a requirements.txt file by running pip freeze > requirements.txt in your activated environment.)

3. Start the Elasticsearch Container
Make sure Docker Desktop is running. Then, run the following command in your terminal to start an Elasticsearch container.

docker run -p 9200:9200 --name es-dev -e "discovery.type=single-node" -e "xpack.security.enabled=false" -d docker.elastic.co/elasticsearch/elasticsearch:8.14.1

4. Ingest the Data
Navigate to the data_ingestion folder and run the script to generate and load the data into Elasticsearch. This will take several minutes.

cd data_ingestion
python generate_and_ingest.py
cd ..

5. Run the Backend Server
Start the FastAPI backend server using Uvicorn.

uvicorn main:app --reload --port 8001

The backend API will now be running at http://127.0.0.1:8001.

6. Run the Frontend Server
Open a new terminal window. Navigate into the frontend folder and start a simple Python web server.

cd frontend
python -m http.server 8000

How to Use
Open your web browser and navigate to http://localhost:8000.

Use the search bar to filter users by their ID, name, email, or country.

Use the "Next" and "Previous" buttons to navigate through the paginated results.

Click the "Download Filtered Results" button to download the current search results as a user_results.jsonl file.

API Endpoints
The backend exposes two main endpoints:

POST /search

Accepts a JSON payload to search for users.

Payload: { "query": "search_term", "page": 1 }

Returns a paginated list of user objects.

POST /download

Accepts a JSON payload to download filtered user data.

Payload: { "query": "search_term" }

Streams a .jsonl file as a response.