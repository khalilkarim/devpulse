from agent_tools import get_trending_user_skills, get_trending_skills, get_top_companies, search_similar_postings


tool_map = {
    "get_trending_skills": get_trending_skills,

    "get_top_companies": get_top_companies,

    "get_trending_user_skills": get_trending_user_skills,

    "search_similar_postings": search_similar_postings
}

tool_descriptions = {
    "get_trending_skills": """ Get skills that are currently trending among job postings.""",

    "get_top_companies": """See which companies are currently hiring the 
    most based on how many job postings they have available""",

    "get_trending_user_skills": """Help user find out which of their skills are a top seeker 
    for employers based on their reference within job postings.""",

 "search_similar_postings": """Find job postings that are semantically similar to a described role, 
skill set, or work style — for open-ended questions about posting content that aren't covered by 
exact skill/company statistics."""
}

gemini_prompt = f"""
     You are chief advisor for our app, which helps users learn about job openings that fit their skills
     or find out what skills employers are hiring for.

     Users can:
     - Check what companies are hiring the most
     - See what skills are most in demand among current job postings
     - Find out which of their own skills are trending in job postings
     - Ask open-ended questions about job postings — for example, describing a role, skill set,
       or work style and finding postings that semantically match, even when there's no exact
       skill or company filter that would answer the question directly

     I want you to choose which tool/tools should be used based on the user's query. Choose exact,
     statistic-based tools (trending skills, top companies, user skill trends) when the question is
     asking for a count, ranking, or specific known value. Choose the semantic search tool only when
     the question is open-ended, descriptive, or doesn't map cleanly to one of the fixed statistics —
     for example, questions about the content or nature of postings rather than counts.

     Provide back the tool that should be used to satisfy the user's query. Return the key from the
     tool's dictionary we should use.

     Tools: {tool_descriptions}"""



def parse_gemini_response(response):
    tool_name = []
    for key in tool_descriptions:
        if key in response:
            tool_name.append(key)
    return tool_name






