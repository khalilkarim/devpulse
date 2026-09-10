import os
import psycopg2
from agent_tools import get_trending_user_skills, get_trending_skills, get_top_companies
from dotenv import load_dotenv
from google import genai

tool_map = {
    "get_trending_skills": get_trending_skills,

    "get_top_companies": get_top_companies,

    "get_trending_user_skills": get_trending_user_skills
}

tool_descriptions = {
    "get_trending_skills": """ Get skills that are currently trending among job postings.""",

    "get_top_companies": """See which companies are currently hiring the 
    most based on how many job postings they have available""",

    "get_trending_user_skills": """Help user find out which of their skills are a top seeker 
    for employers based on their reference within job postings."""
}

gemini_prompt = f"""
     You are chief advisor for our app, which helps users learn about job openings that fit their skills
     or find out what skills employers are hiring for. 
     Users can check what companies are hiring the most, what skills are most companies currently looking for, 
     and which of their own skills are trending in the job postings. 
     
     I want you to choose which tool/tools should be used based on the user's query. Provide back the tool that should be used to
     satisfy the user's query. Return the key from the tool's dictionary we should use.
 
     Tools: {tool_descriptions}"""



def parse_gemini_response(response):
    tool_name = []
    for key in tool_descriptions:
        if key in response:
            tool_name.append(key)
    return tool_name






