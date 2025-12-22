# Eiffel Specialist Models Architecture

**Date:** 2025-12-21
**Status:** Design Discussion
**Concept:** Council of Specialists vs. One Monolithic Model

---

## The Vision

Instead of one large "Eiffel Expert" model, create a **council of specialists**:

```
                    âââââââââââââââââââââââââââ
                    â   Orchestrator/Router   â
                    â  (picks specialist(s))  â
                    âââââââââââââ¬ââââââââââââââ
                                â
        âââââââââââââ¬ââââââââââââ¼ââââââââââââ¬ââââââââââââ
        â¼           â¼           â¼           â¼           â¼
   âââââââââââ âââââââââââ âââââââââââ âââââââââââ âââââââââââ
   â   DBC   â â  SCOOP  â â   MI    â â  Void   â âGenerics â
   âSpecialistâ âSpecialistâ âSpecialistâ â Safety â âSpecialistâ
   âââââââââââ âââââââââââ âââââââââââ âââââââââââ âââââââââââ
        â           â           â           â           â
        âââââââââââââ´ââââââââââââ´ââââââââââââ´ââââââââââââ
                                â
                    âââââââââââââ¼ââââââââââââ
                    â   Response Combiner   â
                    â  (if multi-specialist)â
                    âââââââââââââââââââââââââ
```

---

## The Specialists

### Core Eiffel Specialists

| Specialist | Focus | Training Data Source |
|------------|-------|---------------------|
| **DBC Master** | Preconditions, postconditions, invariants, contract design | All simple_* contracts, ISE stdlib contracts |
| **SCOOP Expert** | Separate types, concurrent patterns, lock-free design | SCOOP examples, concurrent patterns |
| **MI Architect** | Multiple inheritance, feature adaptation, rename/redefine | ISE/Gobo class hierarchies |
| **Void Safety** | Attached/detachable, VJAR fixes, safe patterns | Void-safe code examples, error fixes |
| **Generics Guru** | Generic classes, constrained generics, type parameters | Container classes, generic patterns |
| **Agents Expert** | Inline agents, agent types, callbacks | Agent usage patterns |

### Meta-Specialists

| Specialist | Focus | Purpose |
|------------|-------|---------|
| **Polyglot Translator** | Map other-language patterns to Eiffel | "How do I do X (from Java/Python/C#) in Eiffel?" |
| **Pattern Mapper** | GoF patterns, architectural patterns in Eiffel | "Implement Observer pattern in Eiffel" |
| **Error Doctor** | Compiler errors, runtime errors, diagnosis | "What does VJAR mean? How do I fix it?" |

---

## Why This Architecture?

### Advantages Over Monolithic Model

| Aspect | Monolithic | Specialists |
|--------|-----------|-------------|
| Dataset per model | 50K pairs (diluted) | 5-10K pairs (focused) |
| Training time | Long | Short per model |
| Iteration speed | Retrain everything | Fix one specialist |
| Quality | Jack of all trades | Master of one |
| Model size | Need larger model | Smaller models work |
| Maintenance | Monolithic updates | Targeted updates |

### Potential Model Sizes

| Specialist | Complexity | Suggested Base |
|------------|-----------|----------------|
| DBC Master | Medium | Qwen2.5-Coder-3B or 7B |
| SCOOP Expert | High (rare patterns) | Qwen2.5-Coder-7B |
| Void Safety | Low-Medium | Qwen2.5-Coder-1.5B or 3B |
| Error Doctor | Low | Qwen2.5-Coder-1.5B |

Smaller specialists = faster inference = better UX

---

## The Orchestrator

### Option 1: Rules-Based Router

```eiffel
route_question (q: STRING): ARRAYED_LIST [SPECIALIST]
    do
        create Result.make (3)
        if q.has_substring ("contract") or q.has_substring ("require") then
            Result.extend (dbc_specialist)
        end
        if q.has_substring ("separate") or q.has_substring ("SCOOP") then
            Result.extend (scoop_specialist)
        end
        if q.has_substring ("inherit") or q.has_substring ("redefine") then
            Result.extend (mi_specialist)
        end
        -- etc.
    end
```

**Pros:** Simple, fast, deterministic
**Cons:** Brittle, misses nuanced questions

### Option 2: Classifier Model

Small model trained to classify questions:
```
Input: "How do I make this feature thread-safe?"
Output: [SCOOP: 0.8, DBC: 0.3, VoidSafety: 0.1]
```

**Pros:** Handles nuance, learns patterns
**Cons:** Another model to train/maintain

### Option 3: Keyword + Embedding Hybrid

- Fast keyword check first
- Embedding similarity for ambiguous cases
- No extra model needed (use Ollama embeddings)

---

## The Polyglot Translator

Special role: Help developers coming from other languages.

### Training Data Format

```json
{
  "instruction": "How do I implement the Singleton pattern in Eiffel? In Java I would use a private constructor and static instance.",
  "input": "",
  "output": "In Eiffel, use a once function:\n\ninstance: SINGLETON\n    once\n        create Result.make\n    end\n\nThe `once` keyword ensures the function body executes only once, returning the same object thereafter. No private constructor needed - Eiffel's creation procedure visibility handles access control."
}
```

### Source for Training Pairs

- Stack Overflow: "How to do X in Eiffel" questions
- Common patterns from Java/C#/Python â Eiffel equivalents
- "Rosetta Code" style translations
- Our own curated "Eiffel for X Developers" examples

---

## Integration with simple_ai_client

```eiffel
class EIFFEL_AI_COUNCIL

feature -- Query

    ask (question: STRING): STRING
            -- Route question to appropriate specialist(s)
        local
            specialists: LIST [STRING]
            responses: ARRAYED_LIST [STRING]
        do
            specialists := router.classify (question)
            create responses.make (specialists.count)
            
            across specialists as spec loop
                responses.extend (
                    ollama.query (spec, question)
                )
            end
            
            Result := combiner.synthesize (responses)
        end

feature {NONE} -- Implementation

    router: SPECIALIST_ROUTER
    ollama: OLLAMA_CLIENT  -- from simple_ai_client
    combiner: RESPONSE_COMBINER

end
```

---

## Phased Rollout

### Phase 1: DBC Master (Proof of Concept)
- Most training data available
- Clear success criteria
- High value to community
- Validates the approach

### Phase 2: Void Safety + Error Doctor
- Practical daily-use value
- Smaller focused datasets
- Quick wins

### Phase 3: Polyglot Translator
- Helps Eiffel adoption
- Different data source (cross-language)
- Community contribution potential

### Phase 4: Full Council
- Add remaining specialists
- Build orchestrator
- Integration polish

---

## Open Questions

1. **How do specialists collaborate?** 
   - Chain? (DBC â then Void Safety review)
   - Parallel? (both answer, combine)
   - Vote? (multiple opinions)

2. **Orchestrator training data?**
   - Need questionâspecialist classification pairs
   - Could bootstrap from keyword rules

3. **Response combination?**
   - Simple concatenation?
   - Another model to synthesize?
   - Let user see all specialist opinions?

4. **Shared base knowledge?**
   - Each specialist knows basic Eiffel?
   - Or pure specialization (defer basics to others)?

---

## Next Steps

- [ ] Validate architecture with small prototype
- [ ] Create DBC Master dataset (Phase 1)
- [ ] Train first specialist
- [ ] Build minimal orchestrator
- [ ] Evaluate and iterate

---

## REVISED: Rosetta Code First Strategy (2025-12-21)

Strategic pivot: Start with cross-language translation, not DBC.

### Core Insight
> "We are a small group facing Goliath competition. We need to answer THEIR questions."

### Why Rosetta First?
- Immediate value: Usable DB + training data
- Community appeal: Newcomers from other languages
- Validation: Compiler validates (no experts needed)
- Uniqueness: Bridge TO Eiffel

### The Eiffel Sieve
> Use Eiffel compiler + DBC as quality filter for AI-generated code

### Pipeline
1. Rosetta Code Task
2. Collect solutions (Java, Python, C#)
3. Generate Eiffel (Claude Max)
4. Validate (compile + DBC)
5. Store in simple_sql
6. Generate instruction pairs

### Revised Phased Rollout
- Phase 1: Rosetta Eiffel Database (NEW FIRST)
- Phase 2: Polyglot Translator Specialist
- Phase 3: DBC Master
- Phase 4: Full Council

---

## Updated Next Steps

- [ ] Apply 7-step research to simple_rosetta
- [ ] Build Rosetta Eiffel Database
- [ ] Generate instruction pairs
- [ ] Train Polyglot Translator
