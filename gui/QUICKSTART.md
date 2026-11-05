# Quick Start: 5-Minute Login Example

Learn simple\_vision by reviewing an AI-generated login spec and implementing it.

---

## The Scenario

You have a specification document (from eiffel-research + eiffel-spec pipeline) that describes a login application. You run eiffel-gui-ux to generate a JSON spec, then simple\_spec\_viz visualizes it. Now you implement it in simple\_vision.

---

## Step 1: Review the Generated Spec (1 minute)

Your eiffel-gui-ux skill generated this JSON:

```json
{
  "app": {
    "name": "login\\\_app",
    "title": "Login",
    "version": "1.0.0"
  },
  "windows": \\\[
    {
      "id": "login\\\_window",
      "type": "window",
      "title": "Login",
      "size": { "width": 400, "height": 300 },
      "state\\\_machine": "auth\\\_flow",
      "layout": {
        "type": "vertical",
        "padding": 20,
        "spacing": 10,
        "children": \\\[
          {
            "type": "text",
            "content": "Login",
            "font\\\_size": 18,
            "font\\\_weight": "bold"
          },
          {
            "type": "text\\\_field",
            "id": "username\\\_field",
            "placeholder": "Username"
          },
          {
            "type": "password\\\_field",
            "id": "password\\\_field",
            "placeholder": "Password"
          },
          {
            "type": "row",
            "spacing": 10,
            "children": \\\[
              {
                "type": "button",
                "id": "login\\\_button",
                "label": "Login",
                "enabled\\\_when": "username\\\_not\\\_empty AND password\\\_not\\\_empty"
              },
              {
                "type": "spacer"
              },
              {
                "type": "button",
                "id": "cancel\\\_button",
                "label": "Cancel"
              }
            ]
          }
        ]
      }
    }
  ],
  "state\\\_machines": \\\[
    {
      "id": "auth\\\_flow",
      "initial\\\_state": "logged\\\_out",
      "states": \\\[
        {
          "id": "logged\\\_out",
          "type": "initial",
          "description": "User not authenticated, form visible"
        },
        {
          "id": "authenticating",
          "description": "Attempting to authenticate",
          "entry\\\_action": "show\\\_spinner"
        },
        {
          "id": "authenticated",
          "type": "final",
          "description": "User logged in",
          "entry\\\_action": "close\\\_window"
        },
        {
          "id": "error",
          "description": "Authentication failed",
          "entry\\\_action": "show\\\_error"
        }
      ],
      "transitions": \\\[
        {
          "from": "logged\\\_out",
          "event": "login",
          "to": "authenticating",
          "guard": "username\\\_not\\\_empty AND password\\\_not\\\_empty"
        },
        {
          "from": "authenticating",
          "event": "success",
          "to": "authenticated"
        },
        {
          "from": "authenticating",
          "event": "failure",
          "to": "error"
        },
        {
          "from": "error",
          "event": "retry",
          "to": "logged\\\_out"
        },
        {
          "from": "logged\\\_out",
          "event": "cancel",
          "to": "authenticated"
        }
      ]
    }
  ]
}
```

---

## Step 2: View the Generated Diagrams (1 minute)

Run simple\_spec\_viz to visualize:

```bash
cd /d/prod/simple\\\_spec\\\_viz
./EIFGENs/simple\\\_spec\\\_viz/W\\\_code/simple\\\_spec\\\_viz.exe visualize login\\\_spec.json --output-dir ./output/
```

**state\_machine.svg** shows:

```
┌────────────┐
│ logged\\\_out │◄─────────────────┐
└─────┬──────┘                  │ cancel or error→retry
      │ login                   │
      ↓                         │
┌──────────────┐                │
│authenticating├─────────────────┘
└──┬───────┬──┘
   │       │
success  failure
   ↓       ↓
   ✓       error (shows msg, retry available)
```

**screens.svg** shows:

* Login form with username, password fields
* Login/Cancel buttons
* Loading spinner (when authenticating)
* Error message panel (on failure)

---

## Step 3: Implement in simple\_vision (3 minutes)

Create your Eiffel application:

```eiffel
class
    LOGIN\\\_APP

inherit
    SV\\\_APPLICATION

create
    make\\\_and\\\_launch

feature {NONE} -- Initialization

    make\\\_and\\\_launch
        do
            default\\\_create
            launch
        end

    build\\\_main\\\_window
        local
            sv: SV\\\_QUICK
            machine: SV\\\_STATE\\\_MACHINE
        do
            create sv.make
            create\\\_state\\\_machine (sv)
            create\\\_widgets (sv)
        end

feature {NONE} -- State Machine

    machine: SV\\\_STATE\\\_MACHINE

    create\\\_state\\\_machine (sv: SV\\\_QUICK)
        do
            machine := sv.state\\\_machine ("auth\\\_flow")

            -- Define states
            machine.state ("logged\\\_out")
                .described\\\_as ("User not authenticated, form visible")
                .do\\\_nothing

            machine.state ("authenticating")
                .described\\\_as ("Attempting to authenticate")
                .on\\\_entry (agent show\\\_spinner)
                .on\\\_exit (agent hide\\\_spinner)

            machine.state ("authenticated")
                .described\\\_as ("User logged in")
                .on\\\_entry (agent close\\\_window)

            machine.state ("error")
                .described\\\_as ("Authentication failed")
                .on\\\_entry (agent show\\\_error)

            -- Define transitions
            machine.on ("login")
                .from\\\_state ("logged\\\_out")
                .to ("authenticating")
                .apply
                .do\\\_action (agent authenticate)

            machine.on ("success")
                .from\\\_state ("authenticating")
                .to ("authenticated")
                .apply
                .do\\\_nothing

            machine.on ("failure")
                .from\\\_state ("authenticating")
                .to ("error")
                .apply
                .do\\\_nothing

            machine.on ("retry")
                .from\\\_state ("error")
                .to ("logged\\\_out")
                .apply
                .do\\\_nothing

            machine.on ("cancel")
                .from\\\_state ("logged\\\_out")
                .to ("authenticated")
                .apply
                .do\\\_nothing

            machine.set\\\_initial ("logged\\\_out")
        end

feature {NONE} -- Widgets

    username\\\_field: SV\\\_TEXT\\\_FIELD
    password\\\_field: SV\\\_TEXT\\\_FIELD
    login\\\_button: SV\\\_BUTTON
    error\\\_panel: SV\\\_CARD
    spinner: SV\\\_PROGRESS\\\_BAR

    create\\\_widgets (sv: SV\\\_QUICK)
        do
            main\\\_window := sv.window ("Login")
                .sized (400, 300)
                .child (
                    sv.column
                        .padding (20)
                        .spacing (10)
                        .child (sv.text ("Login")
                            .font\\\_size (18)
                            .font\\\_weight ("bold"))
                        .child (create\\\_username\\\_field (sv))
                        .child (create\\\_password\\\_field (sv))
                        .child (create\\\_error\\\_panel (sv))
                        .child (create\\\_spinner (sv))
                        .child (create\\\_button\\\_row (sv)))
        end

    create\\\_username\\\_field (sv: SV\\\_QUICK): SV\\\_TEXT\\\_FIELD
        do
            create Result
            username\\\_field := sv.text\\\_field
                .placeholder ("Username")
            Result := username\\\_field
        end

    create\\\_password\\\_field (sv: SV\\\_QUICK): SV\\\_PASSWORD\\\_FIELD
        do
            create Result
            password\\\_field := sv.password\\\_field
                .placeholder ("Password")
            Result := password\\\_field
        end

    create\\\_error\\\_panel (sv: SV\\\_QUICK): SV\\\_CARD
        do
            create Result
            error\\\_panel := sv.card\\\_titled ("Error")
                .child (sv.text ("Authentication failed. Please try again."))
            error\\\_panel.hide
            Result := error\\\_panel
        end

    create\\\_spinner (sv: SV\\\_QUICK): SV\\\_PROGRESS\\\_BAR
        do
            create Result
            spinner := sv.progress
                .indeterminate (True)
                .label ("Authenticating...")
            spinner.hide
            Result := spinner
        end

    create\\\_button\\\_row (sv: SV\\\_QUICK): SV\\\_ROW
        do
            create Result
            login\\\_button := sv.button ("Login")
                .on\\\_click (agent handle\\\_login\\\_click)

            Result := sv.row
                .spacing (10)
                .child (login\\\_button)
                .child (sv.spacer)
                .child (sv.button ("Cancel")
                    .on\\\_click (agent handle\\\_cancel\\\_click))
        end

feature {NONE} -- Event Handlers

    handle\\\_login\\\_click
        do
            if not username\\\_field.is\\\_empty and not password\\\_field.is\\\_empty then
                machine.trigger ("login")
            end
        end

    handle\\\_cancel\\\_click
        do
            machine.trigger ("cancel")
        end

    authenticate
        do
            -- Simulate authentication (in real app, call API)
            if username\\\_field.value ~ "admin" and password\\\_field.value ~ "password" then
                machine.trigger ("success")
            else
                machine.trigger ("failure")
            end
        end

    show\\\_spinner
        do
            spinner.show
            login\\\_button.disable
        end

    hide\\\_spinner
        do
            spinner.hide
            login\\\_button.enable
        end

    show\\\_error
        do
            error\\\_panel.show
        end

    close\\\_window
        do
            main\\\_window.close
        end

end
```

---

## Step 4: Build \& Run (staying within 5 minutes)

```bash
# Compile and run
cd your\\\_project
ec -batch -config your\\\_app.ecf -target your\\\_app\\\_tests -c\\\_compile
./EIFGENs/your\\\_app\\\_tests/W\\\_code/your\\\_app.exe
```

**Result:** A working login window that:

* Shows login form in initial state
* Disables login button until both fields filled
* Shows spinner and disables button while authenticating
* Shows error on failed login
* Closes window on successful login or cancel

---

## Key Concepts You Just Used

1. **Factory Pattern (SV\_QUICK)** - Fluent API for building widgets
2. **Fluent Interface** - Chainable method calls (`.child().padding()`)
3. **State Machine** - Explicit states prevent invalid combinations
4. **Events \& Transitions** - Trigger events to move between states
5. **Entry/Exit Actions** - Code runs automatically on state changes
6. **Guards** - Conditions that must be true for transitions

---

## Next Steps

* **Learn Widgets**: [WIDGET\_CATALOG.md](./WIDGET_CATALOG.md)
* **Master State Machines**: [STATE\_MACHINE\_GUIDE.md](./STATE_MACHINE_GUIDE.md)
* **Form Validation**: [VALIDATION\_GUIDE.md](./VALIDATION_GUIDE.md)
* **Complex Layouts**: [LAYOUT\_PATTERNS.md](./LAYOUT_PATTERNS.md)
* **See Full Examples**: Browse `examples/` directory

## What You Learned

1. **Factory Pattern** - Use SV_QUICK for fluent widget construction
2. **State Machines** - Explicit states prevent invalid combinations
3. **Event Handlers** - Respond to user actions
4. **Entry/Exit Actions** - Automatic state-driven UI updates
5. **Validation Guards** - Conditional button enabling

## Next Steps by Interest

**Want to master state machines?**
→ Read [STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md) + study all 10 patterns

**Need advanced form validation?**
→ Read [VALIDATION_GUIDE.md](./VALIDATION_GUIDE.md) + review [data_entry_form example](./examples/data_entry_form/)

**Building complex layouts?**
→ Read [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) + review [dashboard example](./examples/dashboard/)

**Want to understand the full workflow?**
→ Read [WORKFLOW_GUIDE.md](./WORKFLOW_GUIDE.md) + review eiffel-research/eiffel-spec integration

**Need to look up a widget?**
→ Search [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) for detailed API reference

**Want to style your app?**
→ Read [THEMING_GUIDE.md](./THEMING_GUIDE.md) for dark mode, colors, scaling

---

**Time to 'Hello World':** 5 minutes
**Time to Production Confidence:** Read guides above + code 1-2 full features

