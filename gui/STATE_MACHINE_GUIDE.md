# State Machine Guide

Master UI state management with simple_vision's declarative state machines.

---

## Section 1: Why State Machines?

### The Problem

Without state machines, UIs become unpredictable:
- Booleans proliferate: `is_loading`, `is_editing`, `is_submitted`, `is_error` → impossible to keep consistent
- Invalid state combinations: "loading AND submitted" shouldn't happen but can
- Implicit rules: Developers guess what state leads to what next state
- Bugs hide: Race conditions between async operations and state changes

### The Solution

A **state machine** declares:
- Which states are valid
- Which transitions are allowed
- What actions happen on entry/exit
- What guards prevent invalid transitions

**Result:** Invalid states become impossible, transitions are explicit, bugs surface.

### Example: Authentication Flow

**Without State Machine:**
```eiffel
is_logged_out: BOOLEAN
is_logging_in: BOOLEAN
is_logged_in: BOOLEAN
is_error: BOOLEAN

-- What if is_logged_in AND is_logging_in are both true? Bug!
```

**With State Machine:**
```json
{
  "states": [
    { "id": "logged_out" },
    { "id": "logging_in" },
    { "id": "logged_in" },
    { "id": "error" }
  ],
  "transitions": [
    { "from": "logged_out", "event": "login", "to": "logging_in" },
    { "from": "logging_in", "event": "success", "to": "logged_in" },
    { "from": "logging_in", "event": "failure", "to": "error" }
  ]
}
```

Only one state is active at a time. Invalid combinations are impossible.

---

## Section 2: Concepts

### States

A single condition the UI can be in.

```json
{
  "id": "logged_out",
  "label": "User Not Authenticated",
  "description": "Initial state, login form visible"
}
```

**State Properties:**
- `id` - Unique identifier
- `label` - Human-readable name
- `description` - Purpose and UI effects
- `entry_action` - Execute on entering state
- `exit_action` - Execute on leaving state
- `type` - "initial" (start), "final" (end), or "normal"

### Transitions

Movement from one state to another triggered by an event.

```json
{
  "from": "logged_out",
  "event": "login",
  "to": "logging_in",
  "guard": "username_not_empty AND password_not_empty",
  "action": "authenticate_user"
}
```

**Transition Properties:**
- `from` - Source state
- `event` - Trigger (user action, timer, async completion)
- `to` - Target state
- `guard` - Condition that must be true
- `action` - Code to run before transition

### Events

Messages that trigger transitions.

Common events:
- `click` - Button clicked
- `change` - Field value changed
- `submit` - Form submitted
- `timer_fired` - Timer expired
- `success` - Async operation succeeded
- `failure` - Async operation failed
- `loaded` - Data loaded
- `error` - Error occurred

### Guards

Boolean conditions that allow/prevent transitions.

```json
{
  "from": "editing",
  "event": "save",
  "to": "saving",
  "guard": "form_valid AND has_changes",
  "action": "save_to_database"
}
```

Without guard: Any attempt to save triggers transition.
With guard: Only saves when form is valid AND changes exist.

### Actions

Code executed during transitions (entry/exit/on_transition).

```json
{
  "states": [
    {
      "id": "loading",
      "entry_action": "show_spinner",
      "exit_action": "hide_spinner"
    }
  ]
}
```

Or programmatically:
```eiffel
machine.state ("loading")
  .on_entry (agent show_spinner)
  .on_exit (agent hide_spinner)
```

---

## Section 3: simple_vision API Reference

### Programmatic State Machine

Create and manage state machines in Eiffel code.

**Create a Machine:**
```eiffel
local
  machine: SV_STATE_MACHINE
  sv: SV_QUICK
do
  create sv.make
  machine := sv.state_machine ("auth_machine")
  -- Add states and transitions...
end
```

**Add States:**
```eiffel
machine.state ("logged_out")
  .described_as ("User not authenticated")
  .do_nothing

machine.state ("logging_in")
  .described_as ("Authenticating...")
  .on_entry (agent show_spinner)
  .on_exit (agent hide_spinner)

machine.state ("logged_in")
  .described_as ("User authenticated")
  .on_entry (agent show_dashboard)
```

**Set Initial State:**
```eiffel
machine.set_initial ("logged_out")
```

**Add Transitions:**
```eiffel
machine.on ("login")
  .from_state ("logged_out")
  .to ("logging_in")
  .apply
  .do_action (agent authenticate)

machine.on ("success")
  .from_state ("logging_in")
  .to ("logged_in")
  .apply
  .do_action (agent on_login_success)

machine.on ("failure")
  .from_state ("logging_in")
  .to ("logged_out")
  .apply
  .do_action (agent on_login_failure)

machine.on ("logout")
  .from_state ("logged_in")
  .to ("logged_out")
  .apply
  .do_action (agent on_logout)
```

**Trigger Transitions:**
```eiffel
machine.trigger ("login")
if machine.is_in_state ("logging_in") then
  -- Attempting to authenticate...
end

if machine.is_in_state ("logged_in") then
  -- Show main window
end

machine.current_state.name  -- Returns "logged_out", "logging_in", etc.
```

**Query State:**
```eiffel
if machine.can_transition ("logout") then
  machine.trigger ("logout")
end

if machine.is_in_final_state then
  -- Operation complete
end
```

---

## Section 4: JSON Specification Format

### Complete State Machine JSON

```json
{
  "state_machines": [
    {
      "id": "auth_flow",
      "initial_state": "logged_out",
      "states": [
        {
          "id": "logged_out",
          "type": "initial",
          "description": "User not authenticated"
        },
        {
          "id": "logging_in",
          "description": "Authentication in progress",
          "entry_action": "show_spinner",
          "exit_action": "hide_spinner"
        },
        {
          "id": "logged_in",
          "type": "normal",
          "description": "User authenticated"
        },
        {
          "id": "error",
          "description": "Authentication failed",
          "entry_action": "show_error_message"
        }
      ],
      "transitions": [
        {
          "id": "login_attempt",
          "from": "logged_out",
          "event": "login",
          "to": "logging_in",
          "guard": "username_not_empty AND password_not_empty"
        },
        {
          "id": "login_success",
          "from": "logging_in",
          "event": "success",
          "to": "logged_in",
          "action": "save_session"
        },
        {
          "id": "login_failure",
          "from": "logging_in",
          "event": "failure",
          "to": "error",
          "action": "log_failure"
        },
        {
          "id": "retry",
          "from": "error",
          "event": "retry",
          "to": "logged_out"
        },
        {
          "id": "logout",
          "from": "logged_in",
          "event": "logout",
          "to": "logged_out",
          "action": "clear_session"
        }
      ]
    }
  ]
}
```

### Guard Conditions

Guards are boolean expressions:

```json
{
  "guard": "form_valid AND user_authenticated AND not is_loading"
}
```

Common predicates:
- `field_name_not_empty` - Text field has content
- `field_value_matches(pattern)` - Email, phone, etc.
- `form_valid` - All fields pass validation
- `is_loading` / `not is_loading` - Async operation state
- `user_authenticated` - User logged in
- `has_unsaved_changes` - Detect dirty state

---

## Section 5: Visualization with simple_spec_viz

### Generating State Diagrams

After writing JSON spec, visualize it:

```bash
cd /d/prod/simple_spec_viz
./EIFGENs/simple_spec_viz/W_code/simple_spec_viz.exe \
  visualize /path/to/spec.json \
  --output-dir /output/diagrams/
```

Output files:
- `state_machine.svg` - State diagram showing states and transitions
- `screens.svg` - Screen mockups for each state

### Reading State Diagrams

A state diagram shows:
- **Circles/Boxes** = States
- **Arrows** = Transitions
- **Labels** = Events and guards
- **Entry/Exit** = Actions on state change

Example auth flow diagram:
```
┌─────────────┐
│ logged_out  │◄────────────────┐
└──────┬──────┘                 │ logout
       │ login                  │
       ↓                        │
┌─────────────┐                 │
│ logging_in  │                 │
└──┬────────┬─┘                 │
   │        │                   │
success    failure              │
   ↓        ↓                   │
┌──────┐ ┌──────┐               │
│ logged_in (success) ──────────┘
└──────┘ └──────┘
```

### What to Look For in Review

1. **Does every state have an entry point?** - No orphaned states
2. **Can you exit every state?** - No dead ends (except final states)
3. **Are guards sensible?** - Do conditions match the flow?
4. **Are actions named clearly?** - Easy to implement?
5. **Does the flow match your design intent?** - Does it look right?

---

## Section 6: Common Patterns

### Pattern 1: Authentication

Login/logout with error recovery.

```json
{
  "initial_state": "logged_out",
  "states": [
    { "id": "logged_out", "type": "initial" },
    { "id": "logging_in", "entry_action": "show_spinner" },
    { "id": "logged_in", "entry_action": "load_dashboard" },
    { "id": "auth_error", "entry_action": "show_error" }
  ],
  "transitions": [
    { "from": "logged_out", "event": "login", "to": "logging_in", "guard": "credentials_provided" },
    { "from": "logging_in", "event": "success", "to": "logged_in" },
    { "from": "logging_in", "event": "failure", "to": "auth_error" },
    { "from": "auth_error", "event": "retry", "to": "logged_out" },
    { "from": "logged_in", "event": "logout", "to": "logged_out" }
  ]
}
```

### Pattern 2: Data Loading

Async data fetch with states.

```json
{
  "initial_state": "idle",
  "states": [
    { "id": "idle", "type": "initial" },
    { "id": "loading", "entry_action": "show_spinner" },
    { "id": "loaded", "entry_action": "display_data" },
    { "id": "error", "entry_action": "show_error" }
  ],
  "transitions": [
    { "from": "idle", "event": "refresh", "to": "loading" },
    { "from": "loading", "event": "data_received", "to": "loaded" },
    { "from": "loading", "event": "error", "to": "error" },
    { "from": "error", "event": "retry", "to": "loading" },
    { "from": "loaded", "event": "refresh", "to": "loading" }
  ]
}
```

### Pattern 3: Form Validation

Multi-step form with validation.

```json
{
  "initial_state": "editing",
  "states": [
    { "id": "editing", "type": "initial" },
    { "id": "validating", "entry_action": "validate_fields" },
    { "id": "valid", "entry_action": "enable_submit" },
    { "id": "invalid", "entry_action": "show_errors" },
    { "id": "submitting", "entry_action": "disable_form" },
    { "id": "submitted", "type": "final", "entry_action": "show_success" }
  ],
  "transitions": [
    { "from": "editing", "event": "validate", "to": "validating" },
    { "from": "validating", "event": "all_valid", "to": "valid" },
    { "from": "validating", "event": "has_errors", "to": "invalid" },
    { "from": "invalid", "event": "field_changed", "to": "editing" },
    { "from": "valid", "event": "submit", "to": "submitting" },
    { "from": "submitting", "event": "success", "to": "submitted" },
    { "from": "submitting", "event": "error", "to": "invalid" }
  ]
}
```

### Pattern 4: Multi-step Wizard

Step-by-step process with navigation.

```json
{
  "initial_state": "step1",
  "states": [
    { "id": "step1", "type": "initial", "entry_action": "show_step_1" },
    { "id": "step2", "entry_action": "show_step_2" },
    { "id": "step3", "entry_action": "show_step_3" },
    { "id": "complete", "type": "final", "entry_action": "show_summary" }
  ],
  "transitions": [
    { "from": "step1", "event": "next", "to": "step2", "guard": "step1_valid" },
    { "from": "step2", "event": "back", "to": "step1" },
    { "from": "step2", "event": "next", "to": "step3", "guard": "step2_valid" },
    { "from": "step3", "event": "back", "to": "step2" },
    { "from": "step3", "event": "finish", "to": "complete", "guard": "step3_valid" },
    { "from": "step1", "event": "cancel", "to": "cancelled" },
    { "from": "step2", "event": "cancel", "to": "cancelled" },
    { "from": "step3", "event": "cancel", "to": "cancelled" }
  ]
}
```

### Pattern 5: CRUD Operations

Create, read, update, delete lifecycle.

```json
{
  "initial_state": "list_view",
  "states": [
    { "id": "list_view", "type": "initial", "entry_action": "load_list" },
    { "id": "viewing", "entry_action": "show_detail" },
    { "id": "creating", "entry_action": "show_create_form" },
    { "id": "editing", "entry_action": "show_edit_form" },
    { "id": "saving", "entry_action": "show_spinner" },
    { "id": "deleting", "entry_action": "show_confirmation" },
    { "id": "error", "entry_action": "show_error" }
  ],
  "transitions": [
    { "from": "list_view", "event": "item_selected", "to": "viewing" },
    { "from": "viewing", "event": "create", "to": "creating" },
    { "from": "viewing", "event": "edit", "to": "editing" },
    { "from": "viewing", "event": "delete", "to": "deleting" },
    { "from": "creating", "event": "save", "to": "saving", "guard": "form_valid" },
    { "from": "editing", "event": "save", "to": "saving", "guard": "form_valid" },
    { "from": "saving", "event": "success", "to": "list_view" },
    { "from": "saving", "event": "error", "to": "error" },
    { "from": "deleting", "event": "confirm", "to": "saving" },
    { "from": "deleting", "event": "cancel", "to": "viewing" },
    { "from": "creating", "event": "cancel", "to": "list_view" },
    { "from": "editing", "event": "cancel", "to": "viewing" },
    { "from": "error", "event": "retry", "to": "saving" },
    { "from": "error", "event": "cancel", "to": "list_view" }
  ]
}
```

### Pattern 6: Modal Dialogs

Dialog open/close with confirmation.

```json
{
  "initial_state": "dialog_closed",
  "states": [
    { "id": "dialog_closed", "type": "initial" },
    { "id": "dialog_open", "entry_action": "focus_first_field" },
    { "id": "processing", "entry_action": "show_spinner" }
  ],
  "transitions": [
    { "from": "dialog_closed", "event": "open", "to": "dialog_open" },
    { "from": "dialog_open", "event": "submit", "to": "processing", "guard": "dialog_valid" },
    { "from": "dialog_open", "event": "cancel", "to": "dialog_closed" },
    { "from": "processing", "event": "success", "to": "dialog_closed" },
    { "from": "processing", "event": "error", "to": "dialog_open" }
  ]
}
```

### Pattern 7: Async Operations

Long-running operation with timeout/cancellation.

```json
{
  "initial_state": "idle",
  "states": [
    { "id": "idle", "type": "initial" },
    { "id": "running", "entry_action": "start_timer" },
    { "id": "done", "type": "final" },
    { "id": "timeout", "entry_action": "show_timeout_error" },
    { "id": "cancelled", "entry_action": "cleanup" }
  ],
  "transitions": [
    { "from": "idle", "event": "start", "to": "running" },
    { "from": "running", "event": "complete", "to": "done" },
    { "from": "running", "event": "timeout", "to": "timeout" },
    { "from": "running", "event": "cancel", "to": "cancelled" },
    { "from": "timeout", "event": "retry", "to": "running" },
    { "from": "timeout", "event": "dismiss", "to": "idle" }
  ]
}
```

### Pattern 8: Undo/Redo

State history for undo/redo functionality.

```json
{
  "initial_state": "no_undo",
  "states": [
    { "id": "no_undo", "type": "initial" },
    { "id": "can_undo", "entry_action": "enable_undo" },
    { "id": "can_redo", "entry_action": "enable_redo" }
  ],
  "transitions": [
    { "from": "no_undo", "event": "change", "to": "can_undo" },
    { "from": "can_undo", "event": "undo", "to": "no_undo" },
    { "from": "can_undo", "event": "change", "to": "can_undo" },
    { "from": "can_redo", "event": "change", "to": "can_undo" }
  ]
}
```

### Pattern 9: Error Recovery

Recoverable vs fatal errors.

```json
{
  "initial_state": "normal",
  "states": [
    { "id": "normal", "type": "initial" },
    { "id": "warning", "entry_action": "show_warning" },
    { "id": "error", "entry_action": "show_error" },
    { "id": "fatal", "type": "final", "entry_action": "shutdown" }
  ],
  "transitions": [
    { "from": "normal", "event": "warning", "to": "warning" },
    { "from": "warning", "event": "dismiss", "to": "normal" },
    { "from": "warning", "event": "error", "to": "error" },
    { "from": "error", "event": "retry", "to": "normal" },
    { "from": "error", "event": "fatal", "to": "fatal" }
  ]
}
```

### Pattern 10: Navigation

Tab or page navigation with state.

```json
{
  "initial_state": "home",
  "states": [
    { "id": "home", "type": "initial", "entry_action": "show_home" },
    { "id": "projects", "entry_action": "show_projects" },
    { "id": "settings", "entry_action": "show_settings" },
    { "id": "about", "entry_action": "show_about" }
  ],
  "transitions": [
    { "from": "home", "event": "goto_projects", "to": "projects" },
    { "from": "home", "event": "goto_settings", "to": "settings" },
    { "from": "projects", "event": "goto_home", "to": "home" },
    { "from": "settings", "event": "goto_home", "to": "home" },
    { "from": "about", "event": "goto_home", "to": "home" }
  ]
}
```

---

## Section 7: Best Practices

1. **Keep States Focused** - Each state has one clear purpose
2. **Minimize States** - 5-10 states is typical, avoid explosion
3. **Name States Clearly** - Use verb-noun: `loading`, `editing`, `submitting`
4. **Guards for Logic** - Don't encode business logic in action names
5. **Entry/Exit Actions** - Clean up on exit, initialize on entry
6. **Avoid Redundant Transitions** - If every state can go to error, use a global handler
7. **Test Transitions** - Verify guard conditions work as expected
8. **Document State Purpose** - Use `description` field for clarity

---

## Section 8: Debugging & Troubleshooting

### Common Issues

**Issue: Stuck in a state**
- Check guards are satisfied
- Verify event name matches transition
- Ensure handler is triggering event

**Issue: Unexpected state transition**
- Add logging to entry/exit actions
- Review guard conditions
- Check for race conditions (async operations)

**Issue: State machine not updating UI**
- Ensure actions are connected to widget updates
- Check that widgets listen to state changes
- Verify state_machine reference in window spec

### Logging

Add debug output:
```json
{
  "transitions": [
    {
      "from": "idle",
      "event": "start",
      "to": "loading",
      "action": "debug_log_transition"
    }
  ]
}
```

---

## See Also

**Learning:**
- [QUICKSTART.md](./QUICKSTART.md) - 5-minute intro with state machine
- [WORKFLOW_GUIDE.md](./WORKFLOW_GUIDE.md) - State machines in full workflow
- [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) - Widgets with enabled_when/visible_when

**Real-World Examples:**
- [examples/auth_flow/](./examples/auth_flow/) - Pattern 1: Authentication
- [examples/loading_pattern/](./examples/loading_pattern/) - Pattern 2: Data Loading
- [examples/data_entry_form/](./examples/data_entry_form/) - Pattern 3: Form Validation
- [examples/wizard/](./examples/wizard/) - Pattern 4: Multi-step Wizard
- [examples/crud_application/](./examples/crud_application/) - Pattern 5: CRUD Operations
- [examples/settings/](./examples/settings/) - Settings with nested panels
- [examples/dashboard/](./examples/dashboard/) - Complex tab-based layout

**Implementation:**
- [VALIDATION_GUIDE.md](./VALIDATION_GUIDE.md) - Validation state transitions
- [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) - Container states
- [THEMING_GUIDE.md](./THEMING_GUIDE.md) - Theme state switching

**Tools:**
- simple_spec_viz docs state-machine - Show this guide in CLI
- /eiffel.gui-ux pattern <name> - Show pattern in Claude Code
