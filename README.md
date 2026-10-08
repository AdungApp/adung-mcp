# YouTube Intelligence MCP Server for Claude

[![GitHub Organization](https://img.shields.io/badge/Organization-Adung-7c3aed.svg)](https://github.com/AdungApp)
[![Verified Domain](https://img.shields.io/badge/Verified%20Domain-adung.top-success.svg)](https://adung.top/)
[![MCP Protocol](https://img.shields.io/badge/Protocol-Model%20Context%20Protocol-orange.svg)](https://modelcontextprotocol.io/)
[![Client](https://img.shields.io/badge/Client-Claude%20Desktop%20%7C%20Claude%20Code-purple.svg)](https://claude.ai/)

> **Model Context Protocol (MCP) Server (Developer Preview)**  
> Developed by **Adung** (https://adung.top).  
> This is a local stdio protocol preview, not a live YouTube research service. All four tool adapters are not implemented and return explicit errors with no research data. Claude Desktop / Claude Code compatibility has not been verified end-to-end.

---

## Overview

The **Adung YouTube MCP Server** exposes proposed tool schemas and JSON-RPC request handling for future creator research integrations.

It supports initialization, tool listing, explicit unavailable tool responses, and ping. It does not fetch YouTube content, connect to the desktop database, or call an AI provider. No API key is required for this preview.

---

## Installation and configuration

Python 3.10+ and Git are required separately from the desktop EXE. In a Windows terminal:

```powershell
git clone https://github.com/AdungApp/adung-mcp.git
cd adung-mcp
python -m venv .venv
.venv\Scripts\python.exe -m pip install .
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Use the absolute path to that environment's Python executable in your MCP client's configuration. For Claude Desktop, the following is a configuration example, not a claim of tested client compatibility. Replace the example path with your installation path:

```json
{
  "mcpServers": {
    "adung-youtube": {
      "command": "C:\\path\\to\\adung-mcp\\.venv\\Scripts\\python.exe",
      "args": ["-m", "adung_mcp.server"]
    }
  }
}
```

---

## Tools Exposed to Claude

| Tool Name | Description |
|---|---|
| `fetch_youtube_transcript` | Planned transcript adapter; not implemented. |
| `query_niche_velocity` | Planned niche metrics adapter; not implemented. |
| `extract_creator_dna` | Planned creator analysis adapter; not implemented. |
| `develop_script_outline` | Planned research-backed outline adapter; not implemented. |

Every registered tool call returns MCP `isError: true` and a JSON text payload with `status: "not_implemented"`, `data_source: "none"`, and `data: null`. No fabricated metrics or transcript samples are returned. Tool names and schemas are retained as preview interfaces, not functioning production features.

## Verification scope

The unittest suite launches the installed module as a subprocess from an unrelated temporary directory and checks initialization, notifications, tool listing, all four unavailable responses, unknown tools, and ping over actual stdin/stdout. It requires no paid API calls. The `--test` command is only an in-process smoke test. Neither test establishes full MCP conformance or Claude client compatibility. Live adapters and end-to-end client verification remain future work.

---

## Security & Local-First Guardrails

- **Local subprocess:** Communicates through stdin/stdout. There is no HTTP/SSE listener; host and port environment variables are not used.
- **No credentials needed:** This preview performs no network research or AI inference. Client-side AI usage, if any, is separate.
- **Future adapters:** Must respect content rights and applicable platform terms. This preview is not a compliance certification.

---

## About Adung

- **Official Website:** https://adung.top
- **Flagship Application:** YouTube Adung Commercial v1.2 (Standalone Windows Workstation)
- **Founder:** Dung Duy (founder@adung.top)
- **LinkedIn:** https://www.linkedin.com/in/dung-duy-72a123442/

© 2024–2026 Adung. All rights reserved.
