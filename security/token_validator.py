"""Token Validation and Security Utilities."""
import secrets
from typing import Optional, List


class TokenValidator:
    """Utility class for token validation and security checks."""

    @staticmethod
    def validate_token_format(token: str) -> bool:
        """Validate JWT token format."""
        parts = token.split(".")
        return len(parts) == 3 and all(len(part) > 0 for part in parts)

    @staticmethod
    def generate_api_key(length: int = 64) -> str:
        """Generate secure API key."""
        return secrets.token_urlsafe(length)

    @staticmethod
    def hash_password(password: str, salt_length: int = 16) -> tuple:
        """Hash password with salt."""
        import hashlib
        salt = secrets.token_hex(salt_length)
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return (hashed, salt)

    @staticmethod
    def verify_password(password: str, hash_value: str, salt: str) -> bool:
        """Verify password against hash."""
        import hashlib
        computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return computed_hash == hash_value


class SQLInjectionPrevention:
    """Utility for preventing SQL injection attacks."""

    @staticmethod
    def sanitize_input(data: str) -> str:
        """Sanitize input to prevent SQL injection."""
        if not isinstance(data, str):
            return data
        # Remove potentially dangerous characters
        dangerous_chars = ["'", '"', ";", "--", "/*", "*/", "\\x00"]
        for char in dangerous_chars:
            data = data.replace(char, "")
        return data.strip()

    @staticmethod
    def validate_query(query: str) -> bool:
        """Basic query validation."""
        import re
        # Check for common SQL injection patterns
        patterns = [
            r";\s*DROP\s+",
            r"--",
            r"/\*",
            r"UNION\s+SELECT",
            r"OR\s+1\s*=\s*1",
        ]
        for pattern in patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return False
        return True

