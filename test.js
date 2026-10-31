const SECTORS = ['Commerce','Mode & beauté','Restauration','Services','Tech & digital','Immobilier','Éducation','Autre'];
const ICONS = {
  business: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
  mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>',
  server: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="7" rx="1.5"/><rect x="2" y="14" width="20" height="7" rx="1.5"/><line x1="6" y1="6.5" x2="6.01" y2="6.5"/><line x1="6" y1="17.5" x2="6.01" y2="17.5"/></svg>',
  user: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg>'
};
function icon(key, cls){ return `<span class="ic-svg ${cls||''}">${ICONS[key] || ICONS.user}</span>`; }
function escapeHtml(s){ const d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
function initials(name){ return (name||'').trim().split(/\s+/).map(w=>w[0]).slice(0,2).join('').toUpperCase(); }
function showToast(msg, type='success'){ const t = document.getElementById('toast'); t.textContent = msg; t.style.background = type === 'error' ? '#D9534F' : (type === 'info' ? '#128C4A' : '#0E2A1B'); t.classList.add('show'); setTimeout(()=>t.classList.remove('show'), 3500); }

let activeFilter = 'Tous';
let loadToken = 0;

async function renderFixedNavbar(){
  try{
    const res = await fetch(window.API_BASE + '/api/nav-items', { credentials: 'include' });
    const data = await res.json();
    const items = data.items || [];
    const bar = document.getElementById('fixedNavbar');
    if(items.length === 0){ bar.style.display='none'; return; }
    bar.innerHTML = items.map(it=>`<a class="fnav-btn" href="./${escapeHtml(it.url)}">${icon(it.icon)}<span>${escapeHtml(it.label)}</span></a>`).join('');
  }catch(e){ document.getElementById('fixedNavbar').style.display = 'none'; }
}

function renderFilters(){
  const el = document.getElementById('filters');
  const cats = ['Tous', ...SECTORS];
  el.innerHTML = cats.map(c=>`<button class="chip ${c===activeFilter?'active':''}" onclick="setFilter('${c}')">${c}</button>`).join('');
}
function setFilter(c){ activeFilter = c; renderFilters(); loadProfiles(); }
function debounce(fn, delay){ let t; return (...args)=>{ clearTimeout(t); t = setTimeout(()=>fn(...args), delay); }; }
const debouncedSearch = debounce(()=> loadProfiles(), 400);

async function loadProfiles(){
  const myToken = ++loadToken;
  const grid = document.getElementById('grid');
  grid.innerHTML = '<div class="empty">Chargement…</div>';
  
  const q = document.getElementById('searchInput').value.trim();
  const params = new URLSearchParams();
  if(activeFilter !== 'Tous') params.set('sector', activeFilter);
  if(q) params.set('q', q);
  params.set('limit', 50);

  try{
    const res = await fetch(window.API_BASE + `/api/directory/list?${params.toString()}`, { credentials: 'include' });
    if(!res.ok) throw new Error('Erreur');
    const data = await res.json();
    
    if(myToken !== loadToken) return;
    
    const profiles = data.profiles || [];
    if(profiles.length === 0){
      grid.innerHTML = '<div class="empty">Aucun résultat trouvé.</div>';
      return;
    }

    grid.innerHTML = profiles.map(c => {
      const avatarHtml = c.avatar_url 
        ? `<img src="${escapeHtml(c.avatar_url)}" alt="">`
        : initials(c.business || c.nom);
        
      return `
      <div class="card">
        <div class="card-top">
          <div class="avatar">${avatarHtml}</div>
          <div class="card-info">
            <div class="card-name">${escapeHtml(c.business || c.nom)} ${c.is_boosted ? '<span class="star">⭐</span>' : ''}</div>
            <div class="card-loc">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              ${escapeHtml(c.ville || '')}${c.pays ? ', '+escapeHtml(c.pays) : ''}
            </div>
            <div class="card-cat">${escapeHtml(c.secteur || '')}</div>
          </div>
        </div>
        <div class="card-actions">
          <button class="btn-action btn-wa" onclick="contactWhatsapp('${escapeHtml(c.whatsapp)}', '${escapeHtml(c.business || c.nom)}')">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.297-.497.1-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.126.553 4.12 1.52 5.855L.012 24l6.317-1.652A11.95 11.95 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.826 0-3.542-.5-5.02-1.372l-.36-.212-3.75.98.999-3.65-.234-.375A9.94 9.94 0 012 12c0-5.523 4.477-10 10-10s10 4.477 10 10-4.477 10-10 10z"/></svg>
            WhatsApp
          </button>
          <button class="btn-action btn-save" onclick="openSaveMenu('${escapeHtml(c.business || c.nom)}', '${escapeHtml(c.whatsapp)}', '${escapeHtml(c.ville || '')}', '${escapeHtml(c.pays || '')}', '${escapeHtml(c.secteur || '')}', '${escapeHtml(c.user_id || '')}')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
            Enregistrer
          </button>
        </div>
      </div>
      `;
    }).join('');

  }catch(e){
    if(myToken === loadToken) grid.innerHTML = '<div class="empty">Erreur de chargement.</div>';
  }
}

function contactWhatsapp(phone, business){
  const clean = (phone || '').replace(/\D/g, '');
  const msg = encodeURIComponent(`Bonjour, je vous ai trouvé sur Kontak — je voudrais discuter de ${business || 'votre activité'}.`);
  window.open(`https://wa.me/${clean}?text=${msg}`, '_blank');
}

// Enregistrement DIRECT dans le carnet d'adresses

let ACTIVE_CONTACT = null;

function openSaveMenu(business, phone, ville, pays, secteur, targetUserId) {
  ACTIVE_CONTACT = { business, phone, ville, pays, secteur, targetUserId };
  document.getElementById('saveContactName').textContent = business;
  document.getElementById('saveOverlay').classList.add('open');
}

function closeSaveMenu() {
  document.getElementById('saveOverlay').classList.remove('open');
}

async function saveToPhoneBook() {
  const { business, phone, ville, pays, secteur, targetUserId } = ACTIVE_CONTACT;
  const cleanPhone = (phone || '').replace(/\D/g, '');

  try {
    let mutual = false;
    if (targetUserId) {
      try {
        const res = await fetch(window.API_BASE + '/api/directory/save-contact', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ targetUserId })
        });
        const data = await res.json();
        if (res.ok && data.mutual) mutual = true;
      } catch(e) { console.error(e); }
    }

    if (window.Contacts) {
      const perm = await window.Contacts.checkPermissions();
      if (perm.contacts !== 'granted') {
        const req = await window.Contacts.requestPermissions();
        if (req.contacts !== 'granted') {
          return showToast('Permission refusée.', 'error');
        }
      }

      await window.Contacts.createContact({
        contact: {
          name: { given: business, family: '' },
          organization: { company: 'Kontak', title: secteur || '' },
          phones: [{ label: 'mobile', number: cleanPhone }],
          addresses: [{ label: 'home', street: '', city: ville || '', country: pays || '', postalCode: '', region: '', type: 'home' }],
          note: 'Via l annuaire Kontak'
        }
      });

      if (mutual) showToast('🤝 Vous vous êtes enregistrés mutuellement !', 'info');
      else showToast('Contact enregistré dans ton téléphone ✓', 'success');
      closeSaveMenu();
      return;
    }

    const vcard = [
      'BEGIN:VCARD',
      'VERSION:3.0',
      'FN:' + business,
      'ORG:Kontak',
      'TITLE:' + (secteur || ''),
      'TEL;TYPE=CELL:' + cleanPhone,
      'ADR:;;' + (ville || '') + ';;;' + (pays || ''),
      'NOTE:Via l annuaire Kontak',
      'END:VCARD'
    ].join(String.fromCharCode(13, 10));

    const blob = new Blob([vcard], { type: 'text/vcard;charset=utf-8' });
    const url = URL.createObjectURL(blob);

    if (mutual) showToast('🤝 Vous vous êtes enregistrés mutuellement !', 'info');
    else showToast('Choisis Ajouter aux contacts ✓', 'success');

    setTimeout(() => {
      window.location.href = url;
      setTimeout(() => URL.revokeObjectURL(url), 3000);
    }, mutual ? 1200 : 600);

    closeSaveMenu();
  } catch (error) {
    console.error('Save contact error:', error);
    showToast('Erreur : ' + (error.message || 'impossible d enregistrer'), 'error');
  }
}

async function downloadCSV() {
  const { business, phone, ville, pays, secteur } = ACTIVE_CONTACT;
  const cleanPhone = (phone || '').replace(/\D/g, '');

  const NL = String.fromCharCode(10);
  const header = 'Nom,Business,WhatsApp,Ville,Pays,Secteur,Source';
  const row = [business, business, cleanPhone, ville, pays, secteur, 'Kontak']
    .map(v => '"' + String(v || '').replace(/"/g, '""') + '"')
    .join(',');
  const csv = header + NL + row;

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'kontak-' + (business || 'contact').replace(/\s+/g, '-').toLowerCase() + '.csv';
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 3000);

  showToast('Fichier CSV téléchargé ✓', 'success');
  closeSaveMenu();
}


// Initialisation
renderFilters();
loadProfiles();
renderFixedNavbar();

// Vérifier si le plugin Contacts est chargé


// Demander la permission de manière persistante (au cas où elle a été refusée)
async function requestContactPermission() {
  try {
    const perm = await window.Contacts.checkPermissions();
    if (perm.contacts !== 'granted') {
      await window.Contacts.requestPermissions();
    }
  } catch(e) { console.log('Permission check:', e); }
}

// Petite pause pour laisser Capacitor charger le plugin
setTimeout(() => { requestContactPermission(); }, 1500);
</script>

<div class="overlay" id="saveOverlay">
  <div class="modal">
    <div class="modal-header">
      <h2>Enregistrer ce contact</h2>
      <button class="close-btn" onclick="closeSaveMenu()">✕</button>
    </div>
    <p style="color:var(--muted);font-size:14px;margin-bottom:16px;" id="saveContactName">—</p>
    
    <button class="dl-option" onclick="saveToPhoneBook()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
      <div>
        <div class="dl-title">Enregistrer dans le répertoire</div>
        <div class="dl-sub">Ajout automatique à tes contacts</div>
      </div>
    </button>
    
    <button class="dl-option" onclick="downloadCSV()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>
      <div>
        <div class="dl-title">Télécharger en CSV</div>
        <div class="dl-sub">Compatible Excel, Google Sheets</div>
      </div>
    </button>
  </div>
</div>

