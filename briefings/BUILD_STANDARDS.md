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

Larry's rule, in his words:

> "ALWAYS ensure that cairo.dll dependent libs use the SAME version. This DLL-hell issue should not be happening!"
>
> "NOTE: This ought to be true for any DLL at all and all the time. We don't want to fall into DLL hell ourselves. We cannot stop users. That is their choice. But we can work to prevent it on the simple_* fleet of libs."

**What it means across the simple_* libraries:**

- **One version per DLL name.** A DLL shipped under a given name (`cairo.dll`, `zlib.dll`, `freetype.dll`, …) is one build, byte for byte, everywhere in the fleet. Windows loads only one module of a given name into a process, so two builds under one name is a fault, not a cosmetic difference.
- **One owner per DLL.** Exactly one library owns each shared binary; every other library takes it from the owner (through the owner's ECF and folder), never by carrying its own copy.
- **Check before changing.** Before adding, upgrading or copying any DLL, or the import `.lib`/`.a` that pins one, run the fleet inventory. It fails on any name with two hashes, and no pull request that adds or changes a binary merges while it fails.
- **The owner tests what loads.** The owning library has a test that the version loaded at run time is the expected one.
- **Linux and macOS:** the same rule in their terms. Link the system's (Ubuntu) or Homebrew's (macOS) shared library, and do not vendor a second copy of one the system provides.

**The first case (2026-11-11):** simple_cairo shipped cairo 1.17.2, a development snapshot that cannot write multi-page PDFs, while simple_pdf shipped cairo 1.18.0. poppler-glib loads `cairo.dll` by name, so a GUI program that prints could have loaded either. Both move to 1.18.0, from one source.

What users do in their own programs is their choice; this rule governs the simple_* fleet.

---

## 10. Related Documents

- `/d/prod/reference_docs/briefings/EIFFEL_EXPERT_BRIEFING.md` - Language & pattern guidance
- `/d/prod/reference_docs/analyses/higher-API/EIFFEL_SPEC_KIT_HOWTO.md` - Phase-by-phase workflow
- `/d/prod/CLAUDE.md` - Session boot configuration

---

**This document is the authoritative source for build standards in the simple_* ecosystem. All eiffel-* skills should reference and enforce these rules.**
