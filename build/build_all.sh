#!/bin/bash
# Rebuild every page, then the glossary (which also links page rules text into it).
set -e
cd /home/claude/build/gen
for b in build_spells build_items build_feats build_combat build_atlas build_home build_glossary_page build_sheet_page build_sheet_grades build_shell; do
  [ -f $b.py ] && python3 $b.py > /dev/null
done
cd /home/claude/build/fr && python3 build_fr.py
cd /home/claude/build/sheet && python3 build_sheet_data.py > /dev/null
cd /home/claude/build/gloss && python3 build_glossary.py
cd /home/claude/build && python3 app/build_app.py 2>/dev/null || true
