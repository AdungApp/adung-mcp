"""Regression tests using an installed server in a separate process."""
import json
import subprocess
import sys
import tempfile
import unittest


class StdioTests(unittest.TestCase):
    def exchange(self, messages):
        with tempfile.TemporaryDirectory() as cwd:
            result = subprocess.run(
                [sys.executable, "-m", "adung_mcp.server"],
                input="\n".join(json.dumps(m) for m in messages) + "\n",
                text=True, capture_output=True, cwd=cwd, timeout=15,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        return [json.loads(line) for line in result.stdout.splitlines()]

    def test_preview_tools_never_fabricate_research(self):
        names = ["fetch_youtube_transcript", "query_niche_velocity",
                 "extract_creator_dna", "develop_script_outline"]
        arguments = [{"video_url_or_id": "example"}, {"niche_id": "science"},
                     {"channel_id_or_url": "@example"}, {"topic": "Example"}]
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": "regression", "version": "1"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        ]
        messages += [{"jsonrpc": "2.0", "id": i + 3, "method": "tools/call",
                      "params": {"name": name, "arguments": args}}
                     for i, (name, args) in enumerate(zip(names, arguments))]
        messages.append({"jsonrpc": "2.0", "id": 7, "method": "ping"})
        replies = self.exchange(messages)
        self.assertEqual([r["id"] for r in replies], list(range(1, 8)))
        self.assertEqual(replies[0]["result"]["protocolVersion"], "2024-11-05")
        tools = replies[1]["result"]["tools"]
        self.assertEqual([t["name"] for t in tools], names)
        self.assertTrue(all("not implemented" in t["description"] for t in tools))
        for reply in replies[2:6]:
            self.assertTrue(reply["result"]["isError"])
            data = json.loads(reply["result"]["content"][0]["text"])
            self.assertEqual(data["status"], "not_implemented")
            self.assertIsNone(data["data"])
            self.assertEqual(data["data_source"], "none")
        self.assertEqual(replies[-1]["result"], {})

    def test_unknown_tool_does_not_succeed(self):
        reply = self.exchange([{"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                "params": {"name": "unknown", "arguments": {}}}])[0]
        self.assertTrue(reply["result"]["isError"])


if __name__ == "__main__":
    unittest.main()
