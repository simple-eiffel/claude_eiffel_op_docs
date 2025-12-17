# Simple Eiffel - WSL2 / Linux Setup Guide

**Date:** December 16, 2025
**Tested on:** Ubuntu on WSL2, EiffelStudio 25.02.9.8732

---

## Overview

This guide covers setting up Simple Eiffel on Linux, either natively or via Windows Subsystem for Linux 2 (WSL2).

**What works:**
- 60+ platform-agnostic libraries compile and run on Linux
- All tests pass (e.g., simple_json: 214 tests)
- Same ECF files work on both Windows and Linux

**What doesn't work (yet):**
- 11 Windows-specific libraries (Win32 API dependencies)

---

## Prerequisites

- Ubuntu 20.04+ (native or WSL2)
- ~500 MB disk space for EiffelStudio
- ~300 MB for Simple Eiffel libraries

---

## Installation

### Step 1: Install EiffelStudio 25.02

**Option A: Direct Download (Recommended)**
```bash
cd /tmp
wget https://ftp.eiffel.com/pub/download/25.02/Eiffel_25.02_rev_98732-linux-x86-64.tar.bz2
tar xjf Eiffel_25.02_rev_98732-linux-x86-64.tar.bz2
mv Eiffel_25.02 ~/simple_eiffel/
```

**Option B: Eiffel PPA** (may be slower/older version)
```bash
sudo add-apt-repository ppa:eiffelstudio-team/ppa
sudo apt update
sudo apt install eiffelstudio
```

### Step 2: Get Simple Eiffel Libraries

**Option A: Clone from GitHub**
```bash
mkdir -p ~/simple_eiffel
cd ~/simple_eiffel
git clone https://github.com/simple-eiffel/simple_json
git clone https://github.com/simple-eiffel/simple_sql
# ... repeat for needed libraries
```

**Option B: Copy from Windows (WSL2)**
```bash
mkdir -p ~/simple_eiffel
cp -r /mnt/d/prod/simple_* ~/simple_eiffel/
cp -r /mnt/d/prod/gobo-gobo-25.09 ~/simple_eiffel/
cp -r /mnt/d/prod/eiffel_sqlite_2025 ~/simple_eiffel/
```

> **Note:** Copying to the native Linux filesystem (`~/`) is much faster than accessing `/mnt/d/` directly.

### Step 3: Configure Environment

Add to `~/.bashrc`:

```bash
# Simple Eiffel ecosystem
export SIMPLE_EIFFEL=$HOME/simple_eiffel
export GOBO=$SIMPLE_EIFFEL/gobo-gobo-25.09
export EIFFEL_SQLITE=$SIMPLE_EIFFEL/eiffel_sqlite_2025

# EiffelStudio
export ISE_EIFFEL=$HOME/simple_eiffel/Eiffel_25.02
export ISE_PLATFORM=linux-x86-64
export ISE_LIBRARY=$ISE_EIFFEL
export PATH=$ISE_EIFFEL/studio/spec/$ISE_PLATFORM/bin:$PATH
```

Apply changes:
```bash
source ~/.bashrc
```

Verify installation:
```bash
ec -version
# Expected: ISE EiffelStudio version 25.02.9.8732 - linux-x86-64
```

---

## Compiling Libraries

### Important: Clean Windows Artifacts

If libraries were previously compiled on Windows, remove the `EIFGENs` directory:

```bash
cd $SIMPLE_EIFFEL/simple_json
rm -rf EIFGENs
```

### Compile

```bash
ec -batch -config simple_json.ecf -target simple_json_tests -c_compile
```

Expected output:
```
Eiffel Compilation Manager
Version 25.02.9.8732 - linux-x86-64
...
Compiling C code in C38
...
C compilation completed
```

### Run Tests

```bash
./EIFGENs/simple_json_tests/W_code/simple_json
```

Expected output:
```
========================
Results: 214 passed, 0 failed
ALL TESTS PASSED
```

---

## Troubleshooting

### Error: "Incompatible version for project"

**Cause:** Windows-compiled EIFGENs present
**Solution:** `rm -rf EIFGENs` and recompile

### Error: "Could not open file: .../library/library/base/base.ecf"

**Cause:** Wrong ISE_LIBRARY setting (double "library" in path)
**Solution:** Set `ISE_LIBRARY=$ISE_EIFFEL` (not `$ISE_EIFFEL/library`)

### Error: "VD00 - Could not open file"

**Cause:** Path separator issues or missing dependencies
**Solution:** Ensure all SIMPLE_* paths use forward slashes in ECF files

### WSL2 Slow File Operations

**Cause:** 10x performance penalty accessing `/mnt/d/` (Windows filesystem)
**Solution:** Copy files to native Linux filesystem (`~/simple_eiffel/`)

### Downloads Fail in WSL2

**Cause:** Network configuration issues
**Solution:** Download on Windows, then copy via `/mnt/d/`

---

## Platform-Agnostic Libraries (Verified)

These libraries compile and run on Linux without modification:

| Category | Libraries |
|----------|-----------|
| **Data Formats** | simple_json, simple_xml, simple_yaml, simple_toml, simple_csv, simple_markdown, simple_toon |
| **Web/API** | simple_http, simple_web, simple_websocket, simple_jwt, simple_cors, simple_htmx, simple_alpine |
| **Database** | simple_sql, simple_cache |
| **Security** | simple_encryption, simple_hash, simple_base64 |
| **Utilities** | simple_datetime, simple_decimal, simple_fraction, simple_uuid, simple_regex, simple_validation, simple_template, simple_logger, simple_i18n |
| **Infrastructure** | simple_smtp, simple_mq, simple_telemetry, simple_scheduler, simple_grpc |
| **Developer** | simple_testing, simple_cli, simple_config, simple_eiffel_parser |
| **AI** | simple_ai_client |

---

## Windows-Only Libraries

These libraries require Windows and will not compile on Linux:

| Library | Dependency |
|---------|------------|
| simple_clipboard | Win32 clipboard API |
| simple_console | Windows console API |
| simple_gui_designer | WEL (Windows Eiffel Library) |
| simple_ipc | Windows named pipes |
| simple_mmap | Windows memory mapping |
| simple_process | Windows process API |
| simple_win32_api | By design |
| simple_registry | Windows registry |
| simple_docker | Windows Docker socket path |
| simple_lsp | Windows-specific paths |
| simple_oracle | Windows-specific paths |
| simple_pkg | Windows environment |

---

## Batch Compilation Script

Create `~/simple_eiffel/compile_all.sh`:

```bash
#!/bin/bash
set -e

source ~/.bashrc

LIBS="simple_json simple_xml simple_yaml simple_csv simple_sql simple_cache simple_datetime simple_uuid simple_validation simple_template simple_logger"

for lib in $LIBS; do
    echo "=== Compiling $lib ==="
    cd $SIMPLE_EIFFEL/$lib
    rm -rf EIFGENs
    ec -batch -config ${lib}.ecf -target ${lib}_tests -c_compile
    echo "=== Testing $lib ==="
    ./EIFGENs/${lib}_tests/W_code/$lib
    echo ""
done

echo "=== ALL DONE ==="
```

---

## CI/CD Integration

For automated testing on Linux, you can:

1. **GitHub Actions:** Use Ubuntu runner with EiffelStudio tarball
2. **Docker:** Build custom image (no official EiffelStudio 25.02 image exists)
3. **Self-hosted runner:** WSL2 or Linux VM

Example GitHub Actions step:
```yaml
- name: Install EiffelStudio
  run: |
    wget -q https://ftp.eiffel.com/pub/download/25.02/Eiffel_25.02_rev_98732-linux-x86-64.tar.bz2
    tar xjf Eiffel_25.02_rev_98732-linux-x86-64.tar.bz2
    echo "ISE_EIFFEL=$PWD/Eiffel_25.02" >> $GITHUB_ENV
    echo "ISE_PLATFORM=linux-x86-64" >> $GITHUB_ENV
    echo "ISE_LIBRARY=$PWD/Eiffel_25.02" >> $GITHUB_ENV
```

---

## Resources

- [EiffelStudio Downloads](https://www.eiffel.org/downloads)
- [Simple Eiffel GitHub](https://github.com/simple-eiffel)
- [Cross-Platform Roadmap](../roadmaps/CROSS_PLATFORM_ROADMAP.md)
- [WSL2 Documentation](https://docs.microsoft.com/en-us/windows/wsl/)

---

*Last verified: December 16, 2025*
