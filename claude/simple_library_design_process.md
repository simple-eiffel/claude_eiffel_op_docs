# simple_* Library Pre-Design/Build Process

## Overview

Before creating a new simple_* library, follow this comprehensive research and design process to ensure the library is world-class, addresses real developer needs, and anticipates future requirements.

## The Seven-Step Process

### Step 1: Deep Web Research - Specifications

Do deep-level web research to discover:
- RFCs (Request for Comments) relevant to the target domain
- ECMA, ISO, IEEE, and other formal specifications
- W3C recommendations (for web-related libraries)
- Industry standards and best practices documentation

**Example for simple_regex:**
- POSIX regex specification
- PCRE (Perl Compatible Regular Expressions) documentation
- Unicode Technical Standard #18 (Unicode Regular Expressions)
- ECMAScript RegExp specification

### Step 2: Research Latest Tech-Stack Libraries

Research the latest and most popular libraries/APIs in other languages:
- **JavaScript/TypeScript**: npm ecosystem leaders
- **Python**: PyPI top packages
- **Rust**: crates.io popular crates
- **Go**: Standard library and popular packages
- **Java**: Apache Commons, Guava patterns
- **C#/.NET**: BCL patterns and popular NuGet packages

Focus on:
- API design patterns that developers love
- Fluent interfaces and method chaining approaches
- Error handling strategies
- Performance optimization techniques
- Documentation and example patterns

### Step 3: Research Eiffel Ecosystem

Research existing Eiffel libraries beyond the standard library:
- **Gobo**: Comprehensive library suite (regex, XML, parsing, etc.)
- **Eiffel Loop**: Finnian Reilly's extensive library collection
- **Pylon**: Additional Eiffel libraries
- **EiffelStudio Contributions**: Community contributions
- **Historical Libraries**: ISE libraries, SmartEiffel heritage

Understand:
- What already exists and works well
- What gaps need filling
- What patterns are idiomatic to Eiffel
- Contract-based design opportunities

### Step 4: Research Developer Pain Points

Research common developer frictions and struggles:
- Stack Overflow questions and complaints
- GitHub issues on popular libraries
- Reddit discussions (r/programming, language-specific subs)
- Blog posts about "why X library is frustrating"
- Twitter/X developer complaints

Document:
- Verbose or confusing APIs
- Missing features developers commonly need
- Performance pitfalls
- Error handling frustrations
- Documentation gaps

### Step 5: Innovation Hat

Put on the innovator's hat and divine useful API features:
- What would make developers' lives easier?
- What patterns could be simplified or automated?
- What validations should happen automatically?
- What contracts can prevent common errors at compile time?
- What fluent patterns would make code more readable?
- What convenience methods address 80% of use cases?

Consider:
- Zero-configuration defaults that "just work"
- Progressive disclosure (simple API for simple cases, full power available)
- Fail-fast with clear error messages
- Integration with the simple_* ecosystem

### Step 6: Synthesize Design Strategy

Combine all research into a cohesive strategy:

#### A. Core Design Principles
- What makes this library "simple"?
- What are the non-negotiable features?
- What is explicitly out of scope?

#### B. API Surface Design
- Main entry point class(es)
- Fluent interface patterns
- Factory methods vs constructors
- Singleton patterns where appropriate

#### C. Contract Strategy
- Preconditions that catch common errors
- Postconditions that guarantee results
- Class invariants that maintain consistency

#### D. Integration Plan
- How does it fit in FOUNDATION_API?
- How does it fit in SERVICE_API?
- Dependencies on other simple_* libraries

#### E. Test Strategy
- Unit test coverage goals
- Edge cases to cover
- Performance benchmarks

### Step 7: Design/Implement/Strategy Report

Produce a comprehensive report containing:

1. **Executive Summary**: What this library does and why it matters
2. **Research Findings**: Key insights from steps 1-5
3. **Competitive Analysis**: How this compares to other solutions
4. **API Design**: Detailed class and feature specifications
5. **Contract Specifications**: Key contracts with rationale
6. **Implementation Roadmap**: Phased approach if needed
7. **Test Plan**: What will be tested and how
8. **Documentation Plan**: What docs are needed
9. **Integration Plan**: API layer integration strategy

---

## Checklist Before Starting Implementation

- [ ] Formal specifications reviewed
- [ ] Top 5 libraries in other languages studied
- [ ] Eiffel ecosystem (Gobo, Eiffel Loop, etc.) researched
- [ ] Developer pain points documented
- [ ] Innovation opportunities identified
- [ ] Design report written and reviewed
- [ ] API surface defined
- [ ] Contract strategy established
- [ ] Test plan created

---

## Template: Research Notes Structure

```
# simple_[name] Research Notes

## Specifications
- [List relevant RFCs, standards]

## Library Analysis
### JavaScript
- [Library name]: [Key insights]
### Python
- [Library name]: [Key insights]
### Rust
- [Library name]: [Key insights]
[etc.]

## Eiffel Ecosystem
- Gobo: [Relevant classes/features]
- Eiffel Loop: [Relevant classes/features]
- [Other sources]

## Pain Points
1. [Common complaint/friction]
2. [Common complaint/friction]

## Innovation Opportunities
1. [Idea and rationale]
2. [Idea and rationale]

## Design Decisions
- [Decision]: [Rationale]
```

---

## Eiffel Code/Test Cycle

### Project Structure Pattern

Follow the existing simple_* library structure:
```
simple_[name]/
  src/              -- Source files
  tests/            -- Test files
    [name]_test.e        -- Test class inheriting TEST_SET_BASE
    [name]_test_app.e    -- Test runner application
  docs/             -- Documentation including DESIGN.md
  simple_[name].ecf -- Configuration file
  README.md
```

### ECF Configuration Pattern

```xml
<!-- Library target (no root, all classes) -->
<target name="simple_[name]">
  <root all_classes="true"/>
  <file_rule>
    <exclude>/EIFGENs$</exclude>
    <exclude>/tests$</exclude>
  </file_rule>
  <!-- libraries and clusters -->
</target>

<!-- Test target (extends library, has root) -->
<target name="simple_[name]_tests" extends="simple_[name]">
  <root class="[NAME]_TEST_APP" feature="make"/>
  <library name="testing" location="$ISE_LIBRARY\library\testing\testing.ecf"/>
  <library name="testing_ext" location="$TESTING_EXT\testing_ext.ecf"/>
  <cluster name="tests" location=".\tests\" recursive="true"/>
</target>
```

### Test App Pattern

Follow the pattern from simple_logger:
```eiffel
class [NAME]_TEST_APP
create
  make
feature {NONE}
  make
    local
      tests: [NAME]_TEST
    do
      create tests
      io.put_string ("simple_[name] test runner%N")
      -- Run each test with run_test
      run_test (agent tests.test_xxx, "test_xxx")
      -- Print results
    end

  run_test (a_test: PROCEDURE; a_name: STRING)
    local
      l_retried: BOOLEAN
    do
      if not l_retried then
        a_test.call (Void)
        io.put_string ("  PASS: " + a_name + "%N")
        passed := passed + 1
      end
    rescue
      io.put_string ("  FAIL: " + a_name + "%N")
      failed := failed + 1
      l_retried := True
      retry
    end
end
```

### Compilation Commands

**CRITICAL**: Always compile from the project directory and use `-batch` flag.

```bash
# Set required environment variables
export TESTING_EXT=/d/prod/testing_ext

# Clean compile test target (run from project directory!)
cd /d/prod/simple_[name]
"/c/Program Files/Eiffel Software/EiffelStudio 25.02 Standard/studio/spec/win64/bin/ec.exe" \
  -batch -config simple_[name].ecf -target simple_[name]_tests -clean -c_compile

# Run tests
/d/prod/simple_[name]/EIFGENs/simple_[name]_tests/W_code/simple_[name].exe
```

### Key Points

1. **Always compile from project directory** - Running ec.exe with a relative config path from another directory causes EIFGENs to be created elsewhere

2. **Use -batch flag** - Ensures non-interactive mode

3. **Use -clean for fresh builds** - When switching targets or after major changes

4. **EIFGENs directory structure** - `EIFGENs/<target_name>/W_code/<system_name>.exe`

5. **Don't reinvent the wheel** - Copy patterns from existing simple_* libraries

6. **Reserved keywords** - Don't use `result` as variable names (use `l_result`)
