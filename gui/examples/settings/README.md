# Settings Panel Example

Nested panels with save/cancel/reset pattern.

## Pattern: Settings Management

Demonstrates:
- Left navigation menu + right content panel
- Dynamic content switching per menu selection
- Dirty state tracking (save button disabled if no changes)
- Save/cancel/reset actions
- Master-detail layout
- Settings persistence

## Implementation

```eiffel
handle_menu_selection (section: STRING)
  do
    case section
    when "general" then show_general_settings
    when "appearance" then show_appearance_settings
    when "notifications" then show_notifications_settings
    when "advanced" then show_advanced_settings
    end
  end

handle_save
  do
    save_settings_to_file
    clear_dirty_flag
  end

handle_reset
  do
    reload_original_values
    clear_dirty_flag
  end

handle_field_change
  do
    set_dirty_flag
    update_save_button_state
  end
```

## Key Patterns

1. **Left Navigation**: Menu for sections
2. **Right Content**: Dynamic panel per selection
3. **Dirty Flag**: Track if settings changed
4. **Save Button State**: Disabled until changes made
5. **Reset**: Restore original values
6. **Nested Panels**: Settings grouped by section

## Related Examples

- [dashboard](../dashboard/) - Tab-based navigation
- [crud_application](../crud_application/) - Master-detail layout

---

**Files:**
- `settings.json` - JSON specification
- `screens.svg` - Screen mockups
- `README.md` - This file
