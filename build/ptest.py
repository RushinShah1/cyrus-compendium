import asyncio, sys
from playwright.async_api import async_playwright
async def main(w,h,out,page_hash,steps):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':w,'height':h})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append('console: '+m.text) if m.type=='error' else None)
        await pg.goto('http://localhost:8765/'+page_hash); await pg.wait_for_timeout(1200)
        for s in steps:
            if s.startswith('click:'):
                await pg.click(s[6:]); await pg.wait_for_timeout(900)
            elif s.startswith('js:'):
                await pg.evaluate(s[3:]); await pg.wait_for_timeout(900)
        await pg.screenshot(path=out); print('errors',errs)
        await b.close()
w,h,out,hs=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],sys.argv[4]
asyncio.run(main(w,h,out,hs,sys.argv[5:]))
