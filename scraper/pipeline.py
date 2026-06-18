from database import save_job_posting
from scraper import scrape_adzuna


if __name__ == "__main__":
   job_data = scrape_adzuna("Software Engineering")
   for job in job_data:
      save_job_posting(job)
