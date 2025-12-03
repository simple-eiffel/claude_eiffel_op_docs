# Creating simple_htmx: From Code Smell Analysis to Reusable Library

**Project:** simple_htmx
**Date:** December 2024
**Pattern:** Library Extraction from Code Smell Analysis

## Overview

This document captures how a code smell analysis of `simple_gui_designer` led to the creation of a new reusable library (`simple_htmx`) that will benefit all future Eiffel web applications.

## The Journey

### Phase 1: God Class Refactoring

Earlier in the session, we refactored `GUI_DESIGNER_SERVER` from a 2,000-line God class into 10 focused handler classes using Eiffel's multiple inheritance. This was documented in `REFACTORING_CASE_STUDY.md`.

### Phase 2: Code Smell Analysis

After the refactoring, we analyzed the remaining codebase for friction points. The exploration agent identified 12 categories of issues:

| Category | Example | Severity |
|----------|---------|----------|
| `.do_nothing` chains | 20+ lines of `Result.put_string(...).do_nothing` | Medium |
| String building noise | 15+ sequential `.append()` calls per render method | Medium |
| Parameter passing | `(a_control, a_spec_id, a_screen_id)` repeated in 30+ methods | Medium |
| HTMX attribute generation | Manual string building for `hx-get`, `hx-target`, etc. | Medium |
| Magic numbers | Hardcoded `24` for grid width | Low |

### Phase 3: The Key Question

The human asked a pivotal question:

> "Does it make sense to create another library something like 'simple_htmx'?"

This question recognized that the friction points weren't unique to `simple_gui_designer` - they would appear in **every** HTMX-based Eiffel web application.

### Phase 4: Architecture Decision

**Question:** Should HTMX support go into `simple_web` or a new library?

**Decision:** Separate library because:
1. **Single responsibility** - `simple_web` handles HTTP plumbing, not markup generation
2. **Optional dependency** - Not every `simple_web` app needs HTMX (some are pure JSON APIs)
3. **Independent evolution** - HTMX patterns change independently of HTTP handling
4. **Testability** - HTML builder is pure functions, no server needed

**The relationship:**
```
simple_web (HTTP server/routing)
     |
     +-- simple_htmx (HTML/HTMX generation) -- optional, for web UIs
     |
     +-- simple_json (already separate) -- for API responses
```

## What We Built

### Core Classes

**HTMX_ELEMENT** (base class)
- Fluent interface (feature chaining) for all HTML attributes
- Standard HTML attributes: `id`, `class_`, `data`, `style`, `title`
- All HTMX attributes: `hx_get`, `hx_post`, `hx_target`, `hx_swap`, `hx_trigger`, etc.
- Child element support: `containing`, `with_children`
- HTML escaping for security
- Output: `to_html`, `to_html_8`

**HTMX_FACTORY** (convenience creation)
```eiffel
html: HTMX_FACTORY
...
l_div := html.div.id ("main").class_ ("container")
l_btn := html.button_text ("Save").hx_post ("/api/save")
l_link := html.link ("https://example.com", "Example").target_blank
```

**HTMX_RENDER_CONTEXT** (URL path building)
```eiffel
ctx := create {HTMX_RENDER_CONTEXT}.make ("/api")
ctx.with_spec ("my-app").with_screen ("main").do_nothing

ctx.url                        -- "/api/specs/my-app/screens/main"
ctx.url_for ("controls")       -- "/api/specs/my-app/screens/main/controls"
ctx.control_url ("btn1")       -- "/api/specs/my-app/screens/main/controls/btn1"
```

### HTML Elements (31 classes)

| Category | Elements |
|----------|----------|
| Containers | div, span, p, h1, h2, h3 |
| Forms | form, input, textarea, select, option, label, button |
| Links/Media | a, img |
| Lists | ul, ol, li |
| Tables | table, thead, tbody, tfoot, tr, th, td |
| Misc | br, hr |

### HTMX Attributes

| Category | Attributes |
|----------|------------|
| Request | `hx_get`, `hx_post`, `hx_put`, `hx_patch`, `hx_delete` |
| Targeting | `hx_target`, `hx_swap`, `hx_swap_inner_html`, `hx_swap_outer_html`, etc. |
| Triggers | `hx_trigger`, `hx_trigger_click`, `hx_trigger_change`, `hx_trigger_load` |
| UX | `hx_confirm`, `hx_indicator`, `hx_disable` |
| Advanced | `hx_vals`, `hx_include`, `hx_select`, `hx_push_url` |

## Before and After

### Before (in simple_gui_designer)

```eiffel
render_simple_control (a_control: GUI_DESIGNER_CONTROL; a_spec_id, a_screen_id: STRING_32): STRING
    do
        create Result.make (500)
        Result.append ("    <div class=%"control col-")
        Result.append (a_control.col_span.out)
        Result.append (" type-")
        Result.append (s8 (a_control.control_type))
        Result.append ("%" data-id=%"")
        Result.append (s8 (a_control.id))
        Result.append ("%" draggable=%"true%" ")
        Result.append ("hx-get=%"/htmx/properties/")
        Result.append (s8 (a_spec_id))
        Result.append ("/")
        Result.append (s8 (a_screen_id))
        Result.append ("/")
        Result.append (s8 (a_control.id))
        Result.append ("%" hx-target=%"#properties%" hx-swap=%"innerHTML%" ")
        -- ... 10 more lines
    end
```

### After (with simple_htmx)

```eiffel
render_simple_control (a_control: GUI_DESIGNER_CONTROL; a_ctx: HTMX_RENDER_CONTEXT): STRING
    do
        Result := html.div
            .classes_from ("control col-" + a_control.col_span.out)
            .class_ ("type-" + a_control.control_type.to_string_8)
            .data ("id", a_control.id)
            .attr ("draggable", "true")
            .hx_get (a_ctx.properties_url (a_control.id))
            .hx_target ("#properties")
            .hx_swap_inner_html
            .to_html_8
    end
```

**Impact:**
- 15+ lines reduced to 8 lines
- No manual string escaping
- Type-safe HTMX attribute names (no typos in "hx-get")
- Render context eliminates parameter passing
- Readable, intention-revealing code

## Eiffel-Specific Learnings

### VKCN(1) - Functions Used as Statements

When using fluent interfaces, the final call in a chain returns a value. If you don't need that value, Eiffel requires you to explicitly discard it:

```eiffel
-- WRONG: Function call used as statement
l_div.class_ ("container")

-- CORRECT: Discard the result explicitly
l_div.class_ ("container").do_nothing
```

This appeared throughout the codebase - in factory methods, test assertions, and element building.

### The `do_nothing` Pattern

The `.do_nothing` pattern is Eiffel's way of saying "I'm calling this for side effects, not the return value." It's the price of feature chaining in a language with strict function/procedure separation.

**Alternative approaches considered:**
1. Make all fluent methods procedures (loses chaining)
2. Always assign to variables (verbose)
3. Use `.do_nothing` (chosen - explicit and chainable)

## Project Statistics

| Metric | Value |
|--------|-------|
| Total classes | 34 (3 core + 31 elements) |
| Total lines | ~2,600 |
| Test cases | 30+ |
| HTMX attributes | 20+ |
| HTML elements | 31 |

## Future Impact

### simple_gui_designer refactoring
When `simple_gui_designer` adopts `simple_htmx`:
- `gds_html_renderer.e` (17KB) could shrink 50-70%
- `gds_static_html.e` (29KB) becomes cleaner
- All `.append()` chains replaced with fluent builders
- Parameter passing eliminated via render context

### Future projects
Any Eiffel project with an HTMX web interface now has:
- Type-safe HTML generation
- Type-safe HTMX attributes
- URL path building
- No string manipulation for HTML
- Consistent patterns across projects

## Collaboration Model

This session demonstrates effective Human-AI collaboration:

**Human contributions:**
- Recognized the library extraction opportunity
- Asked the key architectural question (bloat simple_web vs. new library)
- Decided on separation of concerns
- Identified the pattern name ("feature chaining" for fluent interface)

**AI contributions:**
- Code smell analysis (quantified 12 categories)
- Library design and implementation (34 classes)
- Test suite (30+ tests)
- Documentation
- VKCN error resolution

**Key insight from the human:**
> "pushing this all back into simple_htmx should make simple_gui_app lighter, yes?"

This question validated the architectural direction - the goal isn't just code reuse, it's making consumer projects simpler.

## Files Created

```
simple_htmx/
├── simple_htmx.ecf
├── src/
│   ├── core/
│   │   ├── htmx_element.e
│   │   ├── htmx_factory.e
│   │   └── htmx_render_context.e
│   └── elements/
│       ├── htmx_a.e
│       ├── htmx_br.e
│       ├── htmx_button.e
│       ├── htmx_div.e
│       ├── htmx_form.e
│       ├── htmx_h1.e, htmx_h2.e, htmx_h3.e
│       ├── htmx_hr.e
│       ├── htmx_img.e
│       ├── htmx_input.e
│       ├── htmx_label.e
│       ├── htmx_li.e
│       ├── htmx_ol.e, htmx_ul.e
│       ├── htmx_option.e
│       ├── htmx_p.e
│       ├── htmx_select.e
│       ├── htmx_span.e
│       ├── htmx_table.e
│       ├── htmx_tbody.e, htmx_thead.e, htmx_tfoot.e
│       ├── htmx_td.e, htmx_th.e, htmx_tr.e
│       └── htmx_textarea.e
└── testing/
    ├── application.e
    └── test_htmx_elements.e
```

## Conclusion

What started as a code smell analysis ("what other friction exists?") led to the creation of a foundational library for Eiffel web development. The key was recognizing that the friction wasn't project-specific - it was infrastructure that every HTMX project would need.

This is a poster-child example of:
1. Code smell analysis driving architectural decisions
2. Library extraction based on reuse potential
3. Human-AI collaboration on design decisions
4. Fluent interfaces in Eiffel (with `.do_nothing` pattern)
