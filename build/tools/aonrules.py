"""Rules text and fields for a spell card, from the Archives of Nethys data only."""
import sys, re
sys.path.insert(0, '/home/claude/build/gen')
import entries
from spell_list import RANKS
from spell_evals import E

def plain(md):
    t = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', md or '')
    t = re.sub(r'\{\{\w+ \d+ "([^"]+)"\}\}', r'\1', t)
    t = re.sub(r'<actions string="([^"]+)" />', r'[\1]', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t.replace('**', '')).strip()

def info(n):
    e = entries.entry(n, 'spell'); d = e['doc']
    return dict(name=d['name'], book=d.get('primary_source'), rank=d.get('level'), actions=d.get('actions'), traits=[t for t, _ in e['traits']],
                save=d.get('saving_throw'), area=d.get('area_raw'), range=d.get('range_raw'), targets=d.get('target'), duration=d.get('duration_raw'),
                text=plain(d['markdown'].partition('\n---')[2]), legacy=not e['remaster'])
