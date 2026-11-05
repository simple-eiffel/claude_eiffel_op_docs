# Widget Catalog

Complete reference for all 40+ widgets in simple\_vision. Each widget shows:

* Description and purpose
* Factory method (fluent API via SV\_QUICK)
* JSON spec format
* Eiffel contracts (preconditions, postconditions)
* Fluent API chainable methods
* State machine integration
* Common usage patterns

---

## Windows

### Window

Main application window.

**Factory:**

```eiffel
sv.window ("Title")
```

**JSON:**

```json
{
  "id": "main\_window",
  "type": "window",
  "title": "My Application",
  "size": { "width": 800, "height": 600 },
  "min\_size": { "width": 400, "height": 300 },
  "resizable": true,
  "state\_machine": "app\_states",
  "layout": { "type": "vertical", "children": \[...] },
  "on\_close": "confirm\_exit"
}
```

**Fluent API:**

```eiffel
sv.window ("Title")
  .sized (width, height)
  .min\_sized (min\_width, min\_height)
  .resizable (True|False)
  .on\_close (agent handler)
  .child (widget)
```

**Contracts:**

```eiffel
require
  title\_valid: not title.is\_empty
ensure
  title\_set: window.title ~ title
  visible: window.is\_shown
```

**State Machine Integration:**
Use state machine to control window visibility:

```json
"states": \[
  { "id": "main", "enabled\_when": "user\_logged\_in" }
]
```

---

## Containers

### Row (Horizontal Box)

Arranges children left-to-right.

**Factory:**

```eiffel
sv.row
sv.row\_of (<<widget1, widget2>>)
```

**JSON:**

```json
{
  "type": "row",
  "padding": 10,
  "spacing": 8,
  "align": "stretch",
  "children": \[ ... ]
}
```

**Fluent API:**

```eiffel
sv.row
  .padding (size)
  .spacing (gap)
  .align ("stretch"|"center"|"start"|"end")
  .child (widget)
  .children (<<w1, w2, w3>>)
```

**Contracts:**

```eiffel
require
  padding\_valid: padding >= 0
  spacing\_valid: spacing >= 0
ensure
  children\_added: row.child\_count >= 0
```

**Common Pattern:**

```eiffel
-- Toolbar
sv.row
  .padding (5).spacing (5)
  .child (sv.button ("Save"))
  .child (sv.button ("Cancel"))
  .child (sv.spacer)
  .child (sv.button ("Help"))
```

### Column (Vertical Box)

Arranges children top-to-bottom.

**Factory:**

```eiffel
sv.column
sv.column\_of (<<widget1, widget2>>)
```

**JSON:**

```json
{
  "type": "column",
  "padding": 10,
  "spacing": 8,
  "align": "stretch",
  "children": \[ ... ]
}
```

**Fluent API:**

```eiffel
sv.column
  .padding (size)
  .spacing (gap)
  .align ("stretch"|"center"|"start"|"end")
  .child (widget)
  .children (<<w1, w2, w3>>)
```

### Grid

Arranges children in grid (rows × columns).

**Factory:**

```eiffel
sv.grid
sv.grid\_sized (cols, rows)
```

**JSON:**

```json
{
  "type": "grid",
  "columns": 3,
  "rows": 4,
  "padding": 10,
  "spacing": 8,
  "children": \[ ... ]
}
```

**Fluent API:**

```eiffel
sv.grid\_sized (3, 4)
  .padding (10).spacing (8)
  .child (widget)
```

**Common Pattern - 12-Column Responsive Layout:**

```json
{
  "type": "grid",
  "columns": 12,
  "gap": 16,
  "children": \[
    { "widget": "title", "column\_span": 12 },
    { "widget": "sidebar", "column\_span": 3 },
    { "widget": "main\_content", "column\_span": 9 }
  ]
}
```

### Tabs

Tab panel for multiple pages.

**Factory:**

```eiffel
sv.tabs
```

**JSON:**

```json
{
  "type": "tabs",
  "tabs": \[
    {
      "id": "tab1",
      "label": "General",
      "content": { "type": "column", "children": \[...] }
    },
    {
      "id": "tab2",
      "label": "Advanced",
      "content": { "type": "column", "children": \[...] }
    }
  ],
  "default\_tab": "tab1"
}
```

**Fluent API:**

```eiffel
sv.tabs
  .add\_tab ("General", general\_content)
  .add\_tab ("Advanced", advanced\_content)
  .set\_default\_tab ("General")
  .on\_change (agent handle\_tab\_switch)
```

### Card

Bordered panel (like a card).

**Factory:**

```eiffel
sv.card
sv.card\_titled ("Title")
```

**JSON:**

```json
{
  "type": "card",
  "title": "Card Title",
  "padding": 10,
  "border\_color": "#CCCCCC",
  "children": \[ ... ]
}
```

**Fluent API:**

```eiffel
sv.card\_titled ("Title")
  .padding (10)
  .border\_color (0xCCCCCC)
  .child (widget)
```

### Scroll Area

Scrollable container for overflow content.

**Factory:**

```eiffel
sv.scroll
```

**JSON:**

```json
{
  "type": "scroll",
  "horizontal": true,
  "vertical": true,
  "child": { ... }
}
```

**Fluent API:**

```eiffel
sv.scroll
  .horizontal (True)
  .vertical (True)
  .child (large\_widget)
```

### Splitter

Divider for resizable panels.

**Factory:**

```eiffel
sv.horizontal\_splitter    -- Left/right split
sv.vertical\_splitter      -- Top/bottom split
```

**JSON:**

```json
{
  "type": "splitter",
  "orientation": "horizontal",
  "left\_pane": { "widget": "sidebar" },
  "right\_pane": { "widget": "content" },
  "divider\_width": 5,
  "initial\_position": 200
}
```

**Fluent API:**

```eiffel
sv.horizontal\_splitter
  .left (sidebar)
  .right (content)
  .divider\_width (5)
  .initial\_position (200)
```

### Stack

Absolute positioning (like CSS absolute).

**Factory:**

```eiffel
sv.stack
```

**JSON:**

```json
{
  "type": "stack",
  "width": 400,
  "height": 300,
  "children": \[
    { "widget": "background", "x": 0, "y": 0, "width": 400, "height": 300 },
    { "widget": "overlay", "x": 50, "y": 50, "width": 100, "height": 100 }
  ]
}
```

**Fluent API:**

```eiffel
sv.stack
  .sized (400, 300)
  .add\_at (widget, x, y, width, height)
```

---

## Basic Widgets

### Text / Label

Static text label.

**Factory:**

```eiffel
sv.text ("Label text")
sv.label ("Alternative name")
```

**JSON:**

```json
{
  "type": "text",
  "content": "Hello, World!",
  "font\_size": 12,
  "font\_weight": "normal",
  "text\_align": "left",
  "color": "#000000"
}
```

**Fluent API:**

```eiffel
sv.text ("Hello")
  .font\_size (12)
  .font\_weight ("normal"|"bold")
  .text\_align ("left"|"center"|"right")
  .color (0x000000)
```

**Contracts:**

```eiffel
require
  content\_not\_empty: not content.is\_empty
ensure
  text\_visible: text.is\_visible
```

### Button

Clickable button.

**Factory:**

```eiffel
sv.button ("Click Me")
```

**JSON:**

```json
{
  "type": "button",
  "label": "Submit",
  "enabled\_when": "form\_valid",
  "visible\_when": "not loading",
  "on\_click": "submit\_form"
}
```

**Fluent API:**

```eiffel
sv.button ("Click Me")
  .on\_click (agent handle\_click)
  .enabled (True|False)
  .visible (True|False)
  .style ("primary"|"secondary"|"danger")
```

**Contracts:**

```eiffel
require
  label\_valid: not label.is\_empty
ensure
  clickable: button.is\_clickable
  handler\_set: button.has\_click\_handler
```

**State Machine Integration:**

```json
{
  "enabled\_when": "user\_authenticated",
  "visible\_when": "form\_validation\_complete"
}
```

### Checkbox

Toggle checkbox.

**Factory:**

```eiffel
sv.checkbox ("Enable Feature")
```

**JSON:**

```json
{
  "type": "checkbox",
  "label": "Enable Feature",
  "checked": false,
  "on\_change": "toggle\_feature"
}
```

**Fluent API:**

```eiffel
sv.checkbox ("Enable Feature")
  .checked (True|False)
  .on\_change (agent handle\_change)
```

### Radio Group

Mutually exclusive options.

**Factory:**

```eiffel
sv.radio\_group
sv.radios (<<"Option 1", "Option 2", "Option 3">>)
```

**JSON:**

```json
{
  "type": "radio\_group",
  "options": \[
    { "id": "opt1", "label": "Option 1" },
    { "id": "opt2", "label": "Option 2" },
    { "id": "opt3", "label": "Option 3" }
  ],
  "selected": "opt1",
  "on\_change": "selection\_changed"
}
```

**Fluent API:**

```eiffel
sv.radios (<<"Option 1", "Option 2">>)
  .selected ("Option 1")
  .on\_change (agent handle\_selection)
```

### Dropdown

Select from list.

**Factory:**

```eiffel
sv.dropdown
sv.dropdown\_with (<<"Choice A", "Choice B">>)
```

**JSON:**

```json
{
  "type": "dropdown",
  "options": \[
    { "id": "a", "label": "Choice A" },
    { "id": "b", "label": "Choice B" }
  ],
  "selected": "a",
  "on\_change": "choice\_changed"
}
```

**Fluent API:**

```eiffel
sv.dropdown\_with (<<"A", "B", "C">>)
  .selected ("A")
  .on\_change (agent handle\_selection)
```

### List

Selectable items list.

**Factory:**

```eiffel
sv.list
sv.list\_with (<<"Item 1", "Item 2">>)
```

**JSON:**

```json
{
  "type": "list",
  "items": \[
    { "id": "1", "label": "Item 1" },
    { "id": "2", "label": "Item 2" }
  ],
  "multi\_select": false,
  "on\_selection": "item\_selected"
}
```

**Fluent API:**

```eiffel
sv.list\_with (<<"A", "B", "C">>)
  .multi\_select (True|False)
  .on\_selection (agent handle\_selection)
```

### Slider

Range slider.

**Factory:**

```eiffel
sv.slider
sv.slider\_range (0, 100)
```

**JSON:**

```json
{
  "type": "slider",
  "min": 0,
  "max": 100,
  "value": 50,
  "step": 1,
  "on\_change": "value\_changed"
}
```

**Fluent API:**

```eiffel
sv.slider\_range (0, 100)
  .value (50)
  .step (1)
  .on\_change (agent handle\_change)
```

### Progress Bar

Visual progress indicator.

**Factory:**

```eiffel
sv.progress
```

**JSON:**

```json
{
  "type": "progress",
  "value": 65,
  "max": 100,
  "indeterminate": false,
  "label": "Loading..."
}
```

**Fluent API:**

```eiffel
sv.progress
  .value (65)
  .max (100)
  .indeterminate (False)
  .label ("Loading...")
```

### Spin Box

Numeric input with increment/decrement.

**Factory:**

```eiffel
sv.spin\_box
sv.spin\_box\_range (1, 10)
```

**JSON:**

```json
{
  "type": "spin\_box",
  "min": 1,
  "max": 10,
  "value": 5,
  "step": 1,
  "on\_change": "value\_changed"
}
```

**Fluent API:**

```eiffel
sv.spin\_box\_range (1, 10)
  .value (5)
  .step (1)
  .on\_change (agent handle\_change)
```

### Tree

Hierarchical tree widget.

**Factory:**

```eiffel
sv.tree
sv.tree\_with (root\_items)
```

**JSON:**

```json
{
  "type": "tree",
  "root\_items": \[
    {
      "id": "root1",
      "label": "Root 1",
      "children": \[
        { "id": "child1", "label": "Child 1" }
      ]
    }
  ],
  "on\_selection": "node\_selected"
}
```

**Fluent API:**

```eiffel
sv.tree
  .add\_root (root\_item)
  .on\_selection (agent handle\_selection)
```

---

## Input Fields

### Text Field

Single-line text input.

**Factory:**

```eiffel
sv.text\_field
sv.text\_input ("initial value")
```

**JSON:**

```json
{
  "type": "text\_field",
  "id": "username",
  "placeholder": "Enter username",
  "value": "",
  "max\_length": 50,
  "on\_change": "input\_changed",
  "validation": "username\_format"
}
```

**Fluent API:**

```eiffel
sv.text\_field
  .placeholder ("Enter text")
  .value ("initial")
  .max\_length (50)
  .on\_change (agent handle\_change)
```

**Contracts:**

```eiffel
require
  max\_length\_valid: max\_length > 0
ensure
  field\_created: field.is\_valid
```

### Password Field

Masked text input.

**Factory:**

```eiffel
sv.password\_field
```

**JSON:**

```json
{
  "type": "password\_field",
  "id": "password",
  "placeholder": "Enter password",
  "min\_length": 8,
  "validation": "password\_strength"
}
```

**Fluent API:**

```eiffel
sv.password\_field
  .placeholder ("Enter password")
  .min\_length (8)
  .on\_change (agent handle\_change)
```

---

## Masked Input Fields

Special-purpose input fields with format enforcement.

### Phone Field

US phone number (XXX) XXX-XXXX.

**Factory:**

```eiffel
sv.phone\_field
```

**JSON:**

```json
{
  "type": "masked\_field",
  "mask": "phone",
  "placeholder": "(XXX) XXX-XXXX"
}
```

### Email Field

Email address format validation.

**Factory:**

```eiffel
sv.email\_field
```

**JSON:**

```json
{
  "type": "masked\_field",
  "mask": "email",
  "placeholder": "user@example.com"
}
```

### Date Field

US date MM/DD/YYYY.

**Factory:**

```eiffel
sv.date\_field
sv.date\_field\_iso      -- ISO YYYY-MM-DD
```

**JSON:**

```json
{
  "type": "masked\_field",
  "mask": "date\_us",
  "placeholder": "MM/DD/YYYY"
}
```

### Credit Card Field

Credit card number with spacing.

**Factory:**

```eiffel
sv.credit\_card\_field
```

**JSON:**

```json
{
  "type": "masked\_field",
  "mask": "credit\_card",
  "placeholder": "XXXX XXXX XXXX XXXX"
}
```

### SSN Field

Social Security Number XXX-XX-XXXX.

**Factory:**

```eiffel
sv.ssn\_field
```

**JSON:**

```json
{
  "type": "masked\_field",
  "mask": "ssn",
  "placeholder": "XXX-XX-XXXX"
}
```

### ZIP Code Field

US ZIP code XXXXX or XXXXX-XXXX.

**Factory:**

```eiffel
sv.zip\_code\_field
```

**JSON:**

```json
{
  "type": "masked\_field",
  "mask": "zip\_code",
  "placeholder": "XXXXX"
}
```

### IP Address Field

IPv4 address XXX.XXX.XXX.XXX.

**Factory:**

```eiffel
sv.ip\_address\_field
```

**JSON:**

```json
{
  "type": "masked\_field",
  "mask": "ip\_address",
  "placeholder": "XXX.XXX.XXX.XXX"
}
```

### Time Field

24-hour time HH:MM.

**Factory:**

```eiffel
sv.time\_field
```

**JSON:**

```json
{
  "type": "masked\_field",
  "mask": "time\_24h",
  "placeholder": "HH:MM"
}
```

---

## Data Widgets

### Data Grid

Tabular data display with rows/columns.

**Factory:**

```eiffel
sv.data\_grid
sv.data\_grid\_with (<<"Name", "Email", "Phone">>)
```

**JSON:**

```json
{
  "type": "data\_grid",
  "columns": \[
    { "id": "name", "label": "Name", "width": 150 },
    { "id": "email", "label": "Email", "width": 200 },
    { "id": "phone", "label": "Phone", "width": 120 }
  ],
  "rows": \[
    { "name": "Alice", "email": "alice@example.com", "phone": "555-0001" }
  ],
  "sortable": true,
  "filterable": true
}
```

**Fluent API:**

```eiffel
sv.data\_grid\_with (<<"Name", "Email">>)
  .add\_column ("Phone", 120)
  .add\_row (<<<<"Alice", "alice@example.com", "555-0001">>>>)
  .sortable (True)
  .filterable (True)
```

### Decimal Field

Floating-point number input.

**Factory:**

```eiffel
sv.decimal\_field
```

**JSON:**

```json
{
  "type": "decimal\_field",
  "id": "price",
  "min": 0.0,
  "max": 9999.99,
  "decimal\_places": 2,
  "value": 0.0
}
```

**Fluent API:**

```eiffel
sv.decimal\_field
  .min (0.0)
  .max (9999.99)
  .decimal\_places (2)
  .value (0.0)
```

### Currency Field

Currency input (2 decimal places).

**Factory:**

```eiffel
sv.currency\_field
```

**JSON:**

```json
{
  "type": "decimal\_field",
  "currency": "USD",
  "decimal\_places": 2,
  "value": 0.00
}
```

**Fluent API:**

```eiffel
sv.currency\_field
  .currency ("USD")
  .value (0.00)
```

---

## Application Chrome

### Menu Bar

Main application menu.

**Factory:**

```eiffel
sv.menu\_bar
```

**JSON:**

```json
{
  "type": "menu\_bar",
  "menus": \[
    {
      "id": "file",
      "label": "File",
      "items": \[
        { "id": "open", "label": "Open", "on\_click": "open\_file" },
        { "id": "exit", "label": "Exit", "on\_click": "exit\_app" }
      ]
    }
  ]
}
```

**Fluent API:**

```eiffel
sv.menu\_bar
  .add\_menu (sv.menu ("File")
    .add\_item ("Open", agent open\_file)
    .add\_item ("Exit", agent exit\_app))
```

### Menu

Dropdown menu.

**Factory:**

```eiffel
sv.menu ("File")
```

**JSON:**

```json
{
  "type": "menu",
  "label": "File",
  "items": \[ ... ]
}
```

**Fluent API:**

```eiffel
sv.menu ("File")
  .add\_item ("Open", agent handler)
  .add\_separator
  .add\_item ("Exit", agent handler)
```

### Menu Item

Individual menu option.

**Factory:**

```eiffel
sv.menu\_item ("Open")
```

**JSON:**

```json
{
  "type": "menu\_item",
  "label": "Open",
  "accelerator": "Ctrl+O",
  "on\_click": "open\_file"
}
```

### Toolbar

Button bar for quick actions.

**Factory:**

```eiffel
sv.toolbar
```

**JSON:**

```json
{
  "type": "toolbar",
  "buttons": \[
    { "id": "save", "label": "Save", "icon": "save.png", "on\_click": "save" },
    { "id": "delete", "label": "Delete", "icon": "delete.png", "on\_click": "delete" }
  ]
}
```

**Fluent API:**

```eiffel
sv.toolbar
  .add\_button ("Save", agent save)
  .add\_button ("Delete", agent delete)
```

### Toolbar Button

Individual toolbar button.

**Factory:**

```eiffel
sv.toolbar\_button ("Save")
```

**JSON:**

```json
{
  "type": "toolbar\_button",
  "label": "Save",
  "icon": "save.png",
  "tooltip": "Save file",
  "on\_click": "save\_file"
}
```

### Status Bar

Bottom status display.

**Factory:**

```eiffel
sv.statusbar
sv.statusbar\_with ("Ready")
```

**JSON:**

```json
{
  "type": "statusbar",
  "text": "Ready",
  "sections": \[
    { "id": "status", "width": 200, "text": "Ready" },
    { "id": "info", "width": 300, "text": "" }
  ]
}
```

**Fluent API:**

```eiffel
sv.statusbar\_with ("Ready")
  .add\_section ("info", 300)
  .update\_status ("Updated")
```

---

## Dialogs

### Dialog

Modal dialog window.

**Factory:**

```eiffel
sv.dialog
sv.dialog\_with\_title ("Confirmation")
```

**JSON:**

```json
{
  "type": "dialog",
  "title": "Confirm Action",
  "modal": true,
  "size": { "width": 400, "height": 300 },
  "buttons": \[
    { "id": "ok", "label": "OK", "action": "confirm" },
    { "id": "cancel", "label": "Cancel", "action": "cancel" }
  ]
}
```

### File Dialog

File open/save dialog.

**Factory:**

```eiffel
sv.open\_file\_dialog
sv.save\_file\_dialog
```

**JSON:**

```json
{
  "type": "file\_dialog",
  "action": "open",
  "initial\_directory": "/home/user",
  "file\_types": \[
    { "extension": "txt", "description": "Text files" },
    { "extension": "\*", "description": "All files" }
  ]
}
```

### Message Box

Simple message dialog.

**Factory:**

```eiffel
sv.info\_box ("Information message")
sv.warning\_box ("Warning message")
sv.error\_box ("Error message")
sv.question\_box ("Are you sure?")
sv.confirm\_box ("OK/Cancel?")
```

**JSON:**

```json
{
  "type": "message\_box",
  "message": "Operation completed",
  "style": "info",
  "buttons": \["OK"]
}
```

### Color Picker

Color selection dialog.

**Factory:**

```eiffel
sv.color\_picker
```

**JSON:**

```json
{
  "type": "color\_picker",
  "initial\_color": "#FF0000",
  "allow\_alpha": true
}
```

### Font Picker

Font selection dialog.

**Factory:**

```eiffel
sv.font\_picker
```

**JSON:**

```json
{
  "type": "font\_picker",
  "initial\_font": "Arial",
  "initial\_size": 12
}
```

---

## Layout Helpers

### Spacer

Flexible space between widgets.

**Factory:**

```eiffel
sv.spacer              -- Flexible, grows to fill
sv.spacer\_fixed (20)   -- Fixed size
```

**JSON:**

```json
{
  "type": "spacer",
  "size": 0,
  "grow": true
}
```

**Fluent API:**

```eiffel
sv.row
  .child (sv.button ("Left"))
  .child (sv.spacer)    -- Push right button to right
  .child (sv.button ("Right"))
```

### Separator

Visual line divider.

**Factory:**

```eiffel
sv.separator\_horizontal
sv.separator\_vertical
```

**JSON:**

```json
{
  "type": "separator",
  "orientation": "horizontal",
  "color": "#CCCCCC"
}
```

### Divider

Themed separator line.

**Factory:**

```eiffel
sv.divider
sv.divider\_vertical
```

**JSON:**

```json
{
  "type": "divider",
  "orientation": "horizontal"
}
```

---

## Graphics

### Canvas (Cairo)

Custom drawing surface.

**Factory:**

```eiffel
sv.canvas (400, 300)
sv.canvas\_empty
```

**JSON:**

```json
{
  "type": "canvas",
  "width": 400,
  "height": 300,
  "background": "#FFFFFF"
}
```

**Fluent API:**

```eiffel
sv.canvas (400, 300)
  .background\_hex (0xFFFFFF)
  .on\_draw (agent draw\_handler)
```

**Drawing Example:**

```eiffel
draw\_handler (context: CAIRO\_CONTEXT)
  do
    context.set\_color\_hex (0x3498DB)
      .fill\_rect (10, 10, 100, 50)
      .do\_nothing
    context.set\_color\_hex (0xE74C3C)
      .stroke\_circle (200, 150, 40)
      .do\_nothing
  end
```

### Waveform

Audio waveform visualization.

**Factory:**

```eiffel
sv.waveform (300, 100)
sv.waveform\_default
```

**JSON:**

```json
{
  "type": "waveform",
  "width": 300,
  "height": 100,
  "foreground": "#3498DB",
  "background": "#2C3E50"
}
```

**Fluent API:**

```eiffel
sv.waveform (300, 100)
  .foreground\_hex (0x3498DB)
  .background\_hex (0x2C3E50)
  .set\_data (audio\_samples)
```

### Image

Image display widget.

**Factory:**

```eiffel
sv.image
sv.image\_from ("/path/to/image.png")
```

**JSON:**

```json
{
  "type": "image",
  "source": "/path/to/image.png",
  "width": 200,
  "height": 200,
  "fit": "contain"
}
```

**Fluent API:**

```eiffel
sv.image\_from ("/path/to/image.png")
  .sized (200, 200)
  .fit ("contain"|"cover"|"fill")
```

---

## Widget Lifecycle \& Common Patterns

### Widget Visibility (State Machine Integration)

Use state machine to control widget visibility:

```json
{
  "widgets": \[
    {
      "type": "button",
      "label": "Submit",
      "visible\_when": "form\_valid",
      "enabled\_when": "not loading"
    }
  ],
  "states": \[
    { "id": "editing", "visible\_when": true },
    { "id": "loading", "visible\_when": false },
    { "id": "submitted", "visible\_when": false }
  ]
}
```

### Form Field Validation

Integrate validation into widget specs:

```json
{
  "type": "text\_field",
  "id": "email",
  "placeholder": "Enter email",
  "validation": \[
    { "rule": "required", "message": "Email required" },
    { "rule": "email", "message": "Invalid email format" }
  ],
  "show\_validation\_on": "blur",
  "error\_message\_location": "below"
}
```

### Widget Events

Common widget events used in state machines:

|Event|Triggered By|
|-|-|
|`on\_click`|Button, menu item|
|`on\_change`|Input field, dropdown, checkbox, slider|
|`on\_selection`|List, tree, radio group|
|`on\_close`|Window, dialog|
|`on\_focus`|Input field|
|`on\_blur`|Input field|
|`on\_submit`|Form|

---

## See Also

**Widget Usage:**
* [STATE\_MACHINE\_GUIDE.md](./STATE_MACHINE_GUIDE.md) - Control widget visibility with enabled\_when/visible\_when
* [VALIDATION\_GUIDE.md](./VALIDATION_GUIDE.md) - Add validation to input widgets
* [LAYOUT\_PATTERNS.md](./LAYOUT_PATTERNS.md) - Combine widgets in containers
* [THEMING\_GUIDE.md](./THEMING_GUIDE.md) - Style and customize widgets

**Quick Reference:**
* [QUICKSTART.md](./QUICKSTART.md) - Login example using text\_field, password\_field, button, progress
* [WIDGET\_CATALOG.md](./WIDGET_CATALOG.md) - This file (40+ widgets documented)

**Examples Using Specific Widgets:**
* **Buttons:** All examples
* **Text fields:** auth\_flow, data\_entry\_form
* **Data grids:** crud\_application, dashboard
* **Tabs:** dashboard, settings
* **Cards:** All complex layouts
* **Progress bar:** auth\_flow (loading), loading\_pattern
* **Dropdowns:** data\_entry\_form, settings
* **Checkboxes:** data\_entry\_form, settings
* **List:** settings

**Tools:**
* simple\_spec\_viz docs widget <name> - Show widget reference in CLI
* /eiffel.gui-ux widget <name> - Show widget in Claude Code
