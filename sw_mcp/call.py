"""Call the SolidWorks MCP server over real stdio - smoke test and CLI fallback.

    python call.py                                   # list tools + sw_status
    python call.py doc_info '{"doc": "2605_MASTER"}'
    python call.py @calls.json                       # [["tool", {args}], ...] in one session

Images are written next to the server's work folder and their paths printed.
"""
import asyncio
import base64
import json
import os
import sys
import tempfile
import time

from mcp import Client
from mcp.client.stdio import StdioServerParameters

SERVER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")
OUT = os.path.join(tempfile.gettempdir(), "sw_mcp")


def show(result):
    for block in result.content:
        if block.type == "text":
            print(block.text)
        elif block.type == "image":
            path = os.path.join(OUT, f"cli_{int(time.time() * 1000)}.png")
            with open(path, "wb") as fh:
                fh.write(base64.b64decode(block.data))
            print(f"[image {block.mime_type} -> {path}]")
    if result.is_error:
        print("[tool reported an error]")


async def main(argv):
    if argv and argv[0].startswith("@"):
        calls = json.load(open(argv[0][1:], encoding="utf-8"))
    elif argv:
        calls = [[argv[0], json.loads(argv[1]) if len(argv) > 1 else {}]]
    else:
        calls = None
    params = StdioServerParameters(command=sys.executable, args=[SERVER])
    async with Client(params) as client:
        if calls is None:
            tools = await client.list_tools()
            print("tools:", ", ".join(t.name for t in tools.tools))
            calls = [["sw_status", {}]]
        for name, args in calls:
            t0 = time.time()
            print(f"=== {name} {json.dumps(args)[:200]}")
            show(await client.call_tool(name, args, read_timeout_seconds=7200))
            print(f"--- {time.time() - t0:.1f}s")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
