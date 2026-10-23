"""API Configuration for Figma Agent."""

import os
from typing import Dict, Any
from functools import lru_cache


@lru_cache()
def get_config() -> Dict[str, Any]:
    """Load and cache API configuration."""
    
    return {
        "server": {
            "host": os.getenv("API_HOST", "0.0.0.0"),
            "port": int(os.getenv("API_PORT", 8000)),
            "workers": int(os.getenv("UVICORN_WORKERS", 4))
        },
        "figma_api": {
            "base_url": os.getenv(
                "FIGMA_API_BASE_URL", 
                "https://api.figma.com/v1"
            ),
            "token": os.getenv("FIGMA_API_TOKEN"),
            "rate_limiting": {
                "requests_per_minute": int(os.getenv("RATE_LIMIT_MINUTES", 120)),
                "burst_limit": int(os.getenv("RATE_LIMIT_BURST", 30))
            }
        },
        "endpoints": {
            "export": {
                "enabled": True,
                "supported_formats": ["png", "jpg", "pdf", "svg"],
                "max_resolution": 4096
            },
            "nodes": {
                "enabled": True,
                "pagination_size": 100
            }
        },
        "logging": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "monitoring": {
            "sentry_dsn": os.getenv("SENTRY_DSN"),
            "prometheus_enabled": os.getenv("PROMETHEUS_ENABLED", "true").lower() == "true",
            "otel_endpoint": os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
            "otel_service_name": os.getenv("OTEL_SERVICE_NAME", "figma-agent-api")
        }
    }


# Global configuration instance
API_CONFIG = get_config()


def create_api_app() -> Any:
    """Create FastAPI application instance."""
    
    from fastapi import FastAPI
    
    app = FastAPI(
        title="Figma Agent API",
        description="Agentic Loop Integration with Figma Export and Data Retrieval",
        version="1.0.0"
    )
    
    # Prometheus Instrumentation
    try:
        from prometheus_fastapi_instrumentator import Instrumentator
        
        instrumentator = Instrumentator()
        
        @app.middleware("http")
        async def log_requests(request, call_next):
            """Log all requests for metrics."""
            response = await call_next(request)
            return response
        
        instrumentator.instrument(app).expose(app, endpoint="/metrics")
    except ImportError:
        import logging
        logging.warning("Prometheus instrumentation not available (prometheus-fastapi-instrumentator)")
    
    # Sentry Error Tracking
    if API_CONFIG["monitoring"]["sentry_dsn"]:
        try:
            from sentry_sdk import init_sentry, configure_scope
            
            init_sentry(API_CONFIG["monitoring"]["sentry_dsn"])
            
            def before_send(event, hint):
                """Add context to error events."""
                event.tags = {
                    "service": "figma-agent-api",
                    "python_version": f"{sys.version_info.major}.{sys.version_info.minor}"
                }
                return event
            
            configure_scope(lambda scope: setattr(scope, "before_send", before_send))
        except ImportError:
            import logging
            logging.warning("Sentry integration not available (sentry-sdk)")
    
    return app