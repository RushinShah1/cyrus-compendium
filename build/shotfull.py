import sys, asyncio
from playwright.async_api import async_playwright
async def main(url, out, w, h):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': w, 'height': h})
        msgs=[]
        pg.on('pageerror', lambda e: msgs.append('ERR '+str(e)))
        await pg.goto(url); await pg.wait_for_timeout(1800)
        H = await pg.evaluate('document.documentElement.scrollHeight')
        i=0; y=0
        while y < H and i < 40:
            await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(150)
            await pg.screenshot(path=f'{out}_{i:02d}.png'); y+=h; i+=1
        print(H, i, msgs[:5])
        await b.close()
a=sys.argv; asyncio.run(main(a[1], a[2], int(a[3]), int(a[4])))
