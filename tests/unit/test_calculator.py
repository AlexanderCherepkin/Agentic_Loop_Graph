"""Unit tests for calculator module."""
import pytest


@pytest.mark.unit
class TestCalculator:
    """Test suite for arithmetic operations."""

    def test_addition(self, sample_data):
        """Test addition operation."""
        assert 2 + 2 == 4

    def test_subtraction(self):
        """Test subtraction operation."""
        assert 5 - 3 == 2

    def test_multiplication(self):
        """Test multiplication operation."""
        assert 6 * 7 == 42

    def test_division(self):
        """Test division operation."""
        assert 10 / 2 == 5.0

    @pytest.mark.parametrize("a,b,expected", [
        (3, 4, 7),
        (10, 5, 15),
        (-2, 3, 1)
    ])
    def test_sum(self, a, b, expected):
        """Test sum with parameterized values."""
        assert a + b == expected

    @pytest.mark.parametrize("a,b", [
        (0, 0),
        (5, -5)
    ])
    def test_zero_cases(self, a, b):
        """Test edge cases with zero/negative values."""
        result = abs(a * b)
        assert result == 25
