CREATE TYPE IF NOT EXISTS source_type AS ENUM ('LinkedIn', 'Indeed');
CREATE TYPE IF NOT EXISTS period_type_enum AS ENUM ('week', 'month', 'year');

CREATE TABLE users (
    id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, is_active BOOLEAN DEFAULT true, created_at TIMESTAMP DEFAULT NOW() )
    );

CREATE TABLE skills (
    id SERIAL PRIMARY KEY, name VARCHAR(100)
);

CREATE TABLE companies (
    id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, company_site TEXT NOT NULL, location VARCHAR(100),
    application_success_rate DECIMAL (5,2)
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL
);

CREATE TABLE job_postings (
    id SERIAL PRIMARY KEY, title VARCHAR(100) NOT NULL, description TEXT, location VARCHAR(100),
    url TEXT NOT NULL, source source_type NOT NULL, posted_at DATE, scraped_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true, is_analyzed BOOLEAN DEFAULT false, company_id INT REFERENCES companies(id),
    topic_id INT REFERENCES topics(id)
);

CREATE TABLE market_trends (
    id SERIAL PRIMARY KEY, mention_count BIGINT NOT NULL DEFAULT 0, period_start DATE NOT NULL,
    period_type period_type_enum NOT NULL, topic_id REFERENCES topics(id), skill_id REFERENCES skills(id),
    UNIQUE (skill_id, period_start, period_type)
);

CREATE TABLE user_skills (
    user_id REFERENCES users(id) ON DELETE CASCADE , skill_id REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, skill_id)
);

CREATE TABLE job_posting_skills (
    job_id REFERENCES job_postings(id), skill_id REFERENCES skills(id),
    PRIMARY KEY (job_id, skill_id)
);

CREATE TABLE saved_jobs (
    user_id REFERENCES users(id), job_id REFERENCES job_postings(id),
    saved_at TIMESTAMP DEFAULT NOW(), PRIMARY KEY (user_id, job_id)
);

CREATE TABLE saved_companies (
    user_id REFERENCES users(id), company_id REFERENCES companies(id),
    saved_at TIMESTAMP DEFAULT NOW(), PRIMARY KEY (user_id, company_id)
);

CREATE TABLE saved_trends (
    user_id REFERENCES users(id), trend_id REFERENCES market_trends(id),
    saved_at TIMESTAMP DEFAULT NOW(), PRIMARY KEY (user_id, trend_id)
);

CREATE TABLE scraper_jobs (
    id SERIAL PRIMARY KEY, search_query VARCHAR(100) NOT NULL , source source_type NOT NULL,
    started_at TIMESTAMP DEFAULT NOW(), ended_at TIMESTAMP, scrape_successful BOOLEAN DEFAULT NULL,
    jobs_found_count BIGINT DEFAULT 0, error_message TEXT, next_retry_at TIMESTAMP,
    CHECK ( jobs_found_count >= 0 ),
    CONSTRAINT  check_success_rate CHECK (
        (scrape_successful = true AND error_message IS NULL)
        OR (scrape_successful = false AND error_message IS NOT NULL)
        OR (scrape_successful IS NULL )
        )

);

