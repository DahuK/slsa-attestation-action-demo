# SLSA Demo Server

🚀 A demo Go server demonstrating SLSA (Supply chain Levels for Software Artifacts) compliance with containerization.

## Overview

This project demonstrates how to build a secure, production-ready containerized Go application following SLSA best practices.

## Features

- ✅ **Health Check Endpoint** (`/health`) - Server status and uptime
- ✅ **Info Endpoint** (`/info`) - Server information
- ✅ **CORS Support** - Cross-origin resource sharing
- ✅ **Structured Logging** - Request logging middleware
- ✅ **Multi-stage Docker Build** - Optimized image size and security
- ✅ **Non-root User** - Security best practice
- ✅ **Health Checks** - Docker health check support

## Tech Stack

- **Language**: Go 1.21+
- **Container**: Docker with multi-stage builds
- **Security**: Non-root user, minimal base image

## Quick Start

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd slsa-demo

# Run the application
go run main.go
```

Access the application:
- Homepage: http://localhost:8080
- Health check: http://localhost:8080/health
- Server info: http://localhost:8080/info

### Docker

```bash
# Build the image
docker build -t slsa-demo:latest .

# Run the container
docker run -p 8080:8080 slsa-demo:latest
```

## API Endpoints

### GET /

Returns an HTML page with service information and available endpoints.

**Response**: HTML page

### GET /health

Returns server health status.

**Response**: JSON
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0",
  "uptime": "1h23m45s"
}
```

### GET /info

Returns server information.

**Response**: JSON
```json
{
  "name": "SLSA Demo Server",
  "version": "1.0.0",
  "description": "A demo Go server demonstrating SLSA compliance with containerization",
  "environment": "production"
}
```

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `PORT` | `8080` | Server port |
| `ENVIRONMENT` | `development` | Runtime environment |
| `APP_VERSION` | `1.0.0-dev` | Application version |

## Docker Image

- **Base Image**: `alpine:latest`
- **Build Image**: `golang:1.21-alpine`
- **User**: Non-root user (uid: 1001)
- **Port**: 8080
- **Health Check**: 30s interval

## Security Features

- 🔒 **Non-root User** - Prevents privilege escalation attacks
- 🔒 **Minimal Base Image** - Reduces attack surface
- 🔒 **Multi-stage Build** - Smaller production image
- 🔒 **Static Linking** - Eliminates dynamic library vulnerabilities

## Development

### Project Structure

```
slsa-demo/
├── main.go          # Main application file
├── go.mod          # Go module definition
├── Dockerfile      # Docker build file
├── .dockerignore   # Docker ignore file
└── README.md       # This file
```

### Local Development

```bash
# Install dependencies
go mod download

# Run tests
go test ./...

# Build
go build -o slsa-demo .

# Run
./slsa-demo
```

## SLSA Compliance

This project demonstrates SLSA requirements:

1. **Source Control** - Git version control
2. **Build Process** - Reproducible Docker builds
3. **Dependency Management** - Go modules
4. **Distribution** - Container image distribution
5. **Verification** - Health checks and metadata

## CI/CD

This project includes GitHub Actions workflows for:
- Automated Docker image builds and pushes on main branch
- Security scanning and vulnerability checks
- SLSA compliance verification

## License

MIT License

## Contributing

Issues and pull requests are welcome!

---