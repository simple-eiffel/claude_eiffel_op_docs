# Eiffel LLM Instruction Pairs - Design Discussion

**Date:** 2025-12-21
**Participants:** Larry, Claude
**Status:** In Progress

---

## What Are Instruction Pairs?

An **instruction pair** (also called instruction-tuning data) is a training example that teaches an LLM how to respond to requests. The format is typically:

```json
{
  "instruction": "What you want the model to do",
  "input": "Optional context or code to work with",
  "output": "The expected/correct response"
}
```

### Simple Example

```json
{
  "instruction": "Add Design by Contract preconditions to this Eiffel feature",
  "input": "set_balance (amount: REAL)\n  do\n    balance := amount\n  end",
  "output": "set_balance (amount: REAL)\n  require\n    non_negative: amount >= 0\n  do\n    balance := amount\n  ensure\n    balance_set: balance = amount\n  end"
}
```

### Why This Format?

When we fine-tune with these pairs, the model learns:
1. **Task recognition** - "Add DBC" means add require/ensure clauses
2. **Pattern application** - How to structure contracts for different scenarios
3. **Eiffel idioms** - Naming conventions, structure, style

After training, when a user asks "Add contracts to this feature," the model knows what to do because it's seen thousands of similar examples.

---

## Categories of Instruction Pairs for Eiffel

### 1. DBC (Design by Contract)
| Instruction Type | Example |
|------------------|---------|
| Add preconditions | "What preconditions should this feature have?" |
| Add postconditions | "Add ensure clause to guarantee the result" |
| Add class invariants | "What invariants should this class maintain?" |
| Fix contract violation | "This precondition is too weak, strengthen it" |
| Explain contracts | "Why does this feature have these contracts?" |

### 2. Void Safety
| Instruction Type | Example |
|------------------|---------|
| Fix void-safety error | "Fix VJAR error in this code" |
| Add attached checks | "Make this detachable access safe" |
| Convert to void-safe | "Refactor this legacy code for void safety" |
| Explain void safety | "Why is this assignment unsafe?" |

### 3. SCOOP (Concurrency)
| Instruction Type | Example |
|------------------|---------|
| Make concurrent-safe | "Refactor for SCOOP compatibility" |
| Add separate handling | "This needs separate argument handling" |
| Explain SCOOP pattern | "Why use separate here?" |

### 4. Code Generation
| Instruction Type | Example |
|------------------|---------|
| Write feature | "Write a feature that parses JSON" |
| Write class | "Create a thread-safe cache class" |
| Implement pattern | "Implement the Builder pattern in Eiffel" |
| Complete code | "Complete this partial implementation" |

### 5. Code Explanation
| Instruction Type | Example |
|------------------|---------|
| Explain class | "What does this class do?" |
| Explain feature | "Explain this algorithm" |
| Explain contracts | "What do these contracts guarantee?" |

### 6. Code Review/Improvement
| Instruction Type | Example |
|------------------|---------|
| Review code | "Review this for Eiffel best practices" |
| Refactor | "Simplify this feature" |
| Optimize | "This is inefficient, improve it" |
| Fix bug | "There's a bug in this code, find and fix it" |

### 7. Error Fixing
| Instruction Type | Example |
|------------------|---------|
| Fix compiler error | "Fix VEEN error: unknown identifier" |
| Fix VJAR | "Fix void-safety violation" |
| Fix VTCT | "Fix type conformance error" |

---

## Data Sources

### Tier 1: Highest Quality (Simple Eiffel)
- **796 files, ~90K lines**
- All DBC, void-safe, tested
- We control it, can annotate
- Can extract: feature pairs, class examples, patterns

### Tier 2: High Quality (ISE Stdlib + Gobo)
- **~5,500 files, ~1.1M lines**
- Production quality, well-documented
- Standard patterns, comprehensive
- Can extract: stdlib usage, standard patterns

### Tier 3: Good Quality (EiffelLoop, Contrib)
- **~10K files, ~1.5M lines**
- Real-world usage, varied patterns
- May have legacy patterns
- Can extract: practical examples, domain patterns

---

## Semi-Automated Extraction Strategies

### Strategy 1: Feature Extraction with Contract Analysis

**Process:**
1. Parse Eiffel file â extract features
2. For features WITH contracts â create "explain contracts" pairs
3. For features WITHOUT contracts â use LLM to generate contracts â create "add contracts" pairs
4. Validate generated contracts (compile test)

**Tools:** simple_eiffel_parser + Claude/Ollama

### Strategy 2: Git History Mining

**Process:**
1. Find commits that added/modified contracts
2. Extract before/after pairs
3. Generate instruction: "Add contracts like this developer did"

**Limitation:** Requires good commit history

### Strategy 3: Template-Based Generation

**Process:**
1. Define templates: "Add {contract_type} to {feature_type}"
2. Fill templates with actual code from corpus
3. Generate outputs using rules or LLM

**Example Templates:**
```
- "Add preconditions to this setter" + setter code â setter with require
- "Add postconditions to this query" + query code â query with ensure
- "Make this void-safe" + unsafe code â safe code
```

### Strategy 4: LLM-Assisted Generation

**Process:**
1. Feed code to Claude/Ollama
2. Ask: "Generate 5 instruction-output pairs for this class"
3. Human review and filter
4. Use simple_ai_client for batch processing

**Quality Control:**
- Compile-test generated code
- Sample human review
- Cross-validate with multiple LLMs

---

## Quality vs Quantity Tradeoffs

| Approach | Quality | Volume | Effort |
|----------|---------|--------|--------|
| Pure manual | â­â­â­â­â­ | 100s | Weeks |
| Template + rules | â­â­â­â­ | 1000s | Days |
| LLM-assisted + review | â­â­â­ | 10,000s | Days |
| Pure LLM (no review) | â­â­ | 100,000s | Hours |

**Recommendation:** Hybrid approach
- Manual: 500-1000 high-quality "golden" examples
- Template: 5,000 structural examples
- LLM-assisted: 10,000+ with sampling review

---

## Open Questions

1. **What ratio of categories?** More DBC? More generation? More explanation?

2. **Input length?** Single features? Whole classes? Multiple classes?

3. **Output style?** Just code? Code + explanation? Just explanation?

4. **Negative examples?** Include "what NOT to do" pairs?

5. **Difficulty gradient?** Simple â complex progression?

6. **Domain coverage?** Focus on library code? Application code? Both?

---

## Next Steps

- [ ] Decide on category ratios
- [ ] Build extraction pipeline prototype
- [ ] Create 100 manual "golden" examples
- [ ] Test LLM-assisted generation quality
- [ ] Define validation criteria

---

## Discussion Notes

*This section captures our ongoing discussion...*
