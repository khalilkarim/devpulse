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


def mark_as_analyzed(cursor, job_posting_id):
    cursor.execute(
        "UPDATE job_postings SET is_analyzed = true WHERE id = %s",
        (job_posting_id, )
    )


def save_job_posting_skills(cursor, job_posting_id, skill_id):
      cursor.execute(
        "INSERT INTO job_posting_skills (job_id, skill_id) VALUES (%s, %s)",
        (job_posting_id, skill_id)
         )









def save_job_posting(cursor, job_data):
     company_id = _get_or_create_company(cursor, job_data["company_name"])
     topic_id = _get_or_create_topic(cursor, job_data["topic"])
     _insert_job_posting(cursor, job_data, topic_id, company_id)


