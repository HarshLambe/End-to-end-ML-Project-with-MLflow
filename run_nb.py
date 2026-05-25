import json
import traceback

try:
    with open('research/01_data_ingestion.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    code = []
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if not source.strip().startswith('%'):
                code.append(source)
            
    full_code = '\n'.join(code)
    
    import os
    os.chdir('research')
    
    exec(full_code, globals())
except Exception as e:
    traceback.print_exc()
