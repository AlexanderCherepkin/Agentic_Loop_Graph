"""Prometheus Metrics Integration."""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time


class PrometheusMetrics:
    """Collect and expose metrics for Prometheus."""

    def __init__(self):
        # Request counters
        self.request_count = Counter(
            "http_request_total",
            "Total HTTP requests",
            ["method", "endpoint", "status_code"],
        )
        
        self.figma_api_calls = Counter(
            "figma_api_calls_total",
            "Figma API calls",
            ["endpoint"],
        )

        # Response time histograms
        self.request_duration = Histogram(
            "http_request_duration_seconds",
            "HTTP request duration in seconds",
            ["method", "endpoint"],
            buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0),
        )

        self.figma_api_latency = Histogram(
            "figma_api_duration_seconds",
            "Figma API call latency in seconds",
            buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0),
        )

        # System gauges
        self.active_workflows = Gauge(
            "active_workflows_total",
            "Number of active workflows running",
        )

        self.exported_images = Gauge(
            "exported_images_total",
            "Total images exported successfully",
        )

    def track_request(self, method: str, endpoint: str, status_code: int):
        """Track incoming HTTP request."""
        self.request_count.labels(method=method, endpoint=endpoint, status_code=status_code).inc()

    def track_duration(self, method: str, endpoint: str):
        """Track request duration in a callback context."""
        start_time = time.time()

        def record():
            elapsed = time.time() - start_time
            self.request_duration.labels(method=method, endpoint=endpoint).observe(elapsed)

        return record

    def track_figma_call(self, endpoint: str):
        """Track Figma API call."""
        self.figma_api_calls.labels(endpoint=endpoint).inc()

    def track_figma_latency(self, duration: float):
        """Track Figma API latency."""
        self.figma_api_latency.observe(duration)

    def update_active_workflows(self, count: int):
        """Update active workflows gauge."""
        self.active_workflows.set(count)

    def update_exported_images(self, count: int):
        """Update exported images counter."""
        self.exported_images.set(count)

    def get_metrics(self) -> bytes:
        """Get metrics in Prometheus format."""
        return generate_latest()


def create_metrics():
    """Create and return metrics instance."""
    return PrometheusMetrics()