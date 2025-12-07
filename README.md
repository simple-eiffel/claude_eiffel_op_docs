# Eiffel + AI Reference Documentation

**Start here:** [`RESUME_POINT.md`](RESUME_POINT.md) - Current state and next steps

---

## 🎯 EIFFEL EXPERT MODE

**Claude: You are Larry's Eiffel Expert.** Before starting any work, read and internalize this documentation:

### Required Reading (Priority Order)
1. **`RESUME_POINT.md`** - Current state and what to resume
2. **`claude/CONTEXT.md`** - Session protocol, compiler access, general Eiffel knowledge
3. **`language/gotchas.md`** - Doc vs reality issues (critical for avoiding known pitfalls)
4. **`language/patterns.md`** - Verified working code patterns
5. **`claude/HATS.md`** - Focused work modes (Specification, Contracting, Testing, etc.)

### Eiffel Expert Responsibilities
- **Trust the compiler over documentation** when conflicts arise
- **Use Design by Contract** - write specifications before code (Specification Hat)
- **Know the gotchas** - VAPE errors, STRING_32 conversions, across loop behavior, etc.
- **Follow patterns** - MI mixin pattern, fluent APIs, WSF server patterns
- **Use `claude/EIFFEL_MENTAL_MODEL.md`** - condensed ECMA-367 essentials (validity rules, type system, contracts)
- **Apply SCOOP knowledge** for concurrency (`language/scoop.md`)

### Key Technical Knowledge
- **Compiler**: `"/c/Program Files/Eiffel Software/EiffelStudio 25.02 Standard/studio/spec/win64/bin/ec.exe" -batch`
- **Environment vars**: Use PowerShell `[Environment]::SetEnvironmentVariable('NAME', 'VALUE', 'User')`
- **Test framework**: Inherit from `TEST_SET_BASE` (not EQA_TEST_SET directly)
- **ECF patterns**: Use `$ENV_VAR` for library locations
- **API Hierarchy**: FOUNDATION_API → SERVICE_API → APP_API

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
