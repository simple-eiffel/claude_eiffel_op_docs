# simple_* Ecosystem Assessment Report

**Date:** December 7, 2025
**Author:** Claude Code Analysis

## Executive Summary

The simple_* library collection is a **usability layer** over Eiffel's existing but clunky libraries. It provides genuine value in developer experience but suffers from inconsistent quality standards, no package distribution, and mixed SCOOP/void-safety support. It's currently a well-intentioned hobby project, not a production-ready library suite.

---

## Part 1: Current simple_* Inventory

### Foundation Layer (14 libraries)
| Library | Purpose |
|---------|---------|
| simple_base64 | Base64 encoding/decoding |
| simple_csv | CSV parsing/generation |
| simple_datetime | Date/time/duration/age calculations |
| simple_hash | SHA-256, SHA-1, MD5, HMAC |
| simple_htmx | HTMX component generation |
| simple_json | JSON parsing/building |
| simple_logger | Structured logging with JSON output |
| simple_markdown | Markdown to HTML |
| simple_process | Shell command execution |
| simple_randomizer | Random data generation |
| simple_regex | Pattern matching with fluent builder |
| simple_uuid | UUID generation/validation |
| simple_validation | Fluent data validation |
| simple_xml | XML parsing/building |

### Service Layer (9 libraries)
| Library | Purpose |
|---------|---------|
| simple_cache | Caching |
| simple_cors | CORS headers |
| simple_jwt | JWT tokens |
| simple_pdf | PDF generation |
| simple_rate_limiter | Rate limiting |
| simple_smtp | Email sending |
| simple_sql | Database access |
| simple_template | Templating |
| simple_websocket | WebSocket support |

### Application Layer (5+ libraries)
| Library | Purpose |
|---------|---------|
| simple_foundation_api | Unified facade for foundation libs |
| simple_service_api | Unified facade for service libs |
| simple_app_api | Full application stack |
| simple_web | Web application support |
| simple_showcase | Demo application |

**Total: ~30 libraries**

---

## Part 2: What Eiffel Already Provides

### ISE Standard Library
| Library | Purpose | Quality |
|---------|---------|---------|
| `argument_parser` | CLI argument parsing | Production |
| `encoding` | Character encoding | Production |
| `i18n` | Internationalization | Production |
| `net` | Networking, sockets, mail | Production |
| `preferences` | Configuration management | Production |
| `process` | Process execution | Production |
| `store` | Database ORM (multi-DBMS) | Production |
| `time` | Date/time handling | Production |
| `uuid` | UUID generation | Production |

### Gobo Libraries
| Library | Purpose | Quality |
|---------|---------|---------|
| `regexp` | PCRE regex | Production |
| `xml` | XML parsing | Production |
| `xpath` | XPath queries | Production |
| `xslt` | XSLT transforms | Production |
| `argument` | Argument parsing | Production |
| `string` | String utilities | Production |
| `structure` | Data structures | Production |
| `time` | Time handling | Production |

### Contrib Libraries
| Library | Purpose | Quality |
|---------|---------|---------|
| `http_client` | HTTP requests (curl + net) | Production |
| `ewf` | Web framework | Production |
| `wsf` | Web server framework | Production |
| `wsf_compression` | Gzip/deflate | Production |
| `wsf_session` | Session management | Production |
| `wsf_security` | Security middleware | Production |
| `eel` | Encryption (AES, etc.) | Production |
| `mongo` | MongoDB client | Production |
| `openid` | OAuth/OpenID | Production |
| `etar` | Tar archives | Production |
| `json` | JSON parsing | Production |
| `uri_template` | URI templates | Production |
| `wikitext` | Wiki markup | Production |

---

## Part 3: Void-Safety & SCOOP Status

### simple_* Capability Matrix

| Library | Void-Safe | SCOOP | Status |
|---------|-----------|-------|--------|
| simple_base64 | Not declared | ✅ SCOOP-ready | Inconsistent |
| simple_cors | Not declared | ✅ SCOOP-ready | Inconsistent |
| simple_csv | ❌ Not declared | ❌ Not declared | **Broken** |
| simple_datetime | ❌ Not declared | ❌ Not declared | **Broken** |
| simple_hash | ❌ Not declared | ❌ Not declared | **Broken** |
| simple_htmx | ✅ All | ❌ None | Partial |
| simple_json | ❌ Not declared | ❌ Not declared | **Broken** |
| simple_logger | ❌ Not declared | ❌ Not declared | **Broken** |
| simple_markdown | ❌ Not declared | ❌ Not declared | **Broken** |
| simple_process | Not declared | Thread-only | Partial |
| simple_randomizer | Not declared | ✅ SCOOP-ready | Inconsistent |
| simple_rate_limiter | Not declared | ✅ SCOOP-ready | Inconsistent |
| simple_regex | ✅ All | ❌ None | Partial |
| simple_template | Not declared | ✅ SCOOP-ready | Inconsistent |
| simple_uuid | Not declared | ✅ SCOOP-ready | Inconsistent |
| simple_validation | Not declared | ✅ SCOOP-ready | Inconsistent |
| simple_xml | ❌ Not declared | ❌ Not declared | **Broken** |

### Summary
- **7 libraries** are SCOOP-ready
- **2 libraries** are explicitly void-safe
- **8+ libraries** have NO capability declarations (undefined behavior)
- **0 libraries** ship multiple variants (safe, mt-safe, scoop-safe)

### How EWF Does It Right

EWF ships **6 variants** of wsf:
```
wsf.ecf              -- basic
wsf-safe.ecf         -- void-safe
wsf-mt.ecf           -- multi-threaded
wsf-mt-safe.ecf      -- MT + void-safe
wsf-scoop.ecf        -- SCOOP
wsf-scoop-safe.ecf   -- SCOOP + void-safe
```

simple_* ships **1 variant** with inconsistent settings.

---

## Part 4: Package Distribution

### Iron (Eiffel's npm)

Eiffel has Iron: https://iron.eiffel.com

```bash
iron install http_client    # Install package
iron search json            # Search packages
iron publish                 # Publish your package
```

### simple_* Iron Status

| Library | package.iron | Iron Published |
|---------|--------------|----------------|
| All 30+ libraries | ❌ None | ❌ No |

**Current installation method:**
1. Git clone each repo manually
2. Set environment variable for each library
3. Add to ECF manually

**This is 2005-era distribution.**

### What package.iron Looks Like

```
package simple_json

project
    simple_json = "simple_json.ecf"

note
    title: Simple JSON
    description: "High-level JSON parsing and building for Eiffel"
    collection: simple_*
    tags: json,parser,builder,serialization
    license: MIT
    link[source]: https://github.com/ljr1981/simple_json

end
```

---

## Part 5: Gap Analysis

### What simple_* Provides That Eiffel Doesn't

| Library | Unique Value |
|---------|--------------|
| simple_markdown | No native markdown parser |
| simple_htmx | HTMX component generation |
| simple_csv | No simple CSV in standard lib |
| simple_validation | Fluent validation API |
| simple_logger | Structured JSON logging |
| simple_rate_limiter | Standalone rate limiting |
| simple_datetime | Age calculations, date ranges, nice formatting |
| simple_regex | Fluent builder, pre-built patterns |

### What simple_* Wraps (Usability Layer)

| simple_* | Wraps | Why It's Better |
|----------|-------|-----------------|
| simple_json | contrib/json | One-liner parsing vs callback soup |
| simple_xml | Gobo XML | Readable API vs enterprise verbosity |
| simple_regex | Gobo regexp | Fluent builder vs manual compilation |
| simple_uuid | ISE uuid | Cleaner API |
| simple_hash | ??? | Convenience wrappers |
| simple_process | ISE process | Simpler execution |

### What Eiffel Has That simple_* Should Wrap

| Eiffel Library | Suggested simple_* | Value Add |
|----------------|-------------------|-----------|
| http_client | simple_http | `http.get(url).json` vs callbacks |
| eel (encryption) | simple_encryption | `encrypt(data, key)` one-liner |
| wsf_compression | simple_compression | `compress(string)` / `decompress(string)` |
| preferences | simple_config | Load .env, YAML, with fallbacks |
| mongo | simple_mongo | Hide BSON complexity |
| argument_parser | simple_cli | Fluent subcommand builder |
| etar | simple_archive | `zip(files)` / `unzip(archive)` |
| i18n | simple_i18n | `t("hello.world")` with fallbacks |

### What's Missing From BOTH Ecosystems

| Gap | Description |
|-----|-------------|
| Message Queues | No RabbitMQ, Kafka, Redis pub/sub |
| Background Jobs | No delayed execution, job queues, retries |
| GraphQL | REST only |
| OpenAPI/Swagger | No spec generation from code |
| Metrics | No Prometheus, StatsD, counters/gauges |
| Distributed Tracing | No OpenTelemetry |
| Cloud Storage | No S3/Azure/GCS abstraction |

---

## Part 6: Honest Comparison

### API Usability: simple_* Wins

| Task | Eiffel Native | simple_* |
|------|---------------|----------|
| Parse JSON | Create parser, callbacks, events | `parse_json(str)` |
| Regex match | Create RX_PCRE, compile, match, extract | `regex.match(str).value` |
| Format date | DATE_TIME_CODE_STRING format codes | `date.to_human` |
| Validate email | Write your own | `is_valid_email(str)` |
| Log with fields | Manual string building | `logger.with("user", id).info("Login")` |
| Build XML | Verbose node creation | Fluent builder |

### Production Readiness: Eiffel Native Wins

| Criteria | Eiffel Native | simple_* |
|----------|---------------|----------|
| Void-Safety | Enforced | Inconsistent |
| SCOOP Support | Multiple variants shipped | 7/30 libraries |
| Package Distribution | Iron packages | Manual git clone |
| Documentation | README + Iron metadata | README only |
| Test Coverage | Comprehensive | Variable |
| Maintenance | Eiffel Software backed | Single maintainer |

---

## Part 7: Recommendations

### Immediate Actions

1. **Standardize ALL ECFs** with explicit capabilities:
```xml
<capability>
    <concurrency support="scoop" use="thread"/>
    <void_safety support="all"/>
</capability>
```

2. **Create package.iron for every library**

3. **Audit void-safety** - Run all libraries through void-safe compilation

### Short-Term Actions

4. **Ship SCOOP-safe variants** for critical libraries (at minimum: json, regex, datetime, logger)

5. **Create simple_http** wrapping http_client - This is the biggest missing piece

6. **Create simple_encryption** wrapping EEL

7. **Create simple_compression** wrapping wsf_compression or zlib

### Long-Term Actions

8. **Publish to Iron repository**

9. **Create simple_config** for unified configuration

10. **Consider CI/CD pipeline** that enforces void-safety and runs SCOOP tests

---

## Part 8: Final Verdict

### What simple_* Is
A **usability layer** that makes Eiffel's existing capabilities accessible to developers who don't want to wrestle with verbose, callback-heavy APIs.

### What simple_* Is Not
A **production-ready library suite** - inconsistent quality standards, no package distribution, and spotty SCOOP support make it unsuitable for enterprise use without significant remediation.

### The Path Forward
1. Fix the foundation (void-safety, SCOOP, Iron)
2. Fill the gaps (HTTP client, encryption, compression)
3. Keep the usability focus - that's the actual value proposition

### Bottom Line
The criticism from Eiffel Software is **valid but incomplete**. Yes, SCOOP support is inconsistent. But the bigger issues are:
- No Iron packages
- No void-safety enforcement
- No variant shipping
- 8+ libraries with undefined capabilities

The usability improvements are real and valuable. The engineering discipline is not there yet.
