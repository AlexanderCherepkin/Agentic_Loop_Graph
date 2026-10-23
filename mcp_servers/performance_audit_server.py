"""Performance Audit MCP Server - Lighthouse-based performance auditing via Model Context Protocol."""

import asyncio
import json
import subprocess
import os
from typing import Any, Optional
from mcp.server import Server
from mcp.types import Tool

server = Server("performance-audit-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Return available performance audit tools."""
    return [
        create_audit_lighthouse_metrics_tool(),
        create_validate_accessibility_tool(),
        create_generate_performance_report_tool(),
    ]


def create_audit_lighthouse_metrics_tool() -> Tool:
    """Create Lighthouse metrics audit tool."""
    return Tool(
        name="audit_lighthouse_metrics",
        description=(
            "Audit Lighthouse metrics including Performance, Accessibility, Best Practices, and SEO. "
            "Returns comprehensive scores and actionable recommendations."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "categories": {"type": "array", "items": {"type": "string"}},
                "thresholds": {"type": "object"}
            },
            "required": ["url"]
        }
    )


def create_validate_accessibility_tool() -> Tool:
    """Create accessibility validation tool."""
    return Tool(
        name="validate_accessibility",
        description=(
            "Validate WCAG 2.1 compliance using Lighthouse and axe-core. "
            "Returns detailed violation reports with impact levels."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "url_or_path": {"type": "string"},
                "wcag_version": {"type": "string", "enum": ["2.0", "2.1", "2.2"]},
                "conformance_level": {"type": "string", "enum": ["A", "AA", "AAA"]},
                "axe_rules": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["url_or_path"]
        }
    )


def create_generate_performance_report_tool() -> Tool:
    """Create performance report generation tool."""
    return Tool(
        name="generate_performance_report",
        description=(
            "Generate comprehensive reports with Core Web Vitals and detailed metrics analysis. "
            "Supports JSON, HTML, and Markdown output formats."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "report_format": {"type": "string", "enum": ["json", "html", "markdown"]},
                "include_chromium_audit": {"type": "boolean"},
                "sample_size": {"type": "integer"}
            },
            "required": ["url"]
        }


async def run_lighthouse(url: str, categories=None) -> dict:
    """Run Lighthouse audit via CLI."""
    try:
        cmd = ['npx', '--yes', 'lighthouse', url, '--output=json']
        if categories and isinstance(categories, list):
            for cat in categories:
                cmd.extend(['--category', cat])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return {"success": True, "data": json.loads(result.stdout)}
        else:
            return {"success": False, "error": f"Lighthouse failed with code {result.returncode}", "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Lighthouse timed out after 5 minutes"}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def run_axe_core(url_or_path: str) -> dict:
    """Run axe-core accessibility audit via puppeteer."""
    try:
        cmd = ['npx', '--yes', '@axe-core/puppeteer', url_or_path, '--reporter=json']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return {"success": True, "data": json.loads(result.stdout)}
        else:
            return {"success": False, "error": f"Axe-core failed with code {result.returncode}", "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Axe-core timed out after 5 minutes"}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def run_lighthouse_report(url: str, format_type: str = 'html') -> dict:
    """Generate Lighthouse report in specified format."""
    try:
        cmd = ['npx', '--yes', 'lighthouse', url, f'--output={format_type}']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return {"success": True, "message": f"Report generated successfully as {format_type}", "file": url.replace('/', '_').replace('.', '_') + f'.{format_type}'}
        else:
            return {"success": False, "error": f"Lighthouse failed with code {result.returncode}", "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Lighthouse timed out after 5 minutes"}
    except Exception as e:
        return {"success": False, "error": str(e)}

    )



from typing import Any
from mcp.types import Tool
from mcp.server import Server
import asyncio, json, subprocess, os
