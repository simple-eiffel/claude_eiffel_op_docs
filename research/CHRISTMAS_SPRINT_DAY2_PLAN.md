# Christmas Sprint Day 2: Library Enhancement Plan

**Date:** December 6, 2025
**Purpose:** Expand 6 libraries to full spec compliance and address developer pain points

---

## Executive Summary

Based on deep research into industry specifications and developer pain points, each library needs enhancement to match production-grade requirements. This plan prioritizes high-impact improvements.

---

## 1. simple_smtp

### Current State
- RFC 5321 basic compliance
- AUTH LOGIN authentication
- Multipart MIME (text/html/attachments)
- TLS flags (but not implemented in socket)

### Gaps Identified

| Gap | Priority | Spec/Pain Point |
|-----|----------|-----------------|
| **No actual TLS/STARTTLS** | CRITICAL | RFC 8314 - sockets don't do TLS |
| No AUTH PLAIN support | HIGH | RFC 4954 requires PLAIN for interop |
| No OAuth2 authentication | HIGH | Modern providers require it |
| No connection pooling | MEDIUM | Performance pain point |
| No retry logic | MEDIUM | Common pain point |
| No Reply-To header | LOW | Common use case |
| No Date header | MEDIUM | RFC 5322 required |
| No Message-ID header | MEDIUM | RFC 5322 required |
| No email validation | LOW | Common pain point |
| No MIME boundary uniqueness | LOW | Potential collision |

### Tomorrow's Tasks

1. **Add required headers** (Date, Message-ID)
2. **Add AUTH PLAIN** authentication method
3. **Add Reply-To header** support
4. **Add set_reply_to feature**
5. **Improve boundary generation** (use UUID)
6. **Add email address validation**
7. **Document TLS limitation** (Eiffel socket constraints)
8. **Add tests for new features**

### Deferred (Requires External Libraries)
- TLS/SSL sockets (needs OpenSSL wrapper)
- OAuth2 (needs HTTP client)
- Connection pooling (advanced)

---

## 2. simple_csv

### Current State
- RFC 4180 compliant parsing
- Custom delimiters
- Header row handling
- Quoted field support
- CSV generation

### Gaps Identified

| Gap | Priority | Spec/Pain Point |
|-----|----------|-----------------|
| No streaming for large files | HIGH | Memory pain point |
| No encoding detection/BOM | HIGH | Excel pain point |
| No error handling/recovery | MEDIUM | Malformed input |
| No column type inference | MEDIUM | Convenience |
| No Excel sep= directive | LOW | Excel interop |
| No statistics/profiling | LOW | Data quality |
| No empty vs null distinction | MEDIUM | Common confusion |

### Tomorrow's Tasks

1. **Add UTF-8 BOM support** for Excel compatibility
   - `encode_for_excel: STRING` (adds BOM)
   - `parse_with_bom` detection
2. **Add error handling mode**
   - `set_lenient_mode` - skip/log bad rows
   - `last_parse_errors: LIST[STRING]`
3. **Add row iteration** for memory efficiency
   - `start_iteration`, `next_row`, `current_row`
4. **Add null handling**
   - `set_null_representation (a_string: STRING)`
   - `is_null (a_row, a_col): BOOLEAN`
5. **Add tests for new features**

### Deferred
- Full streaming parser (major refactor)
- Type inference (complex)

---

## 3. simple_uuid

### Current State
- UUID v4 (random) - 122 bits
- UUID v7 (timestamp) - RFC 9562
- Nil UUID
- Version detection
- String/compact formatting

### Gaps Identified

| Gap | Priority | Spec/Pain Point |
|-----|----------|-----------------|
| No v5 (SHA-1 namespace) | MEDIUM | Deterministic UUIDs |
| No Max UUID constant | LOW | RFC 9562 |
| RANDOM not CSPRNG | HIGH | Security concern |
| No monotonicity for v7 | MEDIUM | Database ordering |
| No v7 clock regression handling | MEDIUM | Time sync issues |
| No binary format output | LOW | Database storage |

### Tomorrow's Tasks

1. **Add Max UUID constant** (RFC 9562)
   - `max_uuid: ARRAY[NATURAL_8]`
   - `max_uuid_string: STRING`
2. **Add UUID v5** (SHA-1 namespace)
   - `new_v5 (a_namespace, a_name: STRING): ARRAY[NATURAL_8]`
   - Namespace constants (DNS, URL, OID, X500)
3. **Improve randomness**
   - Document RANDOM limitations
   - Consider seed from multiple entropy sources
4. **Add v7 monotonicity counter**
   - Track last timestamp
   - Increment counter for same-ms UUIDs
5. **Add tests for new features**

### Deferred
- CSPRNG (needs OS-level random)
- Clock regression handling (complex)

---

## 4. simple_jwt

### Current State
- HS256 (HMAC-SHA256) only
- Standard claims (iss, sub, aud, exp, nbf, iat, jti)
- Create and verify tokens
- Expiration checking

### Gaps Identified

| Gap | Priority | Spec/Pain Point |
|-----|----------|-----------------|
| No RS256/ES256 | HIGH | Asymmetric keys |
| No algorithm validation | CRITICAL | Security vulnerability |
| No "none" algorithm rejection | CRITICAL | Security vulnerability |
| No clock skew tolerance | MEDIUM | Distributed systems |
| No audience validation | MEDIUM | Token substitution |
| No key rotation/JWKS | LOW | Key management |
| No JWE (encryption) | LOW | Confidentiality |

### Tomorrow's Tasks

1. **Add algorithm whitelist validation** (CRITICAL)
   - `verify_with_algorithm (a_token: STRING; a_allowed_alg: STRING): BOOLEAN`
   - Reject if header alg doesn't match
2. **Add "none" algorithm rejection** (CRITICAL)
   - Check alg != "none" (case insensitive)
3. **Add clock skew tolerance**
   - `set_clock_skew (a_seconds: INTEGER)`
   - Apply to exp/nbf/iat validation
4. **Add audience (aud) validation**
   - `verify_with_audience (a_token, a_expected_aud: STRING): BOOLEAN`
5. **Add nbf (not before) validation**
   - Check current_time >= nbf
6. **Add jti claim helper**
   - `create_token_with_jti` auto-generates UUID
7. **Add tests for security features**

### Deferred
- RS256/ES256 (needs RSA/ECDSA crypto)
- JWKS (needs HTTP client)
- JWE (complex)

---

## 5. simple_hash

### Current State
- SHA-256 (pure Eiffel implementation)
- HMAC-SHA256
- MD5 (legacy, marked as insecure)

### Gaps Identified

| Gap | Priority | Spec/Pain Point |
|-----|----------|-----------------|
| No SHA-384/SHA-512 | MEDIUM | Stronger hashes |
| No SHA-1 | LOW | Legacy compatibility |
| No file hashing (streaming) | MEDIUM | Large file pain point |
| No constant-time comparison | HIGH | Timing attacks |
| No password hashing (bcrypt/Argon2) | LOW | Different use case |
| No HMAC-SHA512 | MEDIUM | Stronger HMAC |

### Tomorrow's Tasks

1. **Add SHA-512**
   - FIPS 180-4 compliant
   - 64-bit operations
   - `sha512 (a_input: STRING): STRING`
   - `sha512_bytes`: ARRAY[NATURAL_8]
2. **Add HMAC-SHA512**
   - `hmac_sha512 (a_key, a_message: STRING): STRING`
3. **Add constant-time comparison** (CRITICAL for security)
   - `secure_compare (a, b: STRING): BOOLEAN`
   - `secure_compare_bytes (a, b: ARRAY[NATURAL_8]): BOOLEAN`
4. **Add file hashing**
   - `sha256_file (a_path: STRING): STRING`
   - Stream-based, doesn't load entire file
5. **Add tests for new features**

### Deferred
- SHA-1 (deprecated anyway)
- bcrypt/Argon2 (different library scope)

---

## 6. simple_base64

### Current State
- RFC 4648 standard Base64
- URL-safe Base64URL
- Padding control
- Encode/decode strings and bytes

### Gaps Identified

| Gap | Priority | Spec/Pain Point |
|-----|----------|-----------------|
| No MIME Base64 (76-char lines) | MEDIUM | Email attachments |
| No whitespace handling in decode | MEDIUM | Common input issue |
| No streaming for large data | LOW | Memory efficiency |
| No data URI helper | LOW | Convenience |
| No encode from file | LOW | Convenience |

### Tomorrow's Tasks

1. **Add MIME Base64 encoding** (RFC 2045)
   - `encode_mime (a_input: STRING): STRING`
   - Line breaks every 76 characters
   - CRLF line endings
2. **Add whitespace-tolerant decoding**
   - `decode_lenient (a_input: STRING): STRING`
   - Strip whitespace before decoding
3. **Add data URI support**
   - `encode_data_uri (a_data, a_mime_type: STRING): STRING`
   - Returns `data:mime;base64,....`
   - `decode_data_uri (a_uri: STRING): TUPLE[data: STRING; mime: STRING]`
4. **Add tests for new features**

### Deferred
- Streaming (major refactor)
- File encoding (needs file I/O)

---

## Execution Order

### Morning Session (High Priority Security)

1. **simple_jwt** - Security fixes FIRST
   - Algorithm validation
   - "none" rejection
   - Clock skew

2. **simple_hash** - Security additions
   - Constant-time comparison
   - SHA-512

### Afternoon Session (Functionality)

3. **simple_smtp** - Required headers and auth
   - Date, Message-ID headers
   - AUTH PLAIN
   - Reply-To

4. **simple_csv** - Excel compatibility
   - UTF-8 BOM
   - Error handling
   - Null representation

5. **simple_uuid** - Completeness
   - Max UUID
   - UUID v5
   - Monotonicity

6. **simple_base64** - Convenience
   - MIME encoding
   - Whitespace handling
   - Data URI

---

## Test Requirements

Each enhancement needs:
1. Unit tests for happy path
2. Edge case tests
3. Error handling tests
4. AutoTest coverage tags

Minimum test additions per library:
- simple_jwt: +8 tests (security focus)
- simple_hash: +6 tests
- simple_smtp: +5 tests
- simple_csv: +5 tests
- simple_uuid: +5 tests
- simple_base64: +4 tests

**Total: ~33 new tests**

---

## Documentation Updates

After implementation:
1. Update each library's README with new features
2. Update API reference pages
3. Add security notes where applicable
4. Update HATS.md with any new patterns learned

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| TLS not implementable | Document as limitation, recommend external tools |
| SHA-512 complexity | Follow SHA-256 pattern exactly |
| Breaking changes | All new features are additive |
| Time constraints | Prioritize security fixes first |

---

## Success Criteria

- [ ] All security vulnerabilities addressed
- [ ] All new features have tests
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Code committed and pushed

---

**Estimated Lines of Code:** ~1,500-2,000 additions
**Estimated New Tests:** ~33
**Estimated Time:** 8-10 hours

---

*Generated: December 5, 2025*
*Next Session: December 6, 2025*
