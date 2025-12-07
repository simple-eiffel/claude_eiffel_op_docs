# Resume Point

**Date:** 2025-12-07
**Last Session:** simple_pdf library COMPLETE

---

## Current State

### simple_pdf (COMPLETE)
- **Location:** `D:\prod\simple_pdf`
- **Status:** Fully functional, all 9 tests passing
- **GitHub Repo:** Set up and ready for commit
- **Architecture:** Multi-engine with deferred base class
  - `SIMPLE_PDF_ENGINE` (deferred) - base class with page settings
  - `SIMPLE_PDF_WKHTMLTOPDF` - default engine, ships wkhtmltopdf.exe
  - `SIMPLE_PDF_CHROME` - best CSS quality, uses Chrome/Edge headless
  - `SIMPLE_PDF_READER` - text extraction via pdftotext (Poppler)
  - `SIMPLE_PDF_DOCUMENT` - represents generated PDF
  - `SIMPLE_PDF_ENGINES` - engine availability reporter
- **Binaries in bin/:**
  - wkhtmltopdf.exe + wkhtmltox.dll (~120MB)
  - pdftotext.exe + Poppler DLLs (~22MB)
- **Tests:** 9/9 passing (6 unit + 3 integration)

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

---

## Next Steps

1. **Commit simple_pdf to GitHub**
   - All tests passing, ready for initial commit

2. **Tier 1 libraries** from roadmap:
   - simple_xml (wraps XM_* classes)
   - simple_datetime (wraps DATE/TIME)
   - simple_file (wraps FILE/PATH/DIRECTORY)

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

-- With Chrome for best rendering
create pdf.make_with_engine (create {SIMPLE_PDF_CHROME})
doc := pdf.from_url ("https://example.com")

-- Text extraction
create reader.make
text := reader.extract_text ("document.pdf")

-- Engine availability check
create engines
print (engines.report)  -- Shows which engines are available
```
