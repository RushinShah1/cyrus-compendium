import kit
from kit import ic
DOCS=[('home','Overview','home'),('sheet','Character sheet','sheet'),('spells','Spells, scrolls and wands','spells'),('feats','Feat paths','feats'),('aspera','Aspera','aspera'),
('items','Itemisation','items'),('consumables','Consumables','consumables'),('combat','Combat flow and teamwork','combat'),('atlas','Tactical grid atlas','atlas'),('rules','Core rules','corerules'),('glossary','Rules glossary','glossary')]
rail=''.join(f'<a class="doc" href="#{k}" data-doc="{k}">{ic(i)}<span>{t}</span></a>' for k,t,i in DOCS)
html=f'''<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Aspera</title>
<meta name="theme-color" content="#1b1b1f">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Aspera">
<link rel="manifest" href="manifest.webmanifest" id="app-manifest">
<link rel="apple-touch-icon" href="icons/charcoal-gold-180.png" id="app-touch-icon">
<link rel="icon" href="icons/charcoal-gold-180.png" id="app-favicon">
<script>try{{if(localStorage.getItem('cyrus-look')==='basic')document.documentElement.setAttribute('data-look','basic');}}catch(e){{}}</script>
<script>try{{var k=localStorage.getItem('cyrus-icon');if(k){{document.getElementById('app-touch-icon').href='icons/'+k+'-180.png';document.getElementById('app-favicon').href='icons/'+k+'-180.png';document.getElementById('app-manifest').href='manifests/'+k+'.webmanifest';}}}}catch(e){{}}</script>
<link rel="stylesheet" href="assets/style.css">
</head><body>
{kit.sprite()}
<div class="app">
<nav class="rail" aria-label="Documents">
<div class="brand"><span class="emb">{ic('brand')}</span><div><b>Cyrus Val'Dira</b><span>Build Analysis Compendium</span></div></div>
{rail}
<p class="credit">Icons by Lorc, Delapouite and others from <a href="https://game-icons.net">game-icons.net</a> (CC BY 3.0). Action glyphs from the Foundry PF2e system font. Rules text from Archives of Nethys under the ORC and OGL licences.</p>
</nav>
<main id="main"></main>
</div>
<script src="assets/app.js"></script>
</body></html>'''
open('/home/claude/site/index.html','w').write(html)
print(len(html))
