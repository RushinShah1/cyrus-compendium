// Offline cache for Aspera. Each file is cached under its own content hash, so an update downloads only the files
// that changed. Version dd19b7285b64.
const FILES = {"assets/app.js":"d4ace81887","assets/cs/actions.json":"4d43ba5d28","assets/cs/core.json":"503cbd0b4e","assets/cs/cyrus.json":"6366b37e93","assets/cs/effects.json":"7674ea2d88","assets/cs/engine.js":"f73a5bdd13","assets/cs/feats.json":"45ae43fe8b","assets/cs/items.json":"e518207551","assets/cs/sheet.js":"24d1119e21","assets/cs/spells.json":"0a2a0d91f4","assets/fonts/alegreya-latin-500-normal.woff2":"53addbca37","assets/fonts/alegreya-latin-700-normal.woff2":"1c582501ce","assets/fonts/alegreya-latin-800-normal.woff2":"6017cab559","assets/fonts/alegreya-sans-latin-400-italic.woff2":"5dd7c3e61c","assets/fonts/alegreya-sans-latin-400-normal.woff2":"b2a5a35a25","assets/fonts/alegreya-sans-latin-500-normal.woff2":"55b61d22cc","assets/fonts/alegreya-sans-latin-700-normal.woff2":"5acd19a588","assets/g/index.json":"6064f5d4e8","assets/g/s0.json":"3da26848a2","assets/g/s1.json":"331e9cf196","assets/g/s10.json":"5e27818c4f","assets/g/s100.json":"f16f817c3e","assets/g/s101.json":"b4f08bab33","assets/g/s102.json":"f9a4cddf7c","assets/g/s103.json":"f4e0846be5","assets/g/s104.json":"16349ba3e9","assets/g/s105.json":"59ac5e5335","assets/g/s106.json":"ca992d6b44","assets/g/s107.json":"ea49ea9f3e","assets/g/s108.json":"1717753f14","assets/g/s109.json":"1e6409f500","assets/g/s11.json":"7afc2f1c6a","assets/g/s110.json":"6d934d5131","assets/g/s111.json":"b0960d396f","assets/g/s112.json":"5b3d816de3","assets/g/s113.json":"36fa41cf14","assets/g/s114.json":"19d4744cfa","assets/g/s115.json":"d2d383baa8","assets/g/s116.json":"189c243667","assets/g/s117.json":"5798ded1db","assets/g/s118.json":"0786138fb7","assets/g/s119.json":"b5d6b4335c","assets/g/s12.json":"bc4ec3afe5","assets/g/s120.json":"0c2626f318","assets/g/s121.json":"c382c1bcfa","assets/g/s122.json":"470eb78348","assets/g/s123.json":"acdd81fa7d","assets/g/s124.json":"516706cf4a","assets/g/s125.json":"a0a51a5c6c","assets/g/s126.json":"2f5c9f4d00","assets/g/s127.json":"72658b2739","assets/g/s128.json":"12cd2e0776","assets/g/s129.json":"f76fbda00b","assets/g/s13.json":"2085a5e8eb","assets/g/s130.json":"664e831fab","assets/g/s131.json":"c9590faa1a","assets/g/s132.json":"6ac5755871","assets/g/s133.json":"7ea54f341a","assets/g/s134.json":"1dd104fb4f","assets/g/s135.json":"76fa174954","assets/g/s136.json":"68d8efb77d","assets/g/s137.json":"2982fdb689","assets/g/s138.json":"a4b9870cb8","assets/g/s139.json":"8feccd7154","assets/g/s14.json":"22da2b8c42","assets/g/s15.json":"8659687b90","assets/g/s16.json":"18a8f1e553","assets/g/s17.json":"3427a80929","assets/g/s18.json":"e3091a82f2","assets/g/s19.json":"ff961fc460","assets/g/s2.json":"c9fadd842c","assets/g/s20.json":"9165cbeb46","assets/g/s21.json":"ca92f6872b","assets/g/s22.json":"0993656f76","assets/g/s23.json":"400d130b73","assets/g/s24.json":"be58dc1679","assets/g/s25.json":"e4a0aaca57","assets/g/s26.json":"372742e971","assets/g/s27.json":"3a131e01b8","assets/g/s28.json":"8e338ee421","assets/g/s29.json":"463c04a4f9","assets/g/s3.json":"98ae8edd33","assets/g/s30.json":"8a5913b6fb","assets/g/s31.json":"adf4800a5f","assets/g/s32.json":"80b923b85e","assets/g/s33.json":"171523fb28","assets/g/s34.json":"4e6b85aa16","assets/g/s35.json":"37c1a2e4de","assets/g/s36.json":"3f6a8debf4","assets/g/s37.json":"ed53cfc0ce","assets/g/s38.json":"d0de5c3483","assets/g/s39.json":"9f71cd1308","assets/g/s4.json":"0f8ea364dc","assets/g/s40.json":"8a2b3351c2","assets/g/s41.json":"4bc0e6bb2a","assets/g/s42.json":"3e7c29227d","assets/g/s43.json":"99214684a8","assets/g/s44.json":"597fc56cb4","assets/g/s45.json":"9168044768","assets/g/s46.json":"c978f6fae7","assets/g/s47.json":"b9a34b9ab1","assets/g/s48.json":"b7caec59a5","assets/g/s49.json":"ec4e46ef4e","assets/g/s5.json":"b1cd74729e","assets/g/s50.json":"115293e32c","assets/g/s51.json":"7d90c4e29f","assets/g/s52.json":"8fe34009ec","assets/g/s53.json":"b8d8cf2ad2","assets/g/s54.json":"6900efc650","assets/g/s55.json":"8d04f7f5aa","assets/g/s56.json":"c0e35da2bd","assets/g/s57.json":"bc202bb5ea","assets/g/s58.json":"07e1008806","assets/g/s59.json":"7324b9f8c4","assets/g/s6.json":"3cb55a4d53","assets/g/s60.json":"82b482509a","assets/g/s61.json":"cc5ed63d30","assets/g/s62.json":"0c68861ed1","assets/g/s63.json":"cc2f594fcf","assets/g/s64.json":"b742255d22","assets/g/s65.json":"1fc1b75c33","assets/g/s66.json":"943ab6951a","assets/g/s67.json":"f0203cb54e","assets/g/s68.json":"cb0ae5a27f","assets/g/s69.json":"c8f89bfe1f","assets/g/s7.json":"80601fc904","assets/g/s70.json":"b80e40ec4d","assets/g/s71.json":"df78e79afb","assets/g/s72.json":"89c7344ddb","assets/g/s73.json":"1d825e76c4","assets/g/s74.json":"f8d6d2bee0","assets/g/s75.json":"7a85fbe955","assets/g/s76.json":"62955c35a5","assets/g/s77.json":"7f0ade63d7","assets/g/s78.json":"7609cfd64b","assets/g/s79.json":"82e2b57adb","assets/g/s8.json":"e8c7e4df3b","assets/g/s80.json":"39dfb01e3e","assets/g/s81.json":"14737fe594","assets/g/s82.json":"aca8b5c453","assets/g/s83.json":"1175145159","assets/g/s84.json":"21e5ff02e3","assets/g/s85.json":"042a843cec","assets/g/s86.json":"b82c09e9ce","assets/g/s87.json":"ed42035106","assets/g/s88.json":"27d5d3fd57","assets/g/s89.json":"890712ca46","assets/g/s9.json":"4df0294873","assets/g/s90.json":"8f13e2c776","assets/g/s91.json":"4e68a85fbe","assets/g/s92.json":"6c6fdf5790","assets/g/s93.json":"232d8a6bd9","assets/g/s94.json":"04b6ec59a2","assets/g/s95.json":"69a4ada9d6","assets/g/s96.json":"e650ce9161","assets/g/s97.json":"68dfdec38d","assets/g/s98.json":"d68199aa73","assets/g/s99.json":"bdceff916f","assets/pathfinder-2e-actions.woff2":"235ad1a454","assets/style.css":"975e87c817","icons/charcoal-gold-180.png":"2e86795d8a","icons/charcoal-gold-512.png":"b80e6fff93","icons/crimson-180.png":"7b66c77b72","icons/crimson-512.png":"4ce8d729da","icons/emerald-180.png":"58c36e6437","icons/emerald-512.png":"e547e3e61a","icons/icons.json":"184043af26","icons/midnight-blue-180.png":"431c1fbb5b","icons/midnight-blue-512.png":"54b2ad3636","icons/parchment-180.png":"600db72edc","icons/parchment-512.png":"0ecdc0ea37","icons/violet-shadow-180.png":"e65dd484a9","icons/violet-shadow-512.png":"1b207c1a3a","index.html":"bfad661208","manifest.webmanifest":"5c52f37e36","manifests/charcoal-gold.webmanifest":"532ca32eef","manifests/crimson.webmanifest":"88c40a6b25","manifests/emerald.webmanifest":"74e38b065f","manifests/midnight-blue.webmanifest":"e1a7ef28da","manifests/parchment.webmanifest":"d3bdd1d16f","manifests/violet-shadow.webmanifest":"bdc2ab0855","pages/aspera.html":"36272e0687","pages/atlas.html":"b6d6dc05c6","pages/combat.html":"3930081aa8","pages/consumables.html":"88ecc02887","pages/feats.html":"741f461ad5","pages/glossary.html":"775512f76b","pages/home.html":"67602fe2bf","pages/items.html":"a585ac85f0","pages/rules.html":"dd454d866b","pages/sheet.html":"6854a16cb7","pages/spells.html":"22c141d86b","./":"bfad661208"};
const CACHE = 'aspera-files';
const SCOPE = new URL('./', self.location).pathname;
const key = p => new URL(p + '?v=' + FILES[p], self.location).href;
async function tell(msg){
  const cs = await self.clients.matchAll({includeUncontrolled: true});
  cs.forEach(c => c.postMessage(msg));
}
self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    const paths = Object.keys(FILES), todo = [];
    let done = 0;
    for (const p of paths) { if (await c.match(key(p))) done++; else todo.push(p); }
    const total = paths.length;
    tell({type: 'progress', done, total});
    let i = 0, failed = 0;
    async function worker(){
      while (i < todo.length) {
        const p = todo[i++];
        let ok = false;
        for (let t = 0; t < 3 && !ok; t++) {
          try { const r = await fetch(p, {cache: 'no-cache'}); if (r.ok) { await c.put(key(p), r); ok = true; } } catch (err) {}
        }
        if (!ok) failed++;
        done++;
        if (done % 5 === 0 || done === total) tell({type: 'progress', done, total});
      }
    }
    await Promise.all(Array.from({length: 6}, worker));
    if (failed) throw new Error(failed + ' files could not be saved');
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);
    const c = await caches.open(CACHE), keep = new Set(Object.keys(FILES).map(key));
    for (const req of await c.keys()) if (!keep.has(req.url)) await c.delete(req);
    await self.clients.claim();
    tell({type: 'ready'});
  })());
});
self.addEventListener('message', e => { if (e.data === 'status') e.waitUntil((async () => {
  const c = await caches.open(CACHE); let n = 0;
  for (const p of Object.keys(FILES)) if (await c.match(key(p))) n++;
  e.source.postMessage({type: 'status', done: n, total: Object.keys(FILES).length});
})()); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin || !url.pathname.startsWith(SCOPE)) return;
  let rel = decodeURIComponent(url.pathname.slice(SCOPE.length)) || './';
  if (e.request.mode === 'navigate') rel = 'index.html';
  if (!FILES[rel]) return;
  e.respondWith(caches.open(CACHE).then(c => c.match(key(rel))).then(hit => hit || fetch(e.request)));
});
