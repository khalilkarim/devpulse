import os
import psycopg2
from agent_tools import get_trending_user_skills, get_trending_skills, get_top_companies
from dotenv import load_dotenv
from google import genai

load_dotenv()

user_id = 1  # TODO: replace with authenticated user from request once REST layer exists

user_question = input("What would you like to know? ")

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

client = genai.Client()
chat = {}

# def call_gemini(prompt):
#
#     interaction = client.interactions.create(
#         model = "gemini-3.5-flash",
#         input = prompt
#     )
#
#     chat["response"] = interaction.output_text
#     chat["chat_id"] = interaction.previous_interaction_id
#     return chat

first_gemini_interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=user_question + gemini_prompt
)

print(first_gemini_interaction.output_text)

def parse_gemini_response(response):
    tool_name = []
    for key in tool_descriptions:
        if key in response:
            tool_name.append(key)
    return tool_name



tool_names = parse_gemini_response(first_gemini_interaction.output_text)

try:
    conn = psycopg2.connect(
        dbname="devpulse",
        user="devpulse_user",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    results = {}
    for tool_name in tool_names:
        print(f"about to call: {tool_name}")
        results[tool_name] = tool_map[tool_name](cursor, user_id)

except Exception as e:
    print(f"Error: {e}")

finally:
    cursor.close()
    conn.close()


follow_up = f"""Here is the data from our database: {results} 
I want you to display the table for the user to see as well. even if one of the columns is 0 or null"""



final_response = client.interactions.create(
    model="gemini-3.5-flash",
    input=follow_up,
    previous_interaction_id=first_gemini_interaction.id

)
print(final_response.output_text)




