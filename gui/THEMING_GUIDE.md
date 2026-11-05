# Theming Guide

Control visual appearance of simple_vision applications.

---

## Dark Mode

Toggle between light and dark themes.

### Enable Dark Mode

**JSON Spec:**
```json
{
  "app": {
    "name": "my_app",
    "dark_mode": true
  }
}
```

**Eiffel:**
```eiffel
sv.set_dark_mode (True)
```

### Toggle at Runtime

```eiffel
-- Toggle dark mode
sv.toggle_dark_mode

-- Check current mode
if sv.is_dark_mode then
  print ("Dark mode enabled%N")
end
```

### With State Machine

Control dark mode via state machine:

```json
{
  "states": [
    { "id": "light_mode", "entry_action": "set_light_theme" },
    { "id": "dark_mode", "entry_action": "set_dark_theme" }
  ],
  "transitions": [
    { "from": "light_mode", "event": "toggle", "to": "dark_mode" },
    { "from": "dark_mode", "event": "toggle", "to": "light_mode" }
  ]
}
```

---

## Color Schemes

Predefined color palettes.

### Available Schemes

```eiffel
sv.set_color_scheme ("blue")    -- Default
sv.set_color_scheme ("green")
sv.set_color_scheme ("purple")
```

**JSON:**
```json
{
  "app": {
    "color_scheme": "blue"
  }
}
```

### Color Scheme Colors

Each scheme defines:

**Blue Scheme:**
- Primary: #2196F3 (Blue)
- Success: #4CAF50 (Green)
- Warning: #FF9800 (Orange)
- Error: #F44336 (Red)
- Background: #FFFFFF / #121212 (dark)
- Text: #212121 / #FFFFFF (dark)

**Green Scheme:**
- Primary: #4CAF50 (Green)
- Success: #66BB6A
- Warning: #FFC107 (Amber)
- Error: #F44336 (Red)
- Background: #FFFFFF / #1B5E20 (dark)
- Text: #212121 / #FFFFFF (dark)

**Purple Scheme:**
- Primary: #9C27B0 (Purple)
- Success: #4CAF50 (Green)
- Warning: #FF9800 (Orange)
- Error: #F44336 (Red)
- Background: #FFFFFF / #311B92 (dark)
- Text: #212121 / #FFFFFF (dark)

### Custom Scheme

Define your own colors:

```json
{
  "themes": [
    {
      "id": "corporate",
      "colors": {
        "primary": "#1A5490",
        "secondary": "#2D8659",
        "success": "#27AE60",
        "warning": "#E67E22",
        "error": "#C0392B",
        "info": "#3498DB",
        "light_bg": "#F5F5F5",
        "dark_bg": "#2C3E50",
        "light_text": "#212121",
        "dark_text": "#FFFFFF"
      }
    }
  ]
}
```

**Eiffel:**
```eiffel
theme := sv.create_theme ("corporate")
theme.set_primary (0x1A5490)
theme.set_success (0x27AE60)
theme.set_error (0xC0392B)
sv.apply_theme (theme)
```

---

## UI Scaling

Increase/decrease font sizes and widget sizes.

### Set Scale

```eiffel
sv.set_ui_scale (1.25)   -- 125% (25% larger)
sv.set_ui_scale (0.875)  -- 87.5% (12.5% smaller)
sv.set_ui_scale (1.0)    -- Reset to 100%
```

**JSON:**
```json
{
  "app": {
    "ui_scale": 1.25
  }
}
```

### Increment/Decrement

```eiffel
sv.increase_ui_scale  -- +10%
sv.decrease_ui_scale  -- -10%
sv.reset_ui_scale     -- 100%
```

### Dynamic Scaling

Change scale in response to user action:

```eiffel
handle_zoom_in_click
  do
    sv.increase_ui_scale
    redraw_all_windows
  end

handle_zoom_out_click
  do
    sv.decrease_ui_scale
    redraw_all_windows
  end
```

---

## Widget Styling

### Text Styling

```json
{
  "type": "text",
  "content": "Heading",
  "font_size": 18,
  "font_weight": "bold",
  "text_color": "#2196F3",
  "text_align": "center"
}
```

**Eiffel:**
```eiffel
sv.text ("Heading")
  .font_size (18)
  .font_weight ("bold")
  .color (0x2196F3)
  .text_align ("center")
```

### Button Styling

```json
{
  "type": "button",
  "label": "Submit",
  "style": "primary",
  "size": "large",
  "icon": "save.png"
}
```

**Styles:**
- `primary` - Filled background, white text
- `secondary` - Outlined, colored border
- `danger` - Red for destructive actions
- `success` - Green for confirmations
- `plain` - No background, minimal

**Eiffel:**
```eiffel
sv.button ("Submit")
  .style ("primary")
  .size ("large")
  .icon ("save.png")
```

### Input Field Styling

```json
{
  "type": "text_field",
  "placeholder": "Enter name",
  "styles": {
    "border_color": "#CCCCCC",
    "border_width": 1,
    "border_radius": 4,
    "padding": 8,
    "font_size": 14
  }
}
```

**Eiffel:**
```eiffel
sv.text_field
  .border_color (0xCCCCCC)
  .border_width (1)
  .border_radius (4)
  .padding (8)
```

### Container Styling

```json
{
  "type": "card",
  "border_color": "#E0E0E0",
  "border_width": 1,
  "shadow": "0px 2px 4px rgba(0,0,0,0.1)",
  "background": "#FFFFFF",
  "padding": 16,
  "border_radius": 8
}
```

**Eiffel:**
```eiffel
sv.card
  .border_color (0xE0E0E0)
  .border_width (1)
  .shadow ("0px 2px 4px rgba(0,0,0,0.1)")
  .background (0xFFFFFF)
  .padding (16)
  .border_radius (8)
```

---

## Color Tokens

Use semantic color names instead of hex values.

### Standard Tokens

```json
{
  "tokens": {
    "color_primary": "#2196F3",
    "color_secondary": "#757575",
    "color_success": "#4CAF50",
    "color_warning": "#FF9800",
    "color_error": "#F44336",
    "color_info": "#00BCD4",
    "spacing_small": 8,
    "spacing_medium": 16,
    "spacing_large": 24,
    "border_radius_small": 2,
    "border_radius_medium": 4,
    "border_radius_large": 8,
    "elevation_1": "0px 2px 4px rgba(0,0,0,0.1)",
    "elevation_2": "0px 4px 8px rgba(0,0,0,0.15)"
  }
}
```

### Using Tokens

```json
{
  "type": "button",
  "label": "Save",
  "background": "@color_primary",
  "padding": "@spacing_medium",
  "border_radius": "@border_radius_medium",
  "box_shadow": "@elevation_1"
}
```

**Eiffel:**
```eiffel
theme := sv.get_theme
button := sv.button ("Save")
  .background (theme.color_primary)
  .padding (theme.spacing_medium)
  .border_radius (theme.border_radius_medium)
```

---

## Typography

### Font Family

```eiffel
sv.set_font_family ("Segoe UI")
sv.set_monospace_font ("Courier New")
```

### Font Sizes

**Hierarchy:**
- Display: 32px (large headings)
- Heading 1: 24px (page title)
- Heading 2: 20px (section title)
- Heading 3: 16px (subsection)
- Body: 14px (regular text)
- Small: 12px (labels, hints)
- Tiny: 10px (metadata)

```json
{
  "type": "text",
  "content": "Page Title",
  "size": "h1"
}
```

**Eiffel:**
```eiffel
sv.text ("Page Title")
  .font_size (24)
  .font_weight ("bold")
```

### Font Weights

```eiffel
.font_weight ("light")     -- 300
.font_weight ("normal")    -- 400
.font_weight ("medium")    -- 500
.font_weight ("semibold")  -- 600
.font_weight ("bold")      -- 700
.font_weight ("black")     -- 900
```

---

## Global Theme Configuration

### Theme Definition

```json
{
  "themes": {
    "light": {
      "primary_color": "#2196F3",
      "secondary_color": "#757575",
      "background": "#FFFFFF",
      "text": "#212121",
      "border": "#BDBDBD",
      "font_family": "Segoe UI",
      "font_size_base": 14,
      "border_radius": 4,
      "spacing_unit": 8
    },
    "dark": {
      "primary_color": "#64B5F6",
      "secondary_color": "#BDBDBD",
      "background": "#121212",
      "text": "#FFFFFF",
      "border": "#424242",
      "font_family": "Segoe UI",
      "font_size_base": 14,
      "border_radius": 4,
      "spacing_unit": 8
    }
  }
}
```

### Applying Global Theme

```eiffel
-- Use predefined theme
sv.apply_theme (sv.get_builtin_theme ("light"))

-- Or load from spec
if attached sv.theme_from_json (spec_file) as theme then
  sv.apply_theme (theme)
end
```

---

## Common Theme Patterns

### Material Design (Light)

```json
{
  "theme": "material_light",
  "colors": {
    "primary": "#2196F3",
    "accent": "#FF4081",
    "background": "#FAFAFA",
    "surface": "#FFFFFF",
    "error": "#F44336"
  },
  "typography": {
    "font_family": "Roboto",
    "body_size": 14
  },
  "spacing": 8,
  "corner_radius": 2
}
```

### Material Design (Dark)

```json
{
  "theme": "material_dark",
  "colors": {
    "primary": "#64B5F6",
    "accent": "#FF80AB",
    "background": "#121212",
    "surface": "#1E1E1E",
    "error": "#CF6679"
  },
  "typography": {
    "font_family": "Roboto",
    "body_size": 14
  },
  "spacing": 8,
  "corner_radius": 2
}
```

### Corporate (Professional)

```json
{
  "theme": "corporate",
  "colors": {
    "primary": "#0052CC",
    "secondary": "#626262",
    "background": "#F8F9FA",
    "surface": "#FFFFFF",
    "error": "#AE1A1A"
  },
  "typography": {
    "font_family": "Helvetica Neue",
    "body_size": 13
  },
  "spacing": 12,
  "corner_radius": 4
}
```

### Accessible (High Contrast)

```json
{
  "theme": "accessible",
  "colors": {
    "primary": "#000000",
    "secondary": "#333333",
    "background": "#FFFFFF",
    "surface": "#FFFFFF",
    "error": "#660000",
    "focus_indicator": "#0000FF"
  },
  "typography": {
    "font_family": "Arial",
    "body_size": 16
  },
  "spacing": 10,
  "corner_radius": 0,
  "border_width": 2
}
```

---

## Accessibility

### Color Contrast

Ensure text is readable:
- Normal text: 4.5:1 ratio
- Large text (18pt+): 3:1 ratio

```json
{
  "theme": {
    "validations": [
      {
        "check": "color_contrast",
        "foreground": "#212121",
        "background": "#FFFFFF",
        "minimum_ratio": 4.5
      }
    ]
  }
}
```

### Focus Indicators

Make keyboard navigation visible:

```json
{
  "theme": {
    "focus_style": {
      "outline": "2px solid #0000FF",
      "outline_offset": "2px"
    }
  }
}
```

**Eiffel:**
```eiffel
theme.set_focus_outline (2, 0x0000FF)
```

### Size Adjustments

Support larger text for visibility:

```eiffel
-- Large text mode
sv.set_ui_scale (1.5)  -- 150% scale

-- Large spacing
sv.set_spacing_multiplier (1.5)
```

---

## Best Practices

1. **Limit color palette** - 3-5 colors + neutrals
2. **Maintain contrast** - Test with color blind simulators
3. **Use semantic colors** - Don't use "red" for info
4. **Consistent spacing** - Use multiples of base unit
5. **Font hierarchy** - Clear visual differentiation
6. **Dark mode** - Provide high-contrast variant
7. **User control** - Let users choose theme/scale
8. **Test accessibility** - Use WCAG guidelines
9. **Document tokens** - Keep design system reference
10. **Performance** - Cache themes, avoid runtime recompilation

---

## See Also

**Styling Topics:**
- [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) - Individual widget styling (button style, text color, etc.)
- [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) - Spacing and alignment

**Theme Examples:**
- [dashboard/](./examples/dashboard/) - Professional dashboard styling
- All examples show proper spacing and theming applied

**State Machine Integration:**
- [STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md) - Theme switching state machine
- Dark mode toggle pattern

**Tools:**
- simple_spec_viz docs widget text - Show text styling options
- /eiffel.gui-ux widget button - Show button style options
