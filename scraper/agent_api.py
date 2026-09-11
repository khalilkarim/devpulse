from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv
from google import genai
from agent_instructions import parse_gemini_response, gemini_prompt, tool_map

app = Flask(__name__)
load_dotenv()

client = genai.Client()
chat = {}

def get_db_connection():
    return psycopg2.connect(
        dbname="devpulse",
        user="devpulse_user",
        password=os.getenv("DB_PASSWORD"),
        host="localhost",
        port="5432"
    )

def call_gemini(query, user_id):
    initial_gemini_interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=gemini_prompt + query
    )
    tool_names = parse_gemini_response(initial_gemini_interaction.output_text)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        results = {}
        for tool_name in tool_names:
            print(f"about to call: {tool_name}")
            results[tool_name] = tool_map[tool_name](cursor, user_id, query, client)

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
        previous_interaction_id=initial_gemini_interaction.id

    )

    return final_response.output_text

@app.route("/agent", methods=["POST"])
def ask_agent():
    data = request.get_json()
    user_id = data.get("userId")
    query = data.get("query")

    try:
        answer = call_gemini(query, user_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 502

    return jsonify({"answer": answer}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)