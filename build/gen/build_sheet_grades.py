"""Compendium grades for the character sheet's pickers: spells (spellbook grade and role ratings), feats and items."""
import json
from spell_evals import E
from feat_evals import F
from item_data import I


def key(n):
    return n.replace('’', "'").strip().lower()


out = {
    'sp': {key(n): [v[1][0], v[0]] for n, v in E.items() if v[1][0] not in '-'},
    'ft': {key(n): [v[1], v[0]] for n, v in F.items()},
    'it': {key(n): [v['g'], v['r']] for n, v in I.items()},
}
json.dump(out, open('/home/claude/site/assets/cs/grades.json', 'w'), separators=(',', ':'), ensure_ascii=False)
print({k: len(v) for k, v in out.items()})
