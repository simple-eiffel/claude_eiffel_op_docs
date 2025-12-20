# Eiffel Notebook User Guide

**Version 1.0.0-alpha.20** | December 2025

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Writing Code](#writing-code)
5. [Cell Types](#cell-types)
6. [Commands Reference](#commands-reference)
7. [Troubleshooting](#troubleshooting)

---

## Introduction

**Eiffel Notebook** brings interactive programming to Eiffel. Write code in cells, execute them, and see results immediately. Features real-time streaming compiler output, automatic EiffelStudio detection, and DBC trace logging.

Part of the [Simple Eiffel](https://github.com/simple-eiffel) ecosystem.

---

## Installation

### CLI Tool

1. Download: 2. Run the installer with administrator privileges
3. The CLI is added to PATH automatically
4. EiffelStudio is auto-detected

### Library

Set environment variable: 
Add to ECF:
\
---

## Quick Start

\
---

## Writing Code

### Basic Syntax

Write standard Eiffel code:

\
### Multi-line Input

After typing code, press Enter to get continuation prompt ().
Press Enter on empty line to execute.

### Design by Contract

\
---

## Cell Types

| Content | Type | Action |
|---------|------|--------|
|  | Attribute | Added to class |
|  | Routine | Added to class |
|  | Instruction | Executed |
|  | Expression | Printed |

---

## Commands Reference

### Session

| Command | Alias | Description |
|---------|-------|-------------|
|  |  | Show help |
|  |  | Exit |
|  |  | Clear all cells |

### Cell Management

| Command | Alias | Description |
|---------|-------|-------------|
|  | | List all cells |
|  |  | Show cell N |
|  |  | Edit cell N |
|  |  | Delete cell N |

### Execution

| Command | Description |
|---------|-------------|
|  | Re-execute all cells |
|  | Stream compiler output |
|  | Hide compiler output |

### Inspection

| Command | Description |
|---------|-------------|
|  | Show variables |
|  | Show generated class |
|  | Show classifications |

---

## Troubleshooting

### Failed to start compiler
EiffelStudio not found. Set  or create config.json.

### Unknown identifier
Declare variables first:  then 
### Compilation hangs
Kill  in Task Manager.

### Session Logs
Check the log file path shown at startup.

---

## Acknowledgments

- **Eric Bezault** (Gobo): Cell classification design
- **Javier Velilla**: Original project idea

---

*Built with Design by Contract. Powered by EiffelStudio.*
