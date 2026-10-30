import os
import re

for filename in os.listdir('www'):
    if not filename.endswith('.html'):
        continue

    filepath = os.path.join('www', filename)
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # 1. Nettoyer les doublons séquentiels : "credentials: 'include', credentials: 'include',"
    content = re.sub(
        r"credentials:\s*'include',\s*credentials:\s*'include',",
        "credentials: 'include',",
        content
    )
    
    # 2. Nettoyer les doublons dans les objets de options : { credentials: 'include', ... , credentials: 'include' }
    content = re.sub(
        r"credentials:\s*'include',(.*?)credentials:\s*'include'",
        r"credentials: 'include',\1",
        content
    )

    # 3. Enlever les credentials ajoutés par erreur dans le body JSON
    content = re.sub(
        r"JSON\.stringify\(\{ ([^}]+) \}, \{ credentials: 'include' \}\)",
        r"JSON.stringify({ \1 })",
        content
    )

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print("NETTOYE : " + filename)

print("--- Nettoyage termine ---")
