"""Overview page."""
from kit import ic

TILES = [
    ('sheet', 'sheet', 'Character sheet', 'Build and play Cyrus or any character, with full calculation, inventory, gold and spells.'),
    ('spells', 'spells', 'Spells, scrolls and wands', 'Arcane and occult spells, ranks 0 to 9, with grades by source.'),
    ('feats', 'feats', 'Feat paths', 'Level 1 to 16 plan and every feat considered.'),
    ('aspera', 'aspera', 'Aspera', 'The relic weapon, its gifts, stave and runes.'),
    ('items', 'items', 'Itemisation', 'Purchase plan by level, runes and the item catalogue.'),
    ('consumables', 'consumables', 'Consumables', 'What to carry and when to use it.'),
    ('combat', 'combat', 'Combat flow and teamwork', 'Turn patterns, positioning and the party.'),
    ('atlas', 'atlas', 'Tactical grid atlas', 'Flanking squares and area placement on the grid.'),
    ('rules', 'corerules', 'Core rules', 'Player Core and GM Core, chapter by chapter, for reading offline.'),
    ('glossary', 'glossary', 'Rules glossary', 'Every rule, trait, condition and item the compendium refers to.'),
]

CYRUS = [('Ancestry', 'Human'), ('Heritage', 'Versatile Human'), ('Background', 'Relentless Dedication'),
         ('Class', 'Magus'), ('Hybrid study', 'Laughing Shadow'), ('Weapon', 'Aspera, a relic polearm'), ('Dedication', 'Witch or Psychic at 9, through Multitalented')]
PARTY = [('Mira', 'Champion'), ('Yara', 'Cleric'), ('Theldren', 'Druid'), ('Adrian', 'Animist'), ('Cassius', 'Fighter')]


def home_page():
    tiles = ''.join(f'<a class="tile" href="#{h}">{ic(i)}<b>{t}</b><span>{d}</span></a>' for h, i, t, d in TILES)
    cyrus = ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in CYRUS)
    party = ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in PARTY)
    page = f'''<div class="page doc" data-page="home">
<header class="ph"><h1>Cyrus Val'Dira</h1></header>
<div class="grid3 home">
<div class="panel"><h3>{ic("brand")}Cyrus</h3><dl class="st">{cyrus}</dl></div>
<div class="panel"><h3>{ic("team")}Party</h3><dl class="st">{party}</dl></div>
<div class="panel"><h3>{ic("rules")}Campaign assumptions</h3><ul class="plain">
<li>One or two fights on most days, with rest between them.</li>
<li>Remaster replaces legacy where name and function match; otherwise both are available.</li>
<li>All core, Lost Omens and adventure path options are open; rarity is ignored.</li></ul></div>
</div>
<h2>{ic("book")}Documents</h2>
<div class="tiles">{tiles}</div>
<h2 id="look">{ic("rules")}Appearance</h2>
<div class="appbox"><p>Illustrated is the default, with icons, colour-coded ratings and book typefaces. Basic is a plain dark layout with smaller text and no icons, closer to a Markdown document. The choice is saved on this device.</p>
<div class="lookpick" role="radiogroup" aria-label="Appearance"><button type="button" class="chip" role="radio" data-look="illustrated">Illustrated</button><button type="button" class="chip" role="radio" data-look="basic">Basic</button></div></div>
<h2 id="app">{ic("home")}Use it offline on iPhone</h2>
<div class="appbox">
<p>Open the GitHub Pages address in Safari, choose an icon below, then tap Share and Add to Home Screen. The app works offline once it has opened, including every rules panel. To change the icon later, choose a new one here, delete the old home-screen icon and add it again.</p>
<div class="iconpick" id="iconpick" role="radiogroup" aria-label="App icon"></div>
<p class="muted small" id="offline-status"></p>
</div>
</div>'''
    open('/home/claude/site/pages/home.html', 'w').write(page)


if __name__ == '__main__':
    home_page()
    print('ok')
