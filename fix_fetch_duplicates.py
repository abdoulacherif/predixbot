import os
import re

for filename in os.listdir('www'):
    if not filename.endswith('.html'):
        continue

    filepath = os.path.join('www', filename)
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Supprimer les ", { credentials: 'include' })" qui sont en trop à la fin
    # On garde le premier bloc d'options qui contient déjà credentials
    content = re.sub(
        r",\s*\{\s*credentials:\s*'include'\s*\}\s*\)",
        ")",
        content
    )

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print("NETTOYE : " + filename)

print("--- Termine ---")
