const sitiosProhibidos = [
  "youtube.com",
  "tiktok.com",
  "instagram.com",
  "twitter.com",
  "x.com",
  "discord.com"
];

const nombresSitios = {
  "youtube.com": "YouTube",
  "tiktok.com": "TikTok",
  "instagram.com": "Instagram",
  "twitter.com": "Twitter",
  "x.com": "X",
  "discord.com": "Discord"
};

// Mapa de pestañas prohibidas: tabId -> nombre del sitio
const pestañasProhibidas = new Map();

function esProhibido(url) {
  try {
    const host = new URL(url).hostname;
    return sitiosProhibidos.some(site => host === site || host.endsWith('.' + site));
  } catch (e) {
    return false;
  }
}

function nombreDeSitio(url) {
  try {
    const host = new URL(url).hostname;
    for (const dominio of Object.keys(nombresSitios)) {
      if (host === dominio || host.endsWith('.' + dominio)) return nombresSitios[dominio];
    }
  } catch (e) {}
  return "red social";
}

function avisarProcrastinando(sitio) {
  fetch(`http://localhost:5000/procrastinando?sitio=${encodeURIComponent(sitio || 'red social')}`).catch(() => {});
}

function avisarCerrado() {
  fetch('http://localhost:5000/cerrar').catch(() => {});
}

// Detectar pestañas de redes sociales que ya estaban abiertas al iniciar el navegador
async function revisarPestañasExistentes() {
  try {
    const pestañas = await chrome.tabs.query({});
    let alguna = false;
    pestañas.forEach((tab) => {
      if (tab.id != null && tab.url && esProhibido(tab.url)) {
        pestañasProhibidas.set(tab.id, nombreDeSitio(tab.url));
        alguna = true;
      }
    });
    if (alguna) {
      avisarProcrastinando([...pestañasProhibidas.values()][0]);
    }
  } catch (e) {
    console.error(e);
  }
}

chrome.runtime.onInstalled.addListener(revisarPestañasExistentes);
chrome.runtime.onStartup.addListener(revisarPestañasExistentes);

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (!tab.url) return; // URL aún no disponible, no hacer nada

  if (esProhibido(tab.url)) {
    const nombre = nombreDeSitio(tab.url);
    const anterior = pestañasProhibidas.get(tabId);
    pestañasProhibidas.set(tabId, nombre);
    if (anterior !== nombre) {
      avisarProcrastinando(nombre);
    }
  } else if (pestañasProhibidas.delete(tabId)) {
    avisarCerrado();
  }
});

chrome.tabs.onRemoved.addListener((tabId) => {
  if (pestañasProhibidas.delete(tabId)) {
    avisarCerrado();
  }
});

// --- Cierre de pestaña solicitado por los botones "Sí"/"Obvio" de Python ---

async function cerrarPestanasProhibidas() {
  if (pestañasProhibidas.size === 0) return;

  const ids = [...pestañasProhibidas.keys()];

  try {
    await chrome.tabs.remove(ids);
  } catch (e) {
    console.error('No se pudo cerrar la/s pestaña(s):', e);
  }
}

// Long-poll: espera la señal "cierra" de Python y cierra la pestaña
async function vigilarPeticionDeCierre() {
  while (true) {
    try {
      const respuesta = await fetch('http://localhost:5000/solicitar-cierre');
      const texto = await respuesta.text();
      if (texto.trim() === 'cierra') {
        await cerrarPestanasProhibidas();
      }
    } catch (e) {
      // Python no está corriendo: reintentar en 3 segundos
      await new Promise(resolve => setTimeout(resolve, 3000));
    }
  }
}

// Se ejecuta cada vez que el service worker arranca
vigilarPeticionDeCierre();