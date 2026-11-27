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
mkdir -p /home/claude/ext/aon/2e && git clone --depth 1 --single-branch --branch aon-data https://github.com/RushinShah1/cyrus-compendium.git /home/claude/ext/aon/2e/data
git clone --depth 1 https://github.com/game-icons/icons.git /home/claude/ext/game-icons   # icons used by build/gen/kit.py
mkdir -p /home/claude/png                    # screenshots from build/sheettest.py
python3 /home/claude/build/idx.py            # rebuilds /home/claude/build/idx.pkl
# /home/claude/build/gloss/aon_index.pkl is rebuilt automatically on the first glossary build
```

All displayed rules content (text, traits, fields and links) comes from the Archives of Nethys data on the `aon-data` branch, downloaded from the live site on 26 November 2026. Foundry's data is used only for the character sheet's calculations and its list of options. To refresh the data, run `python -m archiver fetch` from the `2e` folder of https://github.com/SirRodericMurgatroyd/aonprd-archive on a machine that can reach `elasticsearch.aonprd.com` (the cloud workspace cannot), then push the new `data` folder to the `aon-data` branch.

## Build and publish

```bash
cd /home/claude/build && ./build_all.sh
./deploy.sh "What changed"        # commits and pushes main
```

Then publish the changed files (`git -C /home/claude/cyrus-compendium show --name-only --format= HEAD`) to the claude.ai artifact `2073a311-1963-4c29-b9df-16b6ad0207ce` with `publish_files` in patch mode, using the live version as `base_version` (read it with `get_artifact`).

The character sheet's JavaScript and CSS (`site/assets/cs/sheet.js`, `engine.js`, `style.css` and similar) are edited in the site copy directly, not generated, so after restoring, take them from `main`.
