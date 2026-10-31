import os

MOBILE_NAVBAR = """
<nav class="mobile-bottom-nav" style="position:fixed;left:0;right:0;bottom:0;z-index:50;background:#fff;border-top:1px solid rgba(14,42,27,0.1);display:flex;justify-content:space-around;align-items:center;padding:8px 10px calc(8px + env(safe-area-inset-bottom));box-shadow:0 -4px 16px rgba(14,42,27,0.06);">
  <a href="./dashboard.html" style="display:flex;flex-direction:column;align-items:center;gap:4px;text-decoration:none;color:#0E2A1B;font-size:11px;font-weight:600;flex:1;text-align:center;">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#128C4A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7"/><path d="M9 22V12h6v10"/></svg>
    Accueil
  </a>
  <a href="./annuaire.html" style="display:flex;flex-direction:column;align-items:center;gap:4px;text-decoration:none;color:#0E2A1B;font-size:11px;font-weight:600;flex:1;text-align:center;">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#128C4A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>
    Annuaire
  </a>
  <a href="./profile.html" style="display:flex;flex-direction:column;align-items:center;gap:4px;text-decoration:none;color:#0E2A1B;font-size:11px;font-weight:600;flex:1;text-align:center;">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#128C4A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg>
    Profil
  </a>
  <a href="#" onclick="logoutApp();return false;" style="display:flex;flex-direction:column;align-items:center;gap:4px;text-decoration:none;color:#D9534F;font-size:11px;font-weight:600;flex:1;text-align:center;">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#D9534F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
    Quitter
  </a>
</nav>

<script>
async function logoutApp() {
  await fetch(window.API_BASE + '/api/auth/session', { method: 'DELETE', credentials: 'include' });
  window.location.href = './index.html';
}
</script>
"""

connected_pages = ['dashboard.html', 'annuaire.html', 'profile.html', 'abonnement.html',
                   'mail.html', 'parrainage.html', 'support.html', 'faq.html',
                   'business.html', 'serveur.html', 'gain.html', 'reseau.html', 'cagnotte.html']

for filename in connected_pages:
    filepath = os.path.join('www', filename)
    if not os.path.exists(filepath): continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'mobile-bottom-nav' in content:
        print(f'✅ {filename} a déjà la navbar mobile')
        continue
    
    if 'padding-bottom:80px' not in content:
        content = content.replace('body{', 'body{padding-bottom:80px;', 1)
    
    content = content.replace('</body>', MOBILE_NAVBAR + '\n</body>')
    
    with open(filepath, 'w') as f:
        f.write(content)
        print(f'✅ Navbar mobile ajoutée à {filename}')

print('\n🎉 Terminé !')
