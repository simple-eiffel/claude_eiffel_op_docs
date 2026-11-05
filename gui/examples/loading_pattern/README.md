# Loading Pattern Example

Async data fetching with multiple states: idle, loading, loaded, error, refreshing.

## Pattern: Async Operations

Demonstrates:
- Idle state before loading
- Loading state with spinner
- Loaded state with data
- Error state with retry
- Refresh operation
- Conditional visibility per state
- Button enabling/disabling

## State Machine

5 states for complete async lifecycle:
- `idle` → `loading` (on refresh)
- `loading` → `loaded` (on success) or `error` (on failure)
- `loaded` → `refreshing` (on refresh)
- `refreshing` → `loaded` (on success) or `error` (on failure)
- `error` → `loading` (on retry) or `idle` (on dismiss)

## Implementation

```eiffel
handle_refresh
  do
    machine.trigger ("refresh")
  end

load_data
  do
    -- Start async operation
    api.fetch_data (agent on_data_loaded, agent on_load_error)
  end

on_data_loaded (data: DATA_LIST)
  do
    data_grid.populate (data)
    machine.trigger ("success")
  end

on_load_error (error: STRING)
  do
    error_message.set_content ("Failed: " + error)
    machine.trigger ("error")
  end

handle_retry
  do
    machine.trigger ("retry")
  end

handle_dismiss
  do
    machine.trigger ("dismiss")
  end
```

## Key Patterns

1. **Conditional Visibility**: Each state controls what's visible
2. **Spinner During Load**: Progress indicator during async work
3. **Error Message**: Shows specific error text
4. **Retry Logic**: Can retry after error
5. **Refresh Support**: Can reload data from loaded state
6. **Button State**: Refresh disabled while loading

## Variations

1. **Timeout Handling**: Add timeout state after X seconds
2. **Pagination**: Load next page from loaded state
3. **Progress Bar**: Show % complete during load
4. **Cancellation**: Allow user to cancel mid-load
5. **Caching**: Skip load if data recent

## Related Examples

- [auth_flow](../auth_flow/) - Async authentication
- [crud_application](../crud_application/) - Save operations
- [wizard](../wizard/) - Multi-step loading

---

**Files:**
- `loading_pattern.json` - JSON specification
- `state_machine.svg` - State diagram
- `screens.svg` - Screen mockups
- `README.md` - This file
