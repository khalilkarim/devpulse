import psycopg2
import os
from dotenv import load_dotenv
from seed_data import TOPICS
from seed_data import SKILLS

load_dotenv()

def _load_topics_to_db(cursor, topics = TOPICS):
    for topic in topics:
        cursor.execute(
            "INSERT INTO topics (name) VALUES (%s)" , (topic, )
        )

def _load_skills_to_db(cursor, skills = SKILLS):
    for skill in skills:
        cursor.execute(
            "INSERT INTO skills (name) VALUES (%s)", (skill, )
        )

def load_data():
    conn = psycopg2.connect(
        dbname="devpulse",
        user="devpulse_user",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    try:
        _load_topics_to_db(cursor)
        _load_skills_to_db(cursor)
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    load_data()


