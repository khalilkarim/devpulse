import requests
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

def scrape_adzuna(topic, limit=20):
    results = []
    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id" : os.getenv("ADZUNA_APP_ID"),
        "app_key" : os.getenv("ADZUNA_API_KEY"),
        "results_per_page" : limit,
        "what" : topic,
        "content-type" : "application/json"

    }

    response = requests.get(url, params=params)
    data = response.json()

    for job in data["results"]:
        results.append({
            "source" : "Adzuna",
            "title" : job.get("title", ""),
            "description" : job.get("description", ""),
            "company_name" : job.get("company", {}).get("display_name", "Unknown"),
            "location" : job.get("location", {}).get("display_name", "Unknown"),
            "url": job.get("redirect_url", ""),
            "posted_at" : job.get("created", ""),
            "external_id" : str(job.get("id") or uuid.uuid4()),
            "topic" : job.get("category", {}).get("label", "Unknown")


        })

    results.sort(key=lambda x: x["posted_at"], reverse=True)
    return results

def _generate_fallback_id(digits=10):
    return "".join(random.choices("01234567891", k=digits))


if __name__ == "__main__":
    results = scrape_adzuna("software engineer")
    print(f"Total: results: {len(results)}")


    titles = [job["title"] for job in results]
    external_ids = [job["external_id"] for job in results]
    unique_titles = set(titles)
    print(f"Unique titles: {len(unique_titles)}")
    print(f"external_ids: {external_ids}")