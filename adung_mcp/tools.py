"""Tool schemas and execution handlers for the Adung MCP server."""
from typing import Any, Dict, List

TOOLS: List[Dict[str, Any]] = [
    {
        "name": "fetch_youtube_transcript",
        "description": "Developer preview: transcript adapter not implemented. Returns an explicit unavailable error, not transcript data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_url_or_id": {
                    "type": "string",
                    "description": "YouTube video watch URL (e.g. https://www.youtube.com/watch?v=...) or 11-character video ID."
                },
                "include_timestamps": {
                    "type": "boolean",
                    "description": "Whether to preserve exact minute:second timestamps in the caption stream.",
                    "default": True
                }
            },
            "required": ["video_url_or_id"]
        }
    },
    {
        "name": "query_niche_velocity",
        "description": "Developer preview: niche velocity adapter not implemented. No live metrics are available.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "niche_id": {
                    "type": "string",
                    "description": "Niche taxonomy category (e.g. faceless-mystery, tech-explainer, finance-investigative)."
                },
                "min_vph": {
                    "type": "integer",
                    "description": "Minimum Views-Per-Hour velocity threshold to filter breakout videos.",
                    "default": 500
                }
            },
            "required": ["niche_id"]
        }
    },
    {
        "name": "extract_creator_dna",
        "description": "Developer preview: creator analysis adapter not implemented. No channel analysis is available.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel_id_or_url": {
                    "type": "string",
                    "description": "Target creator channel URL or handle (@channel)."
                }
            },
            "required": ["channel_id_or_url"]
        }
    },
    {
        "name": "develop_script_outline",
        "description": "Developer preview: research-backed outline adapter not implemented. No generated outline is available.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Core video subject or thesis question."
                },
                "target_duration_minutes": {
                    "type": "integer",
                    "description": "Target video duration (e.g. 10, 15, 25 minutes).",
                    "default": 15
                },
                "narrative_style": {
                    "type": "string",
                    "enum": ["3-act-documentary", "investigative", "case-study", "video-essay"],
                    "default": "3-act-documentary"
                }
            },
            "required": ["topic"]
        }
    }
]

def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Fail explicitly until production adapters exist; never invent research."""
    if name not in {tool["name"] for tool in TOOLS}:
        raise ValueError(f"Unknown tool: {name}")
    return {
        "status": "not_implemented",
        "tool": name,
        "data_source": "none",
        "data": None,
        "message": "Developer preview only. The production adapter is not implemented. No research was performed; do not infer results from this response.",
    }
