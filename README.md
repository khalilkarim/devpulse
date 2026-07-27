# DevPulse

DevPulse is a job market intelligence tool that scrapes live job postings, extracts the skills employers are asking for, and uses an AI agent to answer natural-language questions about hiring trends.

## What it does

- **Scraper** — pulls live software engineering job postings from the Adzuna API (title, description, company, location, posting date).
- **Pipeline** — orchestrates the flow: scrape postings, store them in Postgres, extract mentioned skills from each posting's title/description, and mark postings as analyzed.
- **Extraction** — matches a known list of skills against job titles and descriptions to tag each posting with the skills it requires.
- **AI Agent** — a Gemini-powered assistant that takes a natural-language question (e.g. "what skills are trending?" or "which companies are hiring the most?"), decides which backend tool/query answers it, runs the corresponding SQL, and returns a readable summary/table back to the user.

## Tech stack

- Python
- PostgreSQL (via `psycopg2`)
- Google Gemini API (`google-genai`) for the agent layer
- Adzuna API for job posting data

## Status

Early-stage / personal project — functional end-to-end pipeline (scrape → store → extract → query via AI agent), but not yet packaged for others to set up and run on their own.
