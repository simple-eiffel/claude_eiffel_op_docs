# simple_tui v1.0 - Terminal UI Library for Eiffel

**Announcing simple_tui** - A modern terminal-based UI framework for Eiffel with EiffelVision2-compatible API.

## What is simple_tui?

simple_tui provides everything you need to build interactive console applications in Eiffel:

- **EiffelVision2-compatible API** - Familiar `extend`/`prune` naming conventions
- **Complete widget set** - Buttons, text fields, checkboxes, radio buttons, lists, combo boxes, progress bars, tabs
- **Menu system** - Drop-down menus with keyboard shortcuts (Alt+key)
- **Modal dialogs** - Message boxes with OK/Cancel buttons
- **256-color support** - Full terminal color palette
- **Mouse input** - Click, drag, and hover support
- **Keyboard navigation** - Tab, arrows, shortcuts, and focus management
- **Unicode rendering** - Box drawing characters and special symbols

## Quick Start

```eiffel
class MY_APP

inherit
    TUI_APPLICATION
        redefine
            setup
        end

create
    make

feature {NONE} -- Initialization

    setup
            -- Build the UI.
        local
            box: TUI_BOX
            btn: TUI_BUTTON
        do
            create box.make_with_title ("My App", 40, 10)
            create btn.make ("Click Me")
            btn.set_on_click (agent on_click)
            box.extend (btn)  -- EV-compatible API
            root.extend (box)
        end

    on_click
            -- Button clicked.
        do
            quit
        end

end
```

## Try It Now

Download the demo from:
- **GitHub**: https://github.com/simple-eiffel/simple_tui

The repository includes:
- Pre-built Windows binary: `bin/tui_demo.exe`
- Comprehensive documentation: `docs/` and `README.md`
- Cookbook with 8 practical recipes
- Full widget demo application

## Widget Overview

| Widget | EV Equivalent | Description |
|--------|---------------|-------------|
| TUI_BUTTON | EV_BUTTON | Clickable button |
| TUI_TEXT_FIELD | EV_TEXT_FIELD | Text input with cursor |
| TUI_CHECKBOX | EV_CHECK_BUTTON | Toggle checkbox |
| TUI_RADIO_BUTTON | EV_RADIO_BUTTON | Exclusive selection |
| TUI_LIST | EV_LIST | Scrollable list |
| TUI_COMBO_BOX | EV_COMBO_BOX | Dropdown selection |
| TUI_PROGRESS | EV_PROGRESS_BAR | Progress indicator |
| TUI_TABS | EV_NOTEBOOK | Tabbed panels |
| TUI_MENU_BAR | EV_MENU_BAR | Horizontal menu bar |
| TUI_MESSAGE_BOX | EV_MESSAGE_DIALOG | Modal dialogs |

## Documentation

- **README.md** - Complete widget reference and examples
- **docs/index.html** - Overview and API reference
- **docs/user-guide.html** - Detailed how-to guide
- **docs/cookbook.html** - 8 practical recipes

## Platform Support

- **Windows**: Full support (Win32 Console API)
- **Linux/macOS**: Planned (ANSI escape sequences)

## Installation

```
SIMPLE_EIFFEL=D:\prod
```

```xml
<library name="simple_tui" location="$SIMPLE_EIFFEL/simple_tui/simple_tui.ecf"/>
```

## Part of Simple Eiffel

simple_tui is part of the [Simple Eiffel](https://github.com/simple-eiffel) ecosystem - a collection of focused, single-purpose Eiffel libraries.

## License

MIT License

---

## Post Summary (for forums/social)

**simple_tui v1.0 Released** - Build terminal UIs in Eiffel with an EiffelVision2-compatible API. Features: buttons, text fields, checkboxes, lists, tabs, menus, dialogs, 256 colors, mouse support, and more. Pre-built Windows demo included.

GitHub: https://github.com/simple-eiffel/simple_tui
Docs: https://simple-eiffel.github.io/simple_tui/

---

## Forum/Email Announcement Text

Subject: [ANN] simple_tui v1.0 - Terminal UI Library for Eiffel

Hello Eiffel community,

I'm pleased to announce the release of simple_tui v1.0 - a terminal-based user interface library for Eiffel.

**Key Features:**
- EiffelVision2-compatible API (extend/prune naming)
- Complete widget set: buttons, text fields, checkboxes, radio buttons, lists, combo boxes, progress bars, tabs
- Menu system with Alt+key shortcuts
- Modal dialogs (message boxes)
- 256-color support
- Mouse and keyboard input
- Unicode box drawing characters

**Why terminal UI?**
- Runs in any terminal/console
- Lightweight, no GUI dependencies
- Great for server administration tools, CLIs, embedded systems
- Familiar API for EV developers

**Try it:**
Download from https://github.com/simple-eiffel/simple_tui
The `bin/tui_demo.exe` shows all widgets in action.

Documentation includes a User Guide and Cookbook with 8 practical recipes.

Currently Windows-only (Win32 Console API). Linux/macOS support is planned.

Feedback and contributions welcome!

Best regards,
Larry Rix
