#!/bin/bash
# Copy the built site into the GitHub Pages repository and push it.
set -e
cd /home/claude/cyrus-compendium
find . -mindepth 1 -maxdepth 1 ! -name .git ! -name README.md ! -name .nojekyll -exec rm -rf {} +
cp -r /home/claude/site/. ./
git add -A
git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "${1:-Update the compendium}

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01GNJJJbNY57GA8gApZ29sma" || true
git -c push.negotiate=true push -q origin main
