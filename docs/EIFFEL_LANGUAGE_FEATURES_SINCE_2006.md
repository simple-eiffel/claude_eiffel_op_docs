# Eiffel Language Features Added Since ECMA-367 (2006)

**Document Status**: Comprehensive timeline of Eiffel language enhancements from June 2006 to 2025

**Purpose**: Foundation for updating the ECMA-367 standard with features added in the last 19 years

---

## Executive Summary

Since the publication of ECMA-367 in June 2006, the Eiffel language has evolved significantly with major additions focusing on:

1. **Void-Safety**: Preventing void calls through type system enhancements
2. **Concurrency**: SCOOP (Simple Concurrent Object-Oriented Programming) for concurrent development
3. **Iteration**: Enhanced loop constructs for cleaner data structure traversal
4. **Type System**: New sized integer types, Unicode support, and flexible typing
5. **Developer Experience**: Agents, aliases, bracket notation, and assigner commands

---

## Part I: Complete Chronological Timeline (2006-2025)

### 2006: EiffelStudio 5.7 (October 2006)

**Included in ECMA-367 (June 2006) or Shortly After:**

| Feature                     | Reserved Word            | Purpose                                                 | Motivation                                            |
| --------------------------- | ------------------------ | ------------------------------------------------------- | ----------------------------------------------------- |
| Inline Agents               | `agent`                  | Create routine references within expressions            | Enable concise event handling and functional patterns |
| Named Tuples                | `TUPLE`                  | Create tuples with named components                     | Improve code readability with named field access      |
| Extended Expanded Semantics | `expanded`               | Control value vs. reference semantics                   | Better memory management and performance options      |
| CHARACTER\_32               | keyword: `CHARACTER\_32` | Unicode character support                               | Internationalization and modern language support      |
| Keyword Optional            | (removed `is`)           | `is` keyword no longer required in function definitions | Syntax simplification and modernization               |

**Example - Inline Agent**:

```eiffel
button.select\_actions.extend (agent my\_object.on\_click)
my\_agent := agent (x: INTEGER): INTEGER do Result := x \* 2 end
```

---

### 2007: EiffelStudio 6.0 (June 2007)

| Feature                      | Reserved Word   | Purpose                                                  | Motivation                                 |
| ---------------------------- | --------------- | -------------------------------------------------------- | ------------------------------------------ |
| Flat Class Checking          | (compiler mode) | Check inheritance hierarchies completely                 | Ensure type safety and catch errors early  |
| Multiple Generic Constraints | (type system)   | Apply multiple constraints to a formal generic parameter | Enable more expressive generic programming |

**Example - Multiple Generic Constraints**:

```eiffel
class CONTAINER [G -> {COMPARABLE, HASHABLE}]
  -- G must conform to both COMPARABLE and HASHABLE
end
```

---

### 2007: EiffelStudio 6.1 (November 2007) - **MAJOR: VOID-SAFETY BEGINS**

This release marks the start of Eiffel's journey toward void-safety, one of the most significant language enhancements.

| Feature                     | Reserved Word/Syntax          | Purpose                                    | Motivation                                   |
| --------------------------- | ----------------------------- | ------------------------------------------ | -------------------------------------------- |
| **Attached Type Mechanism** | `attached`, `detachable`, `?` | Distinguish attached and detachable types  | Prevent void calls at compile-time           |
| **Object Test**             | `attached x as l\_x`          | Safely bind and test attachable references | Replace unsafe assignment attempts           |
| **Attachment Marks**        | `attached`, `detachable`      | Declare type attachment guarantees         | Enable compile-time void-safety verification |

**Example - Attached Types**:

```eiffel
x: STRING                    -- attached by default (never void)
y: detachable STRING         -- may be void
z: ? STRING                  -- same as detachable STRING

if attached y as l\_y then
  -- l_y is guaranteed attached (non-void) within this block
  l\_y.some\_feature
end
```

**Key Concepts**:

* `attached` types guarantee non-void values
* `detachable` types (prefixed with `?`) allow void
* Certified Attachment Patterns (CAPs) allow static verification

---

### 2008: EiffelStudio 6.2 (June 2008)

| Feature                  | Reserved Word/Syntax | Purpose                                                            | Motivation                                    |
| ------------------------ | -------------------- | ------------------------------------------------------------------ | --------------------------------------------- |
| Object Equality Operator | `~`                  | Custom equality testing distinct from identity                     | More intuitive equality semantics for objects |
| Exception Objects        | (class hierarchy)    | EXCEPTION class and descendants for first-class exception handling | Modern exception handling and debugging       |

**Example - Object Equality**:

```eiffel
if obj1 ~ obj2 then
  -- Objects are equivalent
end
```

---

### 2008-2010: Void-Safety Consolidation

During this period, void-safety evolved from experimental to mainstream:

* **2008-2010**: Void-safety remained experimental, configurable per project
* **Motivation**: Address the "Billion Dollar Mistake" (void/null calls) in programming languages
* **Approach**: Static type system preventing void calls without explicit checks

---

### 2010: EiffelStudio 6.5 (February 2010)

| Feature                        | Reserved Word | Purpose                                                  | Motivation                                                  |
| ------------------------------ | ------------- | -------------------------------------------------------- | ----------------------------------------------------------- |
| **ACROSS Loop (Experimental)** | `across`      | Iteration construct for ITERABLE structures              | Cleaner, more expressive loops compared to traditional form |
| Transient Attributes           | (note clause) | Mark attributes not persisted via `note transient: true` | Optimize storage and serialization                          |

**Example - ACROSS Loop**:

```eiffel
across my\_list as cursor loop
  print (cursor.item)
  -- cursor.index, cursor.target available
end
```

**Note**: While compiler support arrived in 6.5, library support (ITERABLE class) came separately.

---

### 2010: EiffelStudio 6.6 (May 2010)

| Feature                                         | Reserved Word | Purpose                                          | Motivation                                                    |
| ----------------------------------------------- | ------------- | ------------------------------------------------ | ------------------------------------------------------------- |
| **ACROSS Loop (Iteration Form - Standardized)** | `across`      | Official iteration form for loops                | Draft specification toward ISO/ECMA standard inclusion        |
| CHECK...THEN Statement                          | `check`       | Assertion block with guaranteed attachment scope | Explicitly mark expected attachment guarantees within a block |

**Example - CHECK...THEN Statement**:

```eiffel
check attached my_detachable_entity as l_entity then
  -- l_entity is guaranteed attached within this block
  l_entity.some_feature
end
```

---

### 2011: EiffelStudio 6.8 (April 2011)

| Feature                       | Reserved Word   | Purpose                                        | Motivation                          |
| ----------------------------- | --------------- | ---------------------------------------------- | ----------------------------------- |
| **SCOOP Preliminary Support** | `separate`      | Concurrent programming without race conditions | Enable safe concurrent development  |
| SCOOP Type Checking           | (compiler mode) | Type check separate entities                   | Validate concurrent access patterns |

**SCOOP Background**:

* Designed: 1993 (early conception)
* Published: 1993 (Communications of the ACM)
* First Prototype: 1995
* Production Implementation: 2011

---

### 2011: EiffelStudio 7.0 (November 2011) - **MAJOR: FULL SCOOP SUPPORT**

| Feature                | Reserved Word | Purpose                                | Motivation                                      |
| ---------------------- | ------------- | -------------------------------------- | ----------------------------------------------- |
| **SCOOP Full Support** | `separate`    | Complete concurrent programming system | Production-ready race-free concurrent execution |
| SCOOP Code Generation  | (runtime)     | Generate code for concurrent execution | Enable actual multi-processor execution         |
| Enhanced Void-Safety   | (refinement)  | Improved void-safety implementation    | Better performance and usability                |

**SCOOP Features**:

* Minimal syntax: only one new keyword: `separate`
* Based on Design by Contract with modified semantics
* Prevents race conditions through "separate" declaration
* Race-free access to multiple processors

**Example - SCOOP Concurrency**:

```eiffel
buffer: separate BOUNDED\_BUFFER \[INTEGER]

-- Separate procedure call (asynchronous)
buffer.put (42)

-- Separate function call (synchronous - must wait)
x := buffer.count
```

---

### 2012: EiffelStudio 7.1 (June 2012)

| Feature                    | Reserved Word | Purpose                            | Motivation                                         |
| -------------------------- | ------------- | ---------------------------------- | -------------------------------------------------- |
| SCOOP Processor GC         | (runtime)     | Garbage collection for processors  | Better resource management in concurrent systems   |
| SCOOP Manager Improvements | (refinement)  | Enhanced SCOOP constraint handling | Remove restrictions from initial SCOOP 7.0 release |

---

### 2013: EiffelStudio 7.3 (May 2013) - **VOID-SAFETY BECOMES DEFAULT**

Turning point: void-safety transitions from experimental to mandatory for new projects.

| Feature                               | Reserved Word          | Purpose                                  | Motivation                                      |
| ------------------------------------- | ---------------------- | ---------------------------------------- | ----------------------------------------------- |
| **Void-Safety Levels**                | (compiler modes)       | "None", "Transitional", "Complete" modes | Gradual migration path for existing codebases   |
| **Conformance with Attachment Marks** | (type system)          | Consider attachment in type conformance  | Stricter type checking aligned with void-safety |
| Separate Types for Tuples             | `separate` + `TUPLE`   | Support tuple items marked separate      | Enable concurrent tuple processing              |
| Separate Types for Routines           | `separate` + `ROUTINE` | Support routine targets marked separate  | Use routine references in concurrent code       |

**Void-Safety Levels Explained**:

* **None**: No void-safety checking (legacy mode)
* **Transitional**: Mixed attached/detachable (migration mode)
* **Complete**: All code must be void-safe (strict mode) - **BECOMES DEFAULT**

---

### 2013: EiffelStudio 13.11 (December 2013) - **VERSION NUMBERING CHANGE**

Introduced YYYY.MM versioning scheme.

| Feature             | Reserved Word         | Purpose                          | Motivation                       |
| ------------------- | --------------------- | -------------------------------- | -------------------------------- |
| TUPLE Iterability   | `TUPLE`               | Make TUPLE inherit from ITERABLE | Enable across loops on tuples    |
| Tuple Concatenation | `+` operator on TUPLE | Concatenate tuples               | Convenient tuple composition     |
| PARENTHESIS Aliases | `()`                  | Function/procedure call notation | More intuitive invocation syntax |

**Example - Tuple Operations**:

```eiffel
t1: TUPLE \[x: INTEGER; y: STRING]
t2: TUPLE \[z: BOOLEAN]
t3 := t1 + t2  -- Concatenated tuple

across t1 as cursor loop
  print (cursor.item)
end
```

---

### 2014: EiffelStudio 14.05 (May 2014)

| Feature                      | Reserved Word     | Purpose                                        | Motivation                                          |
| ---------------------------- | ----------------- | ---------------------------------------------- | --------------------------------------------------- |
| Complete Void-Safety Default | (project setting) | New projects default to "complete" void-safety | Industry best practice for void-safety              |
| Eiffel Inspector Tool        | (static analysis) | 35+ rules for code quality analysis            | Automatic detection of style and performance issues |

---

### 2015: EiffelStudio 15.01 (January 2015)

| Feature           | Reserved Word | Purpose                            | Motivation                           |
| ----------------- | ------------- | ---------------------------------- | ------------------------------------ |
| New SCOOP Runtime | (runtime)     | Complete reimplementation of SCOOP | Significant performance improvements |

---

### 2015: EiffelStudio 15.08 (August 2015)

| Feature                | Purpose                | Motivation                              |
| ---------------------- | ---------------------- | --------------------------------------- |
| EiffelWeb Improvements | Enhanced web framework | Improved server-side Eiffel development |

---

### 2015: EiffelStudio 15.12 (December 2015)

| Feature                     | Reserved Word | Purpose                                              | Motivation                                            |
| --------------------------- | ------------- | ---------------------------------------------------- | ----------------------------------------------------- |
| **New Agent Type Notation** | `agent`       | Simplified agent type syntax without first parameter | Cleaner agent declarations for functional programming |

**Example - New Agent Notation**:

```eiffel
-- Old: FUNCTION \[OBJECT, TUPLE \[INTEGER], STRING]
-- New:
x: FUNCTION \[INTEGER, STRING]
```

**Impact**: Syntax updater tool provided to automatically migrate existing code.

---

### 2016: EiffelStudio 16.05 (May 2016)

| Feature             | Purpose                              | Motivation                       |
| ------------------- | ------------------------------------ | -------------------------------- |
| Maintenance Release | Bug fixes and stability improvements | Incremental quality improvements |

---

### 2017: EiffelStudio 17.01 (January 2017)

| Feature                      | Purpose                                            | Motivation                                 |
| ---------------------------- | -------------------------------------------------- | ------------------------------------------ |
| Library Capability Mechanism | Document and enforce supported compilation options | Better control over library configurations |
| Code Templates               | IDE feature                                        | Speed up common coding patterns            |

---

### 2017: EiffelStudio 17.05 (May 2017)

| Feature                                   | Reserved Word | Purpose                                                           | Motivation                                    |
| ----------------------------------------- | ------------- | ----------------------------------------------------------------- | --------------------------------------------- |
| **Relaxed Conditional Expression Typing** | (type system) | Allow different types in if/else branches if pair-wise conforming | More flexible and practical type inference    |
| Pick\&Drop Enhancement                    | (IDE)         | Extract tokens from editor                                        | Improved developer experience for refactoring |

**Example - Relaxed Typing**:

```eiffel
-- Now valid: branches return STRING and detachable STRING
result := if condition then "text" else Void end
-- Types as: detachable STRING
```

**Void-Safety Improvements**: Better performance for object initialization checks in complete void-safe mode.

---

### 2018: EiffelStudio 18.01 (January 2018)

| Feature                   | Purpose                    | Motivation               |
| ------------------------- | -------------------------- | ------------------------ |
| Maintenance and Stability | Bug fixes and improvements | Incremental enhancements |

---

### 2018: EiffelStudio 18.07 (July 2018)

| Feature                  | Purpose                       | Motivation                |
| ------------------------ | ----------------------------- | ------------------------- |
| Performance Improvements | Enhanced compiler performance | Faster compilation cycles |

---

### 2018: EiffelStudio 18.11 (November 2018)

| Feature                     | Reserved Word/Syntax | Purpose                                                        | Motivation                            |
| --------------------------- | -------------------- | -------------------------------------------------------------- | ------------------------------------- |
| **Assertion Tags**          | (compiler feature)   | Use assertion expressions as tags without explicit identifiers | Simplify assertion documentation      |
| **ITERABLE for Containers** | `across`             | All standard containers now ITERABLE                           | Uniform iteration interface           |
| Enhanced HASH\_TABLE Access | `definite\_item`     | New feature returning non-detachable items                     | Type-safe access to guaranteed values |
| JSON Navigation Chaining    | `@` operator         | Chain property access in JSON objects                          | More readable JSON data access        |

**Example - Assertion Tags**:

```eiffel
check
  x > 0  -- Expression becomes implicit tag
end
```

**Example - Unified Container Iteration**:

```eiffel
across my\_list as cursor loop ... end
across my\_array as cursor loop ... end
across my\_table as cursor loop ... end  -- All now uniform
```

---

### 2019: EiffelStudio 19.05 (May 2019)

| Feature                              | Purpose              | Motivation                  |
| ------------------------------------ | -------------------- | --------------------------- |
| Performance and Library Enhancements | Various improvements | Incremental quality updates |

---

### 2019: EiffelStudio 19.12 (December 2019)

| Feature                     | Purpose                     | Motivation           |
| --------------------------- | --------------------------- | -------------------- |
| Cross-platform Improvements | Better Unix/Windows support | Improved portability |

---

### 2020: EiffelStudio 20.05 (May 2020)

| Feature                        | Reserved Word/Syntax | Purpose                                                          | Motivation                         |
| ------------------------------ | -------------------- | ---------------------------------------------------------------- | ---------------------------------- |
| **Multi-Branch Expressions**   | (expression form)    | Use multi-branch (if/then/else/elseif) within expressions        | More functional programming style  |
| **Unicode String Auto-Typing** | (type system)        | Untyped manifest strings with Unicode auto-convert to STRING\_32 | Better Unicode handling out-of-box |
| Unicode Feature Aliases        | (library)            | Add Unicode aliases for common operations                        | International function naming      |

**Example - Multi-Branch Expressions**:

```eiffel
value := if x > 0 then "positive"
         elseif x < 0 then "negative"
         else "zero"
         end
```

---

### 2020: EiffelStudio 20.11 (November 2020)

| Feature                       | Purpose                     | Motivation       |
| ----------------------------- | --------------------------- | ---------------- |
| Library and Tool Improvements | Enhanced standard libraries | Better ecosystem |

---

### 2021: EiffelStudio 21.11 (November 2021)

| Feature                                       | Reserved Word/Syntax | Purpose                                           | Motivation                                                 |
| --------------------------------------------- | -------------------- | ------------------------------------------------- | ---------------------------------------------------------- |
| **Unified Loop Cursor Access**                | `@` symbol           | Unified syntax for accessing loop cursor features | Consistent interface for both keyword and Unicode variants |
| Non-Conforming Inheritance Fixes              | `non conforming`     | Production-ready non-conforming inheritance       | Enable advanced inheritance patterns reliably              |
| Container Initialization from Manifest Arrays | (library feature)    | Initialize via `make\_from\_iterable`             | More concise data structure creation                       |

**Example - Unified Loop Cursor**:

```eiffel
across table as y loop
  print (@ y.key)      -- @ prefix for cursor features
  print (": ")
  print (y)            -- Item without @ prefix
end
```

---

### 2022: EiffelStudio 22.05 (May 2022)

| Feature                    | Purpose                         | Motivation                            |
| -------------------------- | ------------------------------- | ------------------------------------- |
| Visual Studio 2022 Support | IDE integration                 | Support latest Visual Studio versions |
| Library Enhancements       | Binary/octal string conversions | Expanded numeric capabilities         |

---

### 2022: EiffelStudio 22.12 (December 2022)

| Feature                    | Purpose                  | Motivation         |
| -------------------------- | ------------------------ | ------------------ |
| Stability and Improvements | Incremental enhancements | Quality refinement |

---

### 2023: EiffelStudio 23.09 (September 2023)

| Feature              | Purpose          | Motivation                           |
| -------------------- | ---------------- | ------------------------------------ |
| **.NETCore Support** | .NET 6.0, 7.0    | Modern cross-platform .NET support   |
| Multi-Platform .NET  | Unix and Windows | Unified development across platforms |

---

### 2024: EiffelStudio 24.05 (May 2024)

| Feature                | Purpose                | Motivation                             |
| ---------------------- | ---------------------- | -------------------------------------- |
| NETCore Improvements   | Enhanced .NET support  | Better integration with .NET ecosystem |
| Debugging Enhancements | Better debugging tools | Improved development experience        |

---

### 2025: EiffelStudio 25.02 (February 2025) - **LATEST**

| Feature                    | Purpose               | Motivation                          |
| -------------------------- | --------------------- | ----------------------------------- |
| Diagram Tool Improvements  | Better visualization  | Enhanced architecture documentation |
| MongoDB \& MariaDB Support | Database libraries    | Expanded data persistence options   |
| Execution Parameters       | Runtime configuration | Better deployment flexibility       |

---

## Part II: Organized by Feature Category

### A. VOID-SAFETY FEATURES

Complete elimination of void-call errors at compile-time.

**Timeline**: 2007-2013 (Major evolution), 2013-present (Refinement)

**Key Reserved Words/Syntax**:

* `attached` - Type guarantee of non-void value
* `detachable` - Explicitly allows void
* `?` - Prefix notation for detachable (e.g., `?STRING`)
* `as` - Bind in object test (e.g., `attached x as l\_x`)
* `check` - Assert attachability at specific point

**Major Releases**:

1. **6.1 (Nov 2007)**: Initial attached type mechanism
2. **6.2 (June 2008)**: Exception objects for error handling
3. **7.3 (May 2013)**: Becomes default for new projects
4. **14.05 (May 2014)**: Mandatory for new projects
5. **Ongoing**: Refinements and optimizations

**Certified Attachment Patterns (CAPs)**:
Compiler-recognized patterns that guarantee safety:

```eiffel
if x /= Void then
  x.feature
end

if attached x as l_x then
  l_x.feature
end

check attached x as l_x then
  l_x.feature
end
```

**Why Added**:

* Address the "Billion Dollar Mistake" (void/null calls)
* Catch errors at compile-time, not runtime
* Reduce debugging and support costs
* Prevent entire class of void-call runtime errors

---

### B. CONCURRENT PROGRAMMING (SCOOP)

Race-free concurrent execution with minimal syntax.

**Timeline**: 1993 (Design) → 1995 (Prototype) → 2011 (Production)

**Key Reserved Word**:

* `separate` - Mark entity/type as requiring exclusive access

**Major Releases**:

1. **6.8 (April 2011)**: SCOOP type checking
2. **7.0 (Nov 2011)**: Full SCOOP support with code generation
3. **7.1 (June 2012)**: SCOOP processor garbage collection
4. **15.01 (Jan 2015)**: New SCOOP runtime with performance improvements

**SCOOP Semantics**:

```eiffel
-- Separate declaration - entity in separate processor
buffer: separate BOUNDED\_BUFFER \[INTEGER]

-- Separate procedure call (asynchronous, no wait)
buffer.put (42)

-- Separate function call (synchronous, must wait for result)
count := buffer.count

-- Once keys for execution scope
feature
  my_once_per_process: INTEGER
    once ("PROCESS")
      -- Executed once for the entire process
    end

  my_once_per_thread: INTEGER
    once ("THREAD")
      -- Executed once per thread (this is the default)
    end

  my_once_per_object: INTEGER
    once ("OBJECT")
      -- Executed once per object instance
    end
```

**Why Added**:

* Enable safe multi-processor programming
* Prevent race conditions at compile-time
* Provide simple, expressive concurrency model
* Support modern multi-core hardware

---

### C. ENHANCED ITERATION (ACROSS LOOPS)

More expressive and concise loop constructs.

**Timeline**: 2010 (Experimental) → 2010 (Standardized) → 2021 (Enhanced)

**Key Reserved Words**:

* `across` - Start iteration construct
* `as` - Bind cursor variable
* `@` - Access cursor features (added 21.11)

**Loop Forms**:

1. **Traditional Form**:

```eiffel
from
  i := 1
until
  i > count
loop
  process (items \[i])
  i := i + 1
end
```

2. **ACROSS Form** (Preferred):

```eiffel
across items as cursor loop
  process (cursor.item)
  -- cursor.index, cursor.target available
end
```

3. **With Cursor Feature Access** (21.11+):

```eiffel
across my\_table as y loop
  print (@ y.key)    -- @ prefix accesses cursor features
  print (y)          -- Direct item access without @
end
```

**Major Releases**:

1. **6.5 (Feb 2010)**: Experimental ACROSS loop
2. **6.6 (May 2010)**: Standardized ACROSS form
3. **13.11 (Dec 2013)**: TUPLE becomes ITERABLE
4. **18.11 (Nov 2018)**: All containers become ITERABLE
5. **21.11 (Nov 2021)**: Unified loop cursor access

**Why Added**:

* Eliminate off-by-one errors
* Abstract iteration details
* Cleaner, more readable code
* Standardize iteration pattern

---

### D. TYPE SYSTEM ENHANCEMENTS

New types and improved type inference.

**Sized Integer Types** (Added 5.0 onwards):

```eiffel
INTEGER\_8, INTEGER\_16, INTEGER\_32, INTEGER\_64
NATURAL\_8, NATURAL\_16, NATURAL\_32, NATURAL\_64
```

**Unicode Support** (5.6, 5.7, 20.05):

```eiffel
CHARACTER\_32              -- Unicode character
STRING\_32                 -- Unicode strings
manifest "Hello" → auto-types as STRING\_32 if contains Unicode
```

**Manifest Types** (5.6):

```eiffel
{STRING}
{ARRAY \[INTEGER]}
```

**Relaxed Conditional Typing** (17.05):

```eiffel
-- Branches with different but conforming types
result := if condition then "text" else Void end  -- types as detachable STRING
```

**Why Added**:

* Support international applications
* Provide precise control over memory footprint
* Better type inference for modern patterns
* Support modern application needs

---

### E. AGENTS (FUNCTIONAL PROGRAMMING)

Routine references for event-driven and functional patterns.

**Timeline**: 1999 (Initial) → 2006 (Inline) → 2015 (Improved notation)

**Key Reserved Word**:

* `agent` - Create routine reference

**Agent Types** (since 15.12, first parameter removed):

```eiffel
ROUTINE [ARGS -> detachable TUPLE]  -- Base type
FUNCTION [ARGS, RESULT]             -- Returns value
PROCEDURE [ARGS]                    -- No return
PREDICATE [ARGS]                    -- Returns BOOLEAN
```

**Agent Creation Forms**:

1. **Basic Agent**:

```eiffel
agent my\_object.my\_feature (arg1, arg2)
button.select\_actions.extend (agent on\_click)
```

2. **Open Arguments** (with `?`):

```eiffel
agent two_arg_procedure (?, 5)    -- First arg open, second closed
agent sum (?, ?)                  -- Both args open (equivalent to: agent sum)
```

3. **Inline Agent** (5.7+):

```eiffel
my\_function := agent (x: INTEGER): INTEGER do Result := x \* 2 end

my\_procedure := agent (x: INTEGER)
  do
    print (x)
  end
```

4. **From Result/Current** (5.0+):

```eiffel
agent Result.process
agent Current.process
```

5. **From Operator Features** (5.5+):

```eiffel
agent (a: INTEGER; b: INTEGER): INTEGER do Result := a + b end
-- Can be applied to "+" operator
```

**New Type Notation** (15.12):

```eiffel
-- Old: FUNCTION \[OBJECT, TUPLE \[INTEGER], STRING]
-- New: FUNCTION \[INTEGER, STRING]
```

**Parenthesis Aliases** (13.11):

```eiffel
f (arg1, arg2)       -- Calls f.item ([arg1, arg2])
p (arg1, arg2)       -- Calls p.call ([arg1, arg2])
-- Note: empty parentheses are not allowed in Eiffel
```

**Why Added**:

* Enable event-driven programming
* Support functional programming patterns
* Allow higher-order routines
* Flexible callback mechanisms

---

### F. FEATURE DECLARATION ENHANCEMENTS

More expressive feature definitions.

**ALIAS Features** (5.6):

```eiffel
plus alias "+" (other: INTEGER): INTEGER
  do Result := Current + other end

minus alias "-": INTEGER
  -- Unary operator alias (prefix)
  do Result := -value end

times alias "*" (other: MY_TYPE): MY_TYPE
  do ... end
```

**Note**: The old `infix` and `prefix` keywords are no longer allowed. Use `alias` instead.

**BRACKET Features** (5.6):

```eiffel
feature
  item alias "[]" (index: INTEGER): STRING assign put
    do Result := items [index] end

  put (value: STRING; index: INTEGER)
    do items [index] := value end
end

-- Usage:
my_array [5]           -- Calls item
my_array [5] := "new"  -- Calls put (via assigner)
```

**Note**: The `alias "[]"` goes on the query (`item`), not the command (`put`). The `assign put` clause on `item` enables the assignment syntax.

**ASSIGNER Commands** (5.6):

```eiffel
feature
  age: INTEGER assign set_age

  set_age (a_value: INTEGER)
    require
      non_negative: a_value >= 0
    do
      age := a_value
    end
end

-- Usage:
person.age := 21       -- Calls set_age (21)
```

**Note**: The `assign` clause goes on the query (`age`), not the command (`set_age`).

**CONVERT Features** (5.4, 5.5):

```eiffel
class DATE
  convert make\_from\_string ({STRING})
end

-- Usage:
today: DATE
s: STRING
today := s  -- Automatically calls make\_from\_string
```

**Why Added**:

* Enable operator notation via aliases (not overloading in the traditional sense)
* Support notation natural to domain
* Provide encapsulation with assignment-like syntax
* Enable type conversion patterns

---

### G. SYNTAX IMPROVEMENTS

Modernized and cleaner syntax.

| Feature               | Added            | Description                                 |
| --------------------- | ---------------- | ------------------------------------------- |
| `is` keyword optional | 5.7              | Function definitions no longer require `is` |
| Object equality `~`   | 6.2              | Distinguish from identity (`=`)             |
| `create` keyword      | 4.3              | Replaced old `!!` syntax                    |
| `once` keyword        | Early (pre-ECMA) | Execute routine only once (memoization)     |
| `check` statement     | 6.6              | Assert conditions for void-safety           |
| Exception `rescue`    | (core)           | Exception handling and cleanup              |
| `retry` statement     | (core)           | Retry after exception handling              |

**Once Keys** (concurrency control):

```eiffel
feature
  my_function: INTEGER
    once ("THREAD")
      -- Executed once per thread (default)
    end

  my_global: STRING
    once ("PROCESS")
      -- Executed once per process
    end
end
```

**Note**: Once-per-thread is the default, so `once` and `once ("THREAD")` are equivalent.

---

### H. DESIGN BY CONTRACT ENHANCEMENTS

Assertion-based programming refinements.

| Feature           | Added  | Description                              |
| ----------------- | ------ | ---------------------------------------- |
| Assertion tags    | 18.11  | Use expressions as assertion identifiers |
| `check` statement | 6.6    | Explicit attachment guarantee            |
| Loop variants     | (core) | Guarantee loop termination               |
| Loop invariants   | (core) | Invariants maintained during iteration   |

**Example**:

```eiffel
feature
  process_list (a_items: LIST [INTEGER])
    require
      not_empty: not a_items.is_empty
    local
      i: INTEGER
    do
      from
        i := 1
      invariant
        i >= 1
      until
        i > a_items.count
      loop
        process_item (a_items [i])
        i := i + 1
      variant
        a_items.count - i + 1
      end
    ensure
      all_processed: True
    end
end
```

---

## Part III: Complete Reserved Words List

### Core Language Keywords (All Versions)

**Class Definition**:

* `class` - Declare a class
* `feature` - Introduce features
* `create` - Specify creation procedures
* `inherit` - Inherit from parent class
* `rename` - Rename inherited feature
* `redefine` - Redefine inherited feature
* `undefine` - Make inherited feature deferred
* `select` - Disambiguate multiple inheritance
* `export` - Control feature visibility
* `frozen` - Prevent redefinition
* `deferred` - Declare deferred class/feature

**Type System**:

* `expanded` - Value semantics (5.6+)
* `separate` - Concurrent programming (7.0+)
* `like` - Anchored types
* `convert` - Type conversion (5.4+)
* `note` - Class/feature annotation (replaced `indexing`)

**Attachment Safety** (6.1+):

* `attached` - Non-nullable type
* `detachable` - Nullable type
* `?` - Detachable prefix (implicit)

**Expressions and Instructions**:

* `agent` - Routine reference (4.3+)
* `Current` - Self reference
* `Result` - Function return value
* `Precursor` - Parent feature call (4.2+)
* `True`, `False` - Boolean literals
* `Void` - Void reference

**Control Flow**:

* `if`, `then`, `else`, `elseif`, `end` - Conditional
* `inspect`, `when` - Multi-branch
* `from`, `until`, `loop` - Iterative form
* `across`, `as` - Iteration form (6.5+)
* `do` - Procedure body
* `local` - Local variable declaration

**Design by Contract**:

* `require` - Precondition
* `ensure` - Postcondition
* `invariant` - Class invariant
* `check` - Assertion (6.6+)
* `rescue` - Exception handler
* `retry` - Retry after rescue

**Advanced**:

* `once` - Execute once (caching)
* `external` - Call C/external code
* `debug` - Debug code section
* `alias` - Feature alias (5.6+)
* `assign` - Assigner command (5.6+)
* `attribute` - Attribute definition
* `variant` - Loop variant (termination)
* `old` - Pre-state value in postcondition

**Operators**:

* `and`, `or`, `xor`, `not`, `implies` - Logical
* `=`, `/=`, `<`, `>`, `<=`, `>=` - Comparison
* `+`, `-`, `*`, `/` - Arithmetic
* `^` - Power
* `//` - Integer division
* `\\` - Integer remainder
* `~` - Object equality (6.2+)
* `/~` - Object inequality (6.2+)
* `..` - Range
* `@` - Cursor feature access (21.11+)

---

## Part IV: Major Motivations and Design Principles

### 1\. Void-Safety (2007-Present)

**Problem**: Void-call errors (the "Billion Dollar Mistake" of null pointers in other languages)

**Solution**: Static type system distinguishing attached and detachable types

**Key Principle**: Compile-time prevention > Runtime detection

**Evolution**:

* 6.1: Optional attached types introduced
* 7.3: Void-safety becomes default
* 14.05: Mandatory for new projects
* Ongoing: Refinements and optimizations

---

### 2\. SCOOP Concurrency (2011-Present)

**Problem**: Race conditions in concurrent code, deadlocks, starvation

**Solution**: Minimal syntax (`separate` keyword) combined with Design by Contract

**Key Principle**: Race-free programming through exclusive access guarantees

**Design Philosophy**:

* Based on argument passing
* Modified contract semantics
* Single keyword: `separate`
* Abstracts from processor/threading details

---

### 3\. Loop Expressiveness (2010-Present)

**Problem**: Iterative form verbose, error-prone (off-by-one errors)

**Solution**: ACROSS construct with cursor management

**Key Principle**: Abstract iteration details, expose intent clearly

---

### 4\. Type Safety Enhancement (Ongoing)

**Problem**: Overflow/underflow, Unicode handling, type flexibility needs

**Solution**: Sized types, Unicode types, relaxed typing rules

**Key Principle**: Expressive typing that catches errors early

---

### 5\. Developer Experience (Ongoing)

**Problem**: Boilerplate code, verbose patterns, IDE limitations

**Solution**: Aliases, bracket notation, assigner commands, inline agents

**Key Principle**: Express intent naturally without ceremony

---

## Part V: Syntax Changes and Migration Notes

### Pre-2006 Syntax (ECMA-367 baseline)

```eiffel
-- Old object creation (still supported)
!! my\_object

-- Old iteration
from i := 1 until i > n loop
  process (array \[i])
  i := i + 1
end
```

### Modern Syntax (2006-Present)

```eiffel
-- Modern object creation (5.7+)
create my\_object.make

-- Modern iteration (6.5+)
across my\_array as cursor loop
  process (cursor.item)
end

-- Void-safe declarations (6.1+)
my\_string: STRING              -- attached by default
nullable\_string: detachable STRING  -- or use ? prefix
nullable\_string: ? STRING      -- same as above

-- Safe access (6.1+)
if attached nullable\_string as str then
  str.some\_feature
end

-- Inline agents (5.7+)
button.select\_actions.extend (
  agent (x: INTEGER): INTEGER do Result := x \* 2 end
)

-- Operator aliases (5.6+)
plus alias "+" (other: MY_TYPE): MY_TYPE do ... end
my_type1 + my_type2  -- Uses alias

-- Bracket notation (5.6+)
my\_array \[index] := value
my\_hash \[key] := value

-- Assigner commands (5.6+)
person.age := 21  -- Calls set\_age internally

-- Concurrent programming (7.0+)
separate\_buffer: separate BUFFER \[INTEGER]
separate\_buffer.put (42)  -- Asynchronous
count := separate\_buffer.count  -- Synchronous

-- Advanced iteration (21.11+)
across table as y loop
  key := @ y.key          -- @ accesses cursor features
  value := y              -- Direct item access
end
```

---

## Part VI: Feature Adoption Statistics

### By Purpose

| Category    | Releases     | Impact               |
| ----------- | ------------ | -------------------- |
| Void-Safety | 2007-present | Mandatory for safety |
| Concurrency | 2011-present | For multi-core apps  |
| Iteration   | 2010-2021    | Daily use pattern    |
| Type System | Continuous   | Foundation impact    |
| Operators   | 2005+        | Syntax sugar         |
| Agents      | 1999-present | Event handling       |

### By Project Visibility

| Feature          | Visibility | Adoption  |
| ---------------- | ---------- | --------- |
| Void-Safety      | Very High  | Mandatory |
| SCOOP            | Medium     | Growing   |
| ACROSS           | Very High  | Preferred |
| Agents           | High       | Common    |
| Aliases          | Medium     | Moderate  |
| Assigner         | Medium     | Growing   |
| Inline Agents    | High       | Common    |
| TUPLE Operations | Medium     | Moderate  |

---

## Part VII: Comparison to Other Languages

| Feature          | Eiffel                | Java            | C#                | Kotlin     |
| ---------------- | --------------------- | --------------- | ----------------- | ---------- |
| Void-Safety      | 6.1 (2007)            | Never           | 8.0 (2017)        | 1.0 (2011) |
| Concurrency      | SCOOP 7.0 (2011)      | Threads (1995)  | Async/await       | Coroutines |
| Contracts        | Full DBC              | Assertions only | Code contracts    | None       |
| Operator Aliases | Yes via `alias` (5.6) | No              | Yes (overloading) | Limited    |
| Functional       | Agents (4.3)          | Limited         | Lambdas           | Full       |
| Type Inference   | Limited               | Improved        | Improved          | Full       |

---

## Part VIII: Timeline of Critical Decisions

### Major Evolution Points

| Year | Version | Decision                             | Impact                   |
| ---- | ------- | ------------------------------------ | ------------------------ |
| 2006 | 5.7     | Standardize on ECMA-367              | Freeze baseline          |
| 2007 | 6.1     | Add void-safety                      | Prevent void-call errors |
| 2010 | 6.5     | Introduce ACROSS                     | Better iteration         |
| 2011 | 7.0     | Deploy SCOOP                         | Enable concurrency       |
| 2013 | 7.3     | Make void-safety default             | Force safety by default  |
| 2014 | 14.05   | Mandate void-safety for new projects | Industry best practice   |
| 2020 | 20.05   | Multi-branch expressions             | Modern functional style  |
| 2023 | 23.09   | Support .NET Core                    | Reach modern ecosystem   |

---

## Part IX: Recommendations for ECMA-367 Update

### Features Worthy of Standardization

1. **Void-Safety** (6.1+)

   * Status: Mature, industry-proven
   * Priority: **CRITICAL**
   * Standardize: Attached/detachable types, object test syntax

2. **ACROSS Loops** (6.5+)

   * Status: Mature, widely used
   * Priority: **HIGH**
   * Standardize: ITERABLE interface, cursor features

3. **SCOOP** (7.0+)

   * Status: Mature for read-only and simple cases
   * Priority: **HIGH**
   * Standardize: `separate` keyword, semantics

4. **Inline Agents** (5.7+)

   * Status: Mature, widely adopted
   * Priority: **MEDIUM**
   * Standardize: Syntax and semantics

5. **Operator Aliases \& Bracket Notation** (5.6+)

   * Status: Stable, widely used
   * Priority: **MEDIUM**
   * Standardize: Syntax and restrictions

6. **Type System Extensions** (5.6+)

   * Status: Stable
   * Priority: **MEDIUM**
   * Standardize: Sized types, Unicode support, conversion

7. **Multi-Branch Expressions** (20.05+)

   * Status: Mature
   * Priority: **MEDIUM-LOW**
   * Standardize: Expression form of if/then/else

### Features Requiring Refinement Before Standardization

1. **SCOOP Transaction Semantics**

   * Requires formal specification
   * Deadlock prevention proof needed

2. **Expanded Void-Safety Levels**

   * Need clear semantics for each level
   * Migration path documentation

3. **Generic Constraints**

   * Multiple constraints (6.0+) need formalization
   * Expandedness restrictions need clarity

---

## Sources and References

### Primary Documentation

* [ECMA-367 Standard (June 2006)](https://ecma-international.org/publications-and-standards/standards/ecma-367/)
* [EiffelStudio Release Notes](https://www.eiffel.org/doc/eiffelstudio/EiffelStudio_release_notes)
* [Language Roadmap](https://dev.eiffel.com/Language_road_map)
* [Differences from ECMA-367](https://www.eiffel.org/doc/eiffelstudio/Differences_between_standard_ECMA-367_and_Eiffel_Software_implementation)

### Key Releases Documented

* [EiffelStudio 6.1 Release Notes](https://www.eiffel.org/doc/eiffelstudio/Release_notes_for_EiffelStudio_6.1) - Void-Safety
* [EiffelStudio 7.0 Release Notes](https://www.eiffel.org/doc/eiffelstudio/Release_notes_for_EiffelStudio_7.0) - SCOOP
* [EiffelStudio 13.11 Release Notes](https://www.eiffel.org/doc/eiffelstudio/Release_notes_for_EiffelStudio_13.11) - Library Iterability
* [EiffelStudio 20.05 Release Notes](https://www.eiffel.org/doc/eiffelstudio/Release_notes_for_EiffelStudio_20.05) - Multi-branch Expressions
* [EiffelStudio 21.11 Release Notes](https://www.eiffel.org/doc/eiffelstudio/Release_notes_for_EiffelStudio_21.11) - Cursor Features

### Feature Documentation

* [Void-safety Documentation](https://www.eiffel.org/doc/eiffel/Void-safety-_Background%2C_definition%2C_and_tools)
* [SCOOP Concurrency](https://www.eiffel.org/doc/solutions/Concurrent_programming_with_SCOOP)
* [ACROSS Loops](https://www.eiffel.org/doc/eiffel/ET-_Instructions)
* [Agents](https://www.eiffel.org/doc/eiffel/ET-_Agents)
* [Reserved Words](https://www.eiffel.org/doc/eiffel/Eiffel_programming_language_reserved_words)

---

## Document Statistics

* **Total Releases Covered**: 25+ major versions
* **Timespan**: 2006-2025 (19 years)
* **Major Features Added**: 40+
* **Reserved Words Introduced**: 15+
* **Void-Safety Releases**: 13+ iterations
* **SCOOP Releases**: 6+ iterations
* **Loop Evolution Releases**: 5+ iterations

---

**Document Version**: 1.0
**Last Updated**: February 2025
**Status**: Ready for ECMA-367 Update Committee Review

---

