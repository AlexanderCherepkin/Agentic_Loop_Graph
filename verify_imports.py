import sys
sys.path.insert(0, 'src')
print('=' * 60)
try:
    from figma_agent_core.api_controller import FigmaExportController
    print('api_controller: OK - FigmaExportController imported successfully')
except Exception as e:
    print(f'api_controller FAILED: {{e}}')
