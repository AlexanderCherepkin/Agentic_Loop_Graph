"""Test script for Settngs LLM utils module."""
import sys
sys.path.insert(0, '..')

from Settngs.LLM.utils import clean_text, parse_command_lines, extract_config_vars

# Test clean_text
print("Testing clean_text...")
result = clean_text('  Hello   World!  \n\tTest\n')
assert result == 'Hello World!\nTest', f"Expected 'Hello World!\nTest' but got '{result}'"
print(f"✓ clean_text: '{result}'")

# Test parse_command_lines
print("\nTesting parse_command_lines...")
test_text = """# This is a comment
cd /home/user
export PATH=/usr/bin
python script.py
npm install"""
commands = parse_command_lines(test_text)
print(f"✓ Found {len(commands)} commands: {commands}")

# Test extract_config_vars
print("\nTesting extract_config_vars...")
config_text = 'export MY_VAR="test_value"\n--config my_config.txt'
config = extract_config_vars(config_text)
print(f"✓ Extracted config: {config}")

print("\n✅ All tests passed!")