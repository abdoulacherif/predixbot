import os
import re

# ============================================================
# 1. CODE DU MENU BURGER À DROITE (avec logo à gauche)
# ============================================================
BURGER_HTML = """
<!-- MENU BURGER -->
<div id="burgerBtn" style="position:fixed;top:14px;right:16px;z-index:9998;">
  <button onclick="toggleBurger()" style="width:42px;height:42px;border-radius:12px;background:#fff;border:1px solid rgba(14,42,27,0.1);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
    <span style="width:18px;height:2px;background:#0E2A1B;border-radius:2px;"></span>
    <span style="width:18px;height:2px;background:#0E2A1B;border-radius:2px;"></span>
    <span style="width:18px;height:2px;background:#0E2A1B;border-radius:2px;"></span>
  </button>
</div>
<div id="burgerOverlay" onclick="toggleBurger()" style="position:fixed;inset:0;background:rgba(0,0,0,0.4);z-index:9998;display:none;"></div>
<div id="burgerPanel" style="position:fixed;top:0;right:-300px;width:280px;height:100vh;background:#fff;z-index:9999;transition:right 0.3s ease;box-shadow:-4px 0 24px rgba(0,0,0,0.1);padding:24px 20px;overflow-y:auto;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;">
    <span style="font-family:'Fraunces',serif;font-style:italic;font-size:22px;">Kon<span style="color:#128C4A;">tak</span></span>
    <button onclick="toggleBurger()" style="background:none;border:none;font-size:22px;cursor:pointer;">✕</button>
  </div>
  <a href="./dashboard.html" style="display:block;padding:12px;border-radius:10px;color:#0E2A1B;font-weight:600;text-decoration:none;margin-bottom:4px;">Tableau de bord</a>
  <a href="./annuaire.html" style="display:block;padding:12px;border-radius:10px;color:#0E2A1B;font-weight:600;text-decoration:none;margin-bottom:4px;">Annuaire</a>
  <a href="./profile.html" style="display:block;padding:12px;border-radius:10px;color:#0E2A1B;font-weight:600;text-decoration:none;margin-bottom:4px;">Mon profil</a>
  <a href="./abonnement.html" style="display:block;padding:12px;border-radius:10px;color:#0E2A1B;font-weight:600;text-decoration:none;margin-bottom:4px;">Crédits</a>
  <a href="./mail.html" style="display:block;padding:12px;border-radius:10px;color:#0E2A1B;font-weight:600;text-decoration:none;margin-bottom:4px;">Campagnes mail</a>
  <a href="./parrainage.html" style="display:block;padding:12px;border-radius:10px;color:#0E2A1B;font-weight:600;text-decoration:none;margin-bottom:4px;">Parrainage</a>
  <a href="./support.html" style="display:block;padding:12px;border-radius:10px;color:#0E2A1B;font-weight:600;text-decoration:none;margin-bottom:4px;">Support</a>
  <a href="./faq.html" style="display:block;padding:12px;border-radius:10px;color:#0E2A1B;font-weight:600;text-decoration:none;margin-bottom:4px;">FAQ</a>
  <a href="#" onclick="logoutApp();return false;" style="display:block;padding:12px;border-radius:10px;color:#D9534F;font-weight:600;text-decoration:none;margin-top:16px;border-top:1px solid rgba(0,0,0,0.1);">Déconnexion</a>
</div>
<script>
function toggleBurger() {
  var p = document.getElementById('burgerPanel');
  var o = document.getElementById('burgerOverlay');
  if (p.style.right === '0px') { p.style.right = '-300px'; o.style.display = 'none'; }
  else { p.style.right = '0px'; o.style.display = 'block'; }
}
async function logoutApp() {
  await fetch(window.API_BASE + '/api/auth/session', { method: 'DELETE', credentials: 'include' });
  window.location.href = './index.html';
}
</script>
"""

# ============================================================
# 2. CODE DE LA BARRE DE NAVIGATION BAS (via l'API)
# ============================================================
NAVBAR_HTML = """
<nav class="fixed-navbar" id="fixedNavbar"></nav>
<script>
const ICONS_NAV = {
  business: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
  mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>',
  server: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="7" rx="1.5"/><rect x="2" y="14" width="20" height="7" rx="1.5"/><line x1="6" y1="6.5" x2="6.01" y2="6.5"/><line x1="6" y1="17.5" x2="6.01" y2="17.5"/></svg>',
  user: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg>'
};
function iconNav(key) { return '<span class="ic-svg">' + (ICONS_NAV[key] || ICONS_NAV.user) + '</span>'; }
async function renderFixedNavbar() {
  try {
    const res = await fetch(window.API_BASE + '/api/nav-items', { credentials: 'include' });
    const data = await res.json();
    const items = data.items || [];
    const bar = document.getElementById('fixedNavbar');
    if (!bar) return;
    if (items.length === 0) { bar.style.display = 'none'; return; }
    bar.innerHTML = items.map(it => '<a class="fnav-btn" href="./' + it.url + '">' + iconNav(it.icon) + '<span>' + it.label + '</span></a>').join('');
  } catch(e) { console.error(e); }
}
renderFixedNavbar();
</script>
"""

# ============================================================
# 3. LISTE DES PAGES À TRAITER
# ============================================================
pages_without_burger = [
    'annuaire.html', 'profile.html', 'abonnement.html', 'mail.html',
    'parrainage.html', 'support.html', 'faq.html', 'business.html',
    'serveur.html', 'gain.html', 'reseau.html', 'cagnotte.html',
    'conditions.html', 'politique.html', 'fiche.html'
]

pages_without_navbar = [
    'annuaire.html', 'profile.html', 'abonnement.html', 'mail.html',
    'parrainage.html', 'support.html', 'faq.html', 'business.html'
]

# ============================================================
# 4. APPLICATION DES MODIFICATIONS
# ============================================================
for filename in os.listdir('www'):
    if not filename.endswith('.html'): continue
    filepath = os.path.join('www', filename)
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content

    # --- Ajouter le burger si nécessaire ---
    if filename in pages_without_burger and 'id="burgerBtn"' not in content:
        content = content.replace('</body>', BURGER_HTML + '\n</body>')
        print(f'✅ Burger ajouté à {filename}')

    # --- Ajouter la navbar si nécessaire ---
    if filename in pages_without_navbar and 'id="fixedNavbar"' not in content:
        content = content.replace('</body>', NAVBAR_HTML + '\n</body>')
        print(f'✅ Navbar ajoutée à {filename}')

    # --- Corriger les liens sans .html ---
    for page in ['dashboard', 'annuaire', 'profile', 'abonnement', 'mail',
                 'parrainage', 'support', 'faq', 'business', 'serveur',
                 'gain', 'reseau', 'cagnotte', 'conditions', 'politique',
                 'connexion', 'inscription']:
        content = re.sub(r'href="' + page + r'"', f'href="./{page}.html"', content)
        content = re.sub(r"href='" + page + r"'", f"href='./{page}.html'", content)

    # --- S'assurer que window.API_BASE existe ---
    if 'window.API_BASE' not in content:
        content = content.replace('<head>', '<head>\n<script>window.API_BASE = \'https://kontaks.vercel.app\';</script>', 1)

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)

print("\n🎉 Terminé ! Toutes les pages ont été mises à jour.")
