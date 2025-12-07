# Eiffel Gotchas: Documentation vs. Reality

This file tracks cases where official Eiffel documentation differs from actual compiler behavior.

**Note**: SQLite/database-specific gotchas are in `sqlite_gotchas.md`

---

## EIFGENs Directory - Hands Off!

**NEVER modify files in EIFGENs** - this is EiffelStudio's workspace exclusively.

- **Read-only for everyone** (human and AI alike)
- Any modifications risk corrupting the build
- Segmentation faults on startup often indicate corrupted EIFGENs
- **Solution for segfaults**: Clean compile (`-clean` flag)

```batch
:: Clean compile to fix corrupted EIFGENs
ec.exe -batch -config project.ecf -target my_target -c_compile -freeze -clean
```

**Verified**: 2025-12-02, EiffelStudio 25.02

---

## Format

Each entry follows this structure:

```
### [Topic]
- **Docs say**: What the documentation claims
- **Reality**: What actually works
- **Verified**: Date and EiffelStudio version
- **Example**: Working code
```

---

## Design Principles

### NEVER Use rescue/retry for Internal Code
- **Rule**: ONLY use `rescue`/`retry` when talking to external systems beyond the current Eiffel project universe (e.g. COM, external C libraries, network calls)
- **Reason**: Eiffel's Design by Contract means preconditions should be satisfied BEFORE calling a feature. If a precondition fails, the caller has a bug - don't mask it with exception handling.
- **Action**: Fix the root cause (satisfy the precondition) instead of catching exceptions
- **Verified**: 2025-11-29

---

## Type System Issues

### VAPE Error - Preconditions Referencing Private Features
- **Docs say**: Preconditions should express contract requirements
- **Reality**: Preconditions CANNOT reference features that aren't exported to clients (VAPE = Violation of Assertion PExport)
- **Verified**: 2025-11-29, EiffelStudio 24.x
- **Example**:
```eiffel
-- WRONG: Causes VAPE error
feature {NONE} -- Implementation
    table_name: STRING_8

feature -- Execution
    execute
        require
            has_table: not table_name.is_empty  -- ERROR: table_name is private!

-- CORRECT: Add public status query
feature -- Status (for preconditions)
    has_table: BOOLEAN
        do
            Result := not table_name.is_empty
        end

feature -- Execution
    execute
        require
            has_table: has_table  -- OK: has_table is public
```

### STRING_32 vs STRING_8 Conversions
- **Docs say**: String types are largely interchangeable
- **Reality**: Assignments require explicit conversion; many features return STRING_32
- **Verified**: 2025-11-29, EiffelStudio 24.x
- **Example**:
```eiffel
-- WRONG: Type mismatch (VJAR error)
l_name: STRING_8
l_name := some_feature_returning_string_32

-- CORRECT: Explicit conversion
l_name_32: STRING_32
l_name: STRING_8
l_name_32 := some_feature_returning_string_32
l_name := l_name_32.to_string_8
```

### Inline If-Then-Else Returns ANY
- **Docs say**: Inline conditionals return typed values
- **Reality**: Inline `if-then-else` expressions return type ANY, causing type mismatches
- **Verified**: 2025-11-29, EiffelStudio 24.x
- **Example**:
```eiffel
-- WRONG: Returns ANY, causes VUAR(2) error when passed to typed parameter
some_feature.make (if condition then "a" else "b" end)

-- CORRECT: Use explicit variable
local
    l_value: STRING_8
do
    if condition then
        l_value := "a"
    else
        l_value := "b"
    end
    some_feature.make (l_value)
```

### Obsolete as_string_8
- **Docs say**: Use `as_string_8` for conversion
- **Reality**: `as_string_8` is obsolete; use `to_string_8` instead
- **Verified**: 2025-11-29, EiffelStudio 24.x
- **Example**:
```eiffel
-- WRONG: Obsolete warning
l_upper := a_name.as_string_8.as_upper

-- CORRECT:
l_upper := a_name.to_string_8.as_upper
```

### Numeric Literal Types (REAL_32 vs REAL_64)
- **Docs say**: (assumed) Floating point literals are REAL_64
- **Reality**: Literals like `3.14` may be stored as REAL_32 when passed through ANY. When checking types with `attached {REAL_64}`, REAL_32 values won't match.
- **Verified**: 2025-11-29, EiffelStudio 24.x
- **Example**:
```eiffel
-- WRONG: Only handles REAL_64
if attached {REAL_64} a_value as l_real then
    Result := l_real.out
else
    Result := "NULL"  -- REAL_32 falls through here!
end

-- CORRECT: Handle both REAL types
if attached {REAL_64} a_value as l_real then
    Result := l_real.out
elseif attached {REAL_32} a_value as l_real32 then
    Result := l_real32.out
else
    Result := "NULL"
end
```

---

## String Handling

### Percent Signs in Manifest Strings Need Escaping
- **Docs say**: (assumed) Strings are passed as-is
- **Reality**: In Eiffel manifest strings, `%` is an escape character. For literal `%`, use `%%`
- **Verified**: 2025-12-01, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Single percent is escape character
l_sql := "SELECT * FROM users WHERE name LIKE 'John%'"  -- May cause string parsing issues

-- CORRECT: Escape percent signs
l_sql := "SELECT * FROM users WHERE name LIKE 'John%%'"  -- %% becomes single % in output
```

---

## Documentation Features

### EIS (Eiffel Information System) Annotations
- **Docs say**: Limited documentation available on Eiffel.org
- **Reality**: EIS provides bidirectional linking between Eiffel source and external documentation
- **Verified**: 2025-12-01, EiffelStudio 25.02
- **Key Points**:
  - Outgoing links (source → docs): Add `note EIS:` annotations to class header
  - Incoming links (docs → source): Use `eiffel:?class=...&feature=...` URI scheme
  - Protocol must be "URI" for HTML files, "pdf" for PDFs
  - Path is relative from the .e file location
- **Example**:
```eiffel
-- In Eiffel source (outgoing):
note
    description: "My class"
    EIS: "name=API Reference", "src=../docs/api/myclass.html", "protocol=URI", "tag=documentation"
    EIS: "name=Tutorial", "src=../docs/tutorial.html", "protocol=URI", "tag=tutorial"

-- In HTML documentation (incoming):
<a href="eiffel:?class=MY_CLASS&feature=my_feature">View in EiffelStudio</a>
<a href="eiffel:?class=MY_CLASS">View class</a>
```
- **Usage**: Press F1 in EiffelStudio on a class with EIS annotations to open linked documentation

---

## WSF/EWF Library Issues

### WGI_INPUT_STREAM.read_string is a Procedure
- **Docs say**: (expected) Functions return values directly
- **Reality**: `read_string(n)` is a PROCEDURE that populates `last_string` attribute
- **Verified**: 2025-12-02, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Treating read_string as a function
l_body := wsf_request.input.read_string (content_length)  -- ERROR

-- CORRECT: Call procedure, then access attribute
wsf_request.input.read_string (content_length)
l_body := wsf_request.input.last_string
```

### WSF_VALUE.string_representation Returns READABLE_STRING_32
- **Docs say**: (not documented)
- **Reality**: Use `string_representation` directly, not `as_string.to_string_32`
- **Verified**: 2025-12-02, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: as_string returns WSF_STRING, not a string
Result := l_param.as_string.to_string_32  -- ERROR

-- CORRECT: Use string_representation directly
Result := l_param.string_representation.to_string_32
```

### ECF Environment Variable References
- **Docs say**: (limited documentation)
- **Reality**: Use `$ENV_VAR` syntax in ECF location attributes; avoid hard-coded paths
- **Verified**: 2025-12-02, EiffelStudio 25.02
- **Example**:
```xml
<!-- WRONG: Hard-coded path -->
<library name="framework" location="D:\prod\framework\framework.ecf"/>

<!-- CORRECT: Environment variable reference -->
<library name="framework" location="$FRAMEWORK\framework.ecf"/>
```
- **Setup**: Set environment variables at User level via PowerShell:
```powershell
[System.Environment]::SetEnvironmentVariable('FRAMEWORK', 'D:\prod\framework', 'User')
```

### ECF UUID Must Be Unique - Never Use Fake/Sequential UUIDs
- **Docs say**: ECF system element has uuid attribute
- **Reality**: EiffelStudio uses UUIDs to identify libraries. If two libraries share the same UUID (or similar fake UUIDs), EiffelStudio gets confused and loads the wrong classes from the wrong library!
- **Verified**: 2025-12-07, EiffelStudio 25.02
- **Symptom**: Library shows wrong classes (e.g., validation classes when you expect XML classes) when used as a dependency
- **Example**:
```xml
<!-- WRONG: Fake/sequential UUID that will collide with other libraries -->
<system ... uuid="A1B2C3D4-E5F6-7890-ABCD-EF1234567890" ...>

<!-- WRONG: Incrementing last digit doesn't help if base pattern is reused -->
<system ... uuid="A1B2C3D4-E5F6-7890-ABCD-EF1234567891" ...>

<!-- CORRECT: Generate a real unique UUID -->
<system ... uuid="f8a3b1c2-4d5e-6f7a-8b9c-0d1e2f3a4b5c" ...>
```
- **Fix**: Generate a real UUID using PowerShell:
```powershell
[guid]::NewGuid().ToString()
```
- **AI Note**: This is a common AI code generation mistake - generating plausible-looking but non-unique UUIDs. Always generate fresh UUIDs for each new ECF file.

### Attribution for Reused Design Ideas
- **Rule**: When borrowing design patterns or API ideas from other Eiffel libraries (void-safe or not), provide attribution
- **Where to Attribute**:
  - In the class note section
  - In README.md
  - In docs/index.html
- **Format**: Include library name, author if known, and what was borrowed
- **Example**:
```eiffel
note
    description: "[
        Simple DateTime - High-level date/time API.

        Design influenced by:
        - Eiffel Loop (Finnian Reilly) - EL_DATE_TEXT localization patterns
        - Pylon library - multiple format output (to_iso, to_european, to_rfc)
        - ISO8601 library (Thomas Beale) - validation before conversion pattern
        ]"
```
- **Why**: Respects original authors, helps others find source material, documents design decisions

---

## Test Framework

### Use TEST_SET_BASE, Not EQA_TEST_SET
- **Docs say**: Inherit from `EQA_TEST_SET` for test classes
- **Reality**: Use `TEST_SET_BASE` from testing_ext library for consistent assertions and helpers
- **Verified**: 2025-12-02, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Standard EQA test set
class MY_TEST
inherit
    EQA_TEST_SET

-- CORRECT: Extended test set with helpers
class MY_TEST
inherit
    TEST_SET_BASE
```

### Always Use Test Target for Compiling and Running Tests
- **Docs say**: (operational knowledge)
- **Reality**: Always compile using the test target (e.g., `my_project_tests`) for both compilation AND test execution. This ensures tests are included in the build.
- **Verified**: 2025-12-07, EiffelStudio 25.02
- **Example**:
```batch
:: CORRECT: Compile test target
ec.exe -batch -config my_project.ecf -target my_project_tests -c_compile

:: WRONG: Compiling main target then trying to run tests
ec.exe -batch -config my_project.ecf -target my_project -c_compile
```
- **Benefit**: Saves time and tokens by not having to compile twice

### ECF Test Target Configuration
- **Docs say**: (limited documentation on AutoTest configuration)
- **Reality**: Test targets need a simple root class; EQA_EVALUATOR is frozen and cannot be inherited
- **Verified**: 2025-12-05, EiffelStudio 25.02
- **Complete Setup**:

1. **ECF Target Configuration**:
```xml
<target name="my_project_tests" extends="my_project">
    <root class="MY_TEST_APP" feature="make"/>
    <library name="testing" location="$ISE_LIBRARY\library\testing\testing.ecf"/>
    <library name="testing_ext" location="$TESTING_EXT\testing_ext.ecf"/>
    <cluster name="tests" location=".\tests\" recursive="true"/>
</target>
```

2. **Root Class (MY_TEST_APP.e)** - Just a placeholder, AutoTest handles discovery:
```eiffel
class MY_TEST_APP
create
    make
feature -- Initialization
    make
        do
            do_nothing
        end
end
```

3. **Test Set Classes** - Inherit from TEST_SET_BASE:
```eiffel
class MY_FEATURE_TEST_SET
inherit
    TEST_SET_BASE
feature -- Tests
    test_something
        do
            assert ("description", some_condition)
        end
end
```

- **Key Points**:
  - Root class is just for compilation; AutoTest discovers test_* features automatically
  - Do NOT inherit from EQA_EVALUATOR (frozen class error)
  - Do NOT use `all_classes="true"` as root - need explicit class
  - Test features must start with `test_` prefix

### Percent Signs in Test Assertions
- **Docs say**: (not documented)
- **Reality**: Percent signs in manifest strings must be escaped as `%%`
- **Verified**: 2025-12-05, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Syntax error "incomplete string: missing final quote"
assert ("has_percent", l_html.has_substring ("41%"))

-- CORRECT: Escape the percent sign
assert ("has_percent", l_html.has_substring ("41%%"))
```

---

## Windows Command Execution

### SIMPLE_PROCESS_HELPER and Environment Variables
- **Docs say**: (internal) Pass command line to `output_of_command`
- **Reality**: The helper splits by spaces, breaking `VAR="value" command` syntax
- **Verified**: 2025-12-02, EiffelStudio 25.02
- **Solution**: Wrap in `cmd /c "set VAR=value && command"` pattern
- **Example**:
```eiffel
-- WRONG: Split by space breaks this
l_cmd := "SIMPLE_JSON=%"D:\prod\simple_json%" ec.exe -batch ..."

-- CORRECT: Use cmd /c with set commands
l_cmd := "cmd /c %"set SIMPLE_JSON=D:\prod\simple_json && ec.exe -batch ...%""
```

### Working Directory for External Processes
- **Docs say**: (not documented)
- **Reality**: Pass directory as second parameter to `output_of_command`
- **Verified**: 2025-12-02, EiffelStudio 25.02
- **Example**:
```eiffel
-- Run ec.exe in project directory so EIFGENs is created there
l_output := process_helper.output_of_command (l_cmd, project_directory)
```

---

## Collection Equality

### ARRAYED_LIST.has Uses Reference Equality
- **Docs say**: (expected) `has` checks if item is in list
- **Reality**: `has` uses `=` (reference equality), not `~` (value equality)
- **Verified**: 2025-12-02, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Uses reference equality - won't find equal string
if l_origins.has ("https://example.com") then ...

-- CORRECT: Use across with value equality operator
if across l_origins as ic some ic ~ "https://example.com" end then ...

-- Or create a helper function
has_origin (a_list: ARRAYED_LIST [STRING]; a_origin: STRING): BOOLEAN
    do
        Result := across a_list as ic some ic ~ a_origin end
    end
```

### HASH_TABLE Iteration: key_for_iteration Inside across Loop
- **Docs say**: (expected) `across` loop works uniformly for all collections
- **Reality**: `across` loop creates a separate cursor; internal cursor methods like `key_for_iteration` use a DIFFERENT cursor
- **Verified**: 2025-12-03, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: key_for_iteration uses internal cursor, not across cursor
across my_table as ic loop
    print (my_table.key_for_iteration)  -- PRECONDITION VIOLATION: not_off
end

-- CORRECT: Use from/until/loop with proper cursor methods
from my_table.start until my_table.after loop
    print (my_table.key_for_iteration)  -- OK
    print (my_table.item_for_iteration) -- OK
    my_table.forth
end
```

---

## Agent Limitations

### Inline Agents Cannot Access Local Variables
- **Docs say**: (not clear)
- **Reality**: Inline agents cannot capture or modify local variables
- **Verified**: 2025-12-02, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Inline agent can't access l_executed
local
    l_executed: BOOLEAN
do
    l_pipeline.execute (request, response, agent do l_executed := True end)
    assert (l_executed)

-- CORRECT: Use class attribute and named agent
feature {NONE} -- Test state
    handler_executed: BOOLEAN

    mark_handler_executed
        do
            handler_executed := True
        end

feature -- Test
    test_pipeline
        do
            handler_executed := False
            l_pipeline.execute (request, response, agent mark_handler_executed)
            assert (handler_executed)
        end
```

---

## Multiple Inheritance

### VDUS(3) - Cannot Undefine Deferred Features
- **Docs say**: Use `undefine` to resolve inheritance conflicts
- **Reality**: `undefine` converts effective → deferred, NOT the reverse. You cannot undefine an already-deferred feature.
- **Verified**: 2025-12-03, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: render_canvas is already deferred in GDS_HTML_RENDERER
class GUI_DESIGNER_SERVER
inherit
    GDS_HTMX_HANDLERS
        undefine
            render_canvas  -- ERROR: VDUS(3) - feature is deferred!
        end
    GDS_HTML_RENDERER

-- CORRECT: Just inherit both - feature joining handles it automatically
class GUI_DESIGNER_SERVER
inherit
    GDS_HTMX_HANDLERS
    GDS_HTML_RENDERER
    -- Eiffel joins the deferred features automatically
```

### Feature Joining Rules
- **Deferred + Deferred**: Single deferred feature (one implementation needed)
- **Deferred + Effective**: Effective satisfies deferred (automatic, no clause needed)
- **Effective + Effective**: Conflict - must use `rename`, `undefine`, or `select`

---

## Contract Completeness (The "True but Incomplete" Problem)

### Contracts Can Be Correct Yet Insufficient
- **Docs say**: Write postconditions to specify what a feature guarantees
- **Reality**: A postcondition can be *true* but *incomplete*, passing verification while missing important guarantees
- **Source**: Meyer, "AI for software engineering: from probable to provable" (CACM 2025)
- **Verified**: 2025-12-03

**Why This Matters for AI-Generated Code:**
AI produces "statistically likely" contracts. These are often true but may miss edge cases or fail to capture full behavior. Human review for completeness is essential.

**Example - Incomplete Contract:**
```eiffel
add_item (a_item: STRING)
    require
      item_not_void: a_item /= Void
    do
      items.extend (a_item)
    ensure
      has_item: items.has (a_item)  -- TRUE but INCOMPLETE!
    end
```

**What's Missing:**
```eiffel
    ensure
      has_item: items.has (a_item)
      count_increased: items.count = old items.count + 1
      at_end: items.last ~ a_item
      others_unchanged: across 1 |..| (old items.count) as i all
                          items[i] ~ (old items.twin)[i]
                        end
```

**Common Incomplete Patterns:**

| Operation | Incomplete | Complete Addition |
|-----------|------------|-------------------|
| Add to collection | `has (item)` | `count = old count + 1` |
| Remove from collection | `not has (item)` | `count = old count - 1` |
| Set attribute | `attr = value` | `old other_attr = other_attr` (unchanged) |
| Clear collection | `is_empty` | `count = 0` |
| Search | `Result /= Void implies has (Result)` | `Result = Void implies not has (target)` |

**Defense Strategy:**
1. After writing postcondition, ask: "What ELSE is guaranteed?"
2. For state changes, explicitly state what did NOT change
3. For counts, always specify old vs new relationship
4. Use Specification Hat workflow (contracts before code)

**Reference**: See `contract_patterns.md` for systematic patterns

---

## HTML Generation

### simple_htmx escape_html Breaks JavaScript in Attributes
- **Docs say**: Attribute values are properly escaped for HTML
- **Reality**: `escape_html` escapes `<`, `>`, `&`, `"` which breaks JavaScript in Alpine.js attributes
- **Verified**: 2025-12-03, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Arrow functions get escaped
l_div.x_data ("{ init() { items = [] } }")  -- OK
l_div.x_init ("$watch('value', v => console.log(v))")  -- BROKEN: => becomes &gt;

-- Also broken:
l_div.x_show ("count > 5")       -- > becomes &gt;
l_div.x_if ("a && b")            -- && becomes &amp;&amp;

-- CORRECT: Avoid arrow functions, use alternative patterns
l_div.x_effect ("console.log(value)")  -- Use x-effect instead of $watch with arrow
l_div.x_show ("count >= 5")            -- Rewrite comparisons where possible
```
- **Workaround**: Avoid arrow functions (`=>`), logical AND (`&&`), and comparisons with `<` or `>` in Alpine attribute values. Use `x_effect` instead of `$watch` with callbacks.
- **Future fix**: Add `attr_raw` method to simple_htmx for unescaped attribute values.

---

## Named Tuple Field Access in Across Loops

### Cannot Access Named Tuple Fields via across Cursor
- **Docs say**: (expected) Tuples with named fields can be accessed via dot notation
- **Reality**: Named tuple field access (`tuple.field_name`) doesn't work when iterating with `across` loops
- **Verified**: 2025-12-04, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: VUAR(1) error - wrong number of actual arguments
pages: ARRAY [TUPLE [title: STRING; url: STRING; description: STRING]]
...
across pages as page loop
    -- Cannot access: page.item.title, page.item.url, page.item.description
    l_menu.add_item (page.item.title, page.item.url)  -- ERROR!
end

-- CORRECT: Use parallel arrays instead
page_titles: ARRAY [STRING]
    once Result := <<"Home", "About", "Contact">> end

page_urls: ARRAY [STRING]
    once Result := <<"/", "/about", "/contact">> end

feature -- Generation
    from i := 1 until i > page_count loop
        l_menu.add_item (page_titles[i], page_urls[i])
        i := i + 1
    end
```
- **Alternative**: Use explicit local variables with positional tuple access `page.item.item_1` if needed

---

## Custom Scroll Containers (Alpine.js / JavaScript)

### window.scrollY Doesn't Track Custom Scroll Containers
- **Docs say**: (Alpine.js/JavaScript general knowledge) `window.scrollY` tracks page scroll position
- **Reality**: When using CSS `overflow-y: scroll` on a container (e.g., snap scrolling), `window.scrollY` remains 0. Must track container scroll directly.
- **Verified**: 2025-12-04
- **Example**:
```javascript
// WRONG: Always returns 0 when custom container handles scrolling
x-init="window.addEventListener('scroll', () => { visible = window.scrollY > 100 })"

// CORRECT: Detect and listen to the scroll container
x-init="
  const container = document.querySelector('.snap-container');
  if (container) {
    container.addEventListener('scroll', () => { visible = container.scrollTop > 100 });
  } else {
    window.addEventListener('scroll', () => { visible = window.scrollY > 100 });
  }"
```
- **Common Containers**: `.snap-container`, modal overlays, custom scroll areas

---

## Citation and URL Verification

### AI-Generated URLs May Be Hallucinated
- **Reality**: AI models can generate plausible-looking URLs that don't exist. Always verify external links.
- **Verified**: 2025-12-04
- **Examples of Hallucinated URLs** (all returned 404):
  - `uplevelteam.com/blog/copilot-code-quality-study` → Should be `ai-for-developer-productivity`
  - `veracode.com/state-of-software-security-report` → Should be `blog/ai-generated-code-security-risks/`
  - `answer.ai/posts/2024-09-10-devin-benchmark.html` → Should be `2025-01-08-devin.html`
  - `apiiro.com/blog/ai-generated-code-security-risks/` → Should be `4x-velocity-10x-vulnerabilities...`
- **Defense**:
  1. Test all external links before committing
  2. Use WebFetch or curl to verify URLs return 200
  3. When citing research, verify the actual URL from the source website

---

## Process Launching

### PATH_NAME is Deferred - Cannot Instantiate
- **Docs say**: PATH_NAME provides path manipulation features
- **Reality**: PATH_NAME is deferred and cannot be created directly with `create`
- **Verified**: 2025-12-07, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: VGCC(2) error - PATH_NAME is deferred
l_path_name: PATH_NAME
create l_path_name.make_from_string (l_path)

-- CORRECT: Use EXECUTION_ENVIRONMENT for current working directory
l_env: EXECUTION_ENVIRONMENT
l_cwd: STRING
create l_env
l_cwd := l_env.current_working_path.name.to_string_8
```

### Relative Paths Don't Work for PROCESS_FACTORY Launches
- **Docs say**: (not documented)
- **Reality**: When using PROCESS_FACTORY to launch executables, relative paths like "bin/tool.exe" will fail if the working directory changes (e.g., tests run from EIFGENs folder)
- **Verified**: 2025-12-07, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Relative path works for exists check but not for launch
l_candidates.extend ("bin/wkhtmltopdf.exe")
...
if l_file.exists then
    executable_path := l_path  -- Relative path fails at launch time
end

-- CORRECT: Convert to absolute path
l_env: EXECUTION_ENVIRONMENT
l_cwd: STRING
create l_env
l_cwd := l_env.current_working_path.name.to_string_8
...
if l_file.exists then
    if l_path.starts_with ("C:") or l_path.starts_with ("/") then
        executable_path := l_path
    else
        executable_path := l_cwd + "/" + l_path
    end
end
```

### Environment Variable Returns STRING_32
- **Docs say**: (not documented clearly)
- **Reality**: `EXECUTION_ENVIRONMENT.item` returns `READABLE_STRING_32`, not `STRING`. Use `.to_string_8` for conversion.
- **Verified**: 2025-12-07, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Implicit conversion causes obsolete warning
l_env: EXECUTION_ENVIRONMENT
Result: STRING
if attached l_env.item ("TEMP") as l_temp then
    Result := l_temp  -- Obsolete as_string_8 warning

-- CORRECT: Explicit conversion
if attached l_env.item ("TEMP") as l_temp then
    Result := l_temp.to_string_8
```

---

## Test App Patterns

### Test Apps Should NOT Inherit from EQA_TEST_SET
- **Docs say**: (common pattern) Test classes inherit from EQA_TEST_SET
- **Reality**: Test *app* classes (root class for test target) should NOT inherit from TEST_SET_BASE/EQA_TEST_SET. Only test *set* classes should inherit.
- **Verified**: 2025-12-07, EiffelStudio 25.02
- **Reason**: EQA_TEST_SET has attributes (file_system, environment) that need initialization. A standalone test runner doesn't need this inheritance.
- **Example**:
```eiffel
-- WRONG: Test app inherits from test base
class MY_TEST_APP
inherit
    TEST_SET_BASE  -- ERROR: Uninitialized attributes
create
    make
...

-- CORRECT: Separate app from test set
class MY_TEST_APP
create
    make
feature
    make
        local
            l_tests: MY_TEST_SET
        do
            create l_tests
            run_test (agent l_tests.test_something, "test_something")
        end

class MY_TEST_SET
inherit
    TEST_SET_BASE
feature
    test_something
        do
            assert ("test", condition)
        end
```

---

## Gobo Library Issues

### DS_LIST Requires Cursor-Based Iteration
- **Docs say**: (expected) All list types support `across` iteration
- **Reality**: Gobo's DS_LIST and DS_LINEAR_CURSOR don't support `across` syntax - must use cursor-based from/until/loop
- **Verified**: 2025-12-07, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: across doesn't work with DS_LIST
l_attrs: DS_LIST [XM_ATTRIBUTE]
across l_attrs as ic loop ... end  -- Compilation error

-- CORRECT: Use cursor-based iteration
l_cursor: DS_LINEAR_CURSOR [XM_ATTRIBUTE]
l_cursor := l_attrs.new_cursor
from l_cursor.start until l_cursor.after loop
    print (l_cursor.item.name)
    l_cursor.forth
end
```

### HASH_TABLE across Key Access with @
- **Docs say**: (not clearly documented)
- **Reality**: In `across table as ic` loop, `ic` gives the VALUE directly. For the KEY, use `@ic.key`
- **Verified**: 2025-12-07, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: ic.key doesn't exist
l_table: HASH_TABLE [STRING, STRING]
across l_table as ic loop
    print (ic.key)   -- ERROR: VEEN - unknown identifier 'key'
    print (ic.item)  -- ERROR: trying to call 'item' on STRING
end

-- CORRECT: Use @ prefix for key access
across l_table as ic loop
    print (@ic.key)  -- The key (STRING)
    print (ic)       -- The value (STRING) - ic IS the value
end
```

### ARRAYED_LIST across Gives Item Directly
- **Docs say**: (expected) across cursor has .item accessor
- **Reality**: For ARRAYED_LIST in `across list as ic`, `ic` IS the item directly, not `ic.item`
- **Verified**: 2025-12-07, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: ic.item on ARRAYED_LIST
l_items: ARRAYED_LIST [XM_CHARACTER_DATA]
across l_items as ic loop
    xm_element.delete (ic.item)  -- ERROR: ic IS the item, not ic.item
end

-- CORRECT: ic is the item
across l_items as ic loop
    xm_element.delete (ic)  -- ic IS the XM_CHARACTER_DATA directly
end
```

### VOIT(2) - Loop Variable Conflicts with Feature Name
- **Docs say**: Loop variables follow normal identifier rules
- **Reality**: Loop variable in `across` cannot have the same name as a feature in the class (VOIT(2) = Variable Of ITeration)
- **Verified**: 2025-12-07, EiffelStudio 25.02
- **Example**:
```eiffel
class MY_CLASS
feature
    attr (a_name: STRING): STRING  -- Feature named 'attr'

    element_to_string: STRING
        local
            l_attrs: HASH_TABLE [STRING, STRING]
        do
            -- WRONG: 'attr' conflicts with feature name
            across l_attrs as attr loop ... end  -- ERROR: VOIT(2)

            -- CORRECT: Use different name
            across l_attrs as ic_attr loop ... end  -- OK
        end
```

---

## Pending Investigation

### Across Loop Item Access
- **Status**: RESOLVED - see `across_loops.md`
- **Summary**: Whether you use `ic` or `ic.item` depends on the iteration cursor type. For ARRAYED_LIST, the cursor IS the item. For HASH_TABLE, use `ic.item` for value.
