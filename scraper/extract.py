import psycopg2
import os
from collections import defaultdict


def _load_skills(cursor):
    cursor.execute(
        "SELECT id, name FROM skills"
    )
    skills = cursor.fetchall()
    return skills

def _load_job_posting_titles(cursor):
    cursor.execute(
        "SELECT id, title FROM job_postings"
    )
    titles = cursor.fetchall()
    return titles

def _load_job_posting_descriptions(cursor):
    cursor.execute(
        "SELECT id, description FROM job_postings"
    )
    job_posting_descriptions = cursor.fetchall()
    return job_posting_descriptions

def extract_skills(cursor):
    skills = _load_skills(cursor)
    titles = _load_job_posting_titles(cursor)
    descriptions = _load_job_posting_descriptions(cursor)

    matching_skills = []

    for posting_id, description in descriptions:
        for skill_id in match_skills_in_text(description, skills):
            matching_skills.append((posting_id, skill_id))

    for posting_id, title in titles:
        for skill_id in match_skills_in_text(title, skills):
            matching_skills.append((posting_id, skill_id))

    return _group_skills(matching_skills)



def _group_skills(matching_skills):
    grouped_dict = defaultdict(list)
    for key, value in matching_skills:
        grouped_dict[key].append(value)

    return grouped_dict

def match_skills_in_text(text, skills):
    """text: str. skills: list of (id, name). Returns: list of matching skill_ids."""
    return [skill_id for skill_id, skill_name in skills
            if skill_name.lower() in text.lower()]







if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="devpulse",
        user="devpulse_user",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    grouped_dict = extract_skills(cursor)
    print(f"final_matching_skills: {grouped_dict}")


