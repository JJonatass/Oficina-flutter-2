/* Oficina Flutter 2: service worker. Guarda a página e as fontes para abrir sem internet. */
const VERSAO = '0ea8c35204';
const CACHE = 'oficina2-' + VERSAO;
const BASE = ['./', 'index.html', 'manifest.webmanifest', 'icone-192.png', 'icone-512.png', 'icone-180.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(BASE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k.startsWith('oficina2-') && k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (req.mode === 'navigate' || (url.origin === location.origin && BASE.some((b) => url.pathname.endsWith(b.replace('./', '/'))))) {
    // página: rede primeiro (para pegar a versão nova); sem rede, a cópia guardada
    e.respondWith(fetch(req).then((r) => { const cp = r.clone(); caches.open(CACHE).then((c) => c.put(req, cp)); return r; })
      .catch(() => caches.match(req).then((r) => r || caches.match('index.html'))));
    return;
  }
  if (/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname)) {
    // fontes: cópia guardada primeiro
    e.respondWith(caches.match(req).then((r) => r || fetch(req).then((resp) => { const cp = resp.clone(); caches.open(CACHE).then((c) => c.put(req, cp)); return resp; })));
  }
});
