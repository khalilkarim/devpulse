

def get_trending_skills(cursor, user_id, query, client):
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

def get_top_companies(cursor, user_id, query, client):
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

def get_trending_user_skills(cursor, user_id, query, client):
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

def search_similar_postings(cursor, user_id, query, client):


    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )
    query_vector = result.embeddings[0].values

    cursor.execute(
        """
        SELECT id, title, description,
               1 - (embedding <=> %s::vector) AS similarity
        FROM job_postings
        WHERE embedding IS NOT NULL
          # AND 1 - (embedding <=> %s::vector) > 0.5
        ORDER BY embedding <=> %s::vector
            LIMIT 5
        """,
        (query_vector, query_vector, query_vector)
    )
    return cursor.fetchall()