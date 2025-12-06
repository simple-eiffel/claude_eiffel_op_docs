# Unified API Facade Architecture for Eiffel

## Introduction

We've developed a three-tier API facade architecture that dramatically simplifies how Eiffel applications consume library functionality. Instead of managing 20+ individual library dependencies, applications can reference a single facade and gain access to everything they need with clear semantic separation between layers.

## The Problem

Traditional Eiffel library usage requires:
- Adding each library to your ECF individually
- Managing environment variables for each library
- Understanding the API of each separate library
- Dealing with inconsistent naming conventions across libraries

For a typical web application, this meant including and learning: simple_base64, simple_hash, simple_uuid, simple_json, simple_csv, simple_markdown, simple_validation, simple_process, simple_randomizer, simple_jwt, simple_smtp, simple_sql, simple_cors, simple_rate_limiter, simple_template, simple_websocket, simple_web, simple_alpine, simple_htmx...

## The Solution: Layered API Facades with Composition

We created three facade libraries using **composition over inheritance** for maximum semantic clarity:

```
+------------------------------------------+
| APP_API (Application Layer)              |
|   - alpine, web_client                   |
|   - service (composition)                |
|   - foundation (composition)             |
+------------------------------------------+
         |                    |
         v                    v
+------------------+  +------------------+
| SERVICE_API      |  | FOUNDATION_API   |
| - jwt, smtp,     |  | - base64, hash,  |
|   sql, cors,     |  |   uuid, json,    |
|   templates,     |  |   csv, markdown, |
|   websocket      |  |   validation,    |
| - foundation     |  |   process,       |
|   (composition)  |  |   random         |
+------------------+  +------------------+
         |
         v
+------------------+
| FOUNDATION_API   |
+------------------+
```

## Why Composition Over Inheritance?

With inheritance, typing `api.` in the IDE shows ALL features from all layers - confusing!

With composition:
- `api.` shows only app-level features (alpine, web_client, service, foundation)
- `api.service.` shows only service-level features (jwt, smtp, cors, etc.)
- `api.foundation.` shows only foundation-level features (base64, sha256, etc.)

This makes code **self-documenting**. When you see `api.service.new_jwt(...)`, you immediately know it's a service-layer feature. No prefix naming pollution like `svc_new_jwt` or `fnd_base64_encode`.

## How It Works

### Layer 1: FOUNDATION_API

The `simple_foundation_api` ECF references 9 core utility supplier libraries. The `FOUNDATION_API` class provides unified access:

```eiffel
class FOUNDATION_API

feature -- Base64
    base64_encode (a_string: STRING): STRING
    base64_decode (a_encoded: STRING): STRING
    base64_url_encode (a_string: STRING): STRING

feature -- Hashing
    sha256 (a_string: STRING): STRING
    sha1 (a_string: STRING): STRING
    md5 (a_string: STRING): STRING
    hmac_sha256 (a_key, a_message: STRING): STRING
    secure_compare (a_string1, a_string2: STRING): BOOLEAN

feature -- UUID
    new_uuid: STRING
    new_uuid_compact: STRING
    is_valid_uuid (a_string: STRING): BOOLEAN

feature -- JSON
    parse_json (a_json: STRING): detachable JSON_VALUE
    new_json_object: JSON_OBJECT
    new_json_array: JSON_ARRAY

feature -- CSV
    parse_csv (a_csv: STRING): BOOLEAN
    csv_field (a_row, a_col: INTEGER): STRING

feature -- Markdown
    markdown_to_html (a_markdown: STRING): STRING

feature -- Validation
    new_validator: SIMPLE_VALIDATOR
    is_valid_email (a_email: STRING): BOOLEAN
    is_valid_url (a_url: STRING): BOOLEAN

feature -- Process
    execute_command (a_command: STRING): TUPLE [output: STRING; exit_code: INTEGER]

feature -- Random
    random_integer_in_range (a_min, a_max: INTEGER): INTEGER
    random_alphanumeric_string (a_length: INTEGER): STRING

end
```

### Layer 2: SERVICE_API

The `simple_service_api` ECF references 7 web service supplier libraries plus `simple_foundation_api`. The `SERVICE_API` class uses **composition** to access foundation:

```eiffel
class SERVICE_API

feature -- JWT Authentication
    new_jwt (a_secret: STRING): SIMPLE_JWT
    create_token (a_secret, a_subject, a_issuer: STRING; a_expires: INTEGER): STRING
    verify_token (a_secret, a_token: STRING): BOOLEAN

feature -- SMTP Email
    new_smtp (a_host: STRING; a_port: INTEGER): SIMPLE_SMTP

feature -- SQL Database
    new_database (a_path: STRING): SIMPLE_DATABASE
    new_memory_database: SIMPLE_DATABASE

feature -- CORS
    new_cors: SIMPLE_CORS
    new_cors_permissive: SIMPLE_CORS

feature -- Rate Limiting
    new_rate_limiter (a_max_requests, a_window_seconds: INTEGER): SIMPLE_RATE_LIMITER

feature -- Templates
    new_template: SIMPLE_TEMPLATE
    render_template (a_template: STRING; a_data: HASH_TABLE [STRING, STRING]): STRING

feature -- WebSocket
    new_ws_handshake: WS_HANDSHAKE
    new_ws_text_frame (a_text: STRING; a_is_final: BOOLEAN): WS_FRAME

feature -- Layer Access
    foundation: FOUNDATION_API
        -- Access to foundation layer features ONLY.
        once
            create Result.make
        end

end
```

### Layer 3: APP_API

The `simple_app_api` ECF references 2 application supplier libraries plus `simple_service_api` and `simple_foundation_api`. The `APP_API` class uses **composition**:

```eiffel
class APP_API

feature -- Web Client
    new_web_client: SIMPLE_WEB_CLIENT
    new_get_request (a_url: STRING): SIMPLE_WEB_REQUEST
    new_post_request (a_url: STRING): SIMPLE_WEB_REQUEST
    web_client: SIMPLE_WEB_CLIENT  -- singleton

feature -- Alpine.js Components
    new_alpine_factory: ALPINE_FACTORY
    alpine: ALPINE_FACTORY  -- singleton

feature -- Layer Access
    service: SERVICE_API
        -- Access to service layer features ONLY.
        once
            create Result.make
        end

    foundation: FOUNDATION_API
        -- Access to foundation layer features ONLY.
        once
            create Result.make
        end

end
```

## Usage Examples

### Before: Traditional Approach

```eiffel
class MY_APPLICATION

feature {NONE} -- Initialization

    make
        local
            l_base64: SIMPLE_BASE64
            l_hash: SIMPLE_HASH
            l_uuid: SIMPLE_UUID
            l_json: SIMPLE_JSON
            l_jwt: SIMPLE_JWT
            l_smtp: SIMPLE_SMTP
            l_db: SIMPLE_DATABASE
            l_cors: SIMPLE_CORS
        do
            create l_base64
            create l_hash
            create l_uuid
            create l_json
            create l_jwt.make ("secret")
            create l_smtp.make ("smtp.example.com", 587)
            create l_db.make (":memory:")
            create l_cors

            -- Use each library separately...
            encoded := l_base64.encode ("data")
            hash := l_hash.sha256 ("password")
            -- etc.
        end

end
```

**ECF required:**
```xml
<library name="simple_base64" location="$SIMPLE_BASE64\simple_base64.ecf"/>
<library name="simple_hash" location="$SIMPLE_HASH\simple_hash.ecf"/>
<library name="simple_uuid" location="$SIMPLE_UUID\simple_uuid.ecf"/>
<library name="simple_json" location="$SIMPLE_JSON\simple_json.ecf"/>
<library name="simple_jwt" location="$SIMPLE_JWT\simple_jwt.ecf"/>
<library name="simple_smtp" location="$SIMPLE_SMTP\simple_smtp.ecf"/>
<library name="simple_sql" location="$SIMPLE_SQL\simple_sql.ecf"/>
<library name="simple_cors" location="$SIMPLE_CORS\simple_cors.ecf"/>
<!-- ... and more -->
```

### After: Facade Approach with Composition

```eiffel
class MY_APPLICATION

feature {NONE} -- Initialization

    make
        local
            api: APP_API
        do
            create api.make

            -- App-level features
            div := api.alpine.div
            div.x_data ("{count: 0}")
            request := api.new_get_request ("https://api.example.com/data")

            -- Service-level features (via composition)
            token := api.service.create_token ("secret", "user", "app", 3600)
            db := api.service.new_memory_database
            cors := api.service.new_cors

            -- Foundation-level features (via composition)
            encoded := api.foundation.base64_encode ("data")
            hash := api.foundation.sha256 ("password")
            uuid := api.foundation.new_uuid
        end

end
```

**ECF required:**
```xml
<library name="simple_app_api" location="$SIMPLE_APP_API\simple_app_api.ecf"/>
```

## Semantic Clarity Through Composition

When reading code, you immediately know which layer a feature belongs to:

```eiffel
-- Clear: foundation-level operation
hash := api.foundation.sha256 ("password")

-- Clear: service-level operation
token := api.service.create_token ("secret", "user", "app", 3600)

-- Clear: app-level operation
div := api.alpine.div
```

Compare to the ugly alternative of prefix naming:
```eiffel
-- Ugly: Hungarian-style prefixes
hash := api.fnd_sha256 ("password")       -- What does "fnd" mean?
token := api.svc_create_token (...)       -- Pollutes feature names
div := api.app_alpine_div                 -- Gets ridiculous quickly
```

Composition gives you namespacing through **structure** rather than polluting feature names.

## Choosing the Right Layer

| If your application needs... | Use this class |
|------------------------------|----------------|
| Core utilities only (encoding, hashing, JSON, etc.) | `FOUNDATION_API` |
| Web services (JWT, email, database, etc.) | `SERVICE_API` |
| Full web application (client, UI components) | `APP_API` |

## Design Principles

### 1. Composition Over Inheritance

Each API layer is a separate object. When you type `api.`, IntelliSense shows only features appropriate to that level. Access lower layers through explicit accessors (`api.service`, `api.foundation`).

### 2. Factory Methods Over Direct Construction

Instead of exposing raw classes, the facades provide factory methods:

```eiffel
-- Good: Factory method
jwt := api.service.new_jwt ("secret")

-- Avoided: Direct construction requiring knowledge of class internals
create {SIMPLE_JWT} jwt.make_with_secret ("secret")
```

### 3. Convenience Methods for Common Operations

The facades add convenience methods that combine multiple operations:

```eiffel
-- Convenience: One call does it all
token := api.service.create_token ("secret", "user@example.com", "my-app", 3600)

-- Without convenience method (more verbose)
jwt := api.service.new_jwt ("secret")
jwt.set_subject ("user@example.com")
jwt.set_issuer ("my-app")
jwt.set_expiration (3600)
token := jwt.generate
```

### 4. Singleton Access for Shared Resources

Some objects benefit from singleton access:

```eiffel
-- Get the same Alpine factory throughout your application
div := api.alpine.div
span := api.alpine.span
-- Both use the same factory instance
```

### 5. Design by Contract Throughout

All features include proper contracts:

```eiffel
new_get_request (a_url: STRING): SIMPLE_WEB_REQUEST
    require
        url_not_void: a_url /= Void
        url_not_empty: not a_url.is_empty
    do
        create Result.make_get (a_url)
    ensure
        result_not_void: Result /= Void
    end
```

## Benefits

1. **Simplified Dependencies** - One ECF reference instead of 20+
2. **Consistent API** - All features follow the same naming conventions
3. **Semantic Clarity** - Composition shows which layer each feature belongs to
4. **IDE-Friendly** - IntelliSense shows only relevant features for each layer
5. **Self-Documenting Code** - `api.service.new_jwt` is clearer than `api.new_jwt`
6. **Reduced Boilerplate** - No need to create and manage multiple library objects
7. **Layered Architecture** - Choose the appropriate level for your needs
8. **Future-Proof** - New supplier libraries can be added to facades without changing client code

## Repository Links

- [simple_foundation_api](https://github.com/ljr1981/simple_foundation_api) - Core utilities
- [simple_service_api](https://github.com/ljr1981/simple_service_api) - Web services
- [simple_app_api](https://github.com/ljr1981/simple_app_api) - Application layer
- [simple_showcase](https://github.com/ljr1981/simple_showcase) - Example application using simple_app_api

## Conclusion

The three-tier API facade architecture demonstrates how Eiffel's composition can create clean, unified APIs with clear semantic boundaries. By bundling related libraries behind facade classes and using composition for layer access, we've made it dramatically easier to build Eiffel applications while maintaining the language's strong typing and Design by Contract principles.

The composition approach provides namespacing through structure, making code self-documenting without polluting feature names with layer prefixes.

---

*This architecture was developed as part of the simple_* library ecosystem for Eiffel.*
