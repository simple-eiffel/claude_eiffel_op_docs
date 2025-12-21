
## String Conversion Rules (NO OBSOLETE CODE)

**NEVER use implicit `as_string_8` conversions.** Always use explicit conversions:

| Situation | BAD (obsolete) | GOOD |
|-----------|----------------|------|
| substring on READABLE_STRING_8 | `l_str := readable.substring(1,5)` | `l_str := readable.substring(1,5).to_string_8` |
| Environment variable | `l_path := env.get("HOME")` | `l_path := env.get("HOME").to_string_8` |
| String concatenation | `err := "Error: " + msg` (if msg is STRING_32) | `err := "Error: " + msg.to_string_8` |

**Key types:**
- `READABLE_STRING_8` - parent of STRING_8, substring returns READABLE_STRING_8
- `STRING` = `STRING_8` - use this for local variables
- `STRING_32` - Unicode strings, need explicit `.to_string_8` for conversion

**Watch for these patterns (all cause obsolete warnings):**
1. Assigning `READABLE_STRING_8.substring()` to `STRING`
2. Concatenating `STRING_32` with `STRING_8` using `+`
3. Getting environment variables (often return STRING_32)
4. File path operations (PATH returns STRING_32)

