import os
import json
import glob

notebooks = glob.glob('research/*.ipynb')
for nb_file in notebooks:
    with open(nb_file, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    modified = False
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            
            # check if source is just %pwd
            if len(source) > 0 and '%pwd' in source[0] and not source[0].startswith('#'):
                new_source = []
                for line in source:
                    if '%pwd' in line and not line.strip().startswith('#'):
                        new_source.append(line.replace('%pwd', '# %pwd'))
                    else:
                        new_source.append(line)
                cell['source'] = new_source
                modified = True
                
    if modified:
        with open(nb_file, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f"Fixed %pwd in {nb_file}")
