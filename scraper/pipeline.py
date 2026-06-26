import psycopg2
import os
from database import save_job_posting
from database import save_job_posting_skills
from scraper import scrape_adzuna
from extract import extract_skills
from database import mark_as_analyzed
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="devpulse",
        user="devpulse_user",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    try:
        job_data = scrape_adzuna("Software Engineering")
        for job in job_data:
            save_job_posting(cursor, job)

        matching_skills = extract_skills(cursor)

        for job_posting_id, skill_ids in matching_skills.items():
            for skill_id in skill_ids:
              save_job_posting_skills(cursor, job_posting_id, skill_id)
            mark_as_analyzed(cursor, job_posting_id)

        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()
