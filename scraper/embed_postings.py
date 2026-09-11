import os
import psycopg2
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

def get_db_connection():
    return psycopg2.connect(
        dbname="devpulse",
        user="devpulse_user",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432"
    )

def embed_text(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values

def run(limit=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT id, description FROM job_postings WHERE embedding IS NULL"
    if limit:
        query += f" LIMIT {limit}"

    cursor.execute(query)
    rows = cursor.fetchall()

    print(f"Found {len(rows)} postings to embed.")

    for posting_id, description in rows:
        if not description:
            print(f"Skipping posting {posting_id} — no description text.")
            continue

        vector = embed_text(description)
        cursor.execute(
            "UPDATE job_postings SET embedding = %s WHERE id = %s",
            (vector, posting_id)
        )
        conn.commit()
        print(f"Embedded posting {posting_id}.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    run(limit=15)