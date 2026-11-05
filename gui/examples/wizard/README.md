# Multi-Step Wizard Example

Onboarding/setup wizard with step navigation and validation.

## Pattern: Sequential Steps

Demonstrates:
- Multiple wizard steps
- Step validation before advancing
- Progress indicator
- Back/next navigation
- Cancel at any step
- Dynamic step content
- Entry/exit actions per step

## State Machine

3 steps + completion + cancellation:
- `step1` → `step2` (if step1_valid)
- `step2` → `step3` (if step2_valid) or back to `step1`
- `step3` → `complete` (if step3_valid) or back to `step2`
- Cancel from any step → `cancelled`

## Implementation

```eiffel
handle_next
  do
    if is_current_step_valid then
      if machine.is_in_state ("step1") then
        machine.trigger ("next")
      end
    end
  end

show_step_1
  do
    step_title.set_content ("Step 1: Personal Info")
    progress_bar.set_value (33)
    step_content.show_step_1
  end

show_step_2
  do
    step_title.set_content ("Step 2: Account Setup")
    progress_bar.set_value (66)
    step_content.show_step_2
  end

show_step_3
  do
    step_title.set_content ("Step 3: Preferences")
    progress_bar.set_value (100)
    step_content.show_step_3
  end
```

## Key Patterns

1. **Progress Indicator**: Shows where user is in process
2. **Step Validation**: Can't advance until current step valid
3. **Back Button**: Visible except on first step
4. **Dynamic Content**: Step content changes per state
5. **Cancel Option**: Always available
6. **Summary Step**: Final step confirms all choices

## Related Examples

- [auth_flow](../auth_flow/) - Multi-step authentication
- [data_entry_form](../data_entry_form/) - Step validation

---

**Files:**
- `wizard.json` - JSON specification
- `state_machine.svg` - State diagram
- `screens.svg` - Screen mockups
- `README.md` - This file
