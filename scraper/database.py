import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def _get_or_create_company(cursor, company_name):
    cursor.execute("SELECT id FROM companies WHERE name = %s", (company_name, ))

    result = cursor.fetchone()
    if result:
        return result[0]

    cursor.execute(
        "INSERT INTO companies (name, company_site) VALUES (%s, %s) RETURNING id",
        (company_name, "adzuna.com")
    )
    company_id = cursor.fetchone()[0]
    return company_id

def _get_or_create_topic(cursor, topic):
    cursor.execute("SELECT id FROM topics WHERE name = %s", (topic, ))

    result = cursor.fetchone()
    if result:
        return result[0]

    cursor.execute(
        "INSERT INTO topics (name) VALUES (%s) RETURNING id",
        (topic, )
    )
    topic_id = cursor.fetchone()[0]
    return topic_id

def _insert_job_posting(cursor, job_data, topic_id, company_id):

    cursor.execute(
        """INSERT INTO job_postings (title, description, url, source, location, posted_at, topic_id, company_id) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """,
        (job_data["title"],
         job_data["description"],
         job_data["url"],
         job_data["source"],
         job_data["location"],
         job_data["posted_at"],
         topic_id,
         company_id
         )
    )

def save_job_posting(job_data):
    conn = psycopg2.connect(
        dbname="devpulse",
        user="devpulse_user",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    try:
        company_id = _get_or_create_company(cursor, job_data["company_name"])
        topic_id = _get_or_create_topic(cursor, job_data["topic"])
        _insert_job_posting(cursor, job_data, topic_id, company_id)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

