"""Standard Model Context Protocol (MCP) stdio server implementation.

Targets MCP protocol version 2024-11-05.
Client-specific compatibility requires separate verification.
"""
import json
import sys
import logging
from typing import Any, Dict

from adung_mcp.tools import TOOLS, handle_tool_call

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("adung_mcp")

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "adung-youtube-mcp"
SERVER_VERSION = "1.2.0"

def format_jsonrpc_response(request_id: Any, result: Any) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result
    }

def format_jsonrpc_error(request_id: Any, code: int, message: str) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message
        }
    }

def process_message(msg: Dict[str, Any]) -> Dict[str, Any] | None:
    method = msg.get("method")
    req_id = msg.get("id")
    params = msg.get("params", {})

    logger.info("Handling MCP method: %s (id: %s)", method, req_id)

    # Handshake notification
    if method == "notifications/initialized":
        logger.info("Client handshake completed successfully.")
        return None

    if method == "initialize":
        return format_jsonrpc_response(req_id, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {
                "tools": {
                    "listChanged": False
                }
            },
            "serverInfo": {
                "name": SERVER_NAME,
                "version": SERVER_VERSION
            }
        })

    elif method == "tools/list":
        return format_jsonrpc_response(req_id, {
            "tools": TOOLS
        })

    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        try:
            result_data = handle_tool_call(tool_name, arguments)
            return format_jsonrpc_response(req_id, {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result_data, indent=2, ensure_ascii=False)
                    }
                ],
                "isError": result_data.get("status") == "not_implemented"
            })
        except Exception as e:
            logger.error("Error executing tool %s: %s", tool_name, str(e))
            return format_jsonrpc_response(req_id, {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error executing tool {tool_name}: {str(e)}"
                    }
                ],
                "isError": True
            })

    elif method == "ping":
        return format_jsonrpc_response(req_id, {})

    else:
        return format_jsonrpc_error(req_id, -32601, f"Method not found: {method}")

def run_test_suite():
    """Validate MCP server requests locally."""
    print(f"--- Testing {SERVER_NAME} v{SERVER_VERSION} ---")
    
    # Test initialize
    init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    init_res = process_message(init_req)
    assert init_res["result"]["serverInfo"]["name"] == SERVER_NAME
    print("✓ Handshake initialize OK")
    
    # Test tools/list
    tools_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    tools_res = process_message(tools_req)
    assert len(tools_res["result"]["tools"]) == 4
    print(f"✓ tools/list returned {len(tools_res['result']['tools'])} registered tools")
    
    # Test tools/call
    call_req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "develop_script_outline",
            "arguments": {"topic": "The Economics of AI Creators", "target_duration_minutes": 12}
        }
    }
    call_res = process_message(call_req)
    assert call_res is not None
    assert call_res["result"]["isError"]
    assert json.loads(call_res["result"]["content"][0]["text"])["status"] == "not_implemented"
    print("OK: preview tool explicitly reports unavailable; no synthetic research")
    print("In-process smoke passed; this does not verify Claude client integration.")

def main():
    if "--test" in sys.argv:
        run_test_suite()
        return

    logger.info("Adung YouTube MCP Server started (stdio). Listening for requests...")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = process_message(req)
            if res is not None:
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError:
            logger.error("Malformed JSON line received: %s", line)
        except Exception as e:
            logger.error("Unhandled server exception: %s", str(e))

if __name__ == "__main__":
    main()
