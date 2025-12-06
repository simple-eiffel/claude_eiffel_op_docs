# Week 3 Library Research & Plan

## Libraries to Build
1. **simple_validation** - Data validation library
2. **simple_websocket** - WebSocket protocol implementation

---

# SIMPLE_VALIDATION

## 1. Industry Standards & Specifications

### HTML5 Constraint Validation API
- **Source**: [WHATWG HTML Standard](https://html.spec.whatwg.org/multipage/forms.html), [MDN Constraint Validation](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation)
- **Key Features**:
  - `required` - field must have value
  - `pattern` - regex matching
  - `minlength` / `maxlength` - string length constraints
  - `min` / `max` - numeric range constraints
  - `type` - email, url, number, date, etc.
  - `step` - numeric step increments
- **API Methods**:
  - `checkValidity()` - returns boolean
  - `reportValidity()` - shows UI feedback
  - `setCustomValidity(message)` - custom error messages
- **ValidityState Object Properties**:
  - `valueMissing`, `typeMismatch`, `patternMismatch`
  - `tooLong`, `tooShort`, `rangeUnderflow`, `rangeOverflow`
  - `stepMismatch`, `badInput`, `customError`, `valid`

### JSON Schema (Draft 2020-12)
- **Source**: [JSON Schema Spec](https://json-schema.org/draft/2020-12), [Validation Vocabulary](https://json-schema.org/draft/2020-12/json-schema-validation)
- **Key Validators**:
  - Type: `type`, `enum`, `const`
  - Numeric: `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`, `multipleOf`
  - String: `minLength`, `maxLength`, `pattern`, `format`
  - Array: `minItems`, `maxItems`, `uniqueItems`, `contains`
  - Object: `required`, `minProperties`, `maxProperties`, `dependentRequired`
- **Formats**: `date-time`, `date`, `time`, `email`, `uri`, `uuid`, `ipv4`, `ipv6`, `regex`

## 2. Pain Points & Developer Frustrations

### From Joi/Yup/Zod Comparisons
- **Sources**: [DEV.to Comparison](https://dev.to/gimnathperera/yup-vs-zod-vs-joi-a-comprehensive-comparison-of-javascript-validation-libraries-4mhi), [Bitovi Comparison](https://www.bitovi.com/blog/comparing-schema-validation-libraries-ajv-joi-yup-and-zod)

| Pain Point | Description |
|------------|-------------|
| **Verbose syntax** | Too much boilerplate for simple validations |
| **Poor error messages** | Generic "invalid" instead of actionable guidance |
| **Hard to compose** | Can't easily combine validators |
| **Type inference** | Joi/Yup don't infer types (Zod does) |
| **Performance** | Some libraries slow with large datasets |
| **Bundle size** | Joi is heavy for client-side use |
| **Learning curve** | Each library has different API patterns |
| **Async validation** | Often awkward to handle (DB lookups, API calls) |
| **Custom validators** | Hard to add business-specific rules |
| **Conditional validation** | Complex when field A depends on field B |

### From UX Best Practices
- **Sources**: [NN/G Form Errors](https://www.nngroup.com/articles/errors-forms-design-guidelines/), [Smashing Magazine Live Validation](https://www.smashingmagazine.com/2022/09/inline-validation-web-forms-ux/)

| UX Issue | Best Practice |
|----------|---------------|
| **Premature validation** | Validate on blur, not while typing |
| **Generic messages** | Be specific: "Enter email like user@example.com" |
| **Hidden errors** | Show error next to the field, not in summary only |
| **No guidance** | Tell user HOW to fix, not just WHAT is wrong |
| **Color-only feedback** | Use icons for colorblind users |
| **Blocking input** | Allow user to continue, don't disable fields |

## 3. Existing simple_* Libraries to Consume

| Library | Use Case |
|---------|----------|
| `simple_json` | Validate JSON structures |
| `simple_template` | Error message templates with placeholders |

## 4. High-Level API Design

### Core Concepts
```
VALIDATOR: Base class for all validators
VALIDATION_RESULT: Success/failure with error messages
VALIDATION_CONTEXT: Holds field name, value, and metadata
VALIDATION_RULE: Single validation check (required, min, max, pattern, etc.)
COMPOSITE_VALIDATOR: Combines multiple rules
```

### Design Principles
1. **Fluent API** - Chain validators naturally
2. **Actionable errors** - Every error explains how to fix
3. **Composable** - Small validators combine into complex ones
4. **Contracts first** - Design by Contract throughout
5. **No magic** - Explicit, predictable behavior

### Proposed Class Structure

```eiffel
class SIMPLE_VALIDATOR
create
    make

feature -- Fluent Configuration
    required: SIMPLE_VALIDATOR
    min_length (n: INTEGER): SIMPLE_VALIDATOR
    max_length (n: INTEGER): SIMPLE_VALIDATOR
    min_value (n: REAL_64): SIMPLE_VALIDATOR
    max_value (n: REAL_64): SIMPLE_VALIDATOR
    pattern (regex: STRING): SIMPLE_VALIDATOR
    email: SIMPLE_VALIDATOR
    url: SIMPLE_VALIDATOR
    uuid: SIMPLE_VALIDATOR
    one_of (values: ARRAY [STRING]): SIMPLE_VALIDATOR
    custom (rule: FUNCTION [STRING, BOOLEAN]; message: STRING): SIMPLE_VALIDATOR

feature -- Validation
    validate (value: detachable ANY): VALIDATION_RESULT
    is_valid (value: detachable ANY): BOOLEAN

feature -- Error Customization
    with_message (msg: STRING): SIMPLE_VALIDATOR
    with_field_name (name: STRING): SIMPLE_VALIDATOR
end

class VALIDATION_RESULT
feature -- Status
    is_valid: BOOLEAN
    errors: ARRAYED_LIST [VALIDATION_ERROR]
    first_error: detachable VALIDATION_ERROR
    error_messages: ARRAYED_LIST [STRING]
end

class VALIDATION_ERROR
feature -- Query
    field_name: STRING
    message: STRING
    code: STRING  -- e.g., "required", "min_length", "pattern"
    constraint: detachable ANY  -- The constraint that was violated
    actual_value: detachable ANY  -- What the user provided
end
```

### Usage Examples

```eiffel
-- Simple validation
validator := create {SIMPLE_VALIDATOR}.make.required.email
result := validator.validate (user_input)
if not result.is_valid then
    print (result.first_error.message)
end

-- Complex validation
password_validator := create {SIMPLE_VALIDATOR}.make
    .required
    .min_length (8)
    .max_length (128)
    .pattern ("[A-Z]")  -- At least one uppercase
    .pattern ("[0-9]")  -- At least one digit
    .with_message ("Password must be 8-128 chars with uppercase and digit")

-- Object validation
user_validator := create {OBJECT_VALIDATOR}.make
user_validator.field ("email", create {SIMPLE_VALIDATOR}.make.required.email)
user_validator.field ("age", create {SIMPLE_VALIDATOR}.make.min_value (18).max_value (120))
user_validator.field ("username", create {SIMPLE_VALIDATOR}.make.required.min_length (3).max_length (20))
```

---

# SIMPLE_WEBSOCKET

## 1. Industry Standards & Specifications

### RFC 6455 - The WebSocket Protocol
- **Source**: [IETF RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455), [MDN WebSocket Servers](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers)

### Handshake Process
**Client Request:**
```
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

**Server Response:**
```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

**Accept Key Calculation:**
1. Concatenate client key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
2. SHA-1 hash
3. Base64 encode

### Frame Format
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                               |Masking-key, if MASK set to 1  |
+-------------------------------+-------------------------------+
| Masking-key (continued)       |          Payload Data         |
+-------------------------------- - - - - - - - - - - - - - - - +
:                     Payload Data continued ...                :
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
```

### Opcodes
| Opcode | Meaning |
|--------|---------|
| 0x0 | Continuation frame |
| 0x1 | Text frame (UTF-8) |
| 0x2 | Binary frame |
| 0x8 | Connection close |
| 0x9 | Ping |
| 0xA | Pong |

### Masking Algorithm
```
j = i MOD 4
transformed[i] = original[i] XOR mask[j]
```
- Client → Server: MUST be masked
- Server → Client: MUST NOT be masked

### Close Codes
| Code | Meaning |
|------|---------|
| 1000 | Normal closure |
| 1001 | Going away |
| 1002 | Protocol error |
| 1003 | Unsupported data |
| 1007 | Invalid UTF-8 |
| 1008 | Policy violation |
| 1009 | Message too big |
| 1011 | Server error |

## 2. Pain Points & Implementation Challenges

- **Sources**: [OpenMyMind WebSocket Framing](https://www.openmymind.net/WebSocket-Framing-Masking-Fragmentation-and-More/), [Cookie Engineer Guide](https://cookie.engineer/weblog/articles/implementers-guide-to-websockets.html)

| Challenge | Description |
|-----------|-------------|
| **Handshake complexity** | HTTP upgrade + SHA-1 + Base64 calculation |
| **Variable-length framing** | 7, 16, or 64-bit payload lengths |
| **Masking implementation** | XOR with 4-byte key cycling |
| **Fragmentation** | Splitting large messages across frames |
| **UTF-8 validation** | Text frames must be valid UTF-8 |
| **Ping/Pong handling** | Must respond to pings with pong |
| **Clean shutdown** | Close handshake with status codes |
| **Buffering** | Accumulating fragmented messages |
| **Error recovery** | What to do on protocol violations |
| **Interleaving** | Control frames can appear mid-fragment |

## 3. Existing simple_* Libraries to Consume

| Library | Use Case |
|---------|----------|
| `simple_base64` | Encoding Sec-WebSocket-Accept |
| `simple_hash` | SHA-1 for handshake |
| `simple_json` | JSON message serialization |

## 4. High-Level API Design

### Core Concepts
```
WS_FRAME: Single WebSocket frame (header + payload)
WS_MESSAGE: Complete message (may span multiple frames)
WS_CONNECTION: Active WebSocket connection
WS_SERVER: Accepts and manages connections
WS_CLIENT: Initiates connection to server
WS_HANDLER: Callback interface for events
```

### Design Principles
1. **RFC 6455 compliant** - Full protocol implementation
2. **Async-friendly** - Non-blocking I/O patterns
3. **Event-driven** - Callbacks for open/message/close/error
4. **Ping/pong automatic** - Keep-alive handled internally
5. **Clean API** - Hide frame complexity from user

### Proposed Class Structure

```eiffel
class WS_SERVER
create
    make, make_with_port

feature -- Configuration
    set_port (p: INTEGER)
    set_max_connections (n: INTEGER)
    set_max_message_size (bytes: INTEGER)
    on_connection (handler: PROCEDURE [WS_CONNECTION])
    on_message (handler: PROCEDURE [WS_CONNECTION, WS_MESSAGE])
    on_close (handler: PROCEDURE [WS_CONNECTION, INTEGER, STRING])
    on_error (handler: PROCEDURE [WS_CONNECTION, STRING])

feature -- Control
    start
    stop
    is_running: BOOLEAN

feature -- Broadcasting
    broadcast_text (message: STRING)
    broadcast_binary (data: ARRAY [NATURAL_8])
end

class WS_CONNECTION
feature -- Sending
    send_text (message: STRING)
    send_binary (data: ARRAY [NATURAL_8])
    ping
    close
    close_with_reason (code: INTEGER; reason: STRING)

feature -- Query
    id: STRING
    is_open: BOOLEAN
    remote_address: STRING
    subprotocol: detachable STRING
end

class WS_CLIENT
create
    make

feature -- Connection
    connect (url: STRING)
    disconnect
    is_connected: BOOLEAN

feature -- Events
    on_open (handler: PROCEDURE)
    on_message (handler: PROCEDURE [WS_MESSAGE])
    on_close (handler: PROCEDURE [INTEGER, STRING])
    on_error (handler: PROCEDURE [STRING])

feature -- Sending
    send_text (message: STRING)
    send_binary (data: ARRAY [NATURAL_8])
end

class WS_MESSAGE
feature -- Query
    is_text: BOOLEAN
    is_binary: BOOLEAN
    text: STRING  -- For text messages
    data: ARRAY [NATURAL_8]  -- For binary messages
    size: INTEGER
end
```

### Usage Examples

```eiffel
-- Server
server := create {WS_SERVER}.make_with_port (8080)
server.on_connection (agent handle_connection)
server.on_message (agent handle_message)
server.start

handle_message (conn: WS_CONNECTION; msg: WS_MESSAGE)
    do
        if msg.is_text then
            print ("Received: " + msg.text)
            conn.send_text ("Echo: " + msg.text)
        end
    end

-- Client
client := create {WS_CLIENT}.make
client.on_open (agent do print ("Connected!") end)
client.on_message (agent (msg: WS_MESSAGE) do print (msg.text) end)
client.connect ("ws://localhost:8080/chat")
client.send_text ("Hello, Server!")
```

---

# Implementation Order

## Phase 1: simple_validation (2 days)
1. Core validator classes
2. Built-in validators (required, length, range, pattern, email, etc.)
3. Error message system
4. Composite validators
5. Tests (target: 30+ tests)

## Phase 2: simple_websocket (3 days)
1. Frame parsing/encoding
2. Handshake (using simple_hash + simple_base64)
3. Server implementation
4. Client implementation
5. Tests (target: 25+ tests)

## Phase 3: Review (Hats)
1. **Code Review Hat** - Deep review with web research
2. **Contracting Hat** - Preconditions/postconditions/invariants
3. **Security Hat** - Input validation, injection prevention

---

# Sources

## Validation
- [MDN Constraint Validation](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)
- [Yup vs Zod vs Joi Comparison](https://dev.to/gimnathperera/yup-vs-zod-vs-joi-a-comprehensive-comparison-of-javascript-validation-libraries-4mhi)
- [NN/G Form Error Guidelines](https://www.nngroup.com/articles/errors-forms-design-guidelines/)

## WebSocket
- [RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455)
- [MDN Writing WebSocket Servers](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers)
- [WebSocket Framing Deep Dive](https://www.openmymind.net/WebSocket-Framing-Masking-Fragmentation-and-More/)
