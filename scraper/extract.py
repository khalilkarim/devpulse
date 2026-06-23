import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def load_skills(cursor):
    cursor.execute(
        "SELECT id, name FROM skills"
    )
    skills = cursor.fetchall()
    return skills

def load_job_posting_descriptions(cursor):
    cursor.execute(
        "SELECT id, description FROM job_postings"
    )
    job_posting_descriptions = cursor.fetchall()
    return job_posting_descriptions

def extract_skills():
    conn = psycopg2.connect(
        dbname="devpulse",
        user="devpulse_user",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    skills = []
    descriptions = []

    try:
       skills = load_skills(cursor)
       descriptions = load_job_posting_descriptions(cursor)
       conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()

    matching_skills = []

    for posting_id, description in descriptions:
        for skill_id, skill_name in skills:
            if skill_name.lower() in description.lower():
                matching_skills.append((posting_id, skill_id))

    return matching_skills





if __name__ == "__main__":
    matched_skills =  extract_skills()
    print(f"{matched_skills}")

