---
name: context-bootloader-skill
description: This skill is a mandatory, foundational bootloader. It must be run first in any new session or TUI instance to validate, load, and synthesize the complete operational context across all foundational files.
---

# context-bootloader-skill

## 🚀 Purpose

Use this skill to execute the mandatory context loading sequence defined in `PROTOCOL.md`. This ensures that the Agent is fully aware of its identity, the user's preferences, and the project's technical standards before any other task can begin.

## ⚙️ Process

1.  **Read Core Context:** Reads `./.pi/memory/SOUL.md`, `./.pi/memory/KNOWLEDGE.md`, `./.pi/memory/USER.md`, and `./.pi/memory/PROTOCOL.md`.
2.  **Validate:** Verifies the existence and integrity of all necessary context files.
3.  **Synthesize & Report:** Prints a structured, readable "Bootloader Success" message to the user, confirming that all pillars of context are loaded and active.
4.  **Validation:** If any critical file is missing, it reports the failure point and suggests remediation (e.g., "Missing `SOUL.md` at path: [path]").

## 💡 Execution Flow

```bash
python3 context-bootloader.py run --bootload
```

This skill must be run before any other domain-specific skill is utilized.
