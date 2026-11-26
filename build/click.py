import sys, asyncio
from playwright.async_api import async_playwright
async def main(url, out, w, h, sel):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': w, 'height': h})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(url); await pg.wait_for_timeout(1500)
        await pg.click(sel); await pg.wait_for_timeout(600)
        await pg.screenshot(path=out); print(errs)
        await b.close()
a=sys.argv; asyncio.run(main(a[1], a[2], int(a[3]), int(a[4]), a[5]))
