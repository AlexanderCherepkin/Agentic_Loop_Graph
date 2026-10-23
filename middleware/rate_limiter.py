"""Rate Limiter Middleware."""
from typing import Dict, Tuple
from collections import defaultdict
import time
from fastapi import Request, HTTPException, status


class RateLimiter:
    """Token bucket rate limiter implementation."""

    def __init__(self):
        self._requests: Dict[str, list] = defaultdict(list)
        self._limits: Dict[str, Tuple[int, int]] = {
            "default": (100, 60),  # requests per window_seconds
            "api_export": (30, 60),
            "figma_access": (10, 60),
        }

    def get_limit(self, path: str) -> Tuple[int, int]:
        """Get rate limit for specific endpoint."""
        return self._limits.get(path, self._limits["default"])

    async def check_rate_limit(self, request: Request) -> bool:
        """Check if request is within rate limits."""
        client_ip = request.client.host if request.client else "unknown"
        path = str(request.url.path)
        max_requests, window_seconds = self.get_limit(path)

        current_time = time.time()
        # Clean old entries outside the window
        self._requests[client_ip] = [
            t for t in self._requests[client_ip] if current_time - t < window_seconds
        ]

        request_count = len(self._requests[client_ip])

        if request_count >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": f"{max_requests} requests per {window_seconds}s",
                    "retry_after": window_seconds - (current_time - self._requests[client_ip][0]) if self._requests[client_ip] else window_seconds,
                },
            )

        self._requests[client_ip].append(current_time)
        return True


def create_rate_limiter() -> RateLimiter:
    """Create and configure rate limiter."""
    return RateLimiter()

