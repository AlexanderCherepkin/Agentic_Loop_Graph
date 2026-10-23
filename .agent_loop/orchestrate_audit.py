#!/usr/bin/env python3
"""
Lighthouse Audit Control System - Main Orchestration Script
Orchestrates audit agents, manages execution flow, and generates compliance reports.
"""

import sys
import os
from pathlib import Path
from datetime import datetime


def initialize_runtime(base_path: str = ".") -> object:
    """Initialize the agent runtime environment."""
    sys.path.insert(0, base_path)
    from agent_runtime import AgentRuntime
    return AgentRuntime(base_path)


def list_agents(runtime):
    """List all available audit agents and their tools."""
    print("\n" + "="*70)
    print("🔍 LIGHTHOUSE AUDIT CONTROL SYSTEM - AVAILABLE AGENTS")
    print("="*70)
    
    agents = runtime.list_available_agents()
    
    if not agents:
        print("\nNo audit agents configured.")
        return
    
    for agent in agents:
        print(f"\n{'─'*70}")
        print(f"📦 Agent: {agent['name']}")
        print(f"   ID: {agent['id']}")
        print(f"   Description: {agent.get('description', '')[:120]}...")
        print(f"   Priority: {agent.get('priority', 'medium').upper()}")
        
        tools = agent.get("tools", [])
        if tools:
            print(f"   Tools:")
            for tool in tools:
                print(f"      • {tool}")


def list_tools(runtime):
    """List all available audit tools."""
    print("\n" + "="*70)
    print("🛠️  LIGHTHOUSE AUDIT CONTROL SYSTEM - AVAILABLE TOOLS")
    print("="*70)
    
    tools = runtime.list_available_tools()
    
    if not tools:
        print("\nNo audit tools available.")
        return
    
    for tool in tools:
        config_path = runtime.tools_dir / f"{tool}.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            description = config.get('description', '')[:100] + "..."
            print(f"\n  {tool}")
            print(f"    Description: {description}")


def execute_tool(runtime, tool_name, params):
    """Execute a specific audit tool with given parameters."""
    print("\n" + "="*70)
    print(f"⚡ EXECUTING TOOL: {tool_name.upper()}")
    print("="*70)
    
    result = runtime.execute_tool(tool_name, params)
    
    if not result.get("success"):
        print(f"\n❌ Tool execution failed:")
        print(f"   Error: {result.get('error', 'Unknown error')}")
        return
    
    print(f"\n✅ Tool executed successfully!")
    print(f"   Status: {result.get('status', 'completed')}")
    if "execution_time" in result:
        print(f"   Completed at: {result['execution_time']}")


def generate_report(runtime, agent_id, results):
    """Generate comprehensive audit report."""
    print("\n" + "="*70)
    print("📊 GENERATING AUDIT REPORT")
    print("="*70)
    
    report_path = runtime.generate_audit_report(agent_id, results)
    print(f"\n✅ Report generated successfully!")
    print(f"   Location: {report_path}")


def main():
    """Main entry point for audit orchestration."""
    base_path = Path(__file__).parent.parent
    
    # Initialize runtime
    runtime = initialize_runtime(str(base_path))
    
    if len(sys.argv) < 2:
        print("\n" + "="*70)
        print("🚀 LIGHTHOUSE AUDIT CONTROL SYSTEM")
        print("="*70)
        print(f"\nBase Path: {base_path}")
        
        # Show available commands
        print("\nAvailable Commands:")
        print("  python -m orchestrate_audit list-agents     # List all audit agents")
        print("  python -m orchestrate_audit tools           # List available tools")
        print("  python -m orchestrate_audit execute <tool>  # Execute specific tool")
        print("  python -m orchestrate_audit report          # Generate audit report")
        
        # Show available agents
        print("\n" + "-"*70)
        list_agents(runtime)
        
        return
    
    command = sys.argv[1]
    
    if command == "list-agents":
        list_agents(runtime)
    
    elif command == "tools":
        list_tools(runtime)
    
    elif command == "execute":
        if len(sys.argv) < 3:
            print("\n❌ Error: Tool name required")
            print(f"   Usage: python -m orchestrate_audit execute <tool_name> [params]")
            return
        
        tool_name = sys.argv[2]
        
        # Parse parameters from remaining arguments
        params = {}
        for arg in sys.argv[3:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                try:
                    params[key.strip()] = json.loads(value.strip())
                except (json.JSONDecodeError, ValueError):
                    params[key.strip()] = value.strip()
        
        execute_tool(runtime, tool_name, params)
    
    elif command == "report":
        agent_id = sys.argv[2] if len(sys.argv) > 2 else "default"
        generate_report(runtime, agent_id, {})
    
    else:
        print(f"\n❌ Unknown command: {command}")
        print("\nAvailable commands:")
        print("  list-agents     # List audit agents")
        print("  tools           # List available tools")
        print("  execute <tool>  # Execute specific tool")
        print("  report          # Generate audit report")


if __name__ == "__main__":
    main()