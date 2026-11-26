import sys, asyncio
from playwright.async_api import async_playwright
async def main(url, out, w=1360, h=1800, full=False, js=None):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': w, 'height': h})
        msgs=[]
        pg.on('console', lambda m: msgs.append(m.text)); pg.on('pageerror', lambda e: msgs.append('ERR '+str(e)))
        await pg.goto(url); await pg.wait_for_timeout(1500)
        if js: await pg.evaluate(js); await pg.wait_for_timeout(500)
        await pg.screenshot(path=out, full_page=full)
        print('\n'.join(msgs[:10]))
        await b.close()
a=sys.argv
asyncio.run(main(a[1], a[2], int(a[3]) if len(a)>3 else 1360, int(a[4]) if len(a)>4 else 1800, False, a[5] if len(a)>5 else None))
