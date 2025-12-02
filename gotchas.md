# Eiffel Gotchas: Documentation vs. Reality

This file tracks cases where official documentation differs from actual compiler behavior.

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

## Rules

### NEVER Use rescue/retry for Internal Code
- **Rule**: ONLY use `rescue`/`retry` when talking to external systems beyond the current Eiffel project universe (e.g. COM, external C libraries, network calls)
- **Reason**: Eiffel's Design by Contract means preconditions should be satisfied BEFORE calling a feature. If a precondition fails, the caller has a bug - don't mask it with exception handling.
- **Action**: Fix the root cause (satisfy the precondition) instead of catching exceptions
- **Verified**: 2025-11-29

---

## Entries

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
- **Reality**: Assignments require explicit conversion; `string_value()` returns STRING_32
- **Verified**: 2025-11-29, EiffelStudio 24.x
- **Example**:
```eiffel
-- WRONG: Type mismatch (VJAR error)
l_name: STRING_8
l_name := row.string_value ("name")  -- string_value returns STRING_32

-- CORRECT: Explicit conversion
l_name_32: STRING_32
l_name: STRING_8
l_name_32 := row.string_value ("name")
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

### SQLITE_DATABASE Missing Features
- **Docs say**: (assumed) `last_row_id` exists on SQLITE_DATABASE
- **Reality**: `last_row_id` only exists on SQLITE_INSERT_STATEMENT, not SQLITE_DATABASE
- **Verified**: 2025-11-29, EiffelStudio 24.x
- **Example**:
```eiffel
-- WRONG: Feature doesn't exist
Result := internal_db.last_row_id

-- CORRECT: Use SQL query
create l_result.make ("SELECT last_insert_rowid();", internal_db)
if not l_result.rows.is_empty and then attached l_result.rows.first as l_row then
    if attached {INTEGER_64} l_row.item (1) as l_id then
        Result := l_id
    end
end
```

### SIMPLE_SQL_ROW Access Methods
- **Docs say**: (assumed) `integer_value_at(index)` for positional access
- **Reality**: Use `item(index)` for positional access, `integer_value(name)` for named access
- **Verified**: 2025-11-29, EiffelStudio 24.x
- **Example**:
```eiffel
-- WRONG: Feature doesn't exist
Result := l_row.integer_value_at (1)

-- CORRECT: Use item() with type cast
if attached {INTEGER_64} l_row.item (1) as l_count then
    Result := l_count.to_integer_32
end

-- OR use named access if column name is known
Result := l_row.integer_value ("count")
```

### SQLite Statements Require Semicolon Terminator
- **Docs say**: (assumed) SQL strings are passed directly to SQLite
- **Reality**: `SQLITE_MODIFY_STATEMENT.make` and `SQLITE_QUERY_STATEMENT.make` have precondition `a_statement_is_complete` which calls `a_db.is_complete_statement(a_sql)`. SQLite requires SQL to end with `;`
- **Verified**: 2025-11-29, EiffelStudio 24.x
- **Example**:
```eiffel
-- WRONG: Precondition violation (a_statement_is_complete)
create l_statement.make ("INSERT INTO test VALUES (1)", database)

-- CORRECT: Add semicolon
l_sql := "INSERT INTO test VALUES (1)"
if not l_sql.ends_with (";") then
    l_sql.append_character (';')
end
create l_statement.make (l_sql, database)
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

### SQLite Type Conversion in Query Results
- **Docs say**: (assumed) Query results can be cast directly to STRING_32
- **Reality**: SQLite query results need `.out` conversion before type-checking or string operations
- **Verified**: 2025-11-30, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Direct cast fails for SQLite compile options
if attached {STRING_32} ic.item (1) as l_str then
    l_option := l_str.as_upper  -- Never executes!
end

-- CORRECT: Use .out to convert first
if attached ic.item (1) as l_val then
    create l_option.make_from_string (l_val.out)  -- .out converts ANY to string
    l_option.to_upper
end
```

### FTS5 Query Escaping for Apostrophes
- **Docs say**: (SQLite FTS5 docs) Special characters in queries need escaping
- **Reality**: Apostrophes (single quotes) in FTS5 queries need BOTH phrase matching AND SQL escaping
- **Verified**: 2025-11-30, SQLite 3.51.1, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Apostrophe breaks query
fts5.search ("documents", "O'Brien")  -- Fails: tokenizer splits at '

-- CORRECT: Wrap in double quotes for phrase matching, escape apostrophe for SQL
-- Query becomes: MATCH '"O''Brien"'
-- (double quotes for FTS5 phrase, doubled apostrophe for SQL literal)
escaped := escaped_fts_query ("O'Brien")
-- Result: "O''Brien" with phrase matching
```

### SQLite Runtime Linking (C Library Compilation)
- **Docs say**: (Visual Studio) Use /MD for dynamic runtime linking
- **Reality**: Eiffel projects use -NODEFAULTLIB:libc flag, requiring /MT (static runtime) for SQLite C compilation
- **Verified**: 2025-11-30, MSVC 19.44, EiffelStudio 25.02
- **Symptoms**: `unresolved external symbol __imp_strcspn` linker error when using /MD
- **Example**:
```batch
REM WRONG: Dynamic runtime causes linker errors
cl /c /O2 /MD sqlite3.c

REM CORRECT: Static runtime embeds C runtime functions
cl /c /O2 /MT sqlite3.c
```

### EiffelStudio Clean Rebuild for Compile Flag Changes
- **Docs say**: (assumed) Recompiling C files is sufficient
- **Reality**: When SQLite compile flags change (e.g., adding SQLITE_ENABLE_FTS5), must use "Compile from scratch" to clear EIFGENs cache
- **Verified**: 2025-11-30, EiffelStudio 25.02
- **Symptoms**: Tests fail even after recompiling .obj files because EiffelStudio uses cached object files
- **Solution**: Project > Compile from scratch (deletes EIFGENs folder completely)

### Gobo Eiffel Runtime Type Definitions
- **Docs say**: (assumed) EIF_NATURAL is a standard type
- **Reality**: Gobo Eiffel runtime defines specific types (EIF_NATURAL_8/16/32/64) but NOT the generic EIF_NATURAL
- **Verified**: 2025-11-30, Gobo Eiffel gobo-25.09
- **Example**:
```c
// WRONG: Compile error with Gobo runtime
void my_function(EIF_NATURAL value) { ... }  // Error: EIF_NATURAL undeclared

// CORRECT: Add compatibility definition
#ifndef EIF_NATURAL
#define EIF_NATURAL EIF_NATURAL_32
#endif
void my_function(EIF_NATURAL value) { ... }  // Now works with both runtimes
```

### SQLite Statements Must Be Single-Line
- **Docs say**: (assumed) Multi-line SQL strings work normally
- **Reality**: `SQLITE_MODIFY_STATEMENT.make` precondition `a_statement_is_complete` calls `a_db.is_complete_statement(a_sql)` which fails on multi-line SQL
- **Verified**: 2025-12-01, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Multi-line SQL fails precondition
l_sql := "[
    CREATE TABLE IF NOT EXISTS test (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
]"
database.execute (l_sql)  -- Precondition failure!

-- CORRECT: Single-line SQL
l_sql := "CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)"
database.execute (l_sql)  -- Works
```

### Percent Signs in SQL Strings Need Escaping
- **Docs say**: (assumed) SQL strings are passed as-is
- **Reality**: In Eiffel manifest strings, `%` is an escape character. For SQL LIKE patterns with `%`, use `%%`
- **Verified**: 2025-12-01, EiffelStudio 25.02
- **Example**:
```eiffel
-- WRONG: Single percent is escape character
l_sql := "SELECT * FROM users WHERE name LIKE 'John%'"  -- May cause string parsing issues

-- CORRECT: Escape percent signs
l_sql := "SELECT * FROM users WHERE name LIKE 'John%%'"  -- %% becomes single % in SQL
```

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

## Pending Investigation

### Across Loop Item Access
- **Docs say**: Use `ic.item` to access current element
- **User reports**: Needed to remove `.item` in some cases
- **Status**: Needs reproduction and verification
- **Notes**: May depend on collection type, EiffelStudio version, or specific context

**Observation from existing code** (2025-11-29):
In `simple_sql_backup.e`, the code uses `ic` directly as the item:
```eiffel
across l_schema.rows as ic loop
    if attached ic.string_value ("sql") as al_sql then  -- ic used directly, not ic.item
        l_file_db.execute (al_sql)
    end
end
```
This code is in production and apparently compiles. The collection is `ARRAYED_LIST[SIMPLE_SQL_ROW]`.
**Needs compiler verification** to confirm whether `ic` or `ic.item` is correct here.

