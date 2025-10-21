package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

// HealthResponse represents the health check response
// test
type HealthResponse struct {
	Status    string    `json:"status"`
	Timestamp time.Time `json:"timestamp"`
	Version   string    `json:"version"`
	Uptime    string    `json:"uptime"`
}

// InfoResponse represents the server info response
type InfoResponse struct {
	Name        string `json:"name"`
	Version     string `json:"version"`
	Description string `json:"description"`
	Environment string `json:"environment"`
}

var startTime = time.Now()

func getVersion() string {
	if version := os.Getenv("APP_VERSION"); version != "" {
		return version
	}
	return "1.0.0-dev"
}

func getEnvironment() string {
	if env := os.Getenv("ENVIRONMENT"); env != "" {
		return env
	}
	return "development"
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	response := HealthResponse{
		Status:    "healthy",
		Timestamp: time.Now(),
		Version:   getVersion(),
		Uptime:    time.Since(startTime).String(),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func infoHandler(w http.ResponseWriter, r *http.Request) {
	response := InfoResponse{
		Name:        "SLSA Demo Server",
		Version:     getVersion(),
		Description: "A demo Go server demonstrating SLSA compliance with containerization",
		Environment: getEnvironment(),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}

	html := fmt.Sprintf(`
<!DOCTYPE html>
<html>
<head>
    <title>SLSA Demo Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
        code { background: #e8e8e8; padding: 2px 5px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 SLSA Demo Server</h1>
        <p>Welcome to the SLSA (Supply chain Levels for Software Artifacts) demo server!</p>

        <h2>Available Endpoints:</h2>
        <div class="endpoint">
            <strong>GET /</strong> - This page
        </div>
        <div class="endpoint">
            <strong>GET /health</strong> - Health check endpoint (<code>application/json</code>)
        </div>
        <div class="endpoint">
            <strong>GET /info</strong> - Server information (<code>application/json</code>)
        </div>

        <h2>Server Information:</h2>
        <ul>
            <li><strong>Version:</strong> %s</li>
            <li><strong>Environment:</strong> %s</li>
            <li><strong>Started:</strong> %s</li>
        </ul>
    </div>
</body>
</html>`, getVersion(), getEnvironment(), startTime.Format("2006-01-02 15:04:05"))

	w.Header().Set("Content-Type", "text/html")
	fmt.Fprint(w, html)
}

func corsMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// Set CORS headers
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		// Handle preflight requests
		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		next(w, r)
	}
}

func loggingMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next(w, r)
		log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
	}
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// Set up routes
	http.HandleFunc("/", corsMiddleware(loggingMiddleware(rootHandler)))
	http.HandleFunc("/health", corsMiddleware(loggingMiddleware(healthHandler)))
	http.HandleFunc("/info", corsMiddleware(loggingMiddleware(infoHandler)))

	log.Printf("🚀 SLSA Demo Server starting on port %s", port)
	log.Printf("📊 Health check available at http://localhost:%s/health", port)
	log.Printf("ℹ️  Server info available at http://localhost:%s/info", port)

	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal("Server failed to start:", err)
	}
}
