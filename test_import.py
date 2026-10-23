import sys
import os

path = r"D:\My_head_folders\My-desktop\Settngs.LLM"
if not os.path.exists(path):
    print("Path does not exist")
else:
    sys.path.insert(0, path)
    from Settngs.LLM.utils import clean_text, parse_command_lines, extract_config_vars
    print("Import OK")

# Test functions
print("\nTesting clean_text...")
result = clean_text('  Hello   World!  \n\tTest\n')
print(f"✓ clean_text: '{result}'")

print("\nTesting parse_command_lines...")
test_text = """# This is a comment
cd /home/user
export PATH=/usr/bin"""
commands = parse_command_lines(test_text)
print(f"✓ Found {len(commands)} commands: {commands}")

print("\n✅ All tests passed!")