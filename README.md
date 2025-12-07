# Eiffel + AI Reference Documentation

**Start here:** [`RESUME_POINT.md`](RESUME_POINT.md) - Current state and next steps

---

## Structure

```
reference_docs/
├── RESUME_POINT.md          ← Start here (current state, next steps)
├── README.md                ← You are here
│
├── language/                ← Eiffel language knowledge
│   ├── gotchas.md           - Doc vs reality corrections
│   ├── sqlite_gotchas.md    - SQLite/DB specific issues
│   ├── patterns.md          - Verified working code
│   ├── across_loops.md      - Iteration constructs
│   └── scoop.md             - Concurrency (SCOOP)
│
├── claude/                  ← AI workflow patterns
│   ├── CONTEXT.md           - Session startup context
│   ├── HATS.md              - Focused work modes
│   ├── EIFFEL_MENTAL_MODEL.md - Core Eiffel knowledge for AI
│   ├── compaction_instructions.md - Pre-compaction checkpoint
│   ├── contract_patterns.md - DBC patterns for AI
│   └── verification_process.md
│
├── strategy/                ← Business/roadmaps
│   ├── SIMPLIFICATION_ROADMAP.md - Future simple_* libraries
│   ├── COMPETITIVE_ANALYSIS.md   - Market positioning
│   └── AI_PRODUCTIVITY.md        - Productivity data
│
├── research/                ← Planning docs (historical)
└── archive/                 ← Completed project plans
```

---

## Quick Reference

| Need | File |
|------|------|
| Resume work | `RESUME_POINT.md` |
| Eiffel gotchas | `language/gotchas.md` |
| SQLite issues | `language/sqlite_gotchas.md` |
| Code patterns | `language/patterns.md` |
| Future libraries | `strategy/SIMPLIFICATION_ROADMAP.md` |

---

## Session Workflow

### Starting
1. Read `RESUME_POINT.md`
2. Check relevant gotchas if working in that area
3. Ask what to work on

### Before Compaction (important!)

When you see the context usage warning:

```
/compact save learnings
```

This triggers a checkpoint that:
1. Scans session for learnings (gotchas, patterns, fixes)
2. Updates relevant `language/*.md` files (non-redundant)
3. Updates `RESUME_POINT.md` with current state
4. Confirms ready for compaction

**Todos survive automatically** - no need to capture those.

---

## Adding Knowledge

When you learn something the hard way:
1. **Gotcha?** → Add to `language/gotchas.md` or `language/sqlite_gotchas.md`
2. **Pattern?** → Add to `language/patterns.md`
3. **Bug fix?** → Leave comment in code + add to gotchas if non-obvious

Format:
```markdown
### Short Title
- **Docs say**: What you expected
- **Reality**: What actually works
- **Verified**: Date, EiffelStudio version
- **Example**: Working code
```

---

*Last updated: 2025-12-07*
