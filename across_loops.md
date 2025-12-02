# Eiffel Across Loops

## Official Syntax

```eiffel
across collection as cursor_name loop
    -- body
end
```

## Element Access (NEEDS VERIFICATION)

Official documentation states:
```eiffel
across my_list as ic loop
    print (ic.item)    -- .item to access element
    print (ic.index)   -- .index for position
    print (ic.key)     -- .key for hash table keys
end
```

**Note**: User has reported needing to remove `.item` in practice. Document actual compiler behavior when encountered.

## Boolean Variants

```eiffel
-- All elements satisfy condition
across my_list as ic all ic.item > 0 end

-- At least one element satisfies condition
across my_list as ic some ic.item > 0 end
```

## Integer Intervals

```eiffel
across 1 |..| 10 as i loop
    print (i.item)
end
```

## Vs. Traditional Loop

Traditional (avoid when possible):
```eiffel
from
    my_list.start
until
    my_list.after
loop
    print (my_list.item)
    my_list.forth
end
```

Across (preferred):
```eiffel
across my_list as ic loop
    print (ic.item)
end
```

## Requirements

- Collection must inherit from `ITERABLE`
- All EiffelBase collections support this
- Do NOT modify collection during iteration with across form

---

## Verified Examples

(Add working, compiler-tested examples here)

