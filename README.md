# Elasticsearch User Search Application

This project is a full-stack web application built to efficiently search, filter, and download data from a large (~600MB) dataset stored in Elasticsearch. It features a Python FastAPI backend for high-performance API endpoints and a clean, lightweight frontend built with vanilla HTML, CSS, and JavaScript.

## Features

-   **Efficient Data Ingestion**: A Python script generates ~3.5 million mock user records and bulk-uploads them directly into Elasticsearch without saving large files to disk.
-   **Fast API Backend**: Built with FastAPI to provide fast, asynchronous API endpoints for search and download.
-   **Fuzzy Search**: Implements Elasticsearch's `multi_match` query with `fuzziness` enabled, allowing users to find results even with minor typos.
-   **Paginated Results**: The frontend displays results in a clean, paginated table, and the backend efficiently serves data page by page.
-   **Streaming Downloads**: Users can download the complete filtered dataset as a **JSONL** (JSON Lines) file. The data is streamed from the backend to ensure low memory usage, even with millions of records.
-   **Dockerized Database**: Elasticsearch runs in a Docker container for easy setup and a clean development environment.

---

## Tech Stack

-   **Backend**: Python, FastAPI
-   **Database**: Elasticsearch
-   **Frontend**: HTML, CSS, JavaScript
-   **Containerization**: Docker
-   **Python Libraries**: `elasticsearch`, `uvicorn`, `faker`

---

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### 1. Prerequisites

-   Python 3.7+
-   Docker Desktop installed and running.
-   Git for cloning the repository.

### 2. Clone the Repository

Clone this repository to your local machine:
```bash
git clone [https://github.com/Harshit-Goel-07/pivot_task.git](https://github.com/Harshit-Goel-07/pivot_task.git)
cd pivot_task
```

### 3. Setup the Backend Environment

Create and activate a Python virtual environment:

```Bash

# On Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install the required packages:

```Bash

pip install -r requirements.txt
```

### 4. Start the Services
1. Start the Elasticsearch Container
Make sure Docker Desktop is running, then run this command in your terminal:

```Bash

docker run -p 9200:9200 --name es-dev -e "discovery.type=single-node" -e "xpack.security.enabled=false" -d docker.elastic.co/elasticsearch/elasticsearch:8.14.1
```
2. Run the Data Ingestion Script
This script will create the index and populate it with mock data. This process will take several minutes.

```Bash

cd data_ingestion
python generate_and_ingest.py
cd ..
```
3. Start the FastAPI Backend Server
From the main project directory (pivot_task), run:

```Bash

uvicorn main:app --reload --port 8001
```
Your backend is now running at http://127.0.0.1:8001.

### 5. Run the Frontend
Open a new, separate terminal window.

Navigate to the frontend folder and start a simple Python web server:

```Bash

cd frontend
python -m http.server
```
(Note: This usually runs on port 8000. If that port is busy, you can specify another, like python -m http.server 8080)

### 6. Access the Application
Open your web browser and navigate to:
http://localhost:8000 (or the port your frontend server is using).

## API Endpoints
The backend provides two main API endpoints:

- POST /search: Accepts a JSON body with a query string and a page number. It returns a paginated list of matching user records.

- POST /download: Accepts a JSON body with a query string. It streams the complete set of matching user records as a user_results.jsonl file.