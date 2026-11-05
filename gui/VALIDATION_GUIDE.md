# Validation Guide

Implement form validation with simple_vision.

---

## Validation Rule Types

### Required

Field must not be empty.

```json
{
  "type": "text_field",
  "id": "username",
  "validation": [
    { "rule": "required", "message": "Username is required" }
  ]
}
```

**Eiffel:**
```eiffel
sv.field ("username")
  .widget (sv.text_field)
  .required
  .error_message ("Username is required")
```

### Min / Max Length

String length constraints.

```json
{
  "type": "password_field",
  "id": "password",
  "validation": [
    { "rule": "min_length", "value": 8, "message": "At least 8 characters" },
    { "rule": "max_length", "value": 128, "message": "Max 128 characters" }
  ]
}
```

**Eiffel:**
```eiffel
sv.field ("password")
  .widget (sv.password_field)
  .min_length (8)
  .max_length (128)
```

### Range

Numeric range.

```json
{
  "type": "spin_box",
  "id": "age",
  "validation": [
    { "rule": "range", "min": 18, "max": 120, "message": "Age must be 18-120" }
  ]
}
```

**Eiffel:**
```eiffel
sv.field ("age")
  .widget (sv.spin_box_range (0, 150))
  .range (18, 120)
```

### Email

Email format validation.

```json
{
  "type": "email_field",
  "id": "email",
  "validation": [
    { "rule": "email", "message": "Enter valid email address" }
  ]
}
```

**Eiffel:**
```eiffel
sv.field ("email")
  .widget (sv.email_field)
  .email_format
```

### Pattern (Regex)

Custom pattern matching.

```json
{
  "type": "text_field",
  "id": "phone",
  "validation": [
    { "rule": "pattern", "value": "^[0-9]{3}-[0-9]{3}-[0-9]{4}$",
      "message": "Phone format: XXX-XXX-XXXX" }
  ]
}
```

**Eiffel:**
```eiffel
sv.field ("phone")
  .widget (sv.phone_field)
  .pattern ("^[0-9]{3}-[0-9]{3}-[0-9]{4}$")
```

### Custom

User-defined validation logic.

```json
{
  "type": "text_field",
  "id": "username",
  "validation": [
    { "rule": "custom", "handler": "check_username_available",
      "message": "Username already taken" }
  ]
}
```

**Eiffel:**
```eiffel
sv.field ("username")
  .widget (sv.text_field)
  .custom_validation (agent is_username_available)

feature
  is_username_available (value: STRING): BOOLEAN
    do
      -- Check database or API
      Result := database.is_username_unique (value)
    end
```

---

## Validation Timing

### On Submit

Validate only when user submits form.

```json
{
  "type": "form",
  "validate_on": "submit",
  "fields": [...]
}
```

**Eiffel:**
```eiffel
form.validate_on (SV_VALIDATE_SUBMIT)
form.on_submit (agent handle_submit)
```

### On Blur

Validate when field loses focus.

```json
{
  "type": "text_field",
  "id": "email",
  "validate_on": "blur",
  "validation": [...]
}
```

**Eiffel:**
```eiffel
sv.field ("email")
  .widget (sv.email_field)
  .validate_on (SV_VALIDATE_BLUR)
```

### Real-time

Validate as user types.

```json
{
  "type": "text_field",
  "id": "password",
  "validate_on": "change",
  "validation": [...]
}
```

**Eiffel:**
```eiffel
sv.field ("password")
  .widget (sv.password_field)
  .validate_on (SV_VALIDATE_CHANGE)
  .on_change (agent validate_password)
```

---

## Error Display

### Inline Message

Show error below field.

```json
{
  "type": "text_field",
  "id": "username",
  "validation": [
    { "rule": "required", "message": "Username required" }
  ],
  "show_error_location": "below"
}
```

**Eiffel:**
```eiffel
sv.field ("username")
  .widget (sv.text_field)
  .error_location ("below")
```

### Tooltip

Show error in tooltip on hover.

```json
{
  "show_error_location": "tooltip"
}
```

### Form-level Summary

Show all errors at top of form.

```json
{
  "type": "form",
  "show_error_summary": true,
  "error_summary_location": "top"
}
```

**Eiffel:**
```eiffel
form.show_error_summary (True)
form.error_summary_location ("top")
```

### Styling

Change appearance based on validation state.

```json
{
  "type": "text_field",
  "styles": {
    "valid": { "border_color": "#00AA00" },
    "invalid": { "border_color": "#AA0000" },
    "error_text_color": "#AA0000"
  }
}
```

---

## Common Patterns

### Login Form

```json
{
  "type": "form",
  "validate_on": "submit",
  "fields": [
    {
      "id": "username",
      "widget": "text_field",
      "validation": [
        { "rule": "required", "message": "Username required" }
      ]
    },
    {
      "id": "password",
      "widget": "password_field",
      "validation": [
        { "rule": "required", "message": "Password required" },
        { "rule": "min_length", "value": 6, "message": "Min 6 characters" }
      ]
    }
  ]
}
```

### Registration Form

```json
{
  "type": "form",
  "validate_on": "blur",
  "fields": [
    {
      "id": "email",
      "widget": "email_field",
      "validation": [
        { "rule": "required", "message": "Email required" },
        { "rule": "email", "message": "Invalid email" },
        { "rule": "custom", "handler": "check_email_unique",
          "message": "Email already registered" }
      ]
    },
    {
      "id": "password",
      "widget": "password_field",
      "validation": [
        { "rule": "required", "message": "Password required" },
        { "rule": "min_length", "value": 8, "message": "Min 8 characters" },
        { "rule": "pattern",
          "value": "^(?=.*[A-Z])(?=.*[0-9]).*$",
          "message": "Need uppercase letter and number" }
      ]
    },
    {
      "id": "password_confirm",
      "widget": "password_field",
      "validation": [
        { "rule": "required", "message": "Confirm password" },
        { "rule": "custom", "handler": "passwords_match",
          "message": "Passwords do not match" }
      ]
    }
  ]
}
```

### Address Form

```json
{
  "type": "form",
  "validate_on": "change",
  "fields": [
    {
      "id": "street",
      "widget": "text_field",
      "validation": [
        { "rule": "required", "message": "Street address required" }
      ]
    },
    {
      "id": "city",
      "widget": "text_field",
      "validation": [
        { "rule": "required", "message": "City required" }
      ]
    },
    {
      "id": "state",
      "widget": "dropdown",
      "validation": [
        { "rule": "required", "message": "State required" }
      ]
    },
    {
      "id": "zip",
      "widget": "zip_code_field",
      "validation": [
        { "rule": "required", "message": "ZIP required" },
        { "rule": "pattern", "value": "^[0-9]{5}(-[0-9]{4})?$",
          "message": "Invalid ZIP format" }
      ]
    }
  ]
}
```

### Credit Card Form

```json
{
  "type": "form",
  "validate_on": "blur",
  "fields": [
    {
      "id": "card_number",
      "widget": "credit_card_field",
      "validation": [
        { "rule": "required", "message": "Card number required" },
        { "rule": "custom", "handler": "validate_luhn",
          "message": "Invalid card number" }
      ]
    },
    {
      "id": "expiry",
      "widget": "text_field",
      "validation": [
        { "rule": "required", "message": "Expiry date required" },
        { "rule": "pattern", "value": "^(0[1-9]|1[0-2])/[0-9]{2}$",
          "message": "Format: MM/YY" }
      ]
    },
    {
      "id": "cvv",
      "widget": "text_field",
      "validation": [
        { "rule": "required", "message": "CVV required" },
        { "rule": "pattern", "value": "^[0-9]{3,4}$",
          "message": "Invalid CVV" }
      ]
    }
  ]
}
```

---

## Form-Level Validation

### Multiple Field Validation

Validate relationships between fields.

```eiffel
form := sv.form
  .add_field (password_field)
  .add_field (confirm_field)
  .custom_validation (agent validate_passwords_match)

feature
  validate_passwords_match: BOOLEAN
    do
      Result := password_field.value ~ confirm_field.value
    end
```

### Conditional Validation

Only validate if condition is met.

```json
{
  "fields": [
    {
      "id": "phone",
      "validation": [
        {
          "rule": "required",
          "when": "contact_method == 'phone'",
          "message": "Phone required if selected"
        }
      ]
    }
  ]
}
```

**Eiffel:**
```eiffel
if contact_method = "phone" then
  form.validate_field ("phone")
end
```

---

## Async Validation

Validate against server/database.

```eiffel
sv.field ("email")
  .widget (sv.email_field)
  .async_validation (agent check_email_availability)
  .error_message ("Email already in use")

feature
  check_email_availability (email: STRING): BOOLEAN
    do
      -- Call API
      Result := api.is_email_available (email)
    end
```

---

## State Machine Integration

Use state machine for validation flow.

```json
{
  "state_machines": [
    {
      "id": "form_validation",
      "initial_state": "editing",
      "states": [
        { "id": "editing", "entry_action": "focus_first_field" },
        { "id": "validating", "entry_action": "show_spinner" },
        { "id": "valid", "entry_action": "enable_submit" },
        { "id": "invalid", "entry_action": "show_errors" },
        { "id": "submitting", "entry_action": "disable_form" },
        { "id": "submitted", "type": "final", "entry_action": "show_success" }
      ],
      "transitions": [
        { "from": "editing", "event": "blur", "to": "validating" },
        { "from": "validating", "event": "all_valid", "to": "valid" },
        { "from": "validating", "event": "has_errors", "to": "invalid" },
        { "from": "invalid", "event": "field_changed", "to": "editing" },
        { "from": "valid", "event": "submit", "to": "submitting" },
        { "from": "submitting", "event": "success", "to": "submitted" },
        { "from": "submitting", "event": "error", "to": "invalid" }
      ]
    }
  ]
}
```

---

## Best Practices

1. **Validate early** - Provide real-time feedback
2. **Be specific** - Error messages should explain the problem
3. **Positive feedback** - Show when field is valid (checkmark)
4. **Summary errors** - Show all errors together for context
5. **Avoid data loss** - Keep user input after validation failure
6. **Async carefully** - Debounce async checks to avoid flooding server
7. **Test edge cases** - Empty strings, special characters, max lengths
8. **Server-side too** - Never trust client-side validation alone
9. **Accessibility** - Use ARIA labels for screen readers
10. **Performance** - Validate in background, don't block UI

---

## See Also

**Validation Concepts:**
- [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) - Input field types (email_field, text_field, etc.)
- [STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md) - Pattern 3: Form Validation States

**Complete Examples:**
- [data_entry_form/](./examples/data_entry_form/) - Registration with complex validation
- [auth_flow/](./examples/auth_flow/) - Login with async validation
- [crud_application/](./examples/crud_application/) - Form validation in CRUD
- [wizard/](./examples/wizard/) - Step validation before advancing

**Related Topics:**
- [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) - Form field layout patterns
- [THEMING_GUIDE.md](./THEMING_GUIDE.md) - Error message styling

**Tools:**
- simple_spec_viz docs pattern form - Show form pattern
- /eiffel.gui-ux example data_entry_form - Show complete validation example
