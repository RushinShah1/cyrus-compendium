"""Character sheet page: a shell that assets/cs/sheet.js fills in."""
page = '''<div class="page doc cs-page" data-page="sheet">
<header class="ph"><h1>Character sheet</h1>
<p class="lede">Build a character level by level and play from the sheet. Every number is worked out from the build, the equipment and the active conditions and effects, using the rule elements of the Foundry PF2e system's data; select any number to see how it is made up. Rules text opens from Archives of Nethys. Characters are saved on this device.</p></header>
<div id="cs-root"></div>
</div>'''
open('/home/claude/site/pages/sheet.html', 'w').write(page)
print('ok')
