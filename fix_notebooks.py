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
            
            # Look for the cell that we modified previously
            has_chdir = any('os.chdir("../")' in line for line in source)
            has_sys_path = any('sys.path.insert' in line for line in source)
            
            if has_chdir and has_sys_path:
                # Replace the source of this cell with a more robust version
                new_source = [
                    "import os\n",
                    "import sys\n",
                    "if os.path.basename(os.getcwd()) == \"research\":\n",
                    "    os.chdir(\"../\")\n",
                    "sys.path.insert(0, os.path.abspath(\"src\"))\n"
                ]
                cell['source'] = new_source
                modified = True
                
    if modified:
        with open(nb_file, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f"Fixed {nb_file}")
