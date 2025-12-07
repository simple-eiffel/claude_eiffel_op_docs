# Resume Point

**Date:** 2025-12-07
**Last Session:** simple_pdf with fluent API and full documentation COMPLETE

---

## 🎯 EIFFEL EXPERT MODE - READ FIRST

**Claude: You are Larry's Eiffel Expert.** At the start of EVERY session:

### Mandatory Startup Protocol
1. **Read this file** - understand current state and next steps
2. **Read `claude/CONTEXT.md`** - compiler paths, ECF patterns, session workflow
3. **Scan `language/gotchas.md`** - avoid known pitfalls (VAPE, STRING_32, across loops)
4. **Reference `language/patterns.md`** - use verified working code patterns
5. **Know the HATS** (`claude/HATS.md`) - use focused work modes when appropriate

### Your Eiffel Knowledge Base
You have access to comprehensive Eiffel documentation in this folder:
- **claude/EIFFEL_MENTAL_MODEL.md** - Condensed ECMA-367 essentials (read this, not the full spec)
- **language/gotchas.md** - Doc vs reality corrections (critical!)
- **language/patterns.md** - Verified working code (MI mixin, fluent API, WSF)
- **language/across_loops.md** - Iteration constructs (cursor.item vs cursor)
- **language/scoop.md** - SCOOP concurrency model
- **language/sqlite_gotchas.md** - Database-specific issues
- **claude/contract_patterns.md** - Complete postcondition templates
- **claude/verification_process.md** - Meyer's "probable to provable" framework
- **claude/HATS.md** - Focused work modes (Specification, Testing, etc.)
- **ECMA-367_Full.md** - Full language spec (only for edge cases)

### Key Eiffel Principles
- **Trust compiler errors** over documentation when they conflict
- **Design by Contract** - specify BEFORE implementing (Specification Hat)
- **MI pattern** - use deferred mixin classes for god-class decomposition
- **Fluent APIs** - return `like Current` and `Result := Current`
- **VAPE rule** - preconditions cannot reference private features
- **STRING_32 vs STRING_8** - explicit `.to_string_8` conversion required

### simple_* Library Ecosystem
- **26 libraries** in the ecosystem
- **API Hierarchy**: FOUNDATION_API → SERVICE_API → APP_API
- Libraries "flow uphill" - adding to SERVICE_API makes it available in APP_API
- **Environment variables**: `$SIMPLE_*` patterns for ECF locations

---

## Current State

### simple_pdf (COMPLETE)
- **Location:** `D:\prod\simple_pdf`
- **Status:** Fully functional, 10 tests passing, committed to GitHub
- **GitHub Repo:** https://github.com/ljr1981/simple_pdf
- **Architecture:** Multi-engine with deferred base class
  - `SIMPLE_PDF_ENGINE` (deferred) - base class with page settings
  - `SIMPLE_PDF_WKHTMLTOPDF` - default engine (bundled)
  - `SIMPLE_PDF_CHROME` - best CSS quality (Chrome/Edge headless)
  - `SIMPLE_PDF_READER` - text extraction via pdftotext (Poppler)
  - `SIMPLE_PDF_DOCUMENT` - result object (is_valid, save_to_file, as_base64)
  - `SIMPLE_PDF_ENGINES` - engine availability reporter
- **Features:**
  - Fluent API: `pdf.page("Letter").landscape.margin_all("1in").from_html(html)`
  - Traditional API: `pdf.set_page_size("A4")`, `pdf.set_orientation("Portrait")`
  - API integration: Part of SERVICE_API (flows up to APP_API)
- **Binaries in bin/:**
  - wkhtmltopdf 0.12.6 (LGPL v3) - ~40MB
  - pdftotext 24.08.0 (Poppler, GPL v2+) - ~22MB
- **Tests:** 10/10 passing (6 unit + 4 integration)

### Libraries Complete
- 26 libraries in simple_* ecosystem (including simple_pdf)
- All integrated into FOUNDATION_API / SERVICE_API / APP_API

---

## Learnings from simple_pdf Build

### 1. PATH_NAME is Deferred
- Cannot instantiate PATH_NAME directly
- Use `EXECUTION_ENVIRONMENT.current_working_path.name.to_string_8` instead
- To get absolute path: Prepend cwd to relative paths

### 2. Executable Path Resolution
- Relative paths like "bin/wkhtmltopdf.exe" work for file.exists check
- But PROCESS_FACTORY needs absolute paths to launch reliably
- Solution: Check if path is absolute, otherwise prepend cwd:
```eiffel
l_cwd := l_env.current_working_path.name.to_string_8
if l_path.starts_with ("C:") or l_path.starts_with ("/") then
    executable_path := l_path
else
    executable_path := l_cwd + "/" + l_path
end
```

### 3. STRING_32 to STRING Conversion
- Environment variables return STRING_32 (READABLE_STRING_32)
- Use `.to_string_8` for explicit conversion to STRING
- Avoids obsolete warnings about implicit as_string_8

### 4. Test App Pattern
- Test apps should NOT inherit from EQA_TEST_SET/TEST_SET_BASE
- Instead, create test app as standalone class
- Create test set class separately, instantiate and call test methods
- Use rescue/retry pattern for test isolation

### 5. Fluent API Pattern in Eiffel
- Return `like Current` from fluent methods to enable chaining
- Set `Result := Current` at end of each fluent method
- Keep traditional setters for backwards compatibility
- Example:
```eiffel
page (a_size: STRING): like Current
    do
        set_page_size (a_size)
        Result := Current
    end

landscape: like Current
    do
        set_orientation ("Landscape")
        Result := Current
    end
```
- Usage: `pdf.page ("Letter").landscape.margin_all ("1in").from_html (html)`

---

## Next Steps

1. **Tier 1 libraries** from roadmap:
   - simple_xml (wraps XM_* classes)
   - simple_datetime (wraps DATE/TIME)
   - simple_file (wraps FILE/PATH/DIRECTORY)

2. **Potential improvements** (if needed):
   - Add more PDF engines (WeasyPrint, Prince)
   - PDF merging/splitting
   - Watermark support

---

## Key Files

| Need | Location |
|------|----------|
| simple_pdf source | `D:\prod\simple_pdf\src\` |
| simple_pdf binaries | `D:\prod\simple_pdf\bin\` |
| Eiffel gotchas | `reference_docs/language/gotchas.md` |
| SQLite gotchas | `reference_docs/language/sqlite_gotchas.md` |
| Library roadmap | `reference_docs/strategy/SIMPLIFICATION_ROADMAP.md` |

---

## API Design for simple_pdf

```eiffel
-- Default usage (wkhtmltopdf)
create pdf.make
doc := pdf.from_html ("<h1>Hello</h1>")
doc.save_to_file ("output.pdf")

-- Fluent API (concise, chainable)
create pdf.make
doc := pdf.page ("Letter").landscape.margin_all ("1in").from_html (report_html)
doc.save_to_file ("report.pdf")

-- Fluent with Chrome for best CSS
create pdf.make
doc := pdf.with_chrome.page ("A4").margins ("1in", "1in", "0.75in", "0.75in").from_url ("https://example.com")

-- Traditional API (explicit setters)
create pdf.make
pdf.set_page_size ("Letter")
pdf.set_orientation ("Landscape")
doc := pdf.from_url ("https://example.com")

-- Text extraction
create reader.make
text := reader.extract_text ("document.pdf")

-- Engine availability check
create engines
print (engines.report)  -- Shows which engines are available
```
