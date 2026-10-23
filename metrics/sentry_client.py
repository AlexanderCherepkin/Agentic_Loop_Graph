"""Sentry Error Tracking Integration."""
import sentry_sdk
from sentry_sdk import capture_exception, capture_message, add_breadcrumb


class SentryClient:
    """Sentry client for error tracking and monitoring."""

    def __init__(self, dsn: str = None):
        self.dsn = dsn or "https://YOUR_DSN@sentry.io/YOUR_PROJECT_ID"
        
    def init(self, environment: str = "production", release: str = None):
        """Initialize Sentry SDK."""
        sentry_sdk.init(
            dsn=self.dsn,
            environment=environment,
            release=release or f"figma-export@{__import__('pkg_resources').get_distribution('figma_export').version}",
            traces_sample_rate=1.0,  # Full tracing for debugging
        )

    def capture_error(self, exception: Exception):
        """Capture and report an error to Sentry."""
        try:
            sentry_sdk.capture_exception(exception)
        except Exception as e:
            print(f"Failed to send error to Sentry: {e}")

    def capture_message(self, message: str, level: str = "error"):
        """Capture a custom message to Sentry."""
        try:
            sentry_sdk.capture_message(message, level=level)
        except Exception as e:
            print(f"Failed to send message to Sentry: {e}")

    def add_breadcrumb(self, message: str, category: str = "http"):
        """Add breadcrumb for context."""
        try:
            sentry_sdk.add_breadcrumb(
                message=message,
                category=category,
                type="default",
            )
        except Exception as e:
            print(f"Failed to add breadcrumb: {e}")


def create_sentry_client(dsn: str = None) -> SentryClient:
    """Create and configure Sentry client."""
    return SentryClient(dsn=dsn)
