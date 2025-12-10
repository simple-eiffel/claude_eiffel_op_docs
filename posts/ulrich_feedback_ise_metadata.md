# Ulrich's Feedback on ISE Metadata Database

**Date:** December 10, 2025
**Context:** Response to simple_lsp discussion

## Key Point

> When ISE Eiffel compiles a system, it creates a "database of metadata" about that system. What if one had a query-like API (Maybe even some command-line tool to query that)?
> The Eiffel IDE can answer most questions from within the IDE, but getting those from any tools seems to be nice.

## Analysis

This is an excellent observation. The ISE compiler creates rich metadata during compilation that includes:

- Full type resolution
- Inheritance chain information
- Feature call graphs
- Contract evaluation details
- Generic instantiation info
- Conformance relationships

This is information our parser-based approach **cannot** provide because:

1. We parse but don't compile - no type checking
2. We don't resolve generics or anchored types
3. We can't see inherited features without walking the hierarchy
4. Contract semantics aren't evaluated

## Two Approaches

**1. Parser-based (our current approach):**
- Works without compilation
- Fast initial indexing
- Works on incomplete/broken code
- Limited semantic understanding

**2. Compiler metadata (Ulrich's suggestion):**
- Requires successful compilation
- Rich semantic information
- Full type resolution
- Accurate inheritance chains
- Could answer "what's the actual type of this?" questions

## Integration Possibility

The ideal LSP would use **both**:
- Parser-based for editing (fast, works on broken code)
- Compiler metadata for accurate semantic queries (post-compile)

## Action Items

1. Research ISE compiler metadata format
2. Look for existing tools that query EC database
3. Consider hybrid approach in simple_lsp roadmap
4. Add "ISE Metadata Integration" to long-term roadmap

---

**From:**
Ulrich
Eiffel User Community
