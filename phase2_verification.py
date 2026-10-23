#!/usr/bin/env python3
"""Phase 2: Static Code Analysis Script"""
import os
import re

print("=" * 60)
print("PHASE 2: STATIC CODE ANALYSIS")
print("=" * 60)

# 2.1 Python Security Analysis (Bandit-like checks)
print("\n[2.1] PYTHON SECURITY CHECKS")
security_patterns = [
    ("eval/exec", r'\b(eval|exec)\s*\('),
    ("__import__", r'__import__'),
    ("os.system/popen", r'(os\.system|subprocess|popen)'),
]

root = "."
vulnerable_files = []
for dirpath, dirnames, filenames in os.walk(root):
    # Skip test directories and __pycache__
    if 'test' in dirpath.lower() or '__pycache__' in dirpath:
        continue
        
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            for pattern_name, regex_pattern in security_patterns:
                matches = re.finditer(regex_pattern, content, re.IGNORECASE)
                if matches:
                    vulnerable_files.append({
                        'file': filepath,
                        'pattern': pattern_name,
                        'matches': [m.group(0)[:50] for m in list(matches)[:3]]  # Limit to first 3 matches
                    })
        except Exception as e:
            pass

if vulnerable_files:
    print(f"  ⚠ Found {len(vulnerable_files)} potential security issues:")
    for v in vulnerable_files[:10]:  # Show top 10
        print(f"    - {v['file']}: {v['pattern']}")
else:
    print("  ✓ No critical security patterns detected")

# 2.2 Python Style Check (Flake8-like basic checks)
print("\n[2.2] PYTHON STYLE CHECKS (Basic)")
style_issues = []
for dirpath, dirnames, filenames in os.walk(root):
    if 'test' in dirpath.lower() or '__pycache__' in dirpath:
        continue
    
    for filename in filenames:
        if not filename.endswith('.py'):
            continue
            
        filepath = os.path.join(dirpath, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                # Check for trailing whitespace
                if line.rstrip('\n').endswith(' ') or line.rstrip('\n').endswith('\t'):
                    style_issues.append(f"{filepath}:{i}: Trailing whitespace")
                    
                # Check for mixed tabs/spaces (basic)
                if '\t' in line and ' ' in line:
                    style_issues.append(f"{filepath}:{i}: Mixed indentation")
                    
        except Exception as e:
            pass

if len(style_issues) > 0:
    print(f"  ⚠ Found {len(style_issues)} style issues (showing first 15)")
    for issue in style_issues[:15]:
        print(f"    - {issue}")
else:
    print("  ✓ No major style issues detected")

# 2.3 Configuration Files Check
print("\n[2.3] CONFIGURATION FILES CHECK")
config_files = ['pyproject.toml', 'docker-compose.yml', '.gitignore', '.safetyignore']
for f in config_files:
    path = os.path.join(root, f)
    if os.path.exists(path):
        print(f"  ✓ {f} exists")
    else:
        print(f"  ✗ {f} missing")

# 2.4 SQL Injection Check (format string usage in DB queries)
print("\n[2.4] SQL INJECTION CHECK")
db_patterns = [r'\.format\([^)]*\)\s*for\s+.*SQL', r'%s.*\.format']
found_format_in_db = False

for dirpath, dirnames, filenames in os.walk(root):
    if 'database' in dirpath.lower() or 'model' in dirpath.lower():
        for filename in filenames:
            if not filename.endswith('.py'):
                continue
                
            filepath = os.path.join(dirpath, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                for pattern in db_patterns:
                    if re.search(pattern, content):
                        print(f"  ⚠ Potential format string in DB query: {filepath}")
                        found_format_in_db = True
            except Exception:
                pass

if not found_format_in_db:
    print("  ✓ No suspicious .format() patterns in database code")

print("\n" + "=" * 60)
print("PHASE 2 COMPLETE")
print("=" * 60)