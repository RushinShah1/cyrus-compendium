import asyncio, sys, json
from playwright.async_api import async_playwright
# usage: sheettest.py W H prefix step...   steps: click:SEL | js:CODE | shot:NAME | full:NAME | wait:MS
async def main(w,h,prefix,steps):
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':w,'height':h}, service_workers='block')
        pg=await ctx.new_page()
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append('console: '+m.text) if m.type=='error' else None)
        await pg.goto('http://localhost:8765/#sheet'); await pg.wait_for_selector('.cs-body', timeout=30000); await pg.wait_for_timeout(500)
        for s in steps:
            k,_,v=s.partition(':')
            if k=='click': await pg.click(v); await pg.wait_for_timeout(500)
            elif k=='js': r=await pg.evaluate(v); await pg.wait_for_timeout(500); r is not None and print('js ->', r)
            elif k=='wait': await pg.wait_for_timeout(int(v))
            elif k=='shot': await pg.screenshot(path=f'/home/claude/png/{prefix}_{v}.png')
            elif k=='full': await pg.screenshot(path=f'/home/claude/png/{prefix}_{v}.png', full_page=True)
        print('errors',errs)
        await b.close()
asyncio.run(main(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],sys.argv[4:]))
