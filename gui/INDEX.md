# GUI Reference Documentation - Complete Index

## Quick Links

**New to simple_vision? Start here:**
- [README.md](./README.md) - Overview and navigation
- [QUICKSTART.md](./QUICKSTART.md) - 5-minute tutorial

**Looking for something specific?**
- [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) - 40+ widgets with full API reference
- [STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md) - UI state management
- [VALIDATION_GUIDE.md](./VALIDATION_GUIDE.md) - Form validation patterns
- [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) - Container layouts and grid
- [THEMING_GUIDE.md](./THEMING_GUIDE.md) - Dark mode, colors, styling
- [WORKFLOW_GUIDE.md](./WORKFLOW_GUIDE.md) - End-to-end development workflow

**Need a working example?**
- [examples/auth_flow/](./examples/auth_flow/) - Login with error recovery
- [examples/data_entry_form/](./examples/data_entry_form/) - Complex form validation
- [examples/crud_application/](./examples/crud_application/) - Full CRUD workflow
- [examples/dashboard/](./examples/dashboard/) - Complex layout with tabs
- [examples/wizard/](./examples/wizard/) - Multi-step onboarding
- [examples/settings/](./examples/settings/) - Nested panels with save/cancel
- [examples/loading_pattern/](./examples/loading_pattern/) - Async data fetching

---

## By Learning Path

### Path 1: Complete Beginner (Recommended first pass)

1. **[README.md](./README.md)** (5 min) - Understand what's available
2. **[QUICKSTART.md](./QUICKSTART.md)** (10 min) - Build your first GUI
3. **[WIDGET_CATALOG.md](./WIDGET_CATALOG.md)** (30 min) - Learn available widgets
4. **[STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md)** (45 min) - Understand state machines
5. Pick an **[example](./examples/)** and implement it (1-2 hours)
6. Reference remaining guides as needed

### Path 2: Focused on Forms

1. **[QUICKSTART.md](./QUICKSTART.md)** (10 min) - Basic concepts
2. **[VALIDATION_GUIDE.md](./VALIDATION_GUIDE.md)** (30 min) - Form validation
3. **[data_entry_form example](./examples/data_entry_form/)** (30 min) - Real example
4. **[WIDGET_CATALOG.md](./WIDGET_CATALOG.md)** - Reference input widgets as needed
5. **[LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md)** - Form layout patterns

### Path 3: Focused on Complex Applications

1. **[WORKFLOW_GUIDE.md](./WORKFLOW_GUIDE.md)** (30 min) - Understand full workflow
2. **[STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md)** (45 min) - Master state machines
3. **[LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md)** (30 min) - Complex layouts
4. Pick an **[example](./examples/)**: [crud_application](./examples/crud_application/) or [dashboard](./examples/dashboard/)
5. **[WIDGET_CATALOG.md](./WIDGET_CATALOG.md)** - Reference widgets

### Path 4: Focused on Styling

1. **[THEMING_GUIDE.md](./THEMING_GUIDE.md)** (30 min) - Colors, dark mode, scaling
2. **[LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md)** (20 min) - Spacing and alignment
3. **[WIDGET_CATALOG.md](./WIDGET_CATALOG.md)** - Widget styling reference
4. **[dashboard example](./examples/dashboard/)** - Professional styling example

---

## By Topic

| Topic | Primary Document | Secondary | Examples |
|-------|------------------|-----------|----------|
| Getting started | README.md | QUICKSTART.md | auth_flow |
| Widgets | WIDGET_CATALOG.md | - | All |
| State machines | STATE_MACHINE_GUIDE.md | - | All |
| Forms & validation | VALIDATION_GUIDE.md | - | data_entry_form |
| Layouts | LAYOUT_PATTERNS.md | - | dashboard, crud_application |
| Styling | THEMING_GUIDE.md | - | dashboard |
| Async operations | STATE_MACHINE_GUIDE.md (Pattern 2) | - | loading_pattern, auth_flow |
| Multi-step | STATE_MACHINE_GUIDE.md (Pattern 4) | - | wizard |
| CRUD | STATE_MACHINE_GUIDE.md (Pattern 5) | - | crud_application |
| Settings | LAYOUT_PATTERNS.md | - | settings |
| Workflow | WORKFLOW_GUIDE.md | - | - |

---

## By Complexity Level

### Beginner: Single-Screen Forms

Start here:
- [QUICKSTART.md](./QUICKSTART.md)
- [VALIDATION_GUIDE.md](./VALIDATION_GUIDE.md)
- [examples/data_entry_form/](./examples/data_entry_form/)

Examples:
- [auth_flow](./examples/auth_flow/) - Simple form with state machine
- [data_entry_form](./examples/data_entry_form/) - Complex form validation

### Intermediate: Multi-Screen Applications

Prerequisites:
- [STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md) - Master state machines
- [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) - Learn layouts

Examples:
- [wizard](./examples/wizard/) - Step-by-step navigation
- [settings](./examples/settings/) - Tabbed/menu navigation
- [loading_pattern](./examples/loading_pattern/) - Async data handling

### Advanced: Complex Enterprise Applications

Prerequisites:
- [WORKFLOW_GUIDE.md](./WORKFLOW_GUIDE.md) - Full workflow understanding
- All state machine patterns
- All layout patterns

Examples:
- [crud_application](./examples/crud_application/) - Master-detail with CRUD
- [dashboard](./examples/dashboard/) - Complex layout with multiple sections

---

## By Use Case

### "I need to build a login page"
1. Read: [QUICKSTART.md](./QUICKSTART.md) (intro) + [auth_flow/README.md](./examples/auth_flow/README.md)
2. Study: [auth_flow.json](./examples/auth_flow/auth_flow.json) (complete spec)
3. Reference: [STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md) (Pattern 1: Authentication)
4. Check: [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) (text_field, password_field, button)

### "I need to build a form with validation"
1. Read: [VALIDATION_GUIDE.md](./VALIDATION_GUIDE.md) (comprehensive guide)
2. Study: [data_entry_form/](./examples/data_entry_form/) (complete example)
3. Reference: [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) (input widgets)
4. Check: [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) (form layout patterns)

### "I need to build a CRUD application"
1. Read: [WORKFLOW_GUIDE.md](./WORKFLOW_GUIDE.md) (process overview)
2. Study: [crud_application/](./examples/crud_application/) (complete example)
3. Learn: [STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md) (Pattern 5: CRUD)
4. Reference: [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) (master-detail layout)

### "I need to build a multi-step wizard"
1. Read: [wizard/README.md](./examples/wizard/README.md)
2. Study: [wizard.json](./examples/wizard/wizard.json) (spec)
3. Learn: [STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md) (Pattern 4: Wizard)
4. Check: [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) (step layout)

### "I need to handle async data loading"
1. Read: [loading_pattern/README.md](./examples/loading_pattern/README.md)
2. Study: [loading_pattern.json](./examples/loading_pattern/loading_pattern.json)
3. Learn: [STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md) (Pattern 2: Data Loading)
4. Check: [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) (progress_bar, data_grid)

### "I need to style my app"
1. Read: [THEMING_GUIDE.md](./THEMING_GUIDE.md) (complete guide)
2. Study: [dashboard/](./examples/dashboard/) (professional styling example)
3. Reference: [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) (spacing)
4. Check: [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) (widget-specific styling)

### "I need a dashboard/complex layout"
1. Read: [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) (complete guide)
2. Study: [dashboard/](./examples/dashboard/) (grid, cards, tabs)
3. Learn: [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) (grid, tabs, card, data_grid)
4. Style: [THEMING_GUIDE.md](./THEMING_GUIDE.md)

---

## File Structure

```
reference_docs/gui/
├── INDEX.md                           ← You are here
├── README.md                          Navigation hub
├── QUICKSTART.md                      5-minute tutorial
├── WIDGET_CATALOG.md                  40+ widgets reference (2000+ lines)
├── STATE_MACHINE_GUIDE.md             State management (10 patterns)
├── LAYOUT_PATTERNS.md                 Grid and container layouts
├── VALIDATION_GUIDE.md                Form validation rules
├── THEMING_GUIDE.md                   Dark mode, colors, styling
├── WORKFLOW_GUIDE.md                  AI-assisted workflow
└── examples/
    ├── auth_flow/                     Login with error recovery
    │   ├── auth_flow.json
    │   ├── state_machine.svg
    │   ├── screens.svg
    │   └── README.md
    ├── data_entry_form/               Complex form validation
    ├── crud_application/              Full CRUD workflow
    ├── dashboard/                     Complex layout with tabs
    ├── wizard/                        Multi-step onboarding
    ├── settings/                      Nested panels with save/cancel
    └── loading_pattern/               Async data fetching
```

Total: 8 guides + 7 examples = 15 documents, 5000+ lines of reference

---

## Tools

### CLI Reference
```bash
# Show widget documentation
simple_spec_viz docs widget Button

# Show state machine guide
simple_spec_viz docs state-machine

# Show pattern documentation
simple_spec_viz docs pattern crud

# Show example
simple_spec_viz docs example auth_flow

# Visualize a JSON spec
simple_spec_viz visualize spec.json --output-dir ./diagrams/
```

### Claude Code Skills
```bash
# Show widget documentation
/eiffel.gui-ux widget Button

# Show pattern documentation
/eiffel.gui-ux pattern auth

# Show example
/eiffel.gui-ux example auth_flow

# Generate JSON spec from specification
/eiffel.gui-ux generate windows specification.md
```

---

## How Documents Are Organized

### Primary Guides (explain concepts)
- **README.md** - Orientation and quick links
- **QUICKSTART.md** - Hands-on introduction
- **WIDGET_CATALOG.md** - API reference for all widgets
- **STATE_MACHINE_GUIDE.md** - State management patterns
- **LAYOUT_PATTERNS.md** - Container and grid strategies
- **VALIDATION_GUIDE.md** - Form validation patterns
- **THEMING_GUIDE.md** - Styling and appearance
- **WORKFLOW_GUIDE.md** - End-to-end development process

### Examples (demonstrate patterns)
- **auth_flow/** - Authentication with error recovery
- **data_entry_form/** - Complex validation
- **crud_application/** - Full CRUD workflow
- **dashboard/** - Complex layouts
- **wizard/** - Multi-step process
- **settings/** - Nested panels
- **loading_pattern/** - Async operations

Each example contains:
- `.json` - Specification file
- `state_machine.svg` - Generated state diagram
- `screens.svg` - Generated screen mockups
- `README.md` - Pattern explanation and implementation notes

---

## Search Tips

**Looking for a specific widget?**
→ Use WIDGET_CATALOG.md (Ctrl+F for widget name)

**Looking for a pattern?**
→ Use STATE_MACHINE_GUIDE.md Section 6 (Ctrl+F for pattern name)

**Looking for a validation example?**
→ Use VALIDATION_GUIDE.md + data_entry_form example

**Looking for a layout example?**
→ Use LAYOUT_PATTERNS.md + dashboard/crud_application examples

**Stuck implementing a feature?**
→ Search examples/ for something similar

---

## Version & Updates

- **Version:** 1.0
- **Last Updated:** 2026-01-25
- **Scope:** simple_vision Phase 7 complete
- **Total Content:** 8 guides, 7 examples, 5000+ lines

**What's included:**
✓ Complete widget reference (40+ widgets)
✓ 10 state machine patterns
✓ 7 canonical examples with JSON specs
✓ Comprehensive validation guide
✓ Layout and responsive design guide
✓ Theming and styling guide
✓ End-to-end workflow guide
✓ 5-minute quickstart
✓ CLI tool integration (simple_spec_viz docs command)
✓ Claude Code skill (eiffel-gui-ux)

---

**Next steps:**
1. Read [README.md](./README.md) for orientation
2. Try [QUICKSTART.md](./QUICKSTART.md) for hands-on intro
3. Pick your learning path from above
4. Reference guides and examples as needed
5. Use CLI and Claude Code skills for quick lookups
