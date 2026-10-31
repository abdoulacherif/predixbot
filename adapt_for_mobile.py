import os
import re

def replace_fetch(match):
    url = match.group(1)
    options = match.group(3)
    if options:
        if 'credentials' not in options:
            return "fetch(window.API_BASE + " + url + ", { credentials: 'include', " + options.lstrip('{').lstrip()
        return "fetch(window.API_BASE + " + url + ", " + options
    return "fetch(window.API_BASE + " + url + ", { credentials: 'include' })"

for filename in os.listdir('www'):
    if not filename.endswith('.html'): continue
    filepath = os.path.join('www', filename)
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content

    # 1. Ajouter window.API_BASE dans le <head>
    if 'window.API_BASE' not in content:
        content = content.replace('<head>', "<head>\n<script>window.API_BASE = 'https://kontaks.vercel.app';</script>", 1)

    # 2. Remplacer les fetch('/api/...') par fetch(window.API_BASE + '/api/...', { credentials: 'include' })
    pattern = r"fetch\((['\"])/api/([^'\"]+)\1(,\s*\{[^}]*\})?\)"
    content = re.sub(pattern, replace_fetch, content)
    
    # Gestion des backticks
    content = content.replace("fetch(`/api/", "fetch(window.API_BASE + `/api/")
    # Si les credentials manquent sur les backticks, on les ajoute
    content = re.sub(r"fetch\(window\.API_BASE \+ `(/api/[^`]+)`\)", r"fetch(window.API_BASE + `\1`, { credentials: 'include' })", content)

    # 3. Remplacer les liens internes sans .html
    for page in ['dashboard', 'annuaire', 'profile', 'abonnement', 'mail',
                 'parrainage', 'support', 'faq', 'business', 'serveur',
                 'gain', 'reseau', 'cagnotte', 'conditions', 'politique',
                 'connexion', 'inscription', 'admin', 'fiche']:
        content = re.sub(r'href="' + page + r'"', f'href="./{page}.html"', content)
        content = re.sub(r"href='" + page + r"'", f"href='./{page}.html'", content)

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'✅ {filename} adapté')

print('\n🎉 Adaptation terminée')
