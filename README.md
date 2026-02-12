# PrintFarm Onground Backend Service

A FastAPI microservice for orchestrating printers, print queues, real-time monitoring, and analytics within the secure PrintFarm intranet environment. This service interfaces directly with hardware, manages local job execution, and enables advanced QA and operational reporting.

## Architecture Overview

- **Printer Backend**: Interfaces with SimplyPrint APIs and custom drivers for STL uploads, slicing, and print job execution
- **Print Queue Orchestrator**: Consumes jobs via RabbitMQ/Kafka, assigns printers, manages retries, logs results
- **Quality Analytics**: Captures camera snapshots and failure logs per job, aggregates metrics for dashboards
- **Local Media Storage**: Persists QA snapshots and job logs for compliance and traceability
- **Security**: Mutual TLS/VPN, API Key/JWT auth, firewall isolation

## Key Features

- Automated assignment and execution of print jobs
- Job prioritization and SLA management
- Robust error handling and retry logic
- Quality monitoring and analytics via camera feeds
- Dashboard-ready operational and historical data
- Scalable for future AI-driven print farm optimizations

## Getting Started

### Prerequisites

- Python 3.9+
- Redis server
- RabbitMQ/Kafka message broker
- SimplyPrint API credentials


### Configuration

Edit `.env` file with your environment-specific settings:


### API Documentation

Once running, access the interactive API documentation:
- Swagger UI: `http://localhost:4000/docs`
- ReDoc: `http://localhost:4000/redoc`

## Repository Structure

```
/app
    /main.py              # FastAPI application entrypoint
    /api/                 # API route definitions
        /v1/              # Version 1 API endpoints
            /printers.py  # Printer management endpoints
            /jobs.py      # Job management endpoints
            /quality.py   # Quality monitoring endpoints
    /core/                # Core application logic
        /config.py        # Configuration management
        /security.py      # Authentication and authorization
        /database.py      # Database connections
    /services/            # Business logic services
        /printer_service.py
        /queue_service.py
        /quality_service.py
    /models/              # Data models
        /printer.py
        /job.py
        /quality.py
    /queue/               # Print queue orchestration
        /orchestrator.py  # Main queue management logic
        /consumers.py     # Message queue consumers
        /producers.py     # Message queue producers
    /printers/            # Printer interface modules
        /simplyprint.py   # SimplyPrint API integration
        /custom_drivers/  # Custom printer drivers
    /quality/             # Quality monitoring modules
        /camera.py        # Camera feed handling
        /analytics.py     # Quality analytics
        /failure_detection.py
    /storage/             # Local media storage handlers
        /media_manager.py # File and media management
        /backup.py        # Backup and archival
/tests/                   # Test suite
    /unit/
    /integration/
    /fixtures/
/docs/                    # Additional documentation
    /api.md              # API documentation
    /deployment.md       # Deployment guide
    /architecture.md     # Detailed architecture docs
/scripts/                 # Utility scripts
    /setup.py            # Environment setup
    /migrate.py          # Database migrations
/docker/                  # Docker configuration
    /Dockerfile
    /docker-compose.yml
.env.example             # Environment variables template
requirements.txt         # Python dependencies
requirements-dev.txt     # Development dependencies
pyproject.toml          # Python project configuration
.gitignore              # Git ignore rules
README.md               # This file
```

## Development

### Code Style

This project uses:
- **Black** for code formatting
- **isort** for import sorting  
- **Flake8** for linting
- **mypy** for type checking



## Deployment

### Docker

```bash
# Build image
docker build -f docker/Dockerfile -t printfarm-onground:latest .

# Run with docker-compose
docker-compose -f docker/docker-compose.yml up -d
```

### Environment Variables

Required environment variables for production:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `RABBITMQ_URL`: RabbitMQ connection string
- `SIMPLYPRINT_API_KEY`: SimplyPrint API credentials
- `JWT_SECRET_KEY`: Secret for JWT token generation
- `MEDIA_STORAGE_PATH`: Path for local media storage

## API Endpoints

### Core Endpoints

- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `POST /api/v1/jobs/receive` - Accept new print job
- `GET /api/v1/jobs/{job_id}/status` - Get job status
- `POST /api/v1/printers/{printer_id}/assign` - Assign job to printer
- `GET /api/v1/quality/snapshots/{job_id}` - Get quality snapshots

### Monitoring

- `GET /api/v1/dashboard/stats` - Real-time operational statistics
- `GET /api/v1/analytics/utilization` - Printer utilization metrics
- `GET /api/v1/analytics/quality` - Quality analytics data

## Monitoring & Observability

### Metrics

The service exposes Prometheus metrics at `/metrics`:

- `printfarm_jobs_total` - Total number of jobs processed
- `printfarm_jobs_duration_seconds` - Job processing duration
- `printfarm_printer_utilization` - Printer utilization percentage
- `printfarm_quality_failures_total` - Total quality failures

### Logging

Structured JSON logging with configurable levels. Logs include:

- Request/response logging
- Job lifecycle events
- Printer status changes
- Quality monitoring events
- Error tracking and alerts

### Health Checks

- `/health` - Basic service health
- `/health/detailed` - Detailed component health (database, message broker, printers)

## Security

### Authentication

- API Key authentication for service-to-service communication
- JWT tokens for internal service authentication
- Rate limiting on all public endpoints

### Network Security

- All communication over TLS
- VPN/mutual TLS for inter-service communication
- Firewall restrictions for intranet-only access
- No direct internet exposure

