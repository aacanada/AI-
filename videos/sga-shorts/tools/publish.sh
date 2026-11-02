#!/usr/bin/env bash
# Stage one finished short in the publish queue: bash tools/publish.sh <N> <YYYY-MM-DD>   (run from videos/sga-shorts)
# Copies sN/{video.mp4,thumbnail.jpg,upload-text.txt,meta.txt} to publish/<date>-sga-short-N/ on the publish branch,
# commits, then adds READY as the last commit (publish/README.md rules).
set -euo pipefail
N=$1; DATE=$2
SRC=$(pwd)/s$N
REPO=$(git rev-parse --show-toplevel)
WT=$(mktemp -d)
DIR=publish/$DATE-sga-short-$N
trailer=$'\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01UwukMvGQkDDfsUPRRFBKhM'
for f in video.mp4 thumbnail.jpg upload-text.txt meta.txt; do test -s "$SRC/$f" || { echo "missing $SRC/$f"; exit 1; }; done
git -C "$REPO" fetch -q origin publish
git -C "$REPO" worktree add -q --detach "$WT" origin/publish
trap 'git -C "$REPO" worktree remove --force "$WT"' EXIT
test ! -e "$WT/$DIR" || { echo "$DIR already exists on publish"; exit 1; }
mkdir -p "$WT/$DIR"
cp "$SRC"/{video.mp4,thumbnail.jpg,upload-text.txt,meta.txt} "$WT/$DIR/"
git -C "$WT" add "$DIR"
git -C "$WT" commit -q -m "Add SGA short $N to the publish queue$trailer"
git -C "$WT" push -q origin HEAD:publish
touch "$WT/$DIR/READY"
git -C "$WT" add "$DIR/READY"
git -C "$WT" commit -q -m "Mark SGA short $N ready$trailer"
git -C "$WT" push -q origin HEAD:publish
git -C "$WT" log --oneline -2
