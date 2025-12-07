# Compaction Instructions

**Trigger:** User issues `/compact save learnings`

**Purpose:** Preserve session learnings before context compression.

---

## Step 1: Scan Session for Learnings

Review the current session for:

- [ ] **Gotchas discovered** - Things that didn't work as expected
- [ ] **Patterns verified** - Working code patterns worth preserving
- [ ] **Bug fixes** - Non-obvious solutions to problems
- [ ] **API discoveries** - Undocumented behaviors or workarounds

---

## Step 2: Update Reference Docs (Non-Redundant)

For each learning, check if it already exists in the target file. Only add if NEW.

| Learning Type | Target File |
|--------------|-------------|
| Eiffel language gotcha | `language/gotchas.md` |
| SQLite/database issue | `language/sqlite_gotchas.md` |
| Working code pattern | `language/patterns.md` |
| SCOOP/concurrency | `language/scoop.md` |
| Across loop patterns | `language/across_loops.md` |

### Gotcha Format

```markdown
### Short Title
- **Docs say**: What you expected
- **Reality**: What actually works
- **Verified**: Date, EiffelStudio version
- **Example**: Working code
```

---

## Step 3: Update RESUME_POINT.md

Update `reference_docs/RESUME_POINT.md` with:

```markdown
# Resume Point

**Date:** YYYY-MM-DD
**Last Session:** Brief description of what was accomplished

---

## Current State

### [Project/Library Name]
- What's working
- What's in progress
- Any blockers

---

## Recent Fixes

### [Fix Title] (Date)
- **Problem:** What went wrong
- **Cause:** Root cause
- **Fix:** Solution applied
- **Details:** Reference to gotchas file if applicable

---

## Next Steps

1. Immediate next task
2. Follow-up items
3. Future considerations

---

## Key Files

| Need | Location |
|------|----------|
| Relevant file 1 | path |
| Relevant file 2 | path |
```

---

## Step 4: Confirm Ready

Reply with:

```
Compaction checkpoint complete:
- [X] Session scanned for learnings
- [X] Updated: [list files modified]
- [X] RESUME_POINT.md current
- Ready for compaction.
```

---

## What NOT to Capture

- Todo items (survive compaction automatically)
- Code already committed to files
- Transient debugging that led nowhere
- Redundant information already in docs

---

*This file lives at: `reference_docs/claude/compaction_instructions.md`*
