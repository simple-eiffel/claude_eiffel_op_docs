# Building a PDF Library in Eiffel in Under 2 Hours with AI Assistance

**Date:** December 7, 2025
**Library:** simple_pdf
**Repository:** https://github.com/ljr1981/simple_pdf

---

## Executive Summary

This post documents a real-time development session where we designed and built a fully functional PDF generation library for Eiffel in approximately 90 minutes. The library supports multiple rendering engines, includes bundled Windows binaries, and passes 10 automated tests including integration tests that generate actual PDF documents.

This demonstrates that AI-assisted development can dramatically accelerate library creation while maintaining proper Eiffel design principles.

---

## The Problem

Eiffel lacks a simple, modern PDF generation library. Existing solutions require complex setup, external dependencies that users must install themselves, or don't leverage Eiffel's strengths like Design by Contract.

**Requirements:**
- Generate PDFs from HTML strings, HTML files, or URLs
- Support multiple rendering engines (flexibility)
- Bundle executables so users don't need separate installs
- Extract text from existing PDFs
- Follow Eiffel naming conventions and design patterns
- Be immediately usable via ECF reference

---

## Architecture Design

We chose a **multi-engine architecture** using Eiffel's deferred classes:

```
SIMPLE_PDF_ENGINE (deferred)
    ├── SIMPLE_PDF_WKHTMLTOPDF (default)
    ├── SIMPLE_PDF_CHROME (best CSS)
    └── [future engines]

SIMPLE_PDF (main API)
    └── delegates to engine

SIMPLE_PDF_DOCUMENT (result object)
SIMPLE_PDF_READER (text extraction)
SIMPLE_PDF_ENGINES (availability reporter)
```

**Why this design?**

1. **Deferred base class** - Engines share interface but have different implementations
2. **Strategy pattern** - Swap engines at runtime without changing client code
3. **Bundled binaries** - wkhtmltopdf.exe and pdftotext.exe ship with the library
4. **Fallback options** - If wkhtmltopdf unavailable, use Chrome/Edge (already on most Windows machines)

---

## Implementation Timeline

| Time | Activity |
|------|----------|
| 0:00 | Design discussion - architecture, engine selection |
| 0:15 | Created project structure, ECF file |
| 0:25 | Implemented SIMPLE_PDF_ENGINE (deferred base) |
| 0:35 | Implemented SIMPLE_PDF_WKHTMLTOPDF engine |
| 0:45 | Implemented SIMPLE_PDF_CHROME engine |
| 0:55 | Implemented SIMPLE_PDF_DOCUMENT, SIMPLE_PDF_READER |
| 1:05 | First compile - fixed type errors |
| 1:15 | Test infrastructure - discovered test app patterns |
| 1:25 | Fixed path resolution issues with EXECUTION_ENVIRONMENT |
| 1:35 | All 9 tests passing, committed to GitHub |
| 1:45 | Added US Constitution demo test (10 tests passing) |

---

## Code Examples

### Basic Usage

```eiffel
-- Generate PDF from HTML
create pdf.make
doc := pdf.from_html ("<h1>Hello World</h1>")
doc.save_to_file ("output.pdf")

-- Generate from URL with settings
create pdf.make
pdf.set_page_size ("Letter")
pdf.set_orientation ("Landscape")
doc := pdf.from_url ("https://example.com")

-- Use Chrome for best CSS rendering
create pdf.make_with_engine (create {SIMPLE_PDF_CHROME})
doc := pdf.from_html (complex_css_html)

-- Extract text from existing PDF
create reader.make
if reader.is_available then
    text := reader.extract_text ("document.pdf")
end

-- Check engine availability
create engines
print (engines.report)
```

### Engine Report Output

```
PDF Engine Availability Report
=============================

wkhtmltopdf: AVAILABLE (D:\prod\simple_pdf/bin/wkhtmltopdf.exe)
Chrome/Edge: AVAILABLE (C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe)

Default engine: wkhtmltopdf
```

---

## Gotchas and Lessons Learned

These are valuable for any Eiffel developer working with external processes:

### 1. PATH_NAME is Deferred

```eiffel
-- WRONG: Cannot instantiate PATH_NAME
create l_path.make_from_string ("bin/tool.exe")  -- Compile error!

-- RIGHT: Use EXECUTION_ENVIRONMENT
create l_env
l_cwd := l_env.current_working_path.name.to_string_8
```

### 2. PROCESS_FACTORY Needs Absolute Paths

Relative paths like `bin/wkhtmltopdf.exe` work for file existence checks but fail when launching processes:

```eiffel
-- Convert relative to absolute for reliable process launching
if l_path.starts_with ("C:") or l_path.starts_with ("/") then
    executable_path := l_path
else
    executable_path := l_cwd + "/" + l_path
end
```

### 3. STRING_32 to STRING Conversion

Environment variables return `READABLE_STRING_32`. Use explicit conversion:

```eiffel
-- Avoid obsolete warnings
if attached l_env.item ("TEMP") as l_temp then
    Result := l_temp.to_string_8  -- Explicit conversion
end
```

### 4. Test App Pattern

Test applications should **NOT** inherit from `EQA_TEST_SET`. Instead:

```eiffel
class MY_TEST_APP
create make
feature
    make
        local
            l_tests: MY_TEST_SET
        do
            create l_tests
            run_test (agent l_tests.test_something, "test_something")
        end

    run_test (a_test: PROCEDURE; a_name: STRING)
        local
            l_retried: BOOLEAN
        do
            if not l_retried then
                a_test.call (Void)
                print ("PASS: " + a_name)
            end
        rescue
            print ("FAIL: " + a_name)
            l_retried := True
            retry
        end
end

class MY_TEST_SET
inherit
    EQA_TEST_SET
feature
    test_something
        do
            assert ("condition", some_condition)
        end
end
```

---

## Final Test Results

```
=== Simple PDF Tests ===

  PASS: test_engine_detection
  PASS: test_wkhtmltopdf_engine_creation
  PASS: test_chrome_engine_creation
  PASS: test_simple_pdf_creation
  PASS: test_document_failed_creation
  PASS: test_reader_creation

--- Integration Tests ---
Test: HTML to PDF - SUCCESS
Test: URL to PDF - SUCCESS
Test: US Constitution PDF - SUCCESS
Test: PDF Text Extraction - SUCCESS

Results: 10 passed, 0 failed
ALL TESTS PASSED
```

---

## Library Contents

```
simple_pdf/
├── simple_pdf.ecf
├── src/
│   ├── core/
│   │   ├── simple_pdf.e           -- Main API
│   │   ├── simple_pdf_document.e  -- Result object
│   │   ├── simple_pdf_engine.e    -- Deferred base
│   │   ├── simple_pdf_engines.e   -- Availability reporter
│   │   └── simple_pdf_reader.e    -- Text extraction
│   └── engines/
│       ├── simple_pdf_wkhtmltopdf.e
│       └── simple_pdf_chrome.e
├── tests/
│   ├── simple_pdf_test_app.e
│   ├── simple_pdf_test_set.e
│   ├── test_set_base.e
│   └── outputs/
│       └── us_constitution.pdf    -- Demo output
└── bin/
    ├── wkhtmltopdf.exe           -- ~40MB
    ├── wkhtmltox.dll             -- ~80MB
    ├── pdftotext.exe             -- Poppler
    └── [Poppler DLLs]            -- ~22MB
```

---

## API Integration

`simple_pdf` is now integrated into the `simple_*` API hierarchy:

```
FOUNDATION_API (core utilities: json, uuid, base64, validation, etc.)
       ↑
SERVICE_API (services: jwt, smtp, sql, cors, cache, websocket, pdf)
       ↑
APP_API (full application stack)
```

### Using via SERVICE_API or APP_API

If your project already uses `simple_service_api` or `simple_app_api`, you automatically have access to `simple_pdf` - no additional ECF entry needed:

```eiffel
class MY_WEB_SERVICE

inherit
    SERVICE_API  -- or APP_API

feature
    generate_report
        local
            pdf: SIMPLE_PDF
            doc: SIMPLE_PDF_DOCUMENT
        do
            create pdf.make
            doc := pdf.from_html (build_report_html)
            if doc.is_valid then
                doc.save_to_file ("report.pdf")
            end
        end
end
```

### Using Standalone

For projects that only need PDF functionality:

1. Clone or reference the repository
2. Set environment variable: `SIMPLE_PDF=D:\path\to\simple_pdf`
3. Add to your ECF:

```xml
<library name="simple_pdf" location="$SIMPLE_PDF/simple_pdf.ecf"/>
```

---

## Conclusion

AI-assisted development allowed us to:

- **Design** a proper multi-engine architecture with deferred classes
- **Implement** 7 classes with full functionality
- **Debug** Eiffel-specific gotchas (PATH_NAME, PROCESS_FACTORY, STRING_32)
- **Test** with 10 automated tests including integration tests
- **Document** gotchas for future reference
- **Ship** a working library to GitHub

All in under 2 hours.

The key was maintaining Eiffel's design principles while leveraging AI for:
- Boilerplate code generation
- Quick iteration on compile errors
- Discovering platform-specific behaviors
- Test infrastructure patterns

The library is now part of the `simple_*` ecosystem and has been integrated into SERVICE_API (and by extension, APP_API) for immediate use in any application.

**Repository:** https://github.com/ljr1981/simple_pdf

---

*This development session was conducted using Claude Code (Anthropic's CLI tool) with Claude Opus 4.5.*
