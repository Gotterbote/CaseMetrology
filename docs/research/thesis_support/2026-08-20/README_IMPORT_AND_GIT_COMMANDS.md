# Import, format-check, commit, and push

This ZIP contains working thesis-support artifacts created on 2026-08-20.

## Recommended repository location

Keep these research-support drafts together under:

`docs/research/thesis_support/2026-08-20/`

This avoids mixing working thesis audits with authoritative formal-validation data and protocols.

## Before running the commands

Copy this ZIP to the Jetson. The commands below assume it is located at:

`~/Downloads/CaseMetrology_thesis_support_2026-08-20.zip`

If you place it somewhere else, change only the ZIP path.

## One command block

```bash
cd ~/Projects/CaseMetrology
source .venv/bin/activate

DEST="docs/research/thesis_support/2026-08-20"
ZIP="$HOME/Downloads/CaseMetrology_thesis_support_2026-08-20.zip"

mkdir -p "$DEST"

rm -rf /tmp/casemetrology_thesis_support_2026-08-20
mkdir -p /tmp/casemetrology_thesis_support_2026-08-20

unzip -q "$ZIP" -d /tmp/casemetrology_thesis_support_2026-08-20

cp -v   /tmp/casemetrology_thesis_support_2026-08-20/CaseMetrology_thesis_support_2026-08-20/*.md   "$DEST"/

echo
echo "=== Markdown whitespace / formatting check ==="
git diff --check

echo
echo "=== Files to be committed ==="
git status --short "$DEST"

git add "$DEST"

echo
echo "=== Staged whitespace check ==="
git diff --cached --check

echo
echo "=== Staged summary ==="
git --no-pager diff --cached --stat

git commit -m "Add thesis evidence and citation audit artifacts"

git push

echo
echo "=== Final repository status ==="
git status -sb

echo
echo "=== Recent commits ==="
git --no-pager log -5 --oneline
```

## Expected final state

After a successful push, the status line should normally read:

`## main...origin/main`

with no `ahead` or `behind` indicator.

## Notes

- The Markdown files have already been normalized to remove trailing whitespace.
- Ruff and Black generally do not modify Markdown files, so the repository's Python hooks may report that there are no applicable files.
- `git diff --check` and `git diff --cached --check` are the important formatting/whitespace gates for this artifact set.
- The integrated Chapter 3 narrative-polished v2 file is the most current Chapter 3 prose draft in this package.
- The earlier Chapter 3 integrated evidence-audited draft is retained intentionally as provenance for the editing process.
- These files are thesis/research-support artifacts; they do not replace the formal protocols, certificates, raw data, or frozen source code already preserved elsewhere in the repository.
