#!/usr/bin/env python3
"""Phase 1: Architecture Verification Script"""
import os
import json

print("=" * 60)
print("PHASE 1: ARCHITECTURE VERIFICATION")
print("=" * 60)

# 1.1 Directory Structure
print("\n[1.1] DIRECTORY STRUCTURE")
root = "D:\\My_head_folders\\My-desktop\\Agentic_Loop_Graph"
for d in os.listdir(root):
    full_path = os.path.join(root, d)
    print(f"  {d}/" if os.path.isdir(full_path) else f"  {d}")

# 1.2 Key Specification Files
print("\n[1.2] KEY SPECIFICATION FILES")
spec_files = [
    "TECHNICAL_ASSIGNMENT.md",
    "AGENTS.md", 
    "project_rules.md",
    "backend_spec_bridge_plan.md"
]
for f in spec_files:
    path = os.path.join(root, f)
    exists = os.path.exists(path)
    print(f"  {'✓' if exists else '✗':3} {f}")

# 1.3 Figma Integration
print("\n[1.3] FIGMA INTEGRATION")
figma_files = [
    "figma_component_map.json",
    "figma_component_mappings.json"
]
for f in figma_files:
    path = os.path.join(root, f)
    if os.path.exists(path):
        with open(path) as fp:
            data = json.load(fp)
            print(f"  ✓ {f} - {type(data).__name__}")
    else:
        print(f"  ✗ {f}")

print("\n" + "=" * 60)
print("PHASE 1 COMPLETE")
print("=" * 60)