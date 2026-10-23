# Figma Agent API Monitoring Guide

## Overview

This guide documents the observability stack for the Figma Agent API, including:
- Prometheus metrics collection
- Sentry error tracking
- OpenTelemetry distributed tracing
- Grafana dashboard visualization

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Application │ ←→ │   API Server  │    └──────────────┘
│   (Node.js)  │    │   (FastAPI)   │
└─────────────┘    └──────┬───────┘

         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
  │    Sentry   │   │   Prometheus│   │ OpenTelemetry│
  │ Error Tracking│ │ Metrics & Logging│  Distributed Tracing│
  └─────────────┘   └──────┬───────┘   └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Grafana  │
                    │ Visualization│
                    └─────────────┘
```

## Quick Start

### Prerequisites
1. Docker and Docker Compose installed
2. Port availability: 8000, 9090, 3000, 4317

### Setup Monitoring Stack (Recommended)
```bash
cd Agentic_Loop_Graph
docker compose -f docker-compose.yml.monitoring up --build -d
```

Access services:
- API Server: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

### Environment Variables (.env file)
```bash
# Monitoring Configuration
PROMETHEUS_ENABLED=true
SENTRY_DSN=your-sentry-dsn-here
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
LOG_LEVEL=INFO

# API Server
API_HOST=0.0.0.0
API_PORT=8000
UVICORN_WORKERS=4

# Figma Integration
FIGMA_API_TOKEN=your-figma-api-token-here
```

## Metrics Collection

### Prometheus Metrics at `/metrics`

**Request Duration Histogram**
- `http_request_duration_seconds` - Response time by endpoint
- Buckets for distribution analysis

**Request Counters**
- `http_requests_total` - Total HTTP requests
- `http_request_size_bytes` - Request body size

**Figma API Metrics**
- `figma_api_calls_total` - Number of Figma API calls
- `figma_api_latency_seconds` - Latency for operations

### Query Examples (PromQL)

```promql
# Total requests in last hour
sum(http_requests_total{job="api"})

# Request rate per second
rate(http_requests_total[1m])

# P95 latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Error rate calculation
sum(rate(http_requests_total{status=~"5.."}[5m])) / 
sum(rate(http_requests_total[5m])) * 100
```

## Sentry Error Tracking

Activated when `SENTRY_DSN` is set in environment variables.

**Features:**
- Automatic error capture for all exceptions
- Request ID correlation across services
- Python version tagging
- Stack trace with source code context

**Captured Data:**
- Full exception traceback
- HTTP request details (method, URL, headers)
- Response time information
- Correlation ID for tracing

## OpenTelemetry Integration

- Distributed tracing across microservices
- Automatic FastAPI instrumentation
- OTLP export at port 4317
- Service name: `figma-agent-api` (configurable via OTEL_SERVICE_NAME)

## Health Checks

```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

Docker Compose uses this for container health monitoring.

## Alerting Setup

Create `prometheus/alerts.yml`:

```yaml
groups:
  - name: figma-agent-alerts
    rules:
      - alert: HighErrorRate
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / 
              sum(rate(http_requests_total[5m])) > 0.1
        for: 5m
        labels:
          severity: critical

      - alert: HighLatencyP95
        expr: histogram_quantile(0.95, 
               sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 1.0
        for: 2m
        labels:
          severity: warning
```

## Grafana Dashboard

Access at http://localhost:3000
- Default login: admin/admin
- Dashboards auto-loaded from grafana/dashboard.yml
- Prometheus datasource configured in datasources.yml

## Troubleshooting

**Metrics Not Appearing:**
1. Check API running: `docker ps | grep api`
2. Verify `/metrics` endpoint: `curl http://localhost:8000/metrics`
3. Ensure PROMETHEUS_ENABLED=true

**Sentry Events Missing:**
1. Verify SENTRY_DSN in .env file
2. Check API logs for initialization messages

**Grafana Not Loading Dashboards:**
1. Validate grafana/dashboard.yml
2. Verify Prometheus datasource connection in Grafana UI

## Security Considerations

- Never commit `.env` files with sensitive credentials
- Use environment variables for all secrets
- Enable HTTPS/TLS in production
- Rotate Sentry DSNs regularly

## Performance Tuning

**Recommended Settings:**
```yaml
UVICORN_WORKERS=8
RATE_LIMIT_MINUTES=300
OTEL_BSP_SCHEDULE_DELAY=5000
```

**Resource Allocation:**
```yaml
api:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 1G
      reservations:
        cpus: '0.5'
        memory: 256M
  
prometheus:
  deploy:
    resources:
      limits:
        memory: 2G
```

## License

Part of the Figma Agent project - see main LICENSE file for details.