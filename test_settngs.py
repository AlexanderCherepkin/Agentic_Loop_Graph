import sys
sys.path.insert(0, r'D:/My_head_folders/My-desktop/Settngs.LLM')
from utils import clean_text, parse_command_lines, extract_config_vars
print('Import successful!')
result = clean_text('  Hello   World!\nTest\n')
print(f'clean_text result: {repr(result)}')
cmds = parse_command_lines('cd /home && export PATH=/usr/bin')
print(f'Commands found: {len(cmds)}')
config = extract_config_vars('export VAR=test --port 8080')
print(f'Config: {config}')
