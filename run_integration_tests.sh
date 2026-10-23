#!/bin/bash
# Integration Test Runner with Code Coverage Report
set -e

cd "$(dirname "$0")"

echo "=========================================="
echo "Running Integration Tests with Coverage"
echo "=========================================="

# Check Python environment
echo "[1/4] Checking Python environment..."
python --version || echo "Python not found, attempting to install..."
pip --version || pip3 --version

# Install pytest-cov if needed
echo "[2/4] Installing test dependencies..."
pip install -q pytest pytest-cov 2>/dev/null || pip3 install -q pytest pytest-cov 2>/dev/null

# Run integration tests with coverage
echo "[3/4] Running integration tests..."
python -m pytest tests/ --cov=api --cov-report=html:coverage_report/tests --cov-report=term-missing -v --tb=short || \
python -m pytest tests/ --cov=api --cov-report=html:coverage_report --cov-report=term-missing -v --tb=short

# Generate summary
echo ""
echo "[4/4] Test run complete!"
echo "Coverage report available at: coverage_report/tests/index.html"