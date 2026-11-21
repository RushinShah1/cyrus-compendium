// Offline cache for Aspera. Each file is cached under its own content hash, so an update downloads only the files
// that changed. Version ab4fd7f4ca9e.
const FILES = {"assets/app.js":"8aefbcde4d","assets/cs/actions.json":"4d43ba5d28","assets/cs/core.json":"f9a2e69a20","assets/cs/cyrus.json":"fdea53a6e7","assets/cs/effects.json":"7674ea2d88","assets/cs/engine.js":"c9af6b229f","assets/cs/feats.json":"7b6f27c54f","assets/cs/items.json":"cf12ab8b35","assets/cs/sheet.js":"ef340e7f29","assets/cs/spells.json":"d91d36c50a","assets/fonts/alegreya-latin-500-normal.woff2":"53addbca37","assets/fonts/alegreya-latin-700-normal.woff2":"1c582501ce","assets/fonts/alegreya-latin-800-normal.woff2":"6017cab559","assets/fonts/alegreya-sans-latin-400-italic.woff2":"5dd7c3e61c","assets/fonts/alegreya-sans-latin-400-normal.woff2":"b2a5a35a25","assets/fonts/alegreya-sans-latin-500-normal.woff2":"55b61d22cc","assets/fonts/alegreya-sans-latin-700-normal.woff2":"5acd19a588","assets/g/index.json":"d116c64e0c","assets/g/s0.json":"ac3b8ec3eb","assets/g/s1.json":"54d5411534","assets/g/s10.json":"243df37909","assets/g/s100.json":"32a099734f","assets/g/s101.json":"5da7cb7da8","assets/g/s102.json":"0e0f5f5127","assets/g/s103.json":"a4c48b1af5","assets/g/s104.json":"4ee885b917","assets/g/s105.json":"fe6d10c1f9","assets/g/s106.json":"73337098ac","assets/g/s107.json":"a96e0ae700","assets/g/s108.json":"6f9e449ffd","assets/g/s109.json":"a38113d01e","assets/g/s11.json":"de3fe09186","assets/g/s110.json":"e0282be4ee","assets/g/s111.json":"f6d4118f53","assets/g/s112.json":"d9814cf37a","assets/g/s113.json":"595c650bc6","assets/g/s114.json":"28c298087a","assets/g/s115.json":"219f7f029f","assets/g/s116.json":"d3fe02c19b","assets/g/s117.json":"c20eec059d","assets/g/s118.json":"9190df9b5e","assets/g/s119.json":"424ae42df7","assets/g/s12.json":"e87cf9d8db","assets/g/s120.json":"9e8624ca5b","assets/g/s121.json":"4129c91e40","assets/g/s122.json":"210fe806f9","assets/g/s123.json":"4ce294441a","assets/g/s124.json":"5bad9a12ad","assets/g/s125.json":"cc1d3d2064","assets/g/s126.json":"f2aa710c1b","assets/g/s127.json":"156058d221","assets/g/s128.json":"17da06f77f","assets/g/s129.json":"eb52e157e0","assets/g/s13.json":"c30c97c0c2","assets/g/s130.json":"d37352492f","assets/g/s131.json":"af8a534229","assets/g/s132.json":"e66e043f89","assets/g/s133.json":"1db014c203","assets/g/s134.json":"babf22ce30","assets/g/s135.json":"b1659d29fd","assets/g/s136.json":"0ecfee1e1b","assets/g/s137.json":"b47f834d01","assets/g/s138.json":"49d079d532","assets/g/s139.json":"e84dfa9920","assets/g/s14.json":"8e69d23320","assets/g/s140.json":"4a61303af8","assets/g/s141.json":"5d6fb19620","assets/g/s142.json":"f74fad9026","assets/g/s143.json":"f5034dc44b","assets/g/s144.json":"9852b579e4","assets/g/s145.json":"fb4a06a935","assets/g/s15.json":"d8920e8137","assets/g/s16.json":"2ca5ac95ac","assets/g/s17.json":"e363024d63","assets/g/s18.json":"143cac7039","assets/g/s19.json":"d0ee4f246d","assets/g/s2.json":"1db435c12a","assets/g/s20.json":"ec43f44e42","assets/g/s21.json":"7c5d25de8e","assets/g/s22.json":"ff5e96028e","assets/g/s23.json":"771fd77f7e","assets/g/s24.json":"839f046d47","assets/g/s25.json":"49a428665e","assets/g/s26.json":"0fc0259b64","assets/g/s27.json":"1eac8dc499","assets/g/s28.json":"869da90387","assets/g/s29.json":"f1abb05ff0","assets/g/s3.json":"451404046a","assets/g/s30.json":"3e9382087e","assets/g/s31.json":"3a336f04ac","assets/g/s32.json":"7c903ccad3","assets/g/s33.json":"15ea50aea8","assets/g/s34.json":"f2f06604d6","assets/g/s35.json":"f39db74d42","assets/g/s36.json":"9a5ccd714c","assets/g/s37.json":"5ec0c6354c","assets/g/s38.json":"71e59f0e21","assets/g/s39.json":"346c94cc10","assets/g/s4.json":"7219b07975","assets/g/s40.json":"e3d275d4d7","assets/g/s41.json":"ca69160cf1","assets/g/s42.json":"6744760afb","assets/g/s43.json":"2923136530","assets/g/s44.json":"f0fd9cf26a","assets/g/s45.json":"82c86efacb","assets/g/s46.json":"f25372d74c","assets/g/s47.json":"8dd6db0fd0","assets/g/s48.json":"79cdc95dfd","assets/g/s49.json":"4947354883","assets/g/s5.json":"e36458217d","assets/g/s50.json":"7d8559e610","assets/g/s51.json":"a366b7d691","assets/g/s52.json":"b18985a278","assets/g/s53.json":"7b9e6288f4","assets/g/s54.json":"e25cf6b167","assets/g/s55.json":"3597b8e496","assets/g/s56.json":"e119dbd5ba","assets/g/s57.json":"ac976f0679","assets/g/s58.json":"1d70ca4e77","assets/g/s59.json":"d0c929de25","assets/g/s6.json":"b88c7835a8","assets/g/s60.json":"95a9be44ff","assets/g/s61.json":"df45f8967c","assets/g/s62.json":"21e93cf173","assets/g/s63.json":"3299464efa","assets/g/s64.json":"3ea237e924","assets/g/s65.json":"d16b0444fd","assets/g/s66.json":"d1b58ae4ad","assets/g/s67.json":"96ff82c89c","assets/g/s68.json":"25d8acbe68","assets/g/s69.json":"40d9748be3","assets/g/s7.json":"abc693a175","assets/g/s70.json":"c5941dde44","assets/g/s71.json":"e75ff0d548","assets/g/s72.json":"ebaa548795","assets/g/s73.json":"15a6eb72b3","assets/g/s74.json":"e9f6903bae","assets/g/s75.json":"a26cd1a66c","assets/g/s76.json":"ff4a730ae9","assets/g/s77.json":"a4085dc71d","assets/g/s78.json":"4ce7789dce","assets/g/s79.json":"12c2845a20","assets/g/s8.json":"4e7ca74770","assets/g/s80.json":"0533ed984b","assets/g/s81.json":"9810b7a4ee","assets/g/s82.json":"a5fff6ab2c","assets/g/s83.json":"4e6215eadf","assets/g/s84.json":"9e2b97d9fb","assets/g/s85.json":"1592f87e29","assets/g/s86.json":"891479de8d","assets/g/s87.json":"64755471a6","assets/g/s88.json":"162de8d9f3","assets/g/s89.json":"65be41de03","assets/g/s9.json":"36c65255ba","assets/g/s90.json":"84604a8bd3","assets/g/s91.json":"250fa6d995","assets/g/s92.json":"204b87df2d","assets/g/s93.json":"31409a3a11","assets/g/s94.json":"f88bdf6e04","assets/g/s95.json":"f7b660645a","assets/g/s96.json":"6449c98fc4","assets/g/s97.json":"b6dedac247","assets/g/s98.json":"208a3d1d12","assets/g/s99.json":"aa3aa90765","assets/pathfinder-2e-actions.woff2":"235ad1a454","assets/style.css":"09308ae6d9","icons/charcoal-gold-180.png":"2e86795d8a","icons/charcoal-gold-512.png":"b80e6fff93","icons/crimson-180.png":"7b66c77b72","icons/crimson-512.png":"4ce8d729da","icons/emerald-180.png":"58c36e6437","icons/emerald-512.png":"e547e3e61a","icons/icons.json":"184043af26","icons/midnight-blue-180.png":"431c1fbb5b","icons/midnight-blue-512.png":"54b2ad3636","icons/parchment-180.png":"600db72edc","icons/parchment-512.png":"0ecdc0ea37","icons/violet-shadow-180.png":"e65dd484a9","icons/violet-shadow-512.png":"1b207c1a3a","index.html":"09c837c667","manifest.webmanifest":"5c52f37e36","manifests/charcoal-gold.webmanifest":"532ca32eef","manifests/crimson.webmanifest":"88c40a6b25","manifests/emerald.webmanifest":"74e38b065f","manifests/midnight-blue.webmanifest":"e1a7ef28da","manifests/parchment.webmanifest":"d3bdd1d16f","manifests/violet-shadow.webmanifest":"bdc2ab0855","pages/aspera.html":"77d47cf2ec","pages/atlas.html":"b6d6dc05c6","pages/combat.html":"3930081aa8","pages/consumables.html":"88ecc02887","pages/feats.html":"5489206267","pages/glossary.html":"775512f76b","pages/home.html":"67602fe2bf","pages/items.html":"a585ac85f0","pages/rules.html":"dd454d866b","pages/sheet.html":"6854a16cb7","pages/spells.html":"9e54cdbaac","./":"09c837c667"};
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
