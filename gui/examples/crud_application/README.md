# CRUD Application Example

Full create-read-update-delete workflow with confirmations and error handling.

## Pattern: Master-Detail with State Machine

Demonstrates:
- List view with user selection
- Detail panel that appears on selection
- Create, edit, delete operations
- Confirmation dialog for destructive actions
- Error recovery
- Form state validation

## State Machine

7 states managing the complete workflow:
1. `list_view` - Initial state, list visible
2. `viewing` - User selected, detail panel shown
3. `creating` - New user form
4. `editing` - Existing user form
5. `saving` - API call in progress
6. `deleting` - Delete confirmation
7. `error` - Error state with retry

## Implementation Pattern

```eiffel
-- Handle list selection
handle_user_selected (user_id: STRING)
  do
    current_user_id := user_id
    machine.trigger ("item_selected")
  end

-- Handle create/edit click
handle_save
  do
    if form_is_valid then
      machine.trigger ("save")
    end
  end

-- API call during save state
save_user
  do
    if api.save_user (user_data) then
      machine.trigger ("success")
    else
      machine.trigger ("error")
    end
  end

-- Confirmation for delete
handle_delete
  do
    machine.trigger ("delete")
  end

handle_confirm_delete
  do
    machine.trigger ("confirm")
  end
```

## Key Patterns

1. **Master-Detail Layout**: List + detail side-by-side
2. **Conditional Visibility**: Detail panel visible only when appropriate state
3. **Button Enabling**: Edit/delete buttons disabled until item selected
4. **Confirmation Dialog**: Prevents accidental deletion
5. **Error Recovery**: Retry or abandon after API error
6. **Form State**: Save button disabled until changes made

## Related Examples

- [data_entry_form](../data_entry_form/) - Form validation
- [auth_flow](../auth_flow/) - Async operations with loading
- [wizard](../wizard/) - Multi-step workflows

---

**Files:**
- `crud_application.json` - JSON specification
- `state_machine.svg` - State diagram
- `screens.svg` - Screen mockups
- `README.md` - This file
