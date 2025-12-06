# Week 2 Library Development Plan

## Overview

This document synthesizes research findings for three new simple_* Eiffel libraries to be developed as part of the Christmas Sprint Week 2 (plus simple_cors which was originally scheduled for Week 1).

**Libraries to Build:**
1. `simple_cors` - Cross-Origin Resource Sharing (completes Week 1)
2. `simple_rate_limiter` - Request Rate Limiting
3. `simple_template` - Template Engine

---

## Library 1: simple_cors

### Specification Reference
- **WHATWG Fetch Standard** (Living Document) - Section on CORS protocol
- **MDN CORS Documentation** - Practical implementation guidance

### Competitor Analysis

| Library | Language | Key Features |
|---------|----------|--------------|
| cors (npm) | Node.js | Simple middleware, origin validation, credentials |
| django-cors-headers | Python | Django middleware, regex patterns, signals |
| flask-cors | Python | Decorator-based, automatic preflight |
| rack-cors | Ruby | Rack middleware, resource-based config |
| rs/cors | Go | Handler wrapper, debug mode, OPTIONS handling |
| Spring CORS | Java | Annotation-based (@CrossOrigin), global config |

### Common Developer Pain Points

1. **Wildcard + Credentials Incompatibility**
   - Cannot use `Access-Control-Allow-Origin: *` with credentials
   - Solution: Echo back specific Origin header when credentials enabled

2. **Preflight Request Confusion**
   - Developers don't understand OPTIONS requests
   - Solution: Automatic preflight handling, clear documentation

3. **Missing Vary Header**
   - Caching issues when Vary: Origin not set
   - Solution: Always include Vary: Origin in CORS responses

4. **Complex Configuration**
   - Multiple headers to coordinate
   - Solution: High-level fluent API with sensible defaults

5. **Origin Validation Security**
   - Regex patterns can be bypassed (e.g., evil.com matches notevil.com)
   - Solution: Exact match list + optional custom validator

### API Design

```eiffel
class SIMPLE_CORS

create
    make,                    -- Default (allow all origins, no credentials)
    make_permissive,         -- Development mode (everything allowed)
    make_restrictive         -- Production (nothing allowed until configured)

feature -- Configuration
    allow_origin (a_origin: STRING)
    allow_origins (a_list: ARRAY [STRING])
    allow_origin_pattern (a_pattern: STRING)  -- Regex pattern
    allow_all_origins

    allow_method (a_method: STRING)
    allow_methods (a_list: ARRAY [STRING])
    allow_all_methods

    allow_header (a_header: STRING)
    allow_headers (a_list: ARRAY [STRING])
    allow_all_headers

    expose_header (a_header: STRING)
    expose_headers (a_list: ARRAY [STRING])

    allow_credentials
    disallow_credentials

    set_max_age (a_seconds: INTEGER)

feature -- Request Processing
    process_request (a_request: CORS_REQUEST): CORS_RESPONSE
    is_cors_request (a_request: CORS_REQUEST): BOOLEAN
    is_preflight_request (a_request: CORS_REQUEST): BOOLEAN

    is_origin_allowed (a_origin: STRING): BOOLEAN
    is_method_allowed (a_method: STRING): BOOLEAN
    is_header_allowed (a_header: STRING): BOOLEAN

feature -- Response Headers
    headers_for_request (a_request: CORS_REQUEST): HASH_TABLE [STRING, STRING]

feature -- Query
    allowed_origins: ARRAYED_LIST [STRING]
    allowed_methods: ARRAYED_LIST [STRING]
    allowed_headers: ARRAYED_LIST [STRING]
    exposed_headers: ARRAYED_LIST [STRING]
    credentials_allowed: BOOLEAN
    max_age: INTEGER
end
```

### Security Considerations
- Never allow null origin (can be spoofed from sandboxed iframes)
- Validate origin exactly (not substring/prefix matching)
- Always set Vary: Origin to prevent cache poisoning
- Document that wildcard + credentials is forbidden by spec

---

## Library 2: simple_rate_limiter

### Specification Reference
- **RFC 6585** - HTTP 429 Too Many Requests
- **draft-ietf-httpapi-ratelimit-headers** - RateLimit header fields (draft)
- **IETF HTTP Working Group** - Standard header naming conventions

### Algorithm Options

| Algorithm | Burst Handling | Memory | Accuracy | Use Case |
|-----------|---------------|--------|----------|----------|
| Token Bucket | Allows bursts | Low | Good | AWS, Stripe, most APIs |
| Leaky Bucket | Smooth output | Low | Good | Consistent throughput |
| Fixed Window | Boundary spikes | Lowest | Poor | Simple implementations |
| Sliding Window Log | No bursts | High | Exact | When precision critical |
| Sliding Window Counter | Minimal bursts | Low | Very Good | Best overall tradeoff |

**Recommendation**: Implement Token Bucket as primary (most common), with Sliding Window Counter as alternative.

### Competitor Analysis

| Library | Language | Features |
|---------|----------|----------|
| express-rate-limit | Node.js | Middleware, multiple stores, skip rules |
| rate-limiter-flexible | Node.js | Multiple backends, cluster support |
| django-ratelimit | Python | Decorator, cache backends, groups |
| Flask-Limiter | Python | Extension, multiple strategies |
| rack-attack | Ruby | Throttle + safelist/blocklist |
| golang.org/x/time/rate | Go | Standard library, token bucket |
| uber-go/ratelimit | Go | Thread-safe, clock injection |
| Bucket4j | Java | Multiple algorithms, JCache |
| Guava RateLimiter | Java | Token bucket, warm-up period |

### Common Developer Pain Points

1. **Distributed Rate Limiting**
   - In-memory doesn't work across servers
   - Solution: Pluggable storage interface (memory, file, future: external)

2. **Key Extraction Complexity**
   - Different apps need different keys (IP, user ID, API key)
   - Solution: Configurable key extraction function

3. **Race Conditions**
   - Multiple requests can slip through
   - Solution: Atomic operations, proper synchronization

4. **Granular Limits**
   - Need different limits for different endpoints
   - Solution: Named limiters, composable rules

5. **Missing Headers**
   - Users don't know when limits reset
   - Solution: Always include RateLimit-* headers

### API Design

```eiffel
class SIMPLE_RATE_LIMITER

create
    make,                           -- Default: 100 req/minute
    make_with_limit,                -- Custom limit/window
    make_token_bucket,              -- Token bucket algorithm
    make_sliding_window             -- Sliding window counter

feature -- Configuration
    set_limit (a_requests: INTEGER; a_window_seconds: INTEGER)
    set_burst_limit (a_max_burst: INTEGER)  -- For token bucket

    set_key_extractor (a_extractor: FUNCTION [REQUEST, STRING])
    set_storage (a_storage: RATE_LIMIT_STORAGE)

    add_whitelist (a_key: STRING)
    add_blacklist (a_key: STRING)
    remove_whitelist (a_key: STRING)
    remove_blacklist (a_key: STRING)

feature -- Rate Limiting
    check_limit (a_key: STRING): RATE_LIMIT_RESULT
    is_allowed (a_key: STRING): BOOLEAN
    consume (a_key: STRING; a_tokens: INTEGER): BOOLEAN

    remaining (a_key: STRING): INTEGER
    reset_time (a_key: STRING): DATE_TIME

    reset (a_key: STRING)
    reset_all

feature -- Response Headers (RFC draft-ietf-httpapi-ratelimit-headers)
    rate_limit_headers (a_key: STRING): HASH_TABLE [STRING, STRING]
    -- Returns: RateLimit-Limit, RateLimit-Remaining, RateLimit-Reset

feature -- Query
    limit: INTEGER
    window_seconds: INTEGER
    algorithm: STRING
    is_whitelisted (a_key: STRING): BOOLEAN
    is_blacklisted (a_key: STRING): BOOLEAN
end

class RATE_LIMIT_RESULT
feature
    is_allowed: BOOLEAN
    remaining: INTEGER
    reset_time: DATE_TIME
    retry_after: INTEGER  -- Seconds until next allowed request
end

deferred class RATE_LIMIT_STORAGE
feature
    get (a_key: STRING): detachable RATE_LIMIT_ENTRY
    set (a_key: STRING; a_entry: RATE_LIMIT_ENTRY)
    increment (a_key: STRING): INTEGER
    reset (a_key: STRING)
    cleanup_expired
end
```

### Storage Implementations
- `MEMORY_RATE_LIMIT_STORAGE` - In-memory hash table (default)
- Future: File-based, Redis, etc.

---

## Library 3: simple_template

### Specification Reference
- **Mustache Specification** (mustache.github.io) - Logic-less templates
- **Handlebars** - Extended Mustache with helpers
- **Jinja2** - Python template engine (reference for features)

### Syntax Comparison

| Feature | Mustache | Handlebars | Jinja2 | Liquid |
|---------|----------|------------|--------|--------|
| Variable | `{{var}}` | `{{var}}` | `{{ var }}` | `{{ var }}` |
| Escaped | default | default | default | default |
| Raw/Unescaped | `{{{var}}}` | `{{{var}}}` | `{{ var\|safe }}` | `{{ var }}` |
| If | `{{#if}}` | `{{#if}}` | `{% if %}` | `{% if %}` |
| Loop | `{{#each}}` | `{{#each}}` | `{% for %}` | `{% for %}` |
| Comment | `{{! }}` | `{{!-- --}}` | `{# #}` | `{% comment %}` |
| Include | `{{>partial}}` | `{{>partial}}` | `{% include %}` | `{% include %}` |

**Recommendation**: Use Mustache-style `{{}}` syntax as it's most widely recognized and cleanest for simple use cases.

### Competitor Analysis

| Library | Language | Philosophy |
|---------|----------|------------|
| Mustache | Multi | Logic-less, minimal |
| Handlebars | JS | Mustache + helpers |
| Jinja2 | Python | Full-featured, powerful |
| Liquid | Ruby | Safe for user templates |
| EJS | Node.js | Embedded JavaScript |
| Pebble | Java | Twig-inspired, typed |

### Common Developer Pain Points

1. **Security (XSS)**
   - Raw output can inject scripts
   - Solution: Auto-escape HTML by default, explicit raw syntax

2. **Server-Side Template Injection (SSTI)**
   - User-controlled templates can execute code
   - Solution: No code execution, pure substitution, sandbox mode

3. **Logic Creep**
   - Templates become unreadable with too much logic
   - Solution: Logic-less core, optional helpers for common patterns

4. **Performance**
   - Parsing on every render
   - Solution: Compile-once, render-many pattern

5. **Error Messages**
   - Cryptic errors with line numbers
   - Solution: Clear error messages with context

6. **Missing Variables**
   - Silent failures or exceptions
   - Solution: Configurable behavior (empty string, exception, default)

### API Design

```eiffel
class SIMPLE_TEMPLATE

create
    make,                    -- Empty template
    make_from_string,        -- Parse template string
    make_from_file           -- Load from file

feature -- Compilation
    parse (a_template: STRING)
    compile: COMPILED_TEMPLATE
    is_valid: BOOLEAN
    last_error: detachable STRING

feature -- Rendering
    render (a_context: TEMPLATE_CONTEXT): STRING
    render_to_file (a_context: TEMPLATE_CONTEXT; a_path: STRING)

feature -- Context Building
    set_variable (a_name: STRING; a_value: STRING)
    set_variables (a_table: HASH_TABLE [STRING, STRING])
    set_list (a_name: STRING; a_items: ARRAY [TEMPLATE_CONTEXT])
    set_section (a_name: STRING; a_visible: BOOLEAN)

    clear_variables

feature -- Configuration
    set_escape_html (a_enabled: BOOLEAN)  -- Default: True
    set_missing_variable_policy (a_policy: INTEGER)
        -- Options: Empty_string, Raise_exception, Keep_placeholder

    register_partial (a_name: STRING; a_template: SIMPLE_TEMPLATE)
    register_helper (a_name: STRING; a_helper: TEMPLATE_HELPER)

feature -- Query
    has_variable (a_name: STRING): BOOLEAN
    required_variables: ARRAYED_LIST [STRING]

feature -- Syntax Elements
    Variable_start: STRING = "{{"
    Variable_end: STRING = "}}"
    Section_start: STRING = "{{#"
    Section_end: STRING = "{{/"
    Inverted_section: STRING = "{{^"
    Comment_start: STRING = "{{!"
    Raw_start: STRING = "{{{"
    Raw_end: STRING = "}}}"
    Partial_start: STRING = "{{>"
end

class TEMPLATE_CONTEXT
create
    make
feature
    put (a_key: STRING; a_value: ANY)
    get (a_key: STRING): detachable ANY
    has (a_key: STRING): BOOLEAN

    put_string (a_key: STRING; a_value: STRING)
    put_integer (a_key: STRING; a_value: INTEGER)
    put_boolean (a_key: STRING; a_value: BOOLEAN)
    put_list (a_key: STRING; a_value: ARRAYED_LIST [TEMPLATE_CONTEXT])
end

class COMPILED_TEMPLATE
feature
    render (a_context: TEMPLATE_CONTEXT): STRING
    -- Optimized rendering without re-parsing
end
```

### Template Syntax

```mustache
{{! Comment - not rendered }}

Hello, {{name}}!

{{#show_greeting}}
Welcome to {{site_name}}.
{{/show_greeting}}

{{^has_items}}
No items found.
{{/has_items}}

{{#items}}
- {{title}}: {{description}}
{{/items}}

{{{raw_html}}}  {{! Not escaped }}

{{>header}}  {{! Include partial }}
```

### Security Considerations
- HTML escape all output by default
- No code execution in templates (pure substitution)
- Limit recursion depth for includes
- No access to Eiffel runtime from templates

---

## Implementation Order

1. **simple_cors** (Priority: High)
   - Completes Week 1 deliverables
   - Foundation for web API security
   - Relatively straightforward implementation

2. **simple_rate_limiter** (Priority: High)
   - Essential for API protection
   - Token bucket algorithm first
   - In-memory storage initially

3. **simple_template** (Priority: Medium)
   - More complex parsing logic
   - Mustache-style syntax
   - Compile/render separation

---

## Testing Strategy

### simple_cors Tests
- Origin matching (exact, pattern, wildcard)
- Preflight request handling
- Credentials + origin combination validation
- Header generation correctness
- Edge cases (null origin, empty headers)

### simple_rate_limiter Tests
- Token bucket behavior (capacity, refill)
- Sliding window accuracy
- Whitelist/blacklist functionality
- Header generation (RateLimit-*)
- Concurrent access safety
- Cleanup of expired entries

### simple_template Tests
- Variable substitution
- Section rendering (truthy/falsy)
- List iteration
- Nested contexts
- Partial includes
- HTML escaping
- Raw output
- Error handling (missing variables)
- Compile/render separation

---

## Documentation Requirements

Each library needs:
1. `docs/index.html` - Main documentation page (consistent with existing simple_* style)
2. `docs/api/{class_name}.html` - API reference for each class
3. `docs/css/style.css` - Consistent styling
4. `docs/images/logo.png` - simple_* ecosystem logo
5. `README.md` - GitHub repository overview

---

## Dependencies

| Library | Dependencies |
|---------|--------------|
| simple_cors | None (standalone) |
| simple_rate_limiter | None (standalone) |
| simple_template | None (standalone) |

All libraries follow the simple_* pattern of minimal external dependencies.

---

## File Structure Template

```
simple_{library}/
├── src/
│   └── simple_{library}.e
├── tests/
│   ├── simple_{library}_test_set.e
│   └── test_application.e
├── docs/
│   ├── index.html
│   ├── api/
│   │   └── simple_{library}.html
│   ├── css/
│   │   └── style.css
│   └── images/
│       └── logo.png
├── simple_{library}.ecf
└── README.md
```

---

*Document created: December 6, 2024*
*Sprint: Christmas Sprint Week 2*
