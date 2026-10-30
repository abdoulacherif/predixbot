import os
import re

for filename in os.listdir('www'):
    if not filename.endswith('.html'):
        continue

    filepath = os.path.join('www', filename)
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Cas 1 : fetch(window.API_BASE + '...', { ... }) sans credentials
    content = re.sub(
        r"fetch\(window\.API_BASE \+ ([^,]+),(\s*)\{(?!\s*credentials)",
        lambda m: "fetch(window.API_BASE + " + m.group(1) + "," + m.group(2) + "{ credentials: 'include',",
        content
    )

    # Cas 2 : fetch(window.API_BASE + '...') sans options
    content = re.sub(
        r"fetch\(window\.API_BASE \+ ([^)]+)\)(?!\s*\.)",
        lambda m: "fetch(window.API_BASE + " + m.group(1) + ", { credentials: 'include' })",
        content
    )

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print("OK : " + filename + " corrige")

print("--- Termine ---")
