import asyncio
from playwright.async_api import async_playwright
JS = """() => {
  const out = []; const W = document.documentElement.clientWidth;
  for (const el of document.querySelectorAll('main *')) {
    const r = el.getBoundingClientRect();
    if (!r.width || el.closest('.tw') || el.closest('.sorted-away')) continue;
    if (r.right > W + 1 && getComputedStyle(el).position !== 'fixed') {
      const cls = (el.className && el.className.baseVal === undefined ? el.className : '') || '';
      out.push(el.tagName + '.' + String(cls).split(' ')[0] + ' ' + Math.round(r.right) + ' ' + (el.textContent||'').trim().slice(0,40));
    }
  }
  const tw = [...document.querySelectorAll('main .tw')].filter(t => t.scrollWidth > t.clientWidth + 2).map(t => 'SCROLLTABLE ' + (t.previousElementSibling?.textContent||'').slice(0,40));
  return out.slice(0, 12).concat(tw.slice(0,8));
}"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 390, 'height': 844})
        for name in ['home','spells','feats','aspera','items','consumables','combat','atlas','rules','glossary']:
            await pg.goto('http://localhost:8765/#' + name); await pg.wait_for_timeout(1500)
            if name == 'rules':
                await pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
            r = await pg.evaluate(JS)
            print('==', name, len(r)); [print('   ', x) for x in r]
        await b.close()
asyncio.run(main())
