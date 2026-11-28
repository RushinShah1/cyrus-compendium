// Offline cache for Aspera. Each file is cached under its own content hash, so an update downloads only the files
// that changed. Version 0bcf4d802a51.
const FILES = {"assets/app.js":"29b36ba3d9","assets/cs/actions.json":"b0b2320b39","assets/cs/core.json":"5a872507fe","assets/cs/cyrus.json":"923a44f8a2","assets/cs/effects.json":"7674ea2d88","assets/cs/engine.js":"61edfdf02e","assets/cs/feats.json":"4a832fc3e3","assets/cs/grades.json":"f4fa4bdef5","assets/cs/items.json":"20677b0619","assets/cs/sheet.js":"81081a6582","assets/cs/spells.json":"eebfae67d5","assets/fonts/alegreya-latin-500-normal.woff2":"53addbca37","assets/fonts/alegreya-latin-700-normal.woff2":"1c582501ce","assets/fonts/alegreya-latin-800-normal.woff2":"6017cab559","assets/fonts/alegreya-sans-latin-400-italic.woff2":"5dd7c3e61c","assets/fonts/alegreya-sans-latin-400-normal.woff2":"b2a5a35a25","assets/fonts/alegreya-sans-latin-500-normal.woff2":"55b61d22cc","assets/fonts/alegreya-sans-latin-700-normal.woff2":"5acd19a588","assets/g/index.json":"12317d22f6","assets/g/s0.json":"860c31d2cd","assets/g/s1.json":"aaed3ed663","assets/g/s10.json":"4725ac3a07","assets/g/s100.json":"a75d2f6443","assets/g/s101.json":"bc224132bc","assets/g/s102.json":"11b7ad593a","assets/g/s103.json":"923821f5ea","assets/g/s104.json":"c31105c0b8","assets/g/s105.json":"7b2355dfaa","assets/g/s106.json":"0af4c6e136","assets/g/s107.json":"5292a6a50c","assets/g/s108.json":"b92290a2ab","assets/g/s109.json":"e06352b657","assets/g/s11.json":"de1a96b0b3","assets/g/s110.json":"5bb35a5c65","assets/g/s111.json":"2b6b606c5c","assets/g/s112.json":"5e0e7ec6db","assets/g/s113.json":"64d77aa753","assets/g/s114.json":"ac0b224560","assets/g/s115.json":"1e2b8eb8a9","assets/g/s116.json":"3c4b1c074a","assets/g/s117.json":"1a93063438","assets/g/s118.json":"63b68ffd92","assets/g/s119.json":"582f2d0067","assets/g/s12.json":"ca9d95e302","assets/g/s120.json":"68b19d4c12","assets/g/s121.json":"ab3a9a5842","assets/g/s122.json":"73970187f4","assets/g/s123.json":"48669d2df7","assets/g/s124.json":"d069b42c85","assets/g/s125.json":"bb18f9eb74","assets/g/s126.json":"23b866b39d","assets/g/s127.json":"63161ed522","assets/g/s128.json":"5d09cd20b0","assets/g/s129.json":"196cbaf9ce","assets/g/s13.json":"c72f7d945c","assets/g/s130.json":"be896bc0e7","assets/g/s131.json":"7db75d6769","assets/g/s132.json":"4966318e3c","assets/g/s133.json":"91c54860f0","assets/g/s134.json":"6b2188a25f","assets/g/s135.json":"33c26faacc","assets/g/s136.json":"d5c09db72d","assets/g/s137.json":"d02acfceff","assets/g/s138.json":"d04799989b","assets/g/s139.json":"9de3802ad3","assets/g/s14.json":"2e46921265","assets/g/s140.json":"c40c8e6e8d","assets/g/s141.json":"0e8ad9a6d9","assets/g/s142.json":"09c8800a8d","assets/g/s143.json":"9f52f771a8","assets/g/s144.json":"d5916f550a","assets/g/s145.json":"dcd6ee4548","assets/g/s146.json":"f588e3ca7b","assets/g/s147.json":"9d3b392366","assets/g/s148.json":"4071b67998","assets/g/s149.json":"c29f73d268","assets/g/s15.json":"0b4067bf2a","assets/g/s150.json":"f9a203e49b","assets/g/s151.json":"96379b7fce","assets/g/s16.json":"34e5df18d6","assets/g/s17.json":"14cf962ca0","assets/g/s18.json":"0588c785df","assets/g/s19.json":"d87c9c5cb6","assets/g/s2.json":"360e4cb9b3","assets/g/s20.json":"acf79d8d84","assets/g/s21.json":"0af37c4d40","assets/g/s22.json":"54a1841a29","assets/g/s23.json":"90ec3a74ed","assets/g/s24.json":"f2b7feeef1","assets/g/s25.json":"f746a0f6c4","assets/g/s26.json":"fc092e9a4b","assets/g/s27.json":"9b9e3e3828","assets/g/s28.json":"a60639ecd0","assets/g/s29.json":"ef2b1df102","assets/g/s3.json":"03b580d495","assets/g/s30.json":"c52f058087","assets/g/s31.json":"006beef853","assets/g/s32.json":"2ad99b5e9e","assets/g/s33.json":"aaf7dead78","assets/g/s34.json":"cb6f0414c2","assets/g/s35.json":"27ef1b03c0","assets/g/s36.json":"a3486ba4ef","assets/g/s37.json":"cafffa9069","assets/g/s38.json":"ec9d050e69","assets/g/s39.json":"371b204a42","assets/g/s4.json":"2d60d68e68","assets/g/s40.json":"3ef60ae8eb","assets/g/s41.json":"cc872a0332","assets/g/s42.json":"abf2a773d3","assets/g/s43.json":"35f156d751","assets/g/s44.json":"6837b8cca0","assets/g/s45.json":"ab77705b21","assets/g/s46.json":"bef79de2af","assets/g/s47.json":"e0433b36ea","assets/g/s48.json":"841e81a88d","assets/g/s49.json":"65c52389b2","assets/g/s5.json":"cf66de3045","assets/g/s50.json":"d2278995ad","assets/g/s51.json":"34320bb6f1","assets/g/s52.json":"fcad75408b","assets/g/s53.json":"a1c07218e5","assets/g/s54.json":"d4cb9e3a0b","assets/g/s55.json":"3b59457879","assets/g/s56.json":"58ff3c15d8","assets/g/s57.json":"4f7bcbff97","assets/g/s58.json":"9b496275f3","assets/g/s59.json":"eb9a95be84","assets/g/s6.json":"96d3bc10c8","assets/g/s60.json":"c5086edaad","assets/g/s61.json":"c56bb56f11","assets/g/s62.json":"e3129b993f","assets/g/s63.json":"381be1e028","assets/g/s64.json":"a0b50a7579","assets/g/s65.json":"99c6100e7f","assets/g/s66.json":"2900a36636","assets/g/s67.json":"bfa82feac7","assets/g/s68.json":"cf7fdc7cf7","assets/g/s69.json":"4cab9b8a74","assets/g/s7.json":"90d75c1218","assets/g/s70.json":"1914b57d1f","assets/g/s71.json":"35324577d4","assets/g/s72.json":"6d72db8891","assets/g/s73.json":"7757b41244","assets/g/s74.json":"363ca17fd7","assets/g/s75.json":"bbec6c9d5d","assets/g/s76.json":"95755d47cc","assets/g/s77.json":"5ad1b566a0","assets/g/s78.json":"3ca41e5b8c","assets/g/s79.json":"be41a99579","assets/g/s8.json":"f374950712","assets/g/s80.json":"0c834e7081","assets/g/s81.json":"d6243eca72","assets/g/s82.json":"41d70e377c","assets/g/s83.json":"be35e4e868","assets/g/s84.json":"249e9e73e4","assets/g/s85.json":"af5ff7b402","assets/g/s86.json":"57988c12b6","assets/g/s87.json":"58afefd35f","assets/g/s88.json":"9e616c8dab","assets/g/s89.json":"070c2f3fcd","assets/g/s9.json":"583a218ce4","assets/g/s90.json":"54e7690c55","assets/g/s91.json":"7c106f3ed1","assets/g/s92.json":"39a02f61a8","assets/g/s93.json":"3b23f5f5ee","assets/g/s94.json":"0e6a77383b","assets/g/s95.json":"e219e7643e","assets/g/s96.json":"0fb793473a","assets/g/s97.json":"a8491ef4a8","assets/g/s98.json":"89e603ce58","assets/g/s99.json":"6827d48079","assets/pathfinder-2e-actions.woff2":"235ad1a454","assets/style.css":"be1f8d79f8","icons/charcoal-gold-180.png":"2e86795d8a","icons/charcoal-gold-512.png":"b80e6fff93","icons/crimson-180.png":"7b66c77b72","icons/crimson-512.png":"4ce8d729da","icons/emerald-180.png":"58c36e6437","icons/emerald-512.png":"e547e3e61a","icons/icons.json":"184043af26","icons/midnight-blue-180.png":"431c1fbb5b","icons/midnight-blue-512.png":"54b2ad3636","icons/parchment-180.png":"600db72edc","icons/parchment-512.png":"0ecdc0ea37","icons/violet-shadow-180.png":"e65dd484a9","icons/violet-shadow-512.png":"1b207c1a3a","index.html":"09c837c667","manifest.webmanifest":"5c52f37e36","manifests/charcoal-gold.webmanifest":"532ca32eef","manifests/crimson.webmanifest":"88c40a6b25","manifests/emerald.webmanifest":"74e38b065f","manifests/midnight-blue.webmanifest":"e1a7ef28da","manifests/parchment.webmanifest":"d3bdd1d16f","manifests/violet-shadow.webmanifest":"bdc2ab0855","pages/aspera.html":"a54c9e4651","pages/atlas.html":"c952443777","pages/combat.html":"4e343e959b","pages/consumables.html":"e77dbc29b6","pages/feats.html":"fb929f253e","pages/glossary.html":"6906834d4a","pages/home.html":"67602fe2bf","pages/items.html":"04d9d40e67","pages/rules.html":"dd454d866b","pages/sheet.html":"6854a16cb7","pages/spells.html":"77721344b1","./":"09c837c667"};
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
