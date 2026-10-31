import os

pages = ['annuaire.html', 'profile.html', 'abonnement.html', 'mail.html',
         'parrainage.html', 'support.html', 'faq.html', 'business.html']

for filename in pages:
    filepath = os.path.join('www', filename)
    if not os.path.exists(filepath): continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'padding-bottom:80px' not in content:
        # Ajouter le padding au body dans le CSS
        content = content.replace('body{', 'body{padding-bottom:80px;', 1)
        with open(filepath, 'w') as f:
            f.write(content)
            print(f'✅ Padding ajouté à {filename}')
    else:
        print(f'✅ {filename} a déjà le padding')

print('\n🎉 Padding ajouté partout !')
