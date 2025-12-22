# simple_rosetta - Design & Implementation Report

**Date:** 2025-12-21
**Status:** Ready for Implementation
**Research Document:** [SIMPLE_ROSETTA_RESEARCH.md](../research/SIMPLE_ROSETTA_RESEARCH.md)

---

## Executive Summary

**simple_rosetta** is a Rosetta Code cross-language translation database for Eiffel. It serves two purposes:

1. **Immediate Value:** Searchable database of 1,338 programming tasks with Eiffel solutions
2. **Strategic Value:** Training data for a "Polyglot Translator" specialist LLM model

### Core Innovation: The Eiffel Sieve

Use Eiffel's strict compiler + Design by Contract as a quality filter for AI-generated code. No other language can validate code this rigorously at compile time.

### Strategic Context

> "We are a small group facing Goliath competition. We need to answer THEIR questions."

When developers from Java/Python/C# ask "How do I do X in Eiffel?", the big LLMs often hallucinate. Our specialist won't.

---

## Problem Statement

### The Gap

| Metric | Value |
|--------|-------|
| Rosetta Code total tasks | 1,338 |
| Tasks WITH Eiffel solutions | 159 (12%) |
| Tasks WITHOUT Eiffel | **1,179 (88%)** |

### Developer Pain Points Addressed

1. **No working library ecosystem** - We provide curated, compiled examples
2. **Simple things take too much effort** - We show idiomatic Eiffel patterns
3. **Finding examples is hard** - We create 1,179 new examples
4. **Translating knowledge from Java/Python/C#** - Side-by-side solutions
5. **Learning both Method and Language** - Examples demonstrate DBC in practice

---

## Technical Architecture

### Dependencies (All simple_*)

| Library | Purpose | Critical? |
|---------|---------|-----------|
| simple_http | MediaWiki API calls | Yes |
| simple_json | Parse API responses | Yes |
| simple_sql | SQLite persistence | Yes |
| simple_regex | Wiki markup parsing | Yes |
| simple_ai_client | Claude Max for generation | Yes |
| simple_process | Compiler validation | Yes |
| simple_cache | Response caching | No |
| simple_rate_limiter | Polite API access | No |
| simple_logger | Progress tracking | No |
| simple_testing | Validation suite | No |

**No Gobo/ISE dependencies required.**

### Database Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    category TEXT,
    has_eiffel BOOLEAN DEFAULT FALSE,
    eiffel_validated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE solutions (
    id INTEGER PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id),
    language TEXT NOT NULL,
    code TEXT NOT NULL,
    source TEXT,  -- 'rosetta', 'generated', 'community'
    validated BOOLEAN DEFAULT FALSE,
    validation_log TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(task_id, language)
);

CREATE TABLE instruction_pairs (
    id INTEGER PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id),
    instruction TEXT NOT NULL,
    input TEXT,
    output TEXT NOT NULL,
    pair_type TEXT,  -- 'translate', 'explain', 'generate'
    source_languages TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE validation_runs (
    id INTEGER PRIMARY KEY,
    solution_id INTEGER REFERENCES solutions(id),
    compile_success BOOLEAN,
    compile_errors TEXT,
    contract_violations TEXT,
    test_passed BOOLEAN,
    run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Class Structure

```
simple_rosetta/
├── src/
│   ├── api/
│   │   ├── rosetta_client.e        -- MediaWiki API wrapper
│   │   └── wiki_parser.e           -- Parse wiki markup
│   ├── models/
│   │   ├── rosetta_task.e          -- Task data model
│   │   ├── rosetta_solution.e      -- Solution data model
│   │   └── instruction_pair.e      -- Training pair model
│   ├── storage/
│   │   └── task_store.e            -- SQLite persistence
│   ├── generation/
│   │   ├── eiffel_generator.e      -- Claude Max translation
│   │   └── eiffel_validator.e      -- Compile + DBC check
│   ├── training/
│   │   ├── pair_generator.e        -- Create instruction pairs
│   │   └── jsonl_exporter.e        -- Export for training
│   ├── facade/
│   │   ├── simple_rosetta.e        -- Main facade
│   │   └── rosetta_quick.e         -- One-liner API
│   └── cli/
│       └── rosetta_cli.e           -- Command-line interface
├── testing/
│   └── lib_tests.e                 -- Test suite
├── simple_rosetta.ecf              -- ECF configuration
└── README.md
```

### Pipeline Flow

```
Phase A: Data Collection
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ MediaWiki   │──▶│ Wiki Parser │──▶│ Solution    │──▶│ Task Store  │
│ API Fetch   │   │ (regex)     │   │ Extractor   │   │ (SQLite)    │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘

Phase B: Eiffel Generation
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Claude Max  │──▶│ Eiffel      │──▶│ Solution    │
│ Generator   │   │ Validator   │   │ Store       │
└─────────────┘   └─────────────┘   └─────────────┘

Phase C: Training Data
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Pair        │──▶│ Quality     │──▶│ JSONL       │
│ Generator   │   │ Filter      │   │ Exporter    │
└─────────────┘   └─────────────┘   └─────────────┘
```

---

## Implementation Plan

### Phase 1: Data Collection (Weeks 1-3)

**1A: Task Fetcher (Week 1)**
```eiffel
class ROSETTA_CLIENT

feature -- API
    fetch_all_tasks: ARRAYED_LIST [ROSETTA_TASK]
        -- Fetch all 1,338 tasks from MediaWiki API

    fetch_task_content (name: STRING): STRING
        -- Fetch raw wiki content for task

feature {NONE} -- Implementation
    api_endpoint: STRING = "https://rosettacode.org/w/api.php"
    rate_limiter: SIMPLE_RATE_LIMITER
    cache: SIMPLE_CACHE
```

**1B: SQLite Storage (Week 2)**
```eiffel
class TASK_STORE

feature -- Commands
    save_task (task: ROSETTA_TASK)
    save_solution (solution: ROSETTA_SOLUTION)

feature -- Queries
    tasks_without_eiffel: ARRAYED_LIST [ROSETTA_TASK]
    validated_solutions: ARRAYED_LIST [ROSETTA_SOLUTION]
```

**1C: Wiki Parser (Week 3)**
```eiffel
class WIKI_PARSER

feature -- Parsing
    extract_solutions (wiki_content: STRING): ARRAYED_LIST [ROSETTA_SOLUTION]
        -- Extract all language solutions from wiki markup

    extract_description (wiki_content: STRING): STRING
        -- Extract task description

feature {NONE} -- Patterns
    header_pattern: STRING = "=={{header\|([^}]+)}}=="
```

### Phase 2: Eiffel Generation (Weeks 4-6)

**2A: Eiffel Generator (Weeks 4-5)**
```eiffel
class EIFFEL_GENERATOR

feature -- Generation
    generate_eiffel (task: ROSETTA_TASK; source_solutions: LIST [ROSETTA_SOLUTION]): STRING
        -- Generate Eiffel from source language examples

feature {NONE} -- AI
    ai_client: SIMPLE_AI_QUICK
    prompt_template: STRING
```

**2B: Eiffel Validator (Week 6)**
```eiffel
class EIFFEL_VALIDATOR

feature -- Validation
    validate (code: STRING): VALIDATION_RESULT
        -- Compile and test Eiffel code

feature {NONE} -- Implementation
    process: SIMPLE_PROCESS_QUICK

    compile (code: STRING): BOOLEAN
        -- Run ec -batch

    run_with_contracts (executable: STRING): BOOLEAN
        -- Execute with assertions enabled
```

### Phase 3: Training Data (Weeks 7-9)

**3A: Pair Generator (Week 7)**
```eiffel
class PAIR_GENERATOR

feature -- Generation
    generate_translation_pair (task: ROSETTA_TASK; source: ROSETTA_SOLUTION; eiffel: ROSETTA_SOLUTION): INSTRUCTION_PAIR
    generate_explanation_pair (task: ROSETTA_TASK; eiffel: ROSETTA_SOLUTION): INSTRUCTION_PAIR
```

**3B: JSONL Exporter (Weeks 8-9)**
```eiffel
class JSONL_EXPORTER

feature -- Export
    export_all (pairs: LIST [INSTRUCTION_PAIR]; path: STRING)
        -- Export instruction pairs to JSONL format
```

### Phase 4: Polish (Week 10)

- CLI interface
- Documentation
- Test coverage
- Performance optimization

---

## API Design

### ROSETTA_QUICK (One-Liner Facade)

```eiffel
class ROSETTA_QUICK

feature -- Data Collection
    import_all_tasks
        -- Import all 1,338 tasks from Rosetta Code

    import_task (name: STRING)
        -- Import single task

feature -- Generation
    generate_missing_eiffel
        -- Generate Eiffel for all tasks without solutions

    generate_eiffel_for (task_name: STRING): STRING
        -- Generate Eiffel for specific task

feature -- Query
    search (query: STRING): ARRAYED_LIST [ROSETTA_TASK]
        -- Search tasks by name/description

    tasks_by_category (category: STRING): ARRAYED_LIST [ROSETTA_TASK]

    compare (task_name: STRING; languages: ARRAY [STRING]): STRING
        -- Side-by-side comparison

feature -- Export
    export_training_data (path: STRING)
        -- Export instruction pairs to JSONL

    export_database (path: STRING)
        -- Export SQLite database

feature -- Statistics
    coverage: REAL
        -- Percentage of tasks with validated Eiffel

    validation_rate: REAL
        -- Percentage of generated solutions that passed validation
```

### CLI Interface

```bash
# Import all tasks
rosetta import --all

# Import single task
rosetta import "Bubble sort"

# Generate Eiffel
rosetta generate --missing
rosetta generate "Fibonacci sequence"

# Search
rosetta search "sorting"
rosetta list --category "Algorithms"

# Compare
rosetta compare "Quicksort" --languages python,java,eiffel

# Export
rosetta export --training data/training.jsonl
rosetta export --database data/rosetta.db

# Statistics
rosetta stats
```

---

## Validation Strategy

### Levels

| Level | Description | Pass Criteria |
|-------|-------------|---------------|
| 0 | Compile failed | - |
| 1 | Compiles, contracts fail | ec -batch succeeds |
| 2 | Compiles, contracts pass | Runtime with assertions |
| 3 | Fully validated | Tests pass |

### The Eiffel Sieve Process

```
1. Generate Eiffel code (Claude Max)
           ▼
2. Syntax validation (ec -batch -config test.ecf)
    ├── FAIL → Log error, retry with feedback
    └── PASS ▼
3. Contract validation (run with assertions=all)
    ├── FAIL → Log violation, retry with fix
    └── PASS ▼
4. Test validation (if test cases available)
    ├── FAIL → Log failure, mark Level 2
    └── PASS → Mark Level 3 (fully validated)
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Rosetta API rate limits | 1 req/sec, SQLite cache, exponential backoff |
| Claude Max API costs | Batch processing, prompt caching, start with subset |
| Low validation rate | Iterative refinement, error feedback loop |
| Scope creep | Strict phase gates, MVP focus |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Tasks imported | 1,338 | Database count |
| Eiffel solutions | 1,000 | Level 2+ solutions |
| Validation rate | >70% | Passed / Generated |
| Instruction pairs | 5,000 | Exported pairs |
| Coverage increase | 12% → 75% | Eiffel solutions / total tasks |

---

## Next Steps

1. **Create simple_rosetta directory structure**
2. **Set up ECF with simple_* dependencies**
3. **Implement ROSETTA_CLIENT (Phase 1A)**
4. **Test with 10 tasks (proof of concept)**
5. **Iterate based on validation results**

---

## Appendix: Prompt Template

```
SYSTEM: You are an expert Eiffel programmer translating {source_lang} to Eiffel.

Requirements:
1. Use Design by Contract (require/ensure/invariant)
2. Use void-safe patterns (attached/detachable)
3. Use across loops instead of from/until where appropriate
4. Follow naming: feature_name not featureName
5. Add class invariant for state constraints
6. Include translation notes as comments

TASK: {task_description}

{source_lang} SOLUTION:
{source_code}

Generate idiomatic Eiffel with full DBC contracts.
```

---

*Generated by 7-step research process on 2025-12-21*
