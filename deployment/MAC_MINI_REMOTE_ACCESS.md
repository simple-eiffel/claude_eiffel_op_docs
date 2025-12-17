# Mac Mini Remote Access Setup

**Purpose**: Access Mac Mini from Windows for Claude Code development without separate mouse/keyboard.

---

## Option 1: SSH (Recommended for Claude Code)

SSH is ideal - works exactly like WSL2 in Claude Code sessions.

### Enable SSH on Mac Mini

1. System Settings → General → Sharing
2. Enable "Remote Login"
3. Note the connection info: `ssh username@macmini.local`

### From Windows

```bash
# Add to ~/.ssh/config for easy access
Host mac
    HostName macmini.local
    User yourusername

# Then just:
ssh mac
```

### Claude Code Usage

Claude Code can run commands on Mac via SSH:
```bash
ssh mac "cd /Users/you/eiffel && ec -batch -config lib.ecf -c_compile"
```

---

## Option 2: VS Code Remote SSH

Best for editing code on Mac from Windows.

### Setup

1. Install "Remote - SSH" extension in VS Code
2. Cmd+Shift+P → "Remote-SSH: Connect to Host"
3. Enter `username@macmini.local`
4. VS Code opens with Mac filesystem access

### Benefits

- Full IntelliSense on Mac codebase
- Integrated terminal runs on Mac
- Extensions run on Mac (e.g., Eiffel syntax highlighting)

---

## Option 3: Screen Sharing (VNC)

For full GUI access when needed.

### Enable on Mac Mini

1. System Settings → General → Sharing
2. Enable "Screen Sharing"

### Connect from Windows

- Use any VNC client (TightVNC, RealVNC)
- Or use Microsoft Remote Desktop (free) with VNC support
- Connect to: `macmini.local:5900`

---

## Option 4: Tailscale (Remote Access Anywhere)

For access when not on same network.

### Setup

1. Install Tailscale on both Windows and Mac
2. Sign in with same account
3. Access Mac via Tailscale IP: `ssh user@100.x.x.x`

---

## Recommended Workflow for Simple Eiffel

1. **Primary**: SSH for command-line operations (compile, test, git)
2. **Editing**: VS Code Remote SSH for code changes
3. **Debugging**: Screen Sharing only when GUI needed

### Example Session

```bash
# Windows terminal
ssh mac

# On Mac (via SSH)
cd ~/eiffel/simple_json
ec -batch -config simple_json.ecf -target simple_json_tests -c_compile
./EIFGENs/simple_json_tests/W_code/simple_json

# Or from Windows directly:
ssh mac "cd ~/eiffel/simple_json && ./EIFGENs/simple_json_tests/W_code/simple_json"
```

---

## Environment Setup on Mac

```bash
# ~/.zshrc (or ~/.bashrc)
export ISE_EIFFEL=/Applications/Eiffel_25.02
export ISE_PLATFORM=macosx-armv6  # For Apple Silicon, or macosx-x86-64 for Intel
export PATH=$PATH:$ISE_EIFFEL/studio/spec/$ISE_PLATFORM/bin

export SIMPLE_EIFFEL=~/eiffel
```

---

## Troubleshooting

### SSH Connection Refused
- Check System Settings → Sharing → Remote Login is ON
- Verify firewall allows SSH (port 22)

### Hostname Not Found
- Use IP address instead: `ssh user@192.168.1.x`
- Or install Bonjour for Windows: https://support.apple.com/kb/DL999

### Permission Denied
- Check username is correct
- Enable password authentication (or set up SSH keys)

---

## Security Notes

- Use SSH keys instead of passwords for production
- Consider firewall rules to limit SSH access
- Tailscale provides encrypted tunnel for remote access
