package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"os"
	"sync"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/pgvector/pgvector-go"
	pgxvec "github.com/pgvector/pgvector-go/pgx"
	"google.golang.org/genai"
)

type Posting struct {
	ID          int
	Description string
}

func fetchPendingPostings(ctx context.Context, pool *pgxpool.Pool, limit int) ([]Posting, error) {
	rows, err := pool.Query(ctx,
		"SELECT id, description FROM job_postings WHERE embedding IS NULL LIMIT $1",
		limit,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var postings []Posting
	for rows.Next() {
		var p Posting
		if err := rows.Scan(&p.ID, &p.Description); err != nil {
			return nil, err
		}
		postings = append(postings, p)
	}
	return postings, nil
}

func embedText(ctx context.Context, client *genai.Client, text string) ([]float32, error) {
	contents := []*genai.Content{
		genai.NewContentFromText(text, genai.RoleUser),
	}
	result, err := client.Models.EmbedContent(ctx, "gemini-embedding-001", contents, nil)
	if err != nil {
		return nil, err
	}
	return result.Embeddings[0].Values, nil
}

func saveEmbedding(ctx context.Context, pool *pgxpool.Pool, id int, embedding []float32) error {
	_, err := pool.Exec(ctx,
		"UPDATE job_postings SET embedding = $1 WHERE id = $2",
		pgvector.NewVector(embedding), id,
	)
	return err
}

func worker(ctx context.Context, id int, jobs <-chan Posting, pool *pgxpool.Pool, client *genai.Client, wg *sync.WaitGroup) {
	defer wg.Done()
	for job := range jobs {
		embedding, err := embedText(ctx, client, job.Description)
		if err != nil {
			log.Printf("worker %d: embed failed for posting %d: %v", id, job.ID, err)
			continue
		}
		if err := saveEmbedding(ctx, pool, job.ID, embedding); err != nil {
			log.Printf("worker %d: save failed for posting %d: %v", id, job.ID, err)
			continue
		}
		fmt.Printf("worker %d: embedded posting %d\n", id, job.ID)
	}
}

func main() {
	limit := flag.Int("limit", 5, "max postings to embed")
	numWorkers := flag.Int("workers", 3, "number of concurrent workers")
	flag.Parse()

	ctx := context.Background()

	connString := fmt.Sprintf(
		"postgres://devpulse_user:%s@localhost:5432/devpulse",
		os.Getenv("DB_PASSWORD"),
	)

	pool, err := pgxpool.New(ctx, connString)
	if err != nil {
		log.Fatalf("unable to create connection pool: %v", err)
	}
	defer pool.Close()

	conn, err := pool.Acquire(ctx)
	if err != nil {
		log.Fatalf("unable to acquire connection: %v", err)
	}
	if err := pgxvec.RegisterTypes(ctx, conn.Conn()); err != nil {
		log.Fatalf("unable to register vector types: %v", err)
	}
	conn.Release()

	client, err := genai.NewClient(ctx, nil)
	if err != nil {
		log.Fatalf("unable to create genai client: %v", err)
	}

	postings, err := fetchPendingPostings(ctx, pool, *limit)
	if err != nil {
		log.Fatalf("unable to fetch postings: %v", err)
	}
	fmt.Printf("found %d postings to embed\n", len(postings))

	jobs := make(chan Posting, len(postings))
	var wg sync.WaitGroup

	start := time.Now()

	for w := 1; w <= *numWorkers; w++ {
		wg.Add(1)
		go worker(ctx, w, jobs, pool, client, &wg)
	}

	for _, p := range postings {
		jobs <- p
	}
	close(jobs)

	wg.Wait()

	fmt.Printf("done in %v\n", time.Since(start))
}