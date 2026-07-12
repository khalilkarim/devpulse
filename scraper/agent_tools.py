

def get_trending_skills(cursor, user_id):
    cursor.execute(
        """
        SELECT skills.name, COUNT(*) as trending_skills
        FROM job_posting_skills JOIN skills 
        ON job_posting_skills.skill_id = skills.id
        GROUP BY skills.name 
        ORDER BY trending_skills DESC
        """
    )
    return cursor.fetchall()

def get_top_companies(cursor, user_id):
    cursor.execute(
        """
        SELECT companies.name, COUNT(job_postings.company_id) as top_companies
        FROM job_postings JOIN companies
        ON job_postings.company_id = companies.id
        GROUP BY companies.name 
        ORDER BY top_companies DESC
        """
    )
    return cursor.fetchall()

def get_trending_user_skills(cursor, user_id):
    cursor.execute(
        """
        SELECT skills.name, 
        COUNT(job_posting_skills.skill_id) as trending_user_skills
        FROM user_skills JOIN skills
        ON user_skills.skill_id = skills.id
        LEFT JOIN job_posting_skills 
        ON job_posting_skills.skill_id = skills.id
        WHERE user_skills.user_id = %s
        GROUP BY skills.name 
        ORDER BY trending_user_skills DESC
        """,
        (user_id, )
    )
    return cursor.fetchall()