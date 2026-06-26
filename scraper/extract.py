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
        lower_desc = description.lower()
        for skill_id, skill_name in skills:
            if skill_name.lower() in lower_desc:
                matching_skills.append((posting_id, skill_id))

    print(f"matching_skills_after_desc: {matching_skills}")

    for posting_id, title in titles:
        lower_title = title.lower()
        for skill_id, skill_name in skills:
            if skill_name.lower() in lower_title:
                matching_skills.append(posting_id, skill_id)

    print(f"matching_skills_after_titles: {matching_skills}")

    grouped_skills = _group_skills(matching_skills)

    return grouped_skills


def _group_skills(matching_skills):
    grouped_dict = defaultdict(list)
    for key, value in matching_skills:
        grouped_dict[key].append(value)

    return grouped_dict







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


