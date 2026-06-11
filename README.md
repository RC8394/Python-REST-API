-Instructions-

Clone the repository:

git clone <repository-url>
cd Python-Rest-API

Install dependencies:

pip install fastapi uvicorn sqlalchemy pydantic

Start the development server:

py -m uvicorn main:app --reload

You should see:

INFO: Uvicorn running on http://127.0.0.1:8000


-Example Output-

PUT /benchmarks/{benchmark_id}

Example Request:

{
  "benchmark_name": "Geekbench 6",
  "platform": "Ubuntu 24.04",
  "score": 3300,
  "cv_percent": 1.55
}
