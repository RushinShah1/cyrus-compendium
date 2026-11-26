"""Rules glossary page: the list is filled in by app.js from assets/glossary.json."""
from kit import ic

TYPES = ['Condition', 'Trait', 'Action', 'Skill', 'Rules', 'Spell', 'Feat', 'Item', 'Weapon', 'Class', 'Relic', 'Background', 'Heritage', 'Hybrid study']
chips = ''.join(f'<button class="chip mini" type="button" data-gt="{t}">{t if t != "Rules" else "Rules sections"}</button>' for t in TYPES)
page = f'''<div class="page doc" data-page="glossary">
<header class="ph"><h1>Rules glossary</h1>
<p class="lede">Everything in Archives of Nethys, with its exact text: rules, traits, conditions, actions, spells, feats, items, ancestries, classes, archetypes, deities, creatures and more. Remastered printings replace legacy ones wherever both exist. The Forgotten Realms deities are listed as their own type, with lore from official Forgotten Realms sources and proposed Pathfinder statistics. Select any linked term anywhere in the compendium to open it in a panel; links inside a panel open further panels on top.</p></header>
<details class="fbox gfbox" open><summary><span>{ic("search")}Search and filter</span><span class="fact" id="g-count"></span></summary>
<div class="controls"><div class="ctop"><label class="search">{ic("search")}<input id="g-q" type="search" placeholder="Search the glossary" autocomplete="off"></label>
<button class="chip fclear" type="button" id="g-clear">Clear</button></div>
<div class="cr"><span class="cgl">Type</span><div class="cc" id="g-types"></div></div>
<div class="cr"><span class="cgl">Text</span><div class="cc"><button class="chip mini" type="button" id="g-full" aria-pressed="false">Also search inside entries</button><span class="muted small">Searching inside entries reads the whole archive, so the first search takes a little while.</span></div></div>
</div></details>
<div id="g-list" class="glist" aria-live="polite"><p class="muted">Loading the glossary…</p></div>
<p class="muted small">Some printings are newer than the offline Archives of Nethys archive. Their entries say so and use the Foundry PF2e system's transcription of the same book.</p>
</div>'''
open('/home/claude/site/pages/glossary.html', 'w').write(page)
print('ok')
