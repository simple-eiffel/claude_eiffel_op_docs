# simple_codec Design Document

**Date:** December 10, 2025
**Status:** Draft
**Author:** Larry + Claude

---

## Overview

simple_codec provides a unified API for encoding/decoding structured data across multiple formats (JSON, TOML, YAML, XML). Instead of learning four different APIs, developers use one common interface with format-specific backends.

---

## Problem Statement

Currently:
- simple_json exists for JSON
- simple_xml exists for XML
- No TOML or YAML support
- Each has its own API and data model
- UCF (Universe Configuration Files) need format flexibility

We need:
- Unified data model across all formats
- Single API for parse/write operations
- Easy format conversion
- Extensible for future formats

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    simple_codec                         │
│                   (unified API)                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │              CODEC_VALUE                          │ │
│  │  Universal data model:                            │ │
│  │  - CODEC_OBJECT (key/value pairs)                 │ │
│  │  - CODEC_ARRAY (ordered collection)               │ │
│  │  - CODEC_STRING, CODEC_NUMBER                     │ │
│  │  - CODEC_BOOLEAN, CODEC_NULL                      │ │
│  └───────────────────────────────────────────────────┘ │
│                         │                               │
│         ┌───────────────┼───────────────┐              │
│         ▼               ▼               ▼              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │simple_json │  │simple_toml │  │simple_yaml │       │
│  │  backend   │  │  backend   │  │  backend   │       │
│  └────────────┘  └────────────┘  └────────────┘       │
│         │               │               │              │
│  ┌────────────┐                                        │
│  │simple_xml  │                                        │
│  │  backend   │                                        │
│  └────────────┘                                        │
└─────────────────────────────────────────────────────────┘
```

---

## Library Structure

### simple_codec (main library)
- SIMPLE_CODEC - Facade class, main entry point
- CODEC_VALUE - Abstract base for all values
- CODEC_OBJECT - Key/value container
- CODEC_ARRAY - Ordered collection
- CODEC_STRING - String value
- CODEC_NUMBER - Numeric value (integer or real)
- CODEC_BOOLEAN - True/false
- CODEC_NULL - Null/void value
- CODEC_FORMAT - Enum: json, toml, yaml, xml

### simple_json (existing, becomes backend)
- JSON_CODEC - Implements JSON parsing/writing
- Adapts JSON_OBJECT/JSON_ARRAY to CODEC_VALUE

### simple_toml (new)
- TOML_CODEC - Implements TOML parsing/writing
- TOML tables → CODEC_OBJECT
- TOML arrays → CODEC_ARRAY

### simple_yaml (new)
- YAML_CODEC - Implements YAML parsing/writing
- YAML mappings → CODEC_OBJECT
- YAML sequences → CODEC_ARRAY

### simple_xml (existing, becomes backend)
- XML_CODEC - Implements XML parsing/writing
- Elements → CODEC_OBJECT (with attributes)
- Repeated elements → CODEC_ARRAY

---

## API Design

### Main Entry Point: SIMPLE_CODEC

```eiffel
class SIMPLE_CODEC

feature -- Parsing

    parse_string (a_content: STRING; a_format: CODEC_FORMAT): CODEC_VALUE
            -- Parse string content in specified format
        require
            content_exists: a_content /= Void
            content_not_empty: not a_content.is_empty
        ensure
            result_exists: Result /= Void
        end

    parse_file (a_path: STRING): CODEC_VALUE
            -- Parse file, auto-detect format from extension
        require
            path_exists: a_path /= Void
            file_exists: file_exists (a_path)
        ensure
            result_exists: Result /= Void
        end

    parse_file_as (a_path: STRING; a_format: CODEC_FORMAT): CODEC_VALUE
            -- Parse file in specified format
        require
            path_exists: a_path /= Void
            file_exists: file_exists (a_path)
        ensure
            result_exists: Result /= Void
        end

feature -- Writing

    to_string (a_value: CODEC_VALUE; a_format: CODEC_FORMAT): STRING
            -- Serialize value to string in specified format
        require
            value_exists: a_value /= Void
        ensure
            result_exists: Result /= Void
        end

    to_file (a_value: CODEC_VALUE; a_path: STRING; a_format: CODEC_FORMAT)
            -- Write value to file in specified format
        require
            value_exists: a_value /= Void
            path_exists: a_path /= Void
        end

    to_file_pretty (a_value: CODEC_VALUE; a_path: STRING; a_format: CODEC_FORMAT)
            -- Write value to file with pretty printing
        require
            value_exists: a_value /= Void
            path_exists: a_path /= Void
        end

feature -- Format Detection

    detect_format (a_path: STRING): CODEC_FORMAT
            -- Detect format from file extension
        require
            path_exists: a_path /= Void
        ensure
            valid_format: Result /= Void
        end

feature -- Conversion

    convert (a_value: CODEC_VALUE; a_from, a_to: CODEC_FORMAT): STRING
            -- Convert between formats
        require
            value_exists: a_value /= Void
        ensure
            result_exists: Result /= Void
        end

end
```

### Universal Data Model: CODEC_VALUE

```eiffel
deferred class CODEC_VALUE

feature -- Type Queries

    is_object: BOOLEAN deferred end
    is_array: BOOLEAN deferred end
    is_string: BOOLEAN deferred end
    is_number: BOOLEAN deferred end
    is_boolean: BOOLEAN deferred end
    is_null: BOOLEAN deferred end

feature -- Conversion

    as_object: CODEC_OBJECT
        require
            is_object: is_object
        end

    as_array: CODEC_ARRAY
        require
            is_array: is_array
        end

    as_string: STRING
        require
            is_string: is_string
        end

    as_integer: INTEGER_64
        require
            is_number: is_number
        end

    as_real: REAL_64
        require
            is_number: is_number
        end

    as_boolean: BOOLEAN
        require
            is_boolean: is_boolean
        end

feature -- Navigation (convenience)

    item (a_key: STRING): detachable CODEC_VALUE
            -- Get item by key (for objects)
        require
            is_object: is_object
        end

    item_at (a_index: INTEGER): CODEC_VALUE
            -- Get item by index (for arrays)
        require
            is_array: is_array
            valid_index: a_index >= 1 and a_index <= as_array.count
        end

    string_item (a_key: STRING): STRING
            -- Convenience: get string value by key
        require
            is_object: is_object
            has_key: as_object.has_key (a_key)
            is_string_value: attached as_object.item (a_key) as v and then v.is_string
        end

    integer_item (a_key: STRING): INTEGER_64
            -- Convenience: get integer value by key
        require
            is_object: is_object
            has_key: as_object.has_key (a_key)
            is_number_value: attached as_object.item (a_key) as v and then v.is_number
        end

end
```

### CODEC_OBJECT

```eiffel
class CODEC_OBJECT inherit CODEC_VALUE

feature -- Access

    item (a_key: STRING): detachable CODEC_VALUE
    has_key (a_key: STRING): BOOLEAN
    keys: ARRAYED_LIST [STRING]
    count: INTEGER

feature -- Modification

    put (a_value: CODEC_VALUE; a_key: STRING)
    remove (a_key: STRING)

feature -- Iteration

    new_cursor: ITERATION_CURSOR [TUPLE [key: STRING; value: CODEC_VALUE]]

invariant
    keys_and_values_match: keys.count = count

end
```

### CODEC_ARRAY

```eiffel
class CODEC_ARRAY inherit CODEC_VALUE

feature -- Access

    item_at alias "[]" (a_index: INTEGER): CODEC_VALUE
    count: INTEGER
    is_empty: BOOLEAN

feature -- Modification

    extend (a_value: CODEC_VALUE)
    put_at (a_value: CODEC_VALUE; a_index: INTEGER)
    remove_at (a_index: INTEGER)

feature -- Iteration

    new_cursor: ITERATION_CURSOR [CODEC_VALUE]

invariant
    count_non_negative: count >= 0

end
```

---

## Format-Specific Considerations

### JSON
- Direct mapping to CODEC_VALUE model
- simple_json already exists
- Adapter pattern to wrap JSON_OBJECT/JSON_ARRAY

### TOML
- Tables → CODEC_OBJECT
- Array of Tables → CODEC_ARRAY of CODEC_OBJECT
- Inline tables → CODEC_OBJECT
- Dates/times → CODEC_STRING (ISO 8601)
- Multi-line strings supported

### YAML
- Mappings → CODEC_OBJECT
- Sequences → CODEC_ARRAY
- Anchors/aliases → resolved to actual values
- Multi-document → array of root values

### XML
- Elements → CODEC_OBJECT
- Attributes → special "_attributes" key in object
- Text content → "_text" key
- Repeated elements → CODEC_ARRAY
- Mixed content → requires special handling

---

## Usage Examples

### Basic Parsing

```eiffel
codec: SIMPLE_CODEC
config: CODEC_VALUE

create codec

-- Auto-detect format from extension
config := codec.parse_file ("universe.toml")

-- Or specify format explicitly
config := codec.parse_file_as ("config.txt", {CODEC_FORMAT}.toml)

-- Access data uniformly
if attached config.string_item ("name") as name then
    print ("Universe: " + name)
end
```

### Working with Objects

```eiffel
codec: SIMPLE_CODEC
universe: CODEC_OBJECT
libs: CODEC_ARRAY

create codec
universe := codec.parse_file ("universe.toml").as_object

-- Iterate libraries
if attached universe.item ("libraries") as l and then l.is_array then
    libs := l.as_array
    across libs as lib loop
        if lib.item.is_object then
            print (lib.item.as_object.string_item ("name"))
        end
    end
end
```

### Format Conversion

```eiffel
codec: SIMPLE_CODEC
data: CODEC_VALUE

create codec

-- Read TOML
data := codec.parse_file ("config.toml")

-- Write as JSON
codec.to_file_pretty (data, "config.json", {CODEC_FORMAT}.json)

-- Write as YAML
codec.to_file_pretty (data, "config.yaml", {CODEC_FORMAT}.yaml)
```

### Building Data Programmatically

```eiffel
codec: SIMPLE_CODEC
universe: CODEC_OBJECT
lib: CODEC_OBJECT
libs: CODEC_ARRAY

create codec
create universe.make
create libs.make

-- Build a library entry
create lib.make
lib.put (create {CODEC_STRING}.make ("simple_json"), "name")
lib.put (create {CODEC_STRING}.make ("/d/prod/simple_json"), "path")

libs.extend (lib)
universe.put (libs, "libraries")
universe.put (create {CODEC_STRING}.make ("simple_ecosystem"), "name")

-- Write to any format
codec.to_file_pretty (universe, "universe.toml", {CODEC_FORMAT}.toml)
```

---

## Implementation Plan

### Phase 1: Core Infrastructure
1. Create simple_codec library with CODEC_VALUE hierarchy
2. Implement CODEC_OBJECT, CODEC_ARRAY, primitives
3. Create SIMPLE_CODEC facade with format detection

### Phase 2: JSON Backend
1. Create JSON_CODEC adapter
2. Wrap existing simple_json functionality
3. Bidirectional: CODEC_VALUE ↔ JSON_OBJECT/JSON_ARRAY

### Phase 3: TOML Backend (simple_toml)
1. Create TOML lexer/parser
2. Implement TOML_CODEC
3. Handle TOML-specific features (dates, multiline strings)

### Phase 4: YAML Backend (simple_yaml)
1. Create YAML lexer/parser
2. Implement YAML_CODEC
3. Handle anchors, aliases, multi-document

### Phase 5: XML Backend
1. Create XML_CODEC adapter
2. Wrap existing simple_xml functionality
3. Define attribute/element mapping conventions

---

## Testing Strategy

Each backend needs:
1. **Round-trip tests** - parse → write → parse = same data
2. **Cross-format tests** - JSON → TOML → JSON = equivalent
3. **Edge cases** - empty, nested, special characters, unicode
4. **Contract verification** - preconditions, postconditions hold

---

## Dependencies

```
simple_codec
├── simple_json (backend)
├── simple_toml (backend, new)
├── simple_yaml (backend, new)
└── simple_xml (backend)
```

---

## Open Questions

1. **XML attribute handling** - How to represent attributes in CODEC_OBJECT?
2. **TOML dates** - Keep as strings or create CODEC_DATE?
3. **YAML anchors** - Resolve immediately or preserve structure?
4. **Error handling** - CODEC_PARSE_ERROR class? Exception vs Result?
5. **Streaming** - Support for large files? (Future consideration)

---

## Success Criteria

- [ ] Parse any format with single API call
- [ ] Convert between formats losslessly (where semantically possible)
- [ ] simple_lsp can read UCF in any supported format
- [ ] Contract Heat Map works regardless of UCF format choice
- [ ] All backends pass round-trip tests
- [ ] Performance: parse 1MB file in < 1 second

---

## References

- simple_json: https://github.com/simple-eiffel/simple_json
- simple_xml: https://github.com/simple-eiffel/simple_xml
- TOML spec: https://toml.io/en/v1.0.0
- YAML spec: https://yaml.org/spec/1.2.2/
- JSON spec: https://www.json.org/
