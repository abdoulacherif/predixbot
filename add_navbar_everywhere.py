import os

# Le code de la navbar (identique à celle du dashboard)
NAVBAR_CODE = """
<nav class="fixed-navbar" id="fixedNavbar" style="position:fixed;left:0;right:0;bottom:0;z-index:50;background:#fff;border-top:1px solid rgba(14,42,27,0.1);display:flex;justify-content:space-around;align-items:center;padding:8px 10px calc(8px + env(safe-area-inset-bottom));box-shadow:0 -4px 16px rgba(14,42,27,0.06);"></nav>
<script>
const ICONS_NAV = {
  business: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
  mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>',
  server: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="7" rx="1.5"/><rect x="2" y="14" width="20" height="7" rx="1.5"/><line x1="6" y1="6.5" x2="6.01" y2="6.5"/><line x1="6" y1="17.5" x2="6.01" y2="17.5"/></svg>',
  user: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg>'
};
function iconNav(key) { return '<span class="ic-svg" style="width:20px;height:20px;display:inline-flex;align-items:center;justify-content:center;">' + (ICONS_NAV[key] || ICONS_NAV.user) + '</span>'; }

async function renderFixedNavbar() {
  try {
    const res = await fetch(window.API_BASE + '/api/nav-items', { credentials: 'include' });
    const data = await res.json();
    const items = data.items || [];
    const bar = document.getElementById('fixedNavbar');
    if (!bar) return;
    if (items.length === 0) { bar.style.display = 'none'; return; }
    bar.innerHTML = items.map(it => 
      '<a class="fnav-btn" href="./' + it.url + '" style="display:flex;flex-direction:column;align-items:center;gap:4px;padding:6px 10px;border-radius:12px;color:rgba(14,42,27,0.55);text-decoration:none;font-size:11px;font-weight:600;flex:1;text-align:center;">' + 
      iconNav(it.icon) + '<span>' + it.label + '</span></a>'
    ).join('');
  } catch(e) { console.error(e); }
}
renderFixedNavbar();
</script>
"""

# Pages qui ont besoin de la navbar
pages_without_navbar = [
    'annuaire.html', 'profile.html', 'abonnement.html', 'mail.html',
    'parrainage.html', 'support.html', 'faq.html', 'business.html',
    'serveur.html', 'gain.html', 'reseau.html', 'cagnotte.html',
    'conditions.html', 'politique.html', 'fiche.html'
]

for filename in pages_without_navbar:
    filepath = os.path.join('www', filename)
    if not os.path.exists(filepath):
        print(f'⚠️ {filename} introuvable, ignoré')
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'id="fixedNavbar"' in content:
        print(f'✅ {filename} a déjà la navbar')
        continue
    
    # Ajouter la navbar avant </body>
    content = content.replace('</body>', NAVBAR_CODE + '\n</body>')
    
    with open(filepath, 'w') as f:
        f.write(content)
        print(f'✅ Navbar ajoutée à {filename}')

print('\n🎉 Navbar ajoutée partout !')
