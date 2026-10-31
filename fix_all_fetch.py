import os
import re

for filename in os.listdir('www'):
    if not filename.endswith('.html'): continue
    filepath = os.path.join('www', filename)
    with open(filepath, 'r') as f:
        content = f.read()
    original = content

    # On ajoute credentials sur tous les fetch qui n'en ont pas
    # (regex simple pour cibler les fetch(window.API_BASE + '...'))
    def add_credentials(match):
        url = match.group(1)
        rest = match.group(2)
        # Si "credentials" est déjà là, on ne touche pas
        if "credentials" in rest:
            return match.group(0)
        if rest.strip().startswith('{'):
            return "fetch(window.API_BASE + " + url + ", { credentials: 'include'," + rest[1:] + ")"
        else:
            return "fetch(window.API_BASE + " + url + ", { credentials: 'include' })"

    content = re.sub(r"fetch\(window\.API_BASE \+ ([^,]+)(,\s*\{[^}]*\})?\)", 
                     lambda m: "fetch(window.API_BASE + " + m.group(1) + (m.group(2) if m.group(2) else ", { credentials: 'include' })") if (m.group(2) and 'credentials' not in m.group(2)) or not m.group(2) else m.group(0),
                     content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print('✅ Fetch corrigé pour ' + filename)
