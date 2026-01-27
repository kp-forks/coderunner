#!/usr/bin/env python3
"""
InstaVM CodeRunner MCP Proxy
Bridges stdio MCP protocol to HTTP endpoint with FastMCP session management
"""

import sys
import os
import json
import urllib.request
import urllib.error
from urllib.parse import urlparse, urlencode

# Get MCP URL from environment or use default
MCP_URL = os.environ.get("MCP_URL", "http://coderunner.local:8222/mcp")

# Session management
session_id = None

def send_request(request):
    """Forward request to HTTP MCP server with session ID"""
    global session_id

    try:
        data = json.dumps(request).encode('utf-8')
        parsed_url = urlparse(MCP_URL)
        host_header = f"{parsed_url.hostname}:{parsed_url.port}" if parsed_url.port else parsed_url.hostname

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream',
            'Host': host_header
        }

        # Add session ID header if we have one (but not for initialize)
        if session_id and request.get("method") != "initialize":
            headers['mcp-session-id'] = session_id

        url = MCP_URL

        req = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=120) as response:
            # Extract session ID from initialize response
            if request.get("method") == "initialize":
                session_id = response.headers.get('mcp-session-id')
                if not session_id:
                    # Fallback: try Set-Cookie header
                    set_cookie = response.headers.get('Set-Cookie', '')
                    if 'mcp_session_id=' in set_cookie:
                        cookie_parts = set_cookie.split(';')
                        for part in cookie_parts:
                            if 'mcp_session_id=' in part:
                                session_id = part.split('=')[1].strip()
                                break

            # Handle SSE response format
            body = response.read().decode('utf-8')
            for line in body.split('\n'):
                line = line.strip()
                if line.startswith('data: '):
                    data_str = line[6:]  # Remove 'data: ' prefix
                    if data_str and data_str != '[DONE]':
                        try:
                            response_obj = json.loads(data_str)
                            print(json.dumps(response_obj), flush=True)
                        except json.JSONDecodeError:
                            pass

    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode('utf-8')
        except:
            pass

        print(json.dumps({
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": e.code,
                "message": f"HTTP Error: {e.reason}"
            }
        }), flush=True)

    except urllib.error.URLError as e:
        print(json.dumps({
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -32603,
                "message": f"Connection Error: {e.reason}. Is CodeRunner running?"
            }
        }), flush=True)

    except Exception as e:
        print(json.dumps({
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -32603,
                "message": f"Internal Error: {str(e)}"
            }
        }), flush=True)

def main():
    """Main proxy loop"""
    # Don't log on startup to avoid confusing MCP clients
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
            send_request(request)
        except json.JSONDecodeError:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }), flush=True)

if __name__ == "__main__":
    main()
