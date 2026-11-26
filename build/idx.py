import json,glob,os,pickle,sys
base='/home/claude/pf2e/packs/pf2e'
idx={}
for pack in ['spells','feats','class-features','equipment','actions','conditions','heritages','ancestry-features','other-effects']:
    for f in glob.glob(f'{base}/{pack}/**/*.json',recursive=True):
        if f.endswith('_folders.json'): continue
        try: d=json.load(open(f))
        except Exception: continue
        if 'name' not in d or 'system' not in d: continue
        idx.setdefault(d['name'].lower(),[]).append((pack,f))
pickle.dump(idx,open('/home/claude/build/idx.pkl','wb'))
print(len(idx))
