import sys
sys.path.insert(0, '.')
from utils import clean_text, parse_command_lines, extract_config_vars

print("\n=== Testing Settngs.LLM Utils ===")

# Test 1: clean_text
result = clean_text('  Hello   World!  \n\tTest\n')
assert 'Hello World!' in result and '\n' not in result, f"clean_text failed: {repr(result)}"
print("✓ clean_text works")

# Test 2: parse_command_lines
test = "cd /home && export PATH=/usr/bin"
cmds = parse_command_lines(test)
assert len(cmds) == 2, f"parse_command_lines failed: {cmds}"
print(f"✓ parse_command_lines works: {len(cmds)} commands")

# Test 3: extract_config_vars
config = extract_config_vars('export PATH=/usr/bin\n--port 8080')
assert 'PATH' in config, f"extract_config_vars failed: {config}"
print(f"✓ extract_config_vars works: {config}")

print("\n✅ All tests passed!")
