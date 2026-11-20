// Offline cache for the Cyrus compendium. Version changes whenever any file changes.
const VERSION = 'cyrus-90a415ff4e3c';
const FILES = ["./", "assets/app.js", "assets/fonts/alegreya-latin-500-normal.woff2", "assets/fonts/alegreya-latin-700-normal.woff2", "assets/fonts/alegreya-latin-800-normal.woff2", "assets/fonts/alegreya-sans-latin-400-italic.woff2", "assets/fonts/alegreya-sans-latin-400-normal.woff2", "assets/fonts/alegreya-sans-latin-500-normal.woff2", "assets/fonts/alegreya-sans-latin-700-normal.woff2", "assets/glossary.json", "assets/pathfinder-2e-actions.woff2", "assets/style.css", "icons/charcoal-gold-180.png", "icons/charcoal-gold-512.png", "icons/crimson-180.png", "icons/crimson-512.png", "icons/emerald-180.png", "icons/emerald-512.png", "icons/icons.json", "icons/midnight-blue-180.png", "icons/midnight-blue-512.png", "icons/parchment-180.png", "icons/parchment-512.png", "icons/violet-shadow-180.png", "icons/violet-shadow-512.png", "index.html", "manifest.webmanifest", "manifests/charcoal-gold.webmanifest", "manifests/crimson.webmanifest", "manifests/emerald.webmanifest", "manifests/midnight-blue.webmanifest", "manifests/parchment.webmanifest", "manifests/violet-shadow.webmanifest", "pages/aspera.html", "pages/atlas.html", "pages/combat.html", "pages/consumables.html", "pages/feats.html", "pages/glossary.html", "pages/home.html", "pages/items.html", "pages/spells.html"];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;
  e.respondWith(caches.match(e.request, {ignoreSearch: true}).then(hit => hit ||
    (e.request.mode === 'navigate' ? caches.match('index.html') : null) ||
    fetch(e.request)).then(r => r || fetch(e.request)));
});
