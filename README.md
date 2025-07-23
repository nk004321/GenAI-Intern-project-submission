SQL Query Generator with Gemini API
This project provides a FastAPI application that acts as an intelligent assistant, converting natural language questions into SQLite SQL queries using the Gemini API. It then executes these queries against a local SQLite database and returns the results.

Features
Natural Language to SQL: Converts user questions into executable SQLite queries.

Database Interaction: Executes generated SQL queries against a specified SQLite database.

API Endpoint: Provides a /ask endpoint to receive questions and return query results.

Error Handling: Includes basic error handling for SQL execution.

Project Structure
main.py: The core FastAPI application, handling API requests, calling the LLM, executing SQL, and returning responses.

llm_handler.py: Contains the ask_gemini function responsible for making API calls to the Gemini model.

config.py: Stores sensitive information like the Gemini API key.

database/ecommerce.db: (Assumed) The SQLite database file containing the ad_sales, total_sales, and eligibility tables.

Setup
Follow these steps to set up and run the project locally:

1. Prerequisites
Python 3.8+

pip (Python package installer)

2. Clone the Repository
If you haven't already, clone this repository to your local machine:

git clone <repository_url>
cd <repository_directory>

3. Install Dependencies
Install the required Python packages using pip:

pip install fastapi uvicorn pydantic requests

4. Configure Gemini API Key
Obtain a Gemini API key from the Google AI Studio.

Open config.py and replace "YOUR_GEMINI_API_KEY" with your actual API key:

# config.py
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

5. Prepare the Database
Ensure you have an SQLite database named ecommerce.db in a database/ directory relative to your project root. This database should contain the tables ad_sales, total_sales, and eligibility.

If you don't have one, you can create a dummy one for testing:

# You can run this once to create a dummy database for testing
import sqlite3

conn = sqlite3.connect('database/ecommerce.db')
cursor = conn.cursor()

# Create dummy tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ad_sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        revenue REAL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS total_sales (
        id INTEGER PRIMARY KEY,
        date TEXT,
        amount REAL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS eligibility (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        status TEXT
    )
''')

# Insert some dummy data
cursor.execute("INSERT INTO ad_sales (product, revenue) VALUES ('Laptop', 1200.50)")
cursor.execute("INSERT INTO ad_sales (product, revenue) VALUES ('Mouse', 25.00)")
cursor.execute("INSERT INTO total_sales (date, amount) VALUES ('2023-01-01', 5000.00)")
cursor.execute("INSERT INTO eligibility (user_id, status) VALUES (101, 'Eligible')")

conn.commit()
conn.close()
print("Dummy database 'ecommerce.db' created with sample data.")

6. Run the Application
Start the FastAPI application using Uvicorn:

uvicorn main:app --reload

The --reload flag will automatically restart the server when you make code changes.

The application will typically run on http://127.0.0.1:8000.

Usage
Once the server is running, you can send POST requests to the /ask endpoint with your natural language questions.

Example Request (using curl)
curl -X POST "http://127.0.0.1:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the total revenue from ad sales?"}'

Example Response
{
  "question": "What is the total revenue from ad sales?",
  "sql": "SELECT SUM(revenue) FROM ad_sales",
  "result": [
    [1225.5]
  ]
}

Example Error Response
If there's an issue with the generated SQL query or database interaction, you might receive an error:

{
  "error": "near \"FROM\": syntax error",
  "sql_attempted": "SELECT revenue FROM ad_sales WHERE product = 'Laptop' AND"
}

API Endpoints
POST /ask
Description: Converts a natural language question into an SQL query, executes it, and returns the result.

Request Body:

{
  "question": "string"
}

Response:

Success (200 OK):

{
  "question": "string",
  "sql": "string",
  "result": "array"
}

Error (200 OK with error field):

{
  "error": "string",
  "sql_attempted": "string"
}

Contributing
Feel free to fork the repository, make improvements, and submit pull requests.

License
This project is open-source and available under the MIT License.
