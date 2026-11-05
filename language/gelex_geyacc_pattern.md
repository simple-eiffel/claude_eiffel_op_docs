# Pattern: grammar-built parsers in a simple_* library (gelex + geyacc)

Use this when a library reads a small text language: references, queries, commands, config. The grammar files become the specification of every accepted form, and geyacc proves the grammar has exactly one reading for each input (zero conflicts).

Worked example: `D:\prod\_gobo-work\06-grammar-spike` (Bible references and search queries for simple_bible, 2026-10-22).

## 1. Layout

```
<lib>/
  grammar/<name>_scanner.l     gelex input (tokens)
  grammar/<name>_parser.y      geyacc input (grammar + actions)
  src/generated/               gelex/geyacc OUTPUT: committed, never hand-edited
  src/<name>_syntax_*.e        plain syntax-tree classes the actions build
  src/<name>_grammar_parser.e  hand-written adapter: syntax -> the library's own result type
  regenerate.sh                runs gelex + geyacc; fails on any conflict
```

**Split the work in two:**
- **The grammar decides what is well formed.** It builds a syntax tree of text and positions only.
- **The adapter decides what that means:** lookups, legal numbers, defaults. It also keeps the library's frozen contract (signature and postconditions) unchanged.

## 2. ECF: only the skeletons

```xml
<library name="gobo_kernel"      location="$GOBO_LIBRARY/kernel/library.ecf"/>
<library name="gobo_lexical_skl" location="$GOBO_LIBRARY/lexical/library_skl.ecf"/>
<library name="gobo_parse_skl"   location="$GOBO_LIBRARY/parse/library_skl.ecf"/>
```

- These are the runtime skeletons: 11 + 4 classes, plus Gobo kernel.
- **Do NOT use `lexical/library.ecf` or `parse/library.ecf`.** Those are gelex's and geyacc's own internals. They don't contain `YY_*_SKELETON`, so you get VTCT errors (unknown class).
- `$GOBO_LIBRARY` is the live `D:\prod\simple_gobo\library`, which is Gobo 26.10.
- The tools are in `D:\prod\gobo-26.10\gobo\bin` (gelex.exe, geyacc.exe). They are not on PATH.

## 3. Regenerate (ec.sh does not run gelex/geyacc)

```bash
( cd src/generated && gelex ../../grammar/x_scanner.l )
( cd src/generated && geyacc -v x_parser.output -t X_TOKENS -o x_syntax_parser.e ../../grammar/x_parser.y )
```

- **geyacc exits 0 even when it reports conflicts** (for example, "Parser contains 1 shift/reduce conflict."). The script must grep its output for `conflict` and fail.
- **Policy: zero conflicts.** If you use `%left`/`%right`, explain each one in a comment. It's better still to put precedence into the grammar's levels (Or_expr → And_expr → Unary), which needs no declarations.
- "Terminals which are not used" is expected for error tokens (`T_UNKNOWN`, `T_UNCLOSED`) that exist only so the error is reported at the right place.
- Commit the grammar AND the generated classes together, in the same commit.

## 4. Class shapes that compile first time

- **Scanner (.l header):** write `deferred class X_SCANNER`, inheriting `YY_COMPRESSED_SCANNER_SKELETON` and `X_TOKENS`.
  - If it isn't deferred, ISE uses `default_create` as its creation procedure and reports VEVI on the skeleton's tables.
- **Parser (.y header):** `class X_SYNTAX_PARSER` inherits `YY_PARSER_SKELETON` (rename `make as make_parser_skeleton`, `parse as yyparse`, redefine `report_error`) and `X_SCANNER` (rename `make` too).
  - `make` must call `make_with_buffer (Empty_buffer)` and then `make_parser_skeleton`.
- **Typed tokens** (`%token <T> T_WORD`) make geyacc declare an **attached** `last_t_value: T` in `X_TOKENS`.
  - Do not redeclare it in the scanner.
  - Create a placeholder for it in the parser's `make`.
- **Don't name a feature `text_count`.** `YY_SCANNER_SKELETON` already has one (VMFN).
- **Positions:** put `%option position` in the scanner. Then `position` is the token's first character, 1-based, counted in **characters** when you feed a `STRING_32` through `new_unicode_string_buffer (a_text)`.
  - At end of input (`last_token <= 0`), report `a_text.count + 1`.
- Give single-character punctuation that you need a position for (`,` `;`) a **typed token** (`T_COMMA`), not a character literal. Character-literal tokens carry no value.

## 5. Unicode: the trap

- Write non-ASCII characters in patterns as escapes, **`\u{2013}`, with braces**, and keep the `.l` file pure ASCII.
- A literal `–` or a no-break space in a BOM-less `.l` file is read as Latin-1 **bytes**. The scanner then matches UTF-8 byte sequences, never the character itself. No error is raised; the test just fails.
- Check: `yyMax_symbol_equiv_class` in the generated scanner is above 256 when the patterns name characters beyond Latin-1.
- Negated classes such as `[^ "()]` cover all of Unicode in the default mode. Hebrew and Greek words scan as words. `%option utf8` is not needed.

## 6. Tests

- Eiffel test files that hold non-ASCII manifest strings need a **UTF-8 BOM** and `{STRING_32}` literals. Without the BOM, ISE reads them as Latin-1.
- **Prove a rewrite with a differential run, old against new, over the same inputs:**
  - every existing test input;
  - a generated corpus of every form × variant (dashes, spaces, malformed input);
  - real text mined read-only.
- Every disagreement must be either a named, spec-backed cause or a fix. "Clean" means zero unexplained rows.
