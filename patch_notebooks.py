import os
import json
import glob

notebooks = glob.glob('research/*.ipynb')
for nb_file in notebooks:
    with open(nb_file, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    modified = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = cell.get('source', [])
            if any('os.chdir("../")' in line for line in source) and not any('sys.path' in line for line in source):
                # append sys.path logic
                new_source = []
                for line in source:
                    new_source.append(line)
                    if 'os.chdir("../")' in line:
                        if not line.endswith('\n'):
                            new_source[-1] = new_source[-1] + '\n'
                        new_source.append('import sys\n')
                        new_source.append('sys.path.insert(0, os.path.abspath("src"))\n')
                cell['source'] = new_source
                modified = True
            elif not any('os.chdir("../")' in line for line in source) and 'mlProject' in str(source):
                pass
                
    if modified:
        with open(nb_file, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f"Modified {nb_file}")
