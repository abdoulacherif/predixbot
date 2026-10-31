import os
import re

for filename in os.listdir('www'):
    if not filename.endswith('.html'): continue
    
    filepath = os.path.join('www', filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # 1. Préfixer les fetch('/api/...') avec window.API_BASE
    content = re.sub(
        r"fetch\((['\"])/api/",
        r"fetch(window.API_BASE + \1/api/",
        content
    )
    
    # 2. S'assurer que credentials: 'include' est présent sur les fetch qui n'en ont pas
    # On cherche fetch(...) avec des options mais sans credentials
    def add_credentials(match):
        url = match.group(1)
        options = match.group(2)
        if 'credentials' in options:
            return match.group(0)
        if options.strip() == '':
            return f"fetch({url}, {{ credentials: 'include' }})"
        # Il y a déjà des options, on ajoute credentials au début
        return f"fetch({url}, {{ credentials: 'include', {options.lstrip('{').strip()})"
    
    # On utilise une regex pour capter fetch(url, { ... })
    content = re.sub(
        r"fetch\((window\.API_BASE \+ ['\"][^'\"]+['\"]|['\"][^'\"]+['\"]),\s*\{([^}]*)\}\)",
        lambda m: m.group(0) if 'credentials' in m.group(2) else f"fetch({m.group(1)}, {{ credentials: 'include', {m.group(2).strip()} }})",
        content
    )
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print('✅ ' + filename + ' corrigé')
