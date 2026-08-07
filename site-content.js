/* =====================================================================
   Connexion Supabase — contenu du site "Millionnaire Digital"
   Ce fichier est partagé par toutes les pages (vente, paiement, admin).
   La clé "anon" ci-dessous est PUBLIQUE par conception (comme une clé
   Stripe publishable) — elle ne permet que la lecture, jamais l'écriture
   sans être connecté (voir les policies RLS dans schema.sql).
   ===================================================================== */
const SUPABASE_URL = "https://kkuurolbouqajpumercz.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtrdXVyb2xib3VxYWpwdW1lcmN6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODYwMDgzNzcsImV4cCI6MjEwMTU4NDM3N30.CyR-sMZCCL3onmdmw7w3Z7gNYDaxhIfe1oi0kWGkIz8";

// Récupère le contenu actuel du site depuis Supabase (lecture publique)
async function fetchSiteContent(){
  const res = await fetch(`${SUPABASE_URL}/rest/v1/site_content?id=eq.1&select=*`, {
    headers: {
      apikey: SUPABASE_ANON_KEY,
      Authorization: `Bearer ${SUPABASE_ANON_KEY}`
    }
  });
  if(!res.ok) return null;
  const rows = await res.json();
  return rows && rows[0] ? rows[0] : null;
}

// Remplit tous les éléments [data-field="xxx"] avec content.xxx
// et les images [data-field-img="xxx"] avec content.xxx comme src (si présent).
function applySiteContent(content){
  if(!content) return;
  document.querySelectorAll('[data-field]').forEach(el => {
    const key = el.getAttribute('data-field');
    if(content[key] !== undefined && content[key] !== null && content[key] !== ''){
      el.textContent = content[key];
    }
  });
  document.querySelectorAll('[data-field-img]').forEach(el => {
    const key = el.getAttribute('data-field-img');
    if(content[key]){
      el.src = content[key];
      el.style.display = 'block';
    }
  });
  document.querySelectorAll('[data-field-video]').forEach(el => {
    const key = el.getAttribute('data-field-video');
    renderVideoInto(el, content[key]);
  });
  window.__siteContent = content;
}

// Affiche une vidéo (YouTube, Vimeo, ou fichier direct) dans un élément conteneur
function renderVideoInto(slot, url){
  if(!slot) return;
  if(!url){
    slot.innerHTML = '<div class="video-placeholder">Vidéo à venir</div>';
    return;
  }
  const ytMatch = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([\w-]+)/);
  const vimeoMatch = url.match(/vimeo\.com\/(\d+)/);
  if(ytMatch){
    slot.innerHTML = `<iframe src="https://www.youtube.com/embed/${ytMatch[1]}" allowfullscreen allow="autoplay; encrypted-media"></iframe>`;
  } else if(vimeoMatch){
    slot.innerHTML = `<iframe src="https://player.vimeo.com/video/${vimeoMatch[1]}" allowfullscreen allow="autoplay; fullscreen"></iframe>`;
  } else {
    slot.innerHTML = `<video controls src="${url}"></video>`;
  }
}

async function loadAndApplySiteContent(){
  const content = await fetchSiteContent();
  applySiteContent(content);
  return content;
}
