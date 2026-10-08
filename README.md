# YouTube Intelligence MCP Server for Claude

[![GitHub Organization](https://img.shields.io/badge/Organization-Adung-7c3aed.svg)](https://github.com/AdungApp)
[![Verified Domain](https://img.shields.io/badge/Verified%20Domain-adung.top-success.svg)](https://adung.top/)
[![MCP Protocol](https://img.shields.io/badge/Protocol-Model%20Context%20Protocol-orange.svg)](https://modelcontextprotocol.io/)
[![Client](https://img.shields.io/badge/Client-Claude%20Desktop%20%7C%20Claude%20Code-purple.svg)](https://claude.ai/)

> **Official Model Context Protocol (MCP) Server for YouTube Adung Commercial**  
> Developed by **Adung** (https://adung.top).

---

## Overview

The **Adung YouTube MCP Server** exposes deep creator intelligence, long-form video transcript extraction, and competitor velocity metrics directly into **Anthropic Claude Desktop** and **Claude Code**.

By connecting this MCP server, Claude gains native capabilities to inspect YouTube content without requiring manual copy-pasting of multi-hour video transcripts.

---

## Configuration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "adung-youtube": {
      "command": "python",
      "args": ["-m", "adung_mcp.server"],
      "env": {
        "ADUNG_HOST": "127.0.0.1",
        "ADUNG_PORT": "8000"
      }
    }
  }
}
```

---

## Tools Exposed to Claude

| Tool Name | Description |
|---|---|
| `fetch_youtube_transcript` | Extracts full spoken timestamped transcripts (4,000 to 18,000+ words) for 3-act narrative dissection. |
| `query_niche_velocity` | Returns real-time Views-Per-Hour (VPH) velocity multipliers across 110 tracked niche taxonomy buckets. |
| `extract_creator_dna` | Analyzes competitor title patterns, upload cadence, and audience retention hooks. |
| `synthesize_script_outline` | Formats structured narrative outlines based on competitor storytelling architectures. |

---

## Security & Local-First Guardrails

- **Localhost Execution:** Operates exclusively on `127.0.0.1` — no external proxy or cloud data relay.
- **BYOK (Bring Your Own Key):** Users configure their own Anthropic Claude API keys.
- **YouTube Compliance:** Strictly adheres to YouTube terms by processing creator-directed public metadata for research and fair-use synthesis.

---

## About Adung

- **Official Website:** https://adung.top
- **Flagship Application:** YouTube Adung Commercial v1.2 (Standalone Windows Workstation)
- **Founder:** Dung Duy (founder@adung.top)
- **LinkedIn:** https://www.linkedin.com/in/dung-duy-72a123442/

© 2024–2026 Adung. All rights reserved.
