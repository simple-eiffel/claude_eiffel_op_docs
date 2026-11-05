# Workflow Guide: From Idea to Implementation

Complete AI-assisted workflow for building GUI applications with simple_vision.

---

## The End-to-End Workflow

```
Developer Idea (shallow or deep)
         ↓
   eiffel-research skill (7-step investigation)
         ↓
   eiffel-spec skill (specification from research)
         ↓
   eiffel-gui-ux skill (generates JSON for Windows/TUI/WebView2)
         ↓
   JSON Specification (AI-generated, ready for review)
         ↓
   simple_spec_viz (visualize → SVG diagrams)
         ↓
   State Diagrams + Screen Mockups (SVG files)
         ↓
   Dev + AI Review (visual feedback loop)
         ↓
   simple_vision (developer implements in Eiffel)
         ↓
   Testing & Deployment
```

---

## Phase 1: Initial Idea

**What you provide:**
- Shallow idea: "I need a login page"
- Deep idea: "I need a login page with username/password, remember-me checkbox, two-factor auth, error recovery, dark mode support..."

**Output:** A clear problem statement.

---

## Phase 2: Research (eiffel-research)

**Command:**
```bash
/eiffel.research "I need a login page with two-factor authentication"
```

**What the skill does:**
1. Analyzes the request
2. Researches similar GUIs
3. Identifies common patterns
4. Documents findings in `research.md`
5. Proposes architecture recommendations

**Output:** `research.md` with:
- Similar GUIs analysis
- User flows
- Architecture recommendations
- Widget candidates
- State machine recommendations

**Example output:**
```markdown
# Research: Two-Factor Authentication UI

## Similar Systems
- GitHub's 2FA
- Google's 2FA
- AWS sign-in

## Common Patterns
- Step 1: Username/password
- Step 2: OTP entry
- Fallback codes option
- Device trust

## Recommended Widgets
- Text field for password
- Masked field (digits only) for OTP
- Checkbox for device trust

## State Machine
States: login → mfa_required → mfa_entry → authenticated
```

---

## Phase 3: Specification (eiffel-spec)

**Command:**
```bash
/eiffel.spec research.md
```

**What the skill does:**
1. Reads research.md
2. Creates formal specification
3. Defines states, transitions, business logic
4. Produces `specification.md`

**Output:** `specification.md` with:
- Requirements (functional, non-functional)
- Use cases
- State definitions
- Validation rules
- Error scenarios

**Example:**
```markdown
# Specification: Two-Factor Authentication

## Requirements
- FR1: User enters username/password on first screen
- FR2: System validates credentials
- FR3: If valid, prompt for OTP code
- NR1: Response time < 2 seconds

## States
- login_form: Username/password input
- validating: Checking credentials
- mfa_required: OTP entry screen
- authenticated: Success

## Validation Rules
- Password: min 8 chars, 1 uppercase, 1 digit
- OTP: 6 digits only
```

---

## Phase 4: JSON Generation (eiffel-gui-ux)

**Command:**
```bash
/eiffel.gui-ux generate windows specification.md
```

**Options:**
- `windows` - Windows GUI (simple_vision)
- `tui` - Text UI (terminal-based)
- `webview` - WebView2 browser
- `all` - Generate all three for comparison

**What the skill does:**
1. Reads specification.md
2. Maps requirements to widgets
3. Creates state machine JSON
4. Generates window layout
5. Produces `<app_name>.json`

**Output:** `auth_2fa.json` with:
- Window definitions
- Widget specifications
- State machine with transitions
- Validation rules
- Action handlers

**The JSON is ready for visualization and review.**

---

## Phase 5: Visualization (simple_spec_viz)

**Command:**
```bash
simple_spec_viz.exe visualize auth_2fa.json --output-dir ./diagrams/
```

**Generates:**
- `state_machine.svg` - Visual state diagram
- `screens.svg` - Mockups of each screen state
- `validation_report.json` - Spec validation

**Example state diagram:**
```
  ┌──────────────┐
  │ login_form   │
  └──────┬───────┘
         │ submit
         ↓
  ┌──────────────┐
  │ validating   │
  └──┬───────────┘
     │
     ├─ success ──→ mfa_required
     │
     └─ failure ──→ login_form (show error)
```

---

## Phase 6: Review & Feedback

**Dev + AI Review Together:**

1. **Review State Diagram**
   - Does every state have entry and exit?
   - Are transitions logically correct?
   - Do guards make sense?

2. **Review Screen Mockups**
   - Is layout clear?
   - Are all widgets present?
   - Does flow match expectations?

3. **Ask Questions**
   - "Should remember-me be on first screen or second?"
   - "What if OTP times out?"
   - "Do we need a fallback code option?"

4. **Iterate**
   - Request changes via Claude Code
   - eiffel-gui-ux regenerates JSON
   - simple_spec_viz visualizes changes
   - Repeat until satisfied

**Example feedback loop:**
```
Dev: "The OTP screen needs a back button to change username"
AI: /eiffel.gui-ux modify auth_2fa.json --add-back-button mfa_required
(generates updated JSON)
Dev: simple_spec_viz visualize updated.json (reviews new diagram)
Dev: "Perfect!"
```

---

## Phase 7: Implementation (simple_vision)

**Now the actual coding begins.**

### Create Eiffel Application

1. **Start with structure:**
```eiffel
class
    AUTH_2FA_APP

inherit
    SV_APPLICATION

create
    make_and_launch

feature {NONE}
    make_and_launch
        do
            default_create
            launch
        end

    build_main_window
        local
            sv: SV_QUICK
        do
            create sv.make
            -- Create state machine from JSON or code
            -- Create widgets matching spec
            -- Implement handlers
        end
end
```

2. **Implement state machine:**
```eiffel
machine := sv.state_machine_from_json (
    file_system.read_json ("auth_2fa.json"))

-- Or build programmatically:
machine.state ("login_form").on_entry (agent show_login)
machine.state ("mfa_required").on_entry (agent show_mfa)
```

3. **Create widgets matching spec:**
```eiffel
-- Match widget IDs from JSON to Eiffel variables
username := sv.text_field.placeholder ("Username")
password := sv.password_field.placeholder ("Password")
otp := sv.text_field.placeholder ("6-digit code")
```

4. **Implement handlers:**
```eiffel
handle_login_submit
    do
        if validate_credentials (username.value, password.value) then
            machine.trigger ("success")
        else
            machine.trigger ("failure")
        end
    end
```

5. **Compile and test:**
```bash
ec -batch -config app.ecf -target app_tests -c_compile
./EIFGENs/app_tests/W_code/app.exe
```

### Reference During Implementation

Use these guides:
- **WIDGET_CATALOG.md** - Widget APIs and properties
- **STATE_MACHINE_GUIDE.md** - State machine patterns
- **VALIDATION_GUIDE.md** - Form validation rules
- **LAYOUT_PATTERNS.md** - Container layout strategies

---

## Phase 8: Testing & Deployment

### Manual Testing

Test against the spec:
- [ ] State transitions work
- [ ] Validations trigger correctly
- [ ] Error messages display
- [ ] Dark mode works
- [ ] Keyboard shortcuts work
- [ ] Accessibility OK

### Automated Testing

```eiffel
class AUTH_2FA_TESTS inherit TEST_SET

    test_login_success
        do
            machine.trigger ("submit")
            assert ("should be in mfa_required",
                machine.is_in_state ("mfa_required"))
        end

    test_invalid_password
        do
            username_field.set_value ("user")
            password_field.set_value ("bad")
            machine.trigger ("submit")
            assert ("should show error", error_panel.is_visible)
        end
end
```

### Deployment

```bash
# Build release binary
ec -batch -config app.ecf -target app -c_compile

# Create installer (INNO)
inno_builder create app_installer.iss

# Sign and distribute
```

---

## Best Practices Throughout Workflow

### 1. Keep Spec and Code in Sync

If spec changes, update code. If code changes, update spec.

```bash
# Document changes
/eiffel.spec update specification.md "Added email field validation"
/eiffel.gui-ux generate windows specification.md
```

### 2. Use Version Control for Specs

Commit JSON specs alongside code:
```
git add auth_2fa.json
git commit -m "spec: add remember-me checkbox to login form"
git add src/auth_2fa_app.e
git commit -m "feat: implement remember-me functionality"
```

### 3. Iterate Early

Don't implement everything before review:
- Week 1: Get feedback on basic flow
- Week 2: Add advanced features
- Week 3: Polish and test

### 4. Reuse Examples

Reference similar examples before starting:
```bash
# Show CRUD pattern
/eiffel.gui-ux example crud_application

# Copy and modify for your app
```

### 5. Document Decisions

If you deviate from spec:
```eiffel
feature {NONE}
    -- NOTE: Added timeout for OTP entry (5 min)
    -- Spec: No timeout mentioned
    -- Reason: Security best practice + user feedback
    otp_timeout_seconds: INTEGER = 300
```

---

## Common Questions

### Q: Do I have to use eiffel-gui-ux?

No. You can:
- Write JSON by hand
- Use simple_spec_viz to visualize
- Implement directly in simple_vision

But eiffel-gui-ux ensures your JSON matches the spec.

### Q: Can I skip simple_spec_viz?

Technically yes, but visualization catches issues early:
- Layout mistakes
- State diagram dead ends
- Missing transitions

It's worth the 2 minutes.

### Q: What if the spec is wrong?

Then iterate! The whole workflow is a feedback loop:
1. AI generates spec
2. You review visual output
3. You suggest changes
4. AI regenerates
5. Repeat

This is way faster than discovering problems after coding.

### Q: How long does this take?

- Idea → Research: 30 minutes
- Research → Spec: 30 minutes
- Spec → JSON: 15 minutes
- JSON → Visualization: 5 minutes
- Review + Feedback: 15-30 minutes
- Implementation: Depends on complexity (1 hour to 1 week)

**Total:** Spec is done in ~2 hours. Implementation starts with clear design.

---

## Workflow for Different App Types

### Simple Forms
1. Idea (10 min)
2. eiffel-research (skip - obvious)
3. eiffel-spec (write manually if simple)
4. eiffel-gui-ux (generates in 5 min)
5. Review (10 min)
6. Code (1 hour)

### Complex Applications
1. Idea (detailed)
2. eiffel-research (1 hour - understand domain)
3. eiffel-spec (2 hours - detailed requirements)
4. eiffel-gui-ux (30 min - multiple iterations)
5. Review (1 hour - stakeholder feedback)
6. Code (3-5 days - multiple screens/flows)

### Existing App Improvements
1. Idea ("Add password reset")
2. Skip research
3. eiffel-spec (sketch new flow)
4. eiffel-gui-ux (generates screen)
5. Review (30 min)
6. Code (2-4 hours)

---

## See Also

**Workflow Steps:**
- [QUICKSTART.md](./QUICKSTART.md) - 5-minute hands-on example
- [eiffel-research](https://github.com/simple-eiffel/eiffel-spec-kit) - Step 2: Research phase
- [eiffel-spec](https://github.com/simple-eiffel/eiffel-spec-kit) - Step 3: Specification phase
- [eiffel-gui-ux skill](~/.claude\skills\eiffel-gui-ux\) - Step 4: JSON generation
- [simple_spec_viz](https://github.com/simple-eiffel/simple_spec_viz) - Step 5: Visualization

**Reference Guides:**
- [WIDGET_CATALOG.md](./WIDGET_CATALOG.md) - Available widgets for Step 7
- [STATE_MACHINE_GUIDE.md](./STATE_MACHINE_GUIDE.md) - State patterns for Step 7
- [VALIDATION_GUIDE.md](./VALIDATION_GUIDE.md) - Form validation for Step 7
- [LAYOUT_PATTERNS.md](./LAYOUT_PATTERNS.md) - Container layouts for Step 7
- [THEMING_GUIDE.md](./THEMING_GUIDE.md) - Styling for Step 7

**Real Examples:**
- [examples/](./examples/) - All 7 examples show complete workflows
- Browse by complexity: auth_flow → data_entry_form → crud_application
