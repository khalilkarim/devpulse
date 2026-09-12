package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/jackc/pgx/v5"
)

func main() {
	connString := fmt.Sprintf(
		"postgres://devpulse_user:%s@localhost:5432/devpulse",
		os.Getenv("DB_PASSWORD"),
	)

	conn, err := pgx.Connect(context.Background(), connString)
	if err != nil {
		log.Fatalf("unable to connect to database: %v\n", err)
	}
	defer conn.Close(context.Background())

	rows, err := conn.Query(context.Background(), "SELECT title FROM job_postings LIMIT 5")
	if err != nil {
		log.Fatalf("query failed: %v\n", err)
	}
	defer rows.Close()

	for rows.Next() {
		var title string
		if err := rows.Scan(&title); err != nil {
			log.Fatalf("row scan failed: %v\n", err)
		}
		fmt.Println("posting:", title)
	}
}