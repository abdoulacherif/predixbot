import os

BURGER_LEFT = """
<!-- BURGER GAUCHE -->
<div id="burgerLeftBtn" style="position:fixed;top:14px;left:14px;z-index:9998;">
  <button onclick="toggleLeftBurger()" style="width:42px;height:42px;border-radius:12px;background:#fff;border:1px solid rgba(14,42,27,0.1);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
    <span style="width:18px;height:2px;background:#0E2A1B;border-radius:2px;"></span>
    <span style="width:18px;height:2px;background:#0E2A1B;border-radius:2px;"></span>
    <span style="width:18px;height:2px;background:#0E2A1B;border-radius:2px;"></span>
  </button>
</div>

<div id="burgerLeftOverlay" onclick="toggleLeftBurger()" style="position:fixed;inset:0;background:rgba(0,0,0,0.4);z-index:9998;display:none;"></div>

<div id="burgerLeftPanel" style="position:fixed;top:0;left:-300px;width:280px;height:100vh;background:#fff;z-index:9999;transition:left 0.3s ease;box-shadow:4px 0 24px rgba(0,0,0,0.1);padding:24px 20px;overflow-y:auto;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;">
    <span style="font-family:'Fraunces',serif;font-style:italic;font-size:22px;">Kon<span style="color:#128C4A;">tak</span></span>
    <button onclick="toggleLeftBurger()" style="background:none;border:none;font-size:22px;cursor:pointer;">✕</button>
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
function toggleLeftBurger() {
  var p = document.getElementById('burgerLeftPanel');
  var o = document.getElementById('burgerLeftOverlay');
  if (p.style.left === '0px') { p.style.left = '-300px'; o.style.display = 'none'; }
  else { p.style.left = '0px'; o.style.display = 'block'; }
}
async function logoutApp() {
  await fetch(window.API_BASE + '/api/auth/session', { method: 'DELETE', credentials: 'include' });
  window.location.href = './index.html';
}
</script>
"""

pages_to_fix = ['annuaire.html', 'fiche.html']

for filename in pages_to_fix:
    filepath = os.path.join('www', filename)
    if not os.path.exists(filepath):
        print(f'⚠️ {filename} introuvable')
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'id="burgerLeftBtn"' in content:
        print(f'✅ {filename} a déjà le burger gauche')
        continue
    
    # Ajouter le burger avant </body>
    content = content.replace('</body>', BURGER_LEFT + '\n</body>')
    
    with open(filepath, 'w') as f:
        f.write(content)
        print(f'✅ Burger gauche ajouté à {filename}')

print('\n🎉 Burger gauche ajouté !')
