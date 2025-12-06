# Eiffel Library Simplification Roadmap

**Created:** December 6, 2025
**Purpose:** Strategic plan for creating simple_* facades over EiffelStudio standard libraries

---

## Philosophy

The simple_* library pattern:
1. **Facade over existing** - Don't reinvent, wrap EiffelStudio libraries
2. **Cleaner API** - One-liners for common operations
3. **Sensible defaults** - Works out of the box
4. **Design by Contract** - Clear preconditions/postconditions
5. **Fold into API layer** - FOUNDATION_API or SERVICE_API

---

## Completed Libraries

| Library | Wraps/Replaces | API Layer | Status |
|---------|---------------|-----------|--------|
| simple_base64 | Custom impl | FOUNDATION | Done |
| simple_hash | Custom impl (SHA, HMAC) | FOUNDATION | Done |
| simple_uuid | UUID_GENERATOR | FOUNDATION | Done |
| simple_json | JSON_* classes | FOUNDATION | Done |
| simple_csv | Custom impl | FOUNDATION | Done |
| simple_markdown | Custom impl | FOUNDATION | Done |
| simple_validation | Custom impl | FOUNDATION | Done |
| simple_process | PROCESS | FOUNDATION | Done |
| simple_randomizer | RANDOM | FOUNDATION | Done |
| simple_web | EiffelNet/EWF | APP | Done |
| simple_websocket | Custom impl | SERVICE | Done |
| simple_jwt | Custom impl | SERVICE | Done |
| simple_smtp | Custom impl | SERVICE | Done |
| simple_cors | Custom impl | SERVICE | Done |
| simple_rate_limiter | Custom impl | SERVICE | Done |
| simple_template | Custom impl | SERVICE | Done |
| simple_sql | SQLite wrapper | SERVICE | Done |

---

## In Progress (Christmas Sprint Victory Lap)

| Library | Wraps/Enhances | API Layer | Status |
|---------|---------------|-----------|--------|
| simple_logger | LOG_LOGGING_FACILITY | FOUNDATION | Done |
| simple_cache | Custom LRU impl | SERVICE | Done |

---

## Future Candidates

### Tier 1: High Value (January 2026)

#### simple_xml
**Wraps:** XML_STANDARD_PARSER, XML_DOCUMENT, XM_* classes
**Pain Points:** Verbose parsing, complex navigation, attribute handling
**Target API:**
```eiffel
-- Parsing
xml := api.foundation.parse_xml ("<root><item id='1'>value</item></root>")
xml := api.foundation.parse_xml_file ("config.xml")

-- Navigation (XPath-lite)
value := xml.text_at ("root/item")
attr := xml.attribute_at ("root/item", "id")
items := xml.elements_at ("root/items/item")

-- Building
xml := api.foundation.new_xml ("root")
xml.add_element ("item", "value")
xml.add_attribute ("item", "id", "1")
output := xml.to_string

-- Convenience
config := api.foundation.xml_to_hash ("config.xml")  -- Flat key-value
```
**Complexity:** 1 week
**Priority:** High - XML configs and data exchange are everywhere

---

#### simple_datetime
**Wraps:** DATE, TIME, DATE_TIME, DATE_TIME_DURATION
**Pain Points:** Verbose creation, formatting, parsing, arithmetic
**Target API:**
```eiffel
-- Current time
now := api.foundation.now
today := api.foundation.today

-- Creation
dt := api.foundation.date (2025, 12, 25)
dt := api.foundation.datetime (2025, 12, 25, 14, 30, 0)

-- Parsing
dt := api.foundation.parse_date ("2025-12-06", "YYYY-MM-DD")
dt := api.foundation.parse_iso8601 ("2025-12-06T14:30:00Z")

-- Formatting
s := api.foundation.format_date (dt, "YYYY-MM-DD")
s := api.foundation.format_datetime (dt, "YYYY-MM-DD HH:mm:ss")
s := dt.to_iso8601

-- Arithmetic
next_week := dt.plus_days (7)
last_month := dt.minus_months (1)
tomorrow := api.foundation.tomorrow

-- Comparison
days := api.foundation.days_between (start_date, end_date)
is_past := dt.is_before (api.foundation.now)
is_weekend := dt.is_weekend
```
**Complexity:** 3-4 days
**Priority:** High - Date handling is constant need

---

#### simple_file
**Wraps:** FILE, PLAIN_TEXT_FILE, RAW_FILE, PATH, DIRECTORY
**Pain Points:** Open/close boilerplate, path handling, directory operations
**Target API:**
```eiffel
-- Reading
content := api.foundation.read_file ("config.txt")
lines := api.foundation.read_lines ("data.txt")
bytes := api.foundation.read_binary ("image.png")

-- Writing
api.foundation.write_file ("output.txt", content)
api.foundation.append_file ("log.txt", line)
api.foundation.write_binary ("output.bin", bytes)

-- Existence/Info
exists := api.foundation.file_exists ("config.txt")
size := api.foundation.file_size ("data.bin")
modified := api.foundation.file_modified_time ("file.txt")

-- Directory
files := api.foundation.list_files ("src")
files := api.foundation.glob ("src/**/*.e")
api.foundation.create_directory ("output/reports")
api.foundation.delete_file ("temp.txt")

-- Path utilities
name := api.foundation.file_name ("/path/to/file.txt")  -- "file.txt"
ext := api.foundation.file_extension ("file.txt")  -- "txt"
dir := api.foundation.parent_directory ("/path/to/file.txt")  -- "/path/to"
full := api.foundation.join_path ("dir", "subdir", "file.txt")
```
**Complexity:** 3-4 days
**Priority:** High - File operations are everywhere

---

### Tier 2: Medium Value (February 2026)

#### simple_regex
**Wraps:** RX_PCRE_REGULAR_EXPRESSION (Gobo)
**Pain Points:** Verbose setup, compile check, match extraction
**Target API:**
```eiffel
-- Simple matching
if api.foundation.matches (email, "^[a-z]+@[a-z]+\.[a-z]+$") then

-- Extraction
groups := api.foundation.extract ("log-2025-12-06.txt", "log-(\d+)-(\d+)-(\d+)")
-- groups.item (1) = "2025", groups.item (2) = "12", groups.item (3) = "06"

-- Find all
matches := api.foundation.find_all (text, "\b\w+@\w+\.\w+\b")

-- Replacement
result := api.foundation.replace (text, "\s+", " ")
result := api.foundation.replace_all (text, "old", "new")

-- Split
parts := api.foundation.split_regex (csv_line, ",\s*")

-- Pre-compiled (for loops)
regex := api.foundation.compile_regex ("pattern")
if regex.matches (text) then
    first_group := regex.group (1)
end
```
**Complexity:** 3-4 days
**Priority:** Medium - Useful but less common than file/date

---

#### simple_http_client
**Wraps:** Enhances simple_web for client-side HTTP
**Pain Points:** Request building, response parsing, error handling
**Target API:**
```eiffel
-- Simple GET
response := api.app.http_get ("https://api.example.com/users")
json := response.json

-- POST with JSON body
response := api.app.http_post ("https://api.example.com/users", user_json)

-- With headers
response := api.app.http_get_with_headers (url, headers)

-- Builder pattern
response := api.app.new_request
    .url ("https://api.example.com/users")
    .method_post
    .header ("Authorization", "Bearer " + token)
    .json_body (data)
    .timeout (30)
    .execute
```
**Complexity:** 3-4 days
**Priority:** Medium - API consumption is common

---

### Tier 3: Lower Priority (Q2 2026)

#### simple_crypto
**Wraps:** EiffelStudio encryption library
**Adds:** AES encryption, RSA, key generation
**Complexity:** 1-2 weeks
**Priority:** Lower - Security-sensitive, needs careful implementation

#### simple_zip
**Wraps:** Compression libraries
**Target:** ZIP/GZIP compress/decompress
**Complexity:** 1 week
**Priority:** Lower - Occasional need

#### simple_image
**Wraps:** Would need external library (ImageMagick?)
**Target:** Resize, crop, format conversion
**Complexity:** 2-3 weeks
**Priority:** Lower - Specialized use case

---

## Decision Framework
## Design by Contract Guidelines

### Postconditions Should Bubble Up to Invariants (Eric's Rule)

When creation procedures establish postconditions, ask: "Is this always true for the lifetime of the object?"

**If YES** → Make it an invariant
**If NO** → Keep as postcondition only

#### Examples:

**SIMPLE_CACHE `make` establishes:**
```eiffel
ensure
    max_size_set: max_size = a_max_size    -- Specific value, not invariant-worthy
    initially_empty: count = 0              -- Initial state only, not invariant
```
**Becomes invariant:**
```eiffel
invariant
    valid_max_size: max_size > 0           -- Always true after any creation
    count_within_limit: count <= max_size  -- Always maintained
```

**SIMPLE_LOGGER `make` establishes:**
```eiffel
ensure
    level_is_info: level = Level_info      -- Specific default, can change
    outputs_to_console: is_console_output  -- Initial state
```
**Becomes invariant:**
```eiffel
invariant
    valid_level: level >= Level_debug and level <= Level_fatal  -- Always true
    non_negative_indent: indent_level >= 0                       -- Always maintained
```

### Checklist for New Classes

1. List all postconditions from all creation procedures
2. For each, ask: "Can this ever become false?"
3. Generalize specific values to ranges where appropriate
4. Add as invariants with clear naming

---


When considering a new simple_* library, ask:

1. **Frequency** - How often is this functionality needed?
2. **Pain Level** - How verbose/complex is the current API?
3. **Stability** - Is the underlying library stable?
4. **Scope** - Can we meaningfully simplify in < 1 week?
5. **Dependencies** - Does it fit cleanly in FOUNDATION or SERVICE?

---

## API Layer Guidelines

| Layer | Criteria | Examples |
|-------|----------|----------|
| FOUNDATION | No external dependencies, pure utilities | base64, hash, uuid, json, csv, datetime, file, regex |
| SERVICE | Network/database/infrastructure services | jwt, smtp, sql, cache, websocket, cors |
| APP | Application-level concerns, UI integration | alpine, web_client, htmx |

---

## Revision History

| Date | Change |
|------|--------|
| 2025-12-06 | Initial roadmap created |
| 2025-12-06 | Added Design by Contract guidelines (Eric's DbC feedback) |

