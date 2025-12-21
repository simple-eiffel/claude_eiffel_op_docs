# simple_notebook Fast Execution Research

## Goal
Sub-second notebook cell execution (currently 10-30 seconds per cell)

## Current Architecture
```
Cell code → Generated .e file → ec.exe -c_compile → gcc/msvc → exe → run
                                       ↑
                                 SLOW (10-30s)
```

## Research Findings

### 1. Gobo gec Compiler
**Status: NOT a solution**

- gec is also an Eiffel-to-C compiler, not an interpreter
- No bytecode/interpreter mode
- SCOOP limitations (wait conditions not supported)
- Would need to build from source (bootstrap C files available)

**Verdict:** Same compilation model as EiffelStudio, won't help with speed.

### 2. tecomp Interpreter
**Status: Abandoned project**

- Could execute Eiffel directly without C compilation
- Last release: 2009 (v0.7)
- Project abandoned, successor is Albatross (also inactive)
- Not ECMA-367 complete

**Verdict:** Not viable - abandoned, incomplete.

Source: [tecomp on SourceForge](https://sourceforge.net/projects/tecomp/)

### 3. EiffelStudio Melting Ice Technology
**Status: PROMISING - needs more investigation**

EiffelStudio has a bytecode interpreter built into workbench executables:

#### Key Files in EIFGENs/target/W_code:
- `TRANSLAT` - main bytecode translation table (~1MB)
- `*.melted` - incremental melted changes (~45KB)
- `*.exe` - workbench executable with embedded interpreter

#### ec.exe -loop Mode Discovery
The `-loop` interactive mode has:
```
(I) Compile menu:
    (L) Melt      - generates bytecode only (FAST, ~2-5s)
    (K) Quick_melt - even faster incremental melt
    (R) Run       - execute the system
    (D) Debug     - debug as command loop
```

#### Melting Ice Workflow:
1. **Initial freeze** (once): Eiffel → C → exe with interpreter (~30s)
2. **Subsequent melts** (fast): Eiffel → bytecode only (~2-5s)
3. **Run**: exe loads TRANSLAT + .melted, interprets bytecode

### 4. Bytecode Tools (from dev.eiffel.com)
- `meltdump` - reads melted file → melted.txt + bytecode.eif
- `bytedump` - reads bytecode.eif → bytecode.txt
- Located in EiffelStudio's C/bench directory (not in standard install)

Source: [EiffelStudio Bytecode](https://dev.eiffel.com/Byte_Code)

## Proposed Architecture for Fast Notebook

### Option A: Warm Process with Melting
```
                    FIRST RUN (slow, once)
Cell code → ec.exe -freeze → W_code/notebook.exe (with interpreter)
                               ↓
                    SUBSEQUENT RUNS (fast)
New cell  → ec.exe -melt → .melted file → notebook.exe interprets
                 ↑                              ↓
              ~2-5s                        sub-second
```

**Implementation:**
1. On notebook start: ensure W_code exe exists (freeze once if needed)
2. On cell execute: melt only, then run exe
3. Keep ec.exe in `-loop` mode for instant melting

### Option B: Persistent Compiler Process
Keep ec.exe running in loop mode, send commands:
```
notebook_cli ←→ ec.exe -loop (persistent)
                    ↓
              I → L (melt) → R (run)
```

**Pros:** No compiler startup overhead per cell
**Cons:** Complex IPC, process management

### Option C: Incremental Melting with Base Image
1. Create "base" notebook with common imports (freeze once)
2. Each cell: add to base, melt only changed parts
3. Run interprets cumulative bytecode

## Next Steps

1. **Verify melt+run works** without C compilation
2. **Measure melt time** for small code changes
3. **Test `-loop` mode** for persistent compiler
4. **Prototype** Option A with simple_notebook
5. **Contact ISE** (Emmanuel Stapf) about bytecode interpreter access

## Questions for ISE

1. Can we invoke the interpreter standalone without the full exe?
2. Is there a way to melt programmatically via library API?
3. Are meltdump/bytedump shipped with EiffelStudio?
4. Any plans for a dedicated REPL/notebook mode?

## Resources

- [EiffelStudio Bytecode Documentation](https://dev.eiffel.com/Byte_Code)
- [Gobo gec Documentation](https://www.gobosoft.com/eiffel/gobo/gec/)
- [tecomp (abandoned)](https://sourceforge.net/projects/tecomp/)
- [Liberty Eiffel](https://www.liberty-eiffel.org/)

---
*Last updated: 2025-12-21*

---

## PROTOTYPE RESULTS (2025-12-21)

### Test Setup
- Location: `/d/prod/melt_prototype`
- Simple APPLICATION class with compute features

### Timing Results

| Operation | Time | Notes |
|-----------|------|-------|
| **Initial Freeze** | 14 seconds | One-time cost, creates W_code exe with interpreter |
| **Melt (first)** | 0.63 seconds | Sub-second! |
| **Melt (subsequent)** | 1.35 seconds | Slightly longer |
| **Quick Melt** | 0.52 seconds | Fastest option |

### Key Finding: IT WORKS!

The W_code executable contains an embedded bytecode interpreter. After the initial freeze:
1. Code changes → melt only (no C compilation)
2. Run exe → interpreter reads `.melted` file
3. Output reflects the new code

**Proof:**
```
Version 1 (after freeze): "Value: 42"
Version 2 (after melt):   "Value: 100", "New feature: 200"
Version 3 (after melt):   "Tripled: 21"
Version 4 (quick_melt):   "Result: 999"
```

### Performance Improvement
- **Current simple_notebook**: 10-30 seconds per cell
- **With melting**: 0.5-1.5 seconds per cell
- **Speedup: 10-30x faster!**

### Commands Used
```bash
# Initial freeze (once)
ec.exe -batch -config project.ecf -target target -freeze -c_compile

# Fast melt (each cell change)
ec.exe -batch -config project.ecf -target target -quick_melt

# Run
./EIFGENs/target/W_code/project.exe
```

## Integration Plan for simple_notebook

### Phase 1: Basic Integration
1. Detect if W_code exe exists
2. If not: freeze once (show "Initializing..." message)
3. On cell execute: quick_melt + run
4. Capture output as before

### Phase 2: Optimization
1. Keep ec.exe process warm (avoid startup overhead)
2. Use `-loop` mode for persistent compiler
3. Only regenerate changed cells

### Phase 3: Advanced
1. Pre-freeze a "base image" with common libraries
2. Incremental bytecode updates
3. Hot-reload without restart

---
*Prototype validated: 2025-12-21*

---

## INTEGRATION COMPLETE (2025-12-21)

### Changes to CELL_EXECUTOR

Added to `cell_executor.e`:

```eiffel
is_frozen: BOOLEAN
    -- Has initial freeze been done?
    -- After freeze, we can use fast melt mode (no C compilation)

check_frozen_status
    -- Check if W_code exe exists (meaning freeze was done previously)

reset_frozen_status
    -- Force fresh freeze on next compile (e.g., after config change)

build_compile_command (a_ecf_path: PATH): STRING
    -- Build the appropriate compile command
    -- Freeze with C compile on first run, quick_melt on subsequent
```

### Behavior

1. **First cell execution**: Shows `(freeze)`, runs ~14 seconds
   - Uses: `ec.exe -batch -clean -config ... -freeze -c_compile`
   - Creates W_code exe with embedded bytecode interpreter

2. **Subsequent cell executions**: Shows `(melt)`, runs ~0.5-1.5 seconds
   - Uses: `ec.exe -batch -config ... -quick_melt`
   - No C compilation, just bytecode generation

3. **On melt failure**: Automatically resets `is_frozen` to force fresh freeze

### Version

Released in **simple_notebook 1.0.0-alpha.23**

---
*Integration complete: 2025-12-21*
