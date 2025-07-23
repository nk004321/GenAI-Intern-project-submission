from fastapi import FastAPI, Request
from pydantic import BaseModel
import sqlite3
from llm_handler import ask_gemini
import re # Import the re module for regular expressions

app = FastAPI()

DB_PATH = "database/ecommerce.db"

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: QueryRequest):
    user_question = req.question

    # Send question to Gemini to get SQL query
    prompt = f"""
    You are an assistant. Convert the following question into an SQLite SQL query.
    Table names are: ad_sales, total_sales, eligibility.
    Only return the SQL query, nothing else. Do not include any markdown formatting (e.g., ```sql).
    Question: {user_question}
    """
    # Emphasize to Gemini not to include markdown formatting in the prompt.
    raw_sql_query = ask_gemini(prompt)

    # Clean the SQL query: remove Markdown code block formatting if present
    # This regex looks for ``` (optional 'sql' or other language specifier)
    # followed by the content, and then ``` at the end. It extracts the content.
    clean_sql_query = re.sub(r"```(?:sql)?\s*([\s\S]*?)\s*```", r"\1", raw_sql_query).strip()

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(clean_sql_query) # Execute the cleaned query
        rows = cursor.fetchall()
        col_names = [description[0] for description in cursor.description]
        conn.close()

        # Format result
        results = [dict(zip(col_names, row)) for row in rows]
        return {"question": user_question, "sql": clean_sql_query, "result": results}

    except Exception as e:
        return {"error": str(e), "sql_attempted": clean_sql_query} # Return the cleaned query for debugging