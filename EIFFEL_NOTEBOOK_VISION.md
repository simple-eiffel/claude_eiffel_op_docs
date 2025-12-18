# EiffelNotebook Vision

**Interactive notebook environment for Eiffel, inspired by Jupyter Notebooks**

*Proposed by: Javier Hector (+1 Eric Bezault) - December 2024*

## Overview

EiffelNotebook is a local, browser-based interactive environment for writing and executing Eiffel code in cells. It serves as both a learning tool and a showcase for the simple-eiffel library ecosystem.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  Browser (localhost:8080)                           │
│  ┌───────────────────────────────────────────────┐  │
│  │  HTML + HTMX + Alpine.js                      │  │
│  │  - Cell editor (Alpine reactive)              │  │
│  │  - hx-post="/execute" for cell runs           │  │
│  │  - hx-swap="innerHTML" for results            │  │
│  └───────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP (localhost only)
┌──────────────────────▼──────────────────────────────┐
│  EiffelNotebook Server (Eiffel)                     │
│                                                     │
│  Routes:                                            │
│    GET  /              → Notebook UI                │
│    POST /execute       → Compile & run cell         │
│    POST /save          → Save notebook.json         │
│    GET  /load/:name    → Load notebook              │
│    GET  /notebooks     → List saved notebooks       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Libraries Used

| Library | Role |
|---------|------|
| simple_web | HTTP server (localhost) |
| simple_htmx | HTMX response helpers |
| simple_alpine | Alpine.js component helpers |
| simple_json | Notebook file format (.eifnb) |
| simple_process | Compile (ec) and run executables |
| simple_file | Read/write notebook files |
| simple_console | Capture stdout/stderr |
| simple_eiffel_parser | Syntax validation, highlighting |
| simple_markdown | Render markdown cells |
| simple_template | HTML generation |

## Execution Model: Accumulated Class + Melting

### The Challenge

- Python/Jupyter: Interpreted → instant execution
- Eiffel: Compiled → requires class structure + compilation

### Solution

Each cell contributes to an accumulated class. State persists via class attributes.

**Example session:**

```
Cell 1:  x: INTEGER
Cell 2:  x := 42
Cell 3:  print(x.out)
Cell 4:  y := x + 10
```

**Generated class:**

```eiffel
class NOTEBOOK_SESSION

create
    make

feature -- State (from declaration cells)

    x: INTEGER
    y: INTEGER

feature -- Cells

    cell_1
        do
            -- declaration only
        end

    cell_2
        do
            x := 42
        end

    cell_3
        do
            print (x.out)
        end

    cell_4
        do
            y := x + 10
        end

feature -- Execution

    make
        do
            cell_1
            cell_2
            cell_3
            cell_4
        end

end
```

### Performance

- **Initial compile:** ~5-10 seconds (precompile base libraries)
- **Per-cell execution:** ~1-3 seconds (melting - incremental compilation)
- **UX:** Show "Compiling..." spinner during execution

### Future-Proof

If Eiffel Software ever creates an IR interpreter, the notebook architecture remains unchanged - only the execution backend swaps from `ec + run` to `interpret`.

## Cell Types

1. **Code cells** - Eiffel code, compiled and executed
2. **Markdown cells** - Documentation, rendered via simple_markdown
3. **Declaration cells** - Class attributes (special code cell type)

## Notebook Format (.eifnb)

JSON-based, similar to Jupyter's .ipynb:

```json
{
  "metadata": {
    "title": "My Notebook",
    "created": "2024-12-18T12:00:00Z",
    "eiffel_version": "25.02"
  },
  "cells": [
    {
      "type": "markdown",
      "source": "# Introduction\nThis notebook demonstrates..."
    },
    {
      "type": "declaration",
      "source": "counter: INTEGER"
    },
    {
      "type": "code",
      "source": "counter := counter + 1\nprint (counter.out)",
      "output": "1",
      "execution_count": 1
    }
  ]
}
```

## Key Features

### MVP (Phase 1)
- [ ] Local HTTP server on configurable port
- [ ] Code cell execution with output capture
- [ ] Markdown cell rendering
- [ ] Save/load notebooks
- [ ] Basic syntax highlighting

### Phase 2
- [ ] Declaration cells (class attributes)
- [ ] Cell reordering (drag & drop)
- [ ] Export to HTML
- [ ] Export to standalone Eiffel class

### Phase 3
- [ ] Multiple notebook tabs
- [ ] Library import cells (use simple_json, etc.)
- [ ] Autocomplete (via simple_lsp integration)
- [ ] Error highlighting with contract violations

### Phase 4
- [ ] Visualization cells (charts via simple_toon or SVG)
- [ ] Database cells (simple_sql integration)
- [ ] HTTP cells (simple_http for API exploration)

## Advantages

1. **Zero external dependencies** - No Node.js, Python, or npm required
2. **Single executable** - Compile once, distribute easily
3. **Dogfooding** - Showcases 10+ simple_* libraries working together
4. **Offline** - Works without internet connection
5. **Lightweight** - HTMX + Alpine.js, no heavy JavaScript frameworks
6. **Eiffel all the way down** - Server logic in Eiffel with full DBC

## Usage

```bash
# Start notebook server
eiffel_notebook --port 8080

# Opens browser automatically to http://localhost:8080
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| GUI framework | HTML + HTMX + Alpine | Lightweight, no build step, simple_htmx/alpine exist |
| Execution model | Accumulated class + melting | Only practical option without interpreter |
| File format | JSON (.eifnb) | Human-readable, simple_json handles it |
| Server | Local only | Security, simplicity, offline use |
| State persistence | Class attributes | Natural Eiffel pattern |

## Non-Goals

- Cloud hosting / multi-user
- Real-time collaboration
- Full IDE replacement
- Support for non-Eiffel languages

## Related Work

- [Jupyter Notebook](https://jupyter.org/) - Inspiration
- [Observable](https://observablehq.com/) - Reactive notebooks
- [Livebook](https://livebook.dev/) - Elixir notebooks

---

*Document created: 2024-12-18*
*Status: Vision / Planning*
