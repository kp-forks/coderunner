# InstaVM CodeRunner Plugin for Claude Code

This plugin enables Claude Code to execute Python code in a local sandboxed Apple container using [InstaVM CodeRunner](https://github.com/instavm/coderunner) via the Model Context Protocol (MCP).

## Quick Start

```bash
# 1. Install and start CodeRunner (one-time setup)
git clone https://github.com/instavm/coderunner.git
cd coderunner
sudo ./install.sh

# 2. Install the Claude Code plugin
claude plugin marketplace add github:BandarLabs/coderunner/instavm-coderunner-plugin
claude plugin install instavm-coderunner@instavm-plugins

# 3. Reconnect to MCP servers
/mcp
```

That's it! Claude Code now has access to all CodeRunner tools.

## Installation

### Prerequisites

**IMPORTANT:** You must have CodeRunner installed and running **before** installing this plugin.

#### Install CodeRunner

```bash
git clone https://github.com/instavm/coderunner.git
cd coderunner
sudo ./install.sh
```

This will:
- Install Apple's container runtime (version 0.8.0+)
- Pull the `instavm/coderunner` container image
- Start the CodeRunner MCP service at `http://coderunner.local:8222/mcp`

**Verify CodeRunner is running:**
```bash
curl http://coderunner.local:8222/execute -X POST -H "Content-Type: application/json" -d '{"code":"print(\"test\")"}'
```

### Install via GitHub URL (Recommended)

```bash
# Add the InstaVM marketplace from GitHub
claude plugin marketplace add github:BandarLabs/coderunner/instavm-coderunner-plugin

# Install the plugin
claude plugin install instavm-coderunner@instavm-plugins
```

### Option 2: Install from Local Path

If you've cloned the repository locally:

```bash
# Add local marketplace
claude plugin marketplace add /path/to/coderunner/instavm-coderunner-plugin

# Install the plugin
claude plugin install instavm-coderunner@instavm-plugins
```

## Usage

Once installed, Claude will have access to the `execute_python_code` tool from CodeRunner. You can ask Claude to execute Python code:

```
Please execute this Python code:
```python
import math
print(f"The square root of 16 is {math.sqrt(16)}")
```
```

Or simply:
```
Execute this code: print("Hello from CodeRunner!")
```

## Available Tools

The plugin exposes the following MCP tools from CodeRunner:

- **execute_python_code**: Execute Python code in a persistent Jupyter kernel with full stdout/stderr capture
- **navigate_and_get_all_visible_text**: Web scraping using Playwright - navigate to URLs and extract visible text
- **list_skills**: List all available skills (both public and user-added) in CodeRunner
- **get_skill_info**: Get documentation for a specific skill (reads SKILL.md)
- **get_skill_file**: Read any file from a skill's directory (e.g., EXAMPLES.md, API.md)

## Features

- **Local Execution**: Code runs on your machine in a sandboxed container
- **No Cloud Uploads**: Process files locally without uploading to cloud services
- **Fast Performance**: Pre-warmed Jupyter kernel pool (2-5 kernels) for quick execution
- **Full Output**: Returns stdout, stderr, execution time, and CPU time
- **Security**: Runs in Apple container isolation
- **MCP Integration**: Uses standard Model Context Protocol for tool communication

## Configuration

By default, the plugin connects to `http://coderunner.local:8222/mcp` via a stdio proxy. To customize the URL, set the `MCP_URL` environment variable in `.mcp.json`:

```json
{
  "mcpServers": {
    "instavm-coderunner": {
      "command": "python3",
      "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/mcp-proxy.py"],
      "env": {
        "MCP_URL": "http://your-custom-url:8222/mcp"
      }
    }
  }
}
```

## Example Output

```python
# Code:
print("Hello from CodeRunner!")
import time
time.sleep(0.1)
for i in range(3):
    print(f"Count: {i}")
```

**Result:**
```
Hello from CodeRunner!
Count: 0
Count: 1
Count: 2

Execution time: 0.156s
```

## Requirements

- macOS 26.0+ (recommended) for Apple Container support
- Python 3.10+
- CodeRunner installed and running
- Claude Code with MCP plugin support

## Troubleshooting

### Plugin shows "failed" status

**Most common cause:** CodeRunner container is not running.

**Solution:**
```bash
# Check if CodeRunner is running
curl http://coderunner.local:8222/execute -X POST -H "Content-Type: application/json" -d '{"code":"print(\"test\")"}'

# If not running, restart it:
cd /path/to/coderunner
sudo ./install.sh
```

### "Invalid Host header" error

The CodeRunner MCP server is running but rejecting requests. This means the container needs to be restarted with proper hostname configuration.

**Solution:**
```bash
# Stop existing containers
sudo pkill -f container
container system start

# Restart CodeRunner container
container run --name coderunner --detach --rm --cpus 8 --memory 4g \
  --volume "$HOME/.coderunner/assets/skills/user:/app/uploads/skills/user" \
  --volume "$HOME/.coderunner/outputs:/app/uploads/outputs" \
  instavm/coderunner
```

### MCP connection errors

1. **Check MCP logs:**
   ```bash
   cat ~/Library/Caches/claude-cli-nodejs/-Users-manish-coderunner-instavm-coderunner-plugin/mcp-logs-*/latest/*.jsonl
   ```

2. **Test MCP endpoint manually:**
   ```bash
   curl -H "Host: coderunner.local:8222" http://coderunner.local:8222/mcp \
     -X POST -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}'
   ```

3. **Verify proxy script:**
   ```bash
   cd /path/to/instavm-coderunner-plugin
   python3 scripts/mcp-proxy.py
   # Then send: {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}
   ```

## How It Works

This plugin uses Claude Code's MCP server integration to connect to the local CodeRunner instance:

1. The `.mcp.json` file defines the MCP server connection
2. Python proxy script bridges stdio MCP to HTTP endpoint
3. Tools from CodeRunner are automatically discovered and made available
4. When you ask Claude to execute code, it uses the `execute_python_code` tool
5. Results are returned via the MCP protocol

## Publishing to GitHub Marketplace

This plugin is published on GitHub and can be installed directly via the GitHub URL. Here's how to publish updates:

### 1. Commit and Push Changes

```bash
cd instavm-coderunner-plugin
git add .
git commit -m "Update plugin"
git push origin main
```

### 2. Users Install from GitHub

Users can install the plugin directly from GitHub:

```bash
# Add the InstaVM marketplace
claude plugin marketplace add github:BandarLabs/coderunner/instavm-coderunner-plugin

# Install the plugin
claude plugin install instavm-coderunner@instavm-plugins
```

That's it! Claude Code will automatically pull the plugin files from GitHub.

## Repository Structure

```
coderunner/
└── instavm-coderunner-plugin/     # Plugin directory
    ├── .claude-plugin/
    │   ├── marketplace.json        # Marketplace metadata
    │   └── plugin.json             # Plugin manifest
    ├── scripts/
    │   └── mcp-proxy.py            # stdio-to-HTTP MCP proxy
    ├── .mcp.json                   # MCP server configuration
    └── README.md                   # This file
```

## License

MIT
