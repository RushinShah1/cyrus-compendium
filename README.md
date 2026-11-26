# Cyrus compendium: build source

This branch holds the generators for the site on `main`. The site is built into `/home/claude/site` and copied into a clone of `main` by `build/deploy.sh`.

## Restore in a new session

```bash
cd /home/claude
git clone -b source https://github.com/RushinShah1/cyrus-compendium.git srcrepo
cp -r srcrepo/build /home/claude/build
cp -r srcrepo/reference-text /home/claude/src
cp -r srcrepo/work-notes /home/claude/work
git clone -b main https://github.com/RushinShah1/cyrus-compendium.git /home/claude/cyrus-compendium
cp -r /home/claude/cyrus-compendium/. /home/claude/site && rm -rf /home/claude/site/.git   # starting copy of the built site
# rules data (paths are hard-coded under /home/claude)
git clone --filter=blob:none https://github.com/foundryvtt/pf2e.git /home/claude/pf2e && (cd /home/claude/pf2e && git checkout d507983d7611aad7bee01b473ba918436c6ea380)
mkdir -p /home/claude/ext && git clone --filter=blob:none https://github.com/SirRodericMurgatroyd/aonprd-archive.git /home/claude/ext/aon && (cd /home/claude/ext/aon && git checkout a8697f7fb97530b2d63f5d01b38f88a8a00b386f)
python3 /home/claude/build/idx.py            # rebuilds /home/claude/build/idx.pkl
# /home/claude/build/gloss/aon_index.pkl is rebuilt automatically on the first glossary build
```

## Build and publish

```bash
cd /home/claude/build && ./build_all.sh
./deploy.sh "What changed"        # commits and pushes main
```

Then publish the changed files (`git -C /home/claude/cyrus-compendium show --name-only --format= HEAD`) to the claude.ai artifact `2073a311-1963-4c29-b9df-16b6ad0207ce` with `publish_files` in patch mode, using the live version as `base_version` (read it with `get_artifact`).

The character sheet's JavaScript and CSS (`site/assets/cs/sheet.js`, `engine.js`, `style.css` and similar) are edited in the site copy directly, not generated, so after restoring, take them from `main`.
