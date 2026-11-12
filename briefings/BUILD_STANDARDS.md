# Simple Eiffel Build Standards

**Authoritative source for build practices in eiffel-* skills and simple_* library development.**

**Version:** 1.0
**Last Updated:** 2026-01-27
**Applies to:** All eiffel-* skills (research, spec, contracts, implement, verify, harden, ship) and simple_* library maintenance.

---

## 1. Library Selection: Prefer simple_* Over ISE/Gobo

**MANDATORY for all phases: research, specification, implementation, and maintenance.**

### Rule
When researching, specifying, building new simple_* libraries, or maintaining existing ones:
- **Always prefer simple_* libraries** over ISE stdlib or Gobo equivalents
- Document dependency on simple_* in ECF, not ISE stdlib

### Examples

| Need | ISE (❌ WRONG) | Gobo (❌ WRONG) | Simple Eiffel (✅ CORRECT) |
|------|---|---|---|
| Process execution | `$ISE_LIBRARY/process` | - | `simple_process` |
| HTTP requests | `$ISE_LIBRARY/net` | - | `simple_http` |
| JSON parsing | Custom code | - | `simple_json` |
| CSV handling | Custom code | - | `simple_csv` |
| Container utilities | `$ISE_LIBRARY/structures` | `DS_*` classes | `simple_container` |
| Regular expressions | `$ISE_LIBRARY/regex` | - | `simple_regex` |
| Configuration files | Custom code | - | `simple_config` |
| Testing framework | `$ISE_LIBRARY/testing` | - | `simple_testing` |
| Logging | Custom code | - | `simple_logger` |
| XML parsing | Custom code | - | `simple_xml` |
| String utilities | `STRING_UTILITIES` | - | `simple_string` |

### Where This Matters

**Phase 0 (Intent):** Document simple_* as primary dependencies in vision
**Phase 1 (Contracts):** ECF must reference simple_* not ISE
**Phase 4 (Implement):** Implementation uses simple_* APIs
**Phase 7 (Ship):** Final ECF audit ensures no ISE where simple_* exists (except base, time, testing)

---

## 2. F_code Finalize: Explicit Compilation Mode

**MANDATORY for all test execution and binary deployment.**

### Rule
When compiling test-runners or shipping binaries, explicitly use `ec.sh` with F_code finalize:

```bash
# For development/testing (keep DbC contracts in binary)
/d/prod/ec.sh -batch -config lib.ecf -target lib_tests -c_compile -finalize -keep

# For production (strip contracts, maximum optimization)
/d/prod/ec.sh -batch -config lib.ecf -target lib_app -c_compile -finalize
```

### When to Use `-keep`

| Scenario | Use `-keep`? | Reason |
|----------|------|--------|
| Test-runner executable (test_app.exe) | **YES** | DbC ensures test coverage; contracts guide debugging |
| Development builds | **YES** | Catch violations during development |
| Production CLI tool | **NO** | Finalize strips contracts for speed/size; binaries already verified by tests |
| Library shipped as source (.e files) | N/A | End-user controls finalization |

### Evidence Collection

After finalization, capture evidence:
```bash
# For test binaries (with -keep)
/d/prod/ec.sh -batch -config lib.ecf -target lib_tests -c_compile -finalize -keep 2>&1 | tee evidence/finalize-test-keep.txt

# For production binaries (without -keep)
/d/prod/ec.sh -batch -config lib.ecf -target lib_app -c_compile -finalize 2>&1 | tee evidence/finalize-prod.txt
```

---

## 3. Test Target Naming and Binary Placement

**MANDATORY for all new simple_* libraries and when maintaining existing ones.**

### Rule
For test targets in simple_* libraries:

1. **Test target exe name:** `test_app`
2. **Compiled binary location:** `bin/test_app.exe`
3. **Supporting DLLs:** Co-located in `bin/` folder

### ECF Configuration

```xml
<target name="lib_tests">
    <description>Test suite for simple_* library</description>
    <root class="TEST_APP" feature="make" />
    <option>
        <assertions value="all" />
        <void_safety value="all" />
        <concurrency value="scoop" />
    </option>
    <setting name="console_application" value="true" />
    <setting name="executable_name" value="test_app" />

    <!-- Keep this: test binaries go to bin/ -->
    <setting name="cdir" value="EIFGENs/lib_tests/W_code" />
    <setting name="infodir" value="EIFGENs/lib_tests/W_code/info" />
    <cluster name="test" location="test" recursive="true" />
</target>
```

### Folder Structure

```
simple_libname/
├── bin/
│   ├── test_app.exe           # Finalized test binary
│   ├── dll1.dll               # Supporting DLL (if any)
│   └── dll2.dll               # Supporting DLL (if any)
├── test/
│   ├── test_app.e             # Root test class
│   └── *.e                    # Test classes
├── src/
│   └── *.e                    # Library implementation
├── data/
│   ├── input/                 # Test input files
│   └── output/                # Test output files
├── docs/
│   └── *.md                   # Documentation
└── simple_libname.ecf         # Project config
```

### Running Tests

From the root directory:
```bash
./bin/test_app.exe
```

This is the canonical test entry point.

---

## 4. Input/Output File Placement

**MANDATORY for libraries handling file I/O (data processing, visualization, configuration).**

### Rule
Organize test data and output by purpose:

```
project_root/
├── data/
│   ├── input/                     # Input test files
│   │   ├── sample.csv
│   │   ├── config.json
│   │   └── graph.dot
│   ├── output/                    # Output generated by tests
│   │   ├── generated_chart.svg
│   │   ├── table_output.txt
│   │   └── report.pdf
│   └── expected/                  # Expected outputs for comparison
│       ├── reference_chart.svg
│       └── expected_report.txt
├── reports/                       # Test reports & analysis
│   ├── TEST_SUITE_REPORT.md
│   ├── test_run_2026-01-27.txt
│   └── coverage_report.txt
└── ...
```

### Examples from Production Libraries

**simple_graphviz:**
```
simple_graphviz/
├── data/
│   ├── input/
│   │   ├── simple_graph.dot         # Input DOT format
│   │   └── complex_network.dot
│   ├── output/
│   │   ├── graph_visualization.svg  # Generated
│   │   └── tree.png                 # Generated
│   └── expected/
│       ├── reference.svg            # For validation
│       └── expected.png
├── reports/
│   └── visualization_tests.md
```

**simple_spec_viz:**
```
simple_spec_viz/
├── data/
│   ├── input/
│   │   ├── spec_simple.e            # Eiffel spec to visualize
│   │   └── spec_complex.e
│   ├── output/
│   │   ├── class_diagram.svg        # Generated
│   │   └── dependency_graph.png     # Generated
│   └── expected/
│       └── reference_diagram.svg
├── reports/
│   └── visualization_coverage.txt
```

**simple_chart:**
```
simple_chart/
├── data/
│   ├── input/
│   │   ├── sales_data.csv           # Chart source data
│   │   └── metrics.json
│   ├── output/
│   │   ├── bar_chart.svg            # Generated
│   │   ├── line_chart.png           # Generated
│   │   └── table_output.txt         # Text rendering
│   └── expected/
│       └── reference_chart.svg
├── reports/
│   ├── TEST_SUITE_REPORT.md         # Comprehensive test report
│   ├── test_2026-01-27.log
│   └── visual_test_evidence/
│       └── screenshot_01.png
```

### Test Code Pattern

```eiffel
class TEST_APP

feature -- Test Execution

    test_generates_output
        local
            l_input_path: PATH
            l_output_path: PATH
            l_expected_path: PATH
        do
            -- Paths relative to project root
            l_input_path := (create {PATH}.make_current).appended ("data/input/sample.csv")
            l_output_path := (create {PATH}.make_current).appended ("data/output/result.svg")
            l_expected_path := (create {PATH}.make_current).appended ("data/expected/reference.svg")

            -- Test generates output to data/output/
            assert ("input exists", l_input_path.exists)
            assert ("output created", l_output_path.exists)
            -- assert ("matches expected", compare_files (l_output_path, l_expected_path))
        end
end
```

### Report Generation

Tests should produce a comprehensive report (e.g., `reports/TEST_SUITE_REPORT.md`):

```markdown
# Test Suite Report

**Date:** 2026-01-27
**Library:** simple_libname
**Target:** lib_tests (test_app.exe)

## Summary
- **Total Tests:** 46
- **Passed:** 46
- **Failed:** 0
- **Skipped:** 0

## Test Categories
- Unit Tests: 13 passed
- Visual/Output Tests: 22 passed
- Integration Tests: 5 passed
- Format Tests (SVG/PNG/PDF): 4 passed
- Stress Tests: 2 passed

## Input Files
- Located: `data/input/`
- Examples: simple.csv, complex.json, reference.dot

## Output Files
- Located: `data/output/`
- Generated formats: SVG, PNG, PDF, text

## Expected/Reference Files
- Located: `data/expected/`
- Used for validation and comparison

## Evidence
- Compilation: [✓] PASS (evidence/finalize-test-keep.txt)
- Test Execution: [✓] PASS (evidence/test_run.log)
```

---

## 5. Integration Checklist

### For All eiffel-* Skills

When any skill creates or maintains a simple_* library, verify:

- [ ] **Research/Spec Phase:** simple_* documented as primary dependencies (Rule 1)
- [ ] **Implementation Phase:** ECF uses simple_* not ISE (Rule 1)
- [ ] **Verify Phase:** Test binary compiled with F_code -keep (Rule 2)
- [ ] **Ship Phase:** Binary named test_app.exe in bin/ (Rule 3)
- [ ] **All Phases:** Input/output files in data/ subfolders (Rule 4)

### For eiffel-ship Specifically

**Before releasing:**

```bash
# Verify test binary exists and has DbC
ls -la bin/test_app.exe

# Verify data folder structure
find data/ -type f | head -20

# Verify reports
ls -la reports/TEST_SUITE_REPORT.md

# Final compilation check
/d/prod/ec.sh -batch -config lib.ecf -target lib_tests -c_compile -finalize -keep
```

---

## 6. Examples: Recent Libraries

### simple_graphviz (v1.0.0)

**Binary placement:**
```bash
ls -la simple_graphviz/bin/test_app.exe
```

**Data organization:**
```bash
find simple_graphviz/data -type f
# data/input/simple_graph.dot
# data/input/complex_network.dot
# data/output/graph.svg
# data/output/tree.png
# data/expected/reference.svg
```

**Test report:**
```bash
cat simple_graphviz/reports/TEST_SUITE_REPORT.md
```

### simple_spec_viz (current)

Follows same patterns as simple_graphviz. Use as template for new visualization libraries.

### simple_chart (latest)

**Test suite report:**
```bash
cat simple_chart/reports/TEST_SUITE_REPORT.md
# Shows: 46 tests (13 unit, 22 visual, 5 SVG, 4 format, 2 stress)
# Input: data/input/*.csv, data/input/*.json
# Output: data/output/*.svg, data/output/*.png, data/output/*.txt
```

---

## 7. Enforcement by Phase

| Phase | Standard | Enforcement |
|-------|----------|------------|
| **0: Intent** | Identify simple_* deps (Rule 1) | Phase 2 review checks approach.md |
| **1: Contracts** | ECF references simple_*, not ISE (Rule 1) | Phase 1 compile gate |
| **2: Review** | Approach confirms simple_* usage (Rule 1) | Human approval required |
| **3: Tasks** | Tasks specify simple_* library calls | Phase 3 decomposition |
| **4: Implement** | Code uses simple_* APIs (Rule 1) | Phase 4 compile gate |
| **5: Verify** | Test binary compiled with F_code -keep (Rule 2) | Phase 5 test execution |
| **6: Harden** | Adversarial tests use test_app.exe (Rule 3) | Phase 6 test execution |
| **7: Ship** | Verify bin/test_app.exe + data/ + reports/ (Rules 2,3,4) | Ship checklist validation |

---

## 8. Quick Reference

### File Paths (All Relative to Project Root)

```
bin/test_app.exe           → Compiled test binary (with DbC via -keep)
data/input/*.csv           → Test input files
data/input/*.json          → Test input files
data/input/*.dot           → Test input files
data/output/*.svg          → Generated outputs
data/output/*.png          → Generated outputs
data/expected/*.svg        → Reference/expected outputs
reports/TEST_SUITE_REPORT.md → Comprehensive test report
src/*.e                    → Library implementation
test/*.e                   → Test classes
lib.ecf                    → Project configuration
```

### Commands

```bash
# Compile for testing (keep DbC)
/d/prod/ec.sh -batch -config lib.ecf -target lib_tests -c_compile -finalize -keep

# Run tests
./bin/test_app.exe

# Check evidence
ls -la evidence/
cat reports/TEST_SUITE_REPORT.md
```

---

## 9. Native Libraries: One Version, One Source, Per DLL Name (Larry, 2026-11-11)

**Larry's rule, in his words** (the two quotations below are his; nothing else in this section is):

> "ALWAYS ensure that cairo.dll dependent libs use the SAME version. This DLL-hell issue should not be happening!"
>
> "NOTE: This ought to be true for any DLL at all and all the time. We don't want to fall into DLL hell ourselves. We cannot stop users. That is their choice. But we can work to prevent it on the simple_* fleet of libs."

**The fleet's reading of it** (written by the sessions; EIF-GROUP's decisions under the rule, not Larry's words):

- **One version per DLL name.** A DLL shipped under a given name (`cairo.dll`, `zlib.dll`, `freetype.dll`, …) is one build, byte for byte, everywhere in the fleet. Windows loads only one module of a given name into a process, so two builds under one name is a fault, not a cosmetic difference.
- **One owner per DLL.** Exactly one library owns each shared binary; every other library takes it from the owner (through the owner's ECF and folder), never by carrying its own copy.
- **Check before changing.** Before adding, upgrading or copying any DLL, or the import `.lib`/`.a` that pins one, run the fleet inventory. It fails on any name with two hashes, and no pull request that adds or changes a binary merges while it fails.
- **The owner tests what loads.** The owning library has a test that the version loaded at run time is the expected one.
- **Linux and macOS:** the same rule in their terms. Link the system's (Ubuntu) or Homebrew's (macOS) shared library, and do not ship a second shared copy of one the system provides. Source compiled into a library (SQLite in eiffel_sqlite_2025, the tree-sitter runtime in simple_tree_sitter) is allowed, with the reason stated in that library's notes. (Every conflict the 2026-11-11 inventory found was a shared binary loaded by name; source compiled in cannot collide that way.)

**The first case (2026-11-11):** simple_cairo shipped cairo 1.17.2, a development snapshot that cannot write multi-page PDFs, while simple_pdf shipped cairo 1.18.0. poppler-glib loads `cairo.dll` by name, so a GUI program that prints could have loaded either. Both move to 1.18.0, from one source.

What users do in their own programs is their choice; this rule governs the simple_* fleet.

**Written exceptions to the fleet's reading** (each meets Larry's rule, "the SAME version", and has a test that forbids drift):

- **simple_pdf/bin mirrors simple_cairo's set** (cairo 1.18.0 and its six neighbors), hash-checked by `test_bin_mirrors_the_owners_cairo_set`, because its helper programs (pdftotext, poppler) load DLLs from their own folder. Removed when staging lands: [simple_pdf issue 1](https://github.com/simple-eiffel/simple_pdf/issues/1).

---

## 10. Same on Every Platform (Larry, 2026-11-11)

**Larry's rule, in his words** (relayed by EIF-GROUP when he decided gray text antialiasing for Windows; the quotation is his, nothing else in this section is):

> "Yes, gray on Windows as well. There's no reason Windows ought to differ if we can make them all the same (e.g. each platform). This thinking ought to guide just about everything. The only platform deviations ought to be those that clearly cannot be helped or a just too much work for very little payoff or benefit."

**The fleet's reading of it** (written by the sessions; EIF-GROUP's decisions under the rule, not Larry's words):

- **Same behavior and same look on Windows, Linux and macOS** for every simple_* library and program, by default.
- **When you meet a platform difference, remove it; don't document it.** Keep one only where it clearly cannot be helped, or where the work far outweighs the benefit, and then write it down where it lives, with its reason, and bring it to EIF-GROUP.
- **Name deviations up front.** A spec lists each platform deviation and its reason before any half is built, so none is discovered late.
- **Accepted deviations so far:**
  - Command and Option in place of Control and Alt for editor keys on macOS: the platform's keyboard convention.
  - **Printing on Windows** (spec 1v-c): the printer's own Preferences choices are not applied; copies are repeated collated jobs; printers named outside ASCII can't be reached; printed text becomes shapes. Removed by simple_pdf#3.
  - **macOS prints through PDFKit**, not Poppler (Larry, 2026-11-11): the platform's own PDF library, as Linux uses Poppler; checked against Poppler page by page.
- **Removed deviations:**
  - **Shaped text on Windows kept ClearType** (2026-11-11 to 2026-11-12). Gray through cairo's win32 font backend (GDI grayscale) cut small-mark contrast below the gate. simple_shaping#8 removed it: shaped runs on Windows are drawn through cairo's FreeType backend, the rasterizer Linux uses, in gray. simple_widgets `gw03_marks_visible` (pointed Hebrew at 14 px, the share of the vowel points' ink at 3:1 or better, needs 25%):

    | | Light | Dark |
    |---|---|---|
    | ClearType (before) | 31% | 45% |
    | Gray through win32 | 2% | 24% |
    | Gray through FreeType (now) | 42% | 46% |
- **Decided under the rule (2026-11-11):**
  - text is drawn with gray antialiasing on every platform (simple_widgets 71);
  - every caret, the primary and the extras, blinks in step on all three and honors each system's no-blink setting;
  - a folded line shows "…" on all three.

---

## 11. Changed Contracts Test Their Consumers (Larry, 2026-11-11)

**Larry's rule, in his words** (relayed by EIF-GROUP after a simple_widgets change broke simple_bible; the quotations are his, nothing else in this section is):

> "I am a little surprised that in our GUI tasking we've not sufficiently addressed the issue of downstream consumer simple_* libs being regression tested."
>
> "I think it would be a big waste of time/tokens to retest all downstream consumers for each and every push/merge/commit, yes?"
>
> "MORE TO THE POINT: Any upstream simple_* lib that changes not just a feature name, but the feature contracts (pre and post-conditions specifically)."
>
> "Adding features is not the issue. It's changes to the API and contract demands."

**The fleet's reading of it** (written by the sessions; EIF-GROUP's decisions under the rule, not Larry's words):

1. **Trigger:** a pull request to any simple_* library that changes an EXISTING exported feature's name (or removes it, or makes it secret), its arguments or result type, its export, its precondition or its postcondition, or a class invariant. **Not a trigger:** new features, new classes, contracts on new features, and internal changes that keep every existing contract.
2. **On a trigger:** find the consumers that call those features (a search across `D:\prod`), and run their test suites with contracts on **before the merge**. Only those consumers, not all.
3. **No trigger:** no consumer runs; the library's own tests carry it.
4. **The check:** `scripts/contract_diff.py <repo> [<base> [<head>]]` (in this repository) compares a pull request's exported features with the base and lists each changed or removed one, with its before and after. It exits 0 with an empty list. **Every pull request states the list either way.**
5. **Each phase end:** one compile round of all consumers, and the full suites of the main two or three (simple_bible first). **At the very end of the GUI plan:** a full pass over every Windows consumer, rebuilt, tested, fixed and released by its owner.

**The first case (2026-11-11):** simple_widgets c430fea added `ends_its_zone` to `SW_DOCK_HOST.move_panel`, a postcondition on an existing feature whose body did not meet it, and simple_bible's GUI suite fell from 60/0 to 12/48. `contract_diff.py` on c430fea lists it (`SW_DOCK_HOST.move_panel: postcondition changed`) among eight changes. Fixed in simple_widgets #74.

**Shared checkouts stay on their default branches (EIF-GROUP, 2026-11-12).** The checkouts in `D:\prod` are read by other sessions (INCIPIT builds simple_bible installers from them), by MACMINI's hand-offs and by Larry's own builds. Never switch one to another branch, not even briefly. Do branch work in a git worktree of your own under `D:\prod\_wt` (`git worktree add D:\prod\_wt\<lib> <branch>`), and build against a tree of junctions, `D:\prod\_wt\tree`, whose entries point at `D:\prod`, except the libraries you are changing, which point at your worktrees. Set `SIMPLE_EIFFEL` to that tree (ec.sh and ec_linux.sh honor it), and build a consumer you only test, such as simple_bible's GUI suite, in a worktree of its own, so its owner's EIFGENs are untouched. *Why:* on 2026-11-12, a branch switched in the shared simple_shaping checkout was compiled into a simple_bible build that was installed on Larry's machine.

**Test programs use the fleet DLLs.** Run every test program that loads cairo with `simple_cairo\runtime\windows` first on PATH, or with its seven DLLs beside the exe, and check what loaded (`(Get-Process <name>).Modules`). With the plain PATH, a test run on 2026-11-12 loaded cairo from Simple Bible's install, FreeType from Graphviz and zlib from Git.

---

## 12. Related Documents

- `/d/prod/reference_docs/briefings/EIFFEL_EXPERT_BRIEFING.md` - Language & pattern guidance
- `/d/prod/reference_docs/analyses/higher-API/EIFFEL_SPEC_KIT_HOWTO.md` - Phase-by-phase workflow
- `/d/prod/CLAUDE.md` - Session boot configuration

---

**This document is the authoritative source for build standards in the simple_* ecosystem. All eiffel-* skills should reference and enforce these rules.**
