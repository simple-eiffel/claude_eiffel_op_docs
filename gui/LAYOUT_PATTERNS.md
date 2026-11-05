# Layout Patterns

Master layouts in simple_vision and JSON specs.

---

## Grid System

Simple_vision supports 12-column grid for responsive design.

### Basic 12-Column Grid

```json
{
  "type": "grid",
  "columns": 12,
  "gap": 16,
  "children": [
    { "widget": "header", "column_span": 12 },
    { "widget": "sidebar", "column_span": 3 },
    { "widget": "main_content", "column_span": 9 },
    { "widget": "footer", "column_span": 12 }
  ]
}
```

**Eiffel:**
```eiffel
sv.grid_sized (12, 1)
  .child (header)  -- full width
  .child (sidebar)  -- 3 cols
  .child (content)  -- 9 cols
  .child (footer)   -- full width
```

### Common Grid Layouts

**1. Full Width**
```
┌─────────────────────┐
│  Header (12)        │
├─────────────────────┤
│  Content (12)       │
├─────────────────────┤
│  Footer (12)        │
└─────────────────────┘
```

**2. Sidebar Layout**
```
┌─────┬──────────────┐
│ S   │  Main (9)    │
│ (3) │              │
│     │              │
├─────┴──────────────┤
│  Footer (12)       │
└────────────────────┘
```

**3. Two Column**
```
┌──────────┬─────────┐
│ Left (6) │ Right (6)
├──────────┴─────────┤
│ Footer (12)        │
└────────────────────┘
```

**4. Three Column**
```
┌────┬────────┬────┐
│(3) │ (6)    │(3) │
├────┴────────┴────┤
│ Footer (12)      │
└──────────────────┘
```

---

## Flexbox Containers

### Row (Horizontal Layout)

Items flow left-to-right.

```json
{
  "type": "row",
  "spacing": 10,
  "align": "stretch",
  "children": [
    { "widget": "button1" },
    { "widget": "button2" },
    { "widget": "spacer", "grow": true },
    { "widget": "button3" }
  ]
}
```

**Eiffel:**
```eiffel
sv.row
  .spacing (10)
  .align ("stretch")
  .child (button1)
  .child (button2)
  .child (sv.spacer)  -- Pushes button3 to right
  .child (button3)
```

**Alignment Options:**
- `stretch` - Fill available space
- `center` - Center items
- `start` - Left align
- `end` - Right align
- `space-between` - Space between items
- `space-around` - Space around items

### Column (Vertical Layout)

Items flow top-to-bottom.

```json
{
  "type": "column",
  "padding": 20,
  "spacing": 10,
  "align": "stretch",
  "children": [
    { "widget": "title" },
    { "widget": "form_fields" },
    { "widget": "button_row" }
  ]
}
```

**Eiffel:**
```eiffel
sv.column
  .padding (20)
  .spacing (10)
  .align ("stretch")
  .child (sv.text ("Form Title"))
  .child (form_content)
  .child (button_row)
```

---

## Common Patterns

### Toolbar

Buttons in a horizontal bar.

```json
{
  "type": "row",
  "padding": 5,
  "spacing": 5,
  "children": [
    { "widget": "save_btn" },
    { "widget": "edit_btn" },
    { "widget": "delete_btn" },
    { "widget": "spacer", "grow": true },
    { "widget": "help_btn" }
  ]
}
```

### Form Layout

Label + field pairs, stacked vertically.

```json
{
  "type": "column",
  "spacing": 15,
  "children": [
    {
      "type": "column",
      "spacing": 5,
      "children": [
        { "type": "text", "content": "Username" },
        { "type": "text_field", "placeholder": "Enter username" }
      ]
    },
    {
      "type": "column",
      "spacing": 5,
      "children": [
        { "type": "text", "content": "Email" },
        { "type": "email_field", "placeholder": "Enter email" }
      ]
    }
  ]
}
```

### Master-Detail

List on left, detail on right.

```json
{
  "type": "row",
  "spacing": 10,
  "children": [
    {
      "type": "column",
      "width": 200,
      "children": [
        { "type": "text", "content": "Items" },
        { "type": "list", "items": [...] }
      ]
    },
    {
      "type": "column",
      "grow": true,
      "children": [
        { "type": "text", "content": "Details" },
        { "type": "card", "child": { "type": "column", "children": [...] } }
      ]
    }
  ]
}
```

**Eiffel:**
```eiffel
sv.row
  .spacing (10)
  .child (
    sv.column
      .width (200)
      .child (sv.text ("Items"))
      .child (items_list))
  .child (
    sv.column
      .child (sv.text ("Details"))
      .child (detail_card))
```

### Dashboard Grid

Cards arranged in grid.

```json
{
  "type": "grid",
  "columns": 3,
  "gap": 16,
  "children": [
    { "widget": "card1", "column_span": 1 },
    { "widget": "card2", "column_span": 1 },
    { "widget": "card3", "column_span": 1 },
    { "widget": "card4", "column_span": 2 },
    { "widget": "card5", "column_span": 1 }
  ]
}
```

### Modal Dialog

Centered dialog over content.

```json
{
  "type": "dialog",
  "title": "Confirm Action",
  "modal": true,
  "width": 400,
  "height": 200,
  "children": [
    { "type": "text", "content": "Are you sure?" },
    {
      "type": "row",
      "spacing": 10,
      "children": [
        { "type": "button", "label": "OK" },
        { "type": "button", "label": "Cancel" }
      ]
    }
  ]
}
```

### Tabs Layout

Multiple pages in tabs.

```json
{
  "type": "tabs",
  "tabs": [
    {
      "id": "general",
      "label": "General",
      "content": {
        "type": "column",
        "children": [...]
      }
    },
    {
      "id": "advanced",
      "label": "Advanced",
      "content": {
        "type": "column",
        "children": [...]
      }
    }
  ]
}
```

---

## Responsive Design

### Breakpoints

Adjust layout based on window size.

```json
{
  "type": "column",
  "children": [
    {
      "type": "row",
      "breakpoint_desktop": { "columns": 3, "gap": 20 },
      "breakpoint_tablet": { "columns": 2, "gap": 15 },
      "breakpoint_mobile": { "columns": 1, "gap": 10 },
      "children": [...]
    }
  ]
}
```

### Flexible Sizing

Use grow/shrink for responsive widgets.

```eiffel
sv.row
  .spacing (10)
  .child (
    sv.column
      .width (200)      -- Fixed width sidebar
      .child (sidebar_content))
  .child (
    sv.column
      .grow (True)      -- Flexible main content
      .child (main_content))
```

---

## Spacing & Padding

### Container Padding

Space inside container.

```json
{
  "type": "card",
  "padding": 20,
  "children": [...]
}
```

### Gap Between Items

Space between child items.

```json
{
  "type": "column",
  "spacing": 10,  -- 10px between items
  "children": [...]
}
```

### Spacers for Layout

Flexible space that grows/shrinks.

```eiffel
sv.row
  .child (sv.button ("Left"))
  .child (sv.spacer)    -- Flexible, pushes next to right
  .child (sv.button ("Right"))
```

Fixed spacer:
```eiffel
sv.row
  .spacing (10)
  .child (sv.spacer_fixed (20))  -- Exactly 20px
```

---

## Nesting

Combine containers for complex layouts.

```
Column
├─ Row (header)
│  ├─ Logo
│  └─ Menu
├─ Row (content)
│  ├─ Column (sidebar)
│  │  ├─ Nav items
│  │  └─ Settings
│  └─ Column (main)
│     ├─ Tabs
│     │  ├─ Tab content
│     │  └─ Tab content
│     └─ Status
└─ Row (footer)
   └─ Footer content
```

**Eiffel:**
```eiffel
main_layout := sv.column
  .padding (0).spacing (0)
  .child (create_header (sv))
  .child (create_content_row (sv))
  .child (create_footer (sv))
```

---

## Overflow & Scrolling

### Scrollable Container

For content that might overflow.

```json
{
  "type": "scroll",
  "vertical": true,
  "horizontal": false,
  "child": {
    "type": "column",
    "children": [...]
  }
}
```

**Eiffel:**
```eiffel
sv.scroll
  .vertical (True)
  .horizontal (False)
  .child (long_list)
```

### Splitter

Resizable divider between panes.

```eiffel
sv.horizontal_splitter
  .left (sidebar)
  .right (main_content)
  .divider_width (5)
  .initial_position (200)
```

---

## Best Practices

1. **Start with the grid** - Use 12-column for alignment
2. **Nest containers** - Build complexity from simple blocks
3. **Use flexible space** - Spacers adapt to window size
4. **Padding vs Gap** - Padding inside, gap between
5. **Label form fields** - Always put label above/left of input
6. **Group related widgets** - Use cards/panels for visual grouping
7. **Consistent spacing** - Use multiples of 8 or 10 for rhythm
8. **Test responsiveness** - Resize window to check layout

---

## See Also

**Layout Techniques:**
- [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) - Grid, row, column, stack, splitter, card
- [THEMING_GUIDE.md](./THEMING_GUIDE.md) - Spacing tokens and alignment

**Examples:**
- [dashboard/](./examples/dashboard/) - 12-column grid with cards
- [crud_application/](./examples/crud_application/) - Master-detail sidebar layout
- [settings/](./examples/settings/) - Left menu + right content
- [wizard/](./examples/wizard/) - Centered form layout

**State Machine Integration:**
- [STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md) - Show/hide containers with states

**Tools:**
- /eiffel.gui-ux widget grid - Show grid documentation
- /eiffel.gui-ux pattern crud - Master-detail pattern example
