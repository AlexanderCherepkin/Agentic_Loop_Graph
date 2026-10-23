print('=== PHASE 1: КЛЮЧЕВЫЕ ФАЙЛЫ ===')
    print(f'{{"✓" if os.path.exists(f) else "✗":20}} {{f}}')
for f in ['TECHNICAL_ASSIGNMENT.md','AGENTS.md','project_rules.md']:
