#!/bin/bash
# InstaVM CodeRunner Plugin Installer for Claude Code

PLUGIN_NAME="instavm-coderunner"
PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Installing $PLUGIN_NAME plugin for Claude Code..."
echo ""

# Check if CodeRunner is running
echo "🔍 Checking if CodeRunner is running..."
if curl -s http://coderunner.local:8222/health > /dev/null 2>&1; then
    echo "✅ CodeRunner is running at http://coderunner.local:8222"
else
    echo "⚠️  Warning: CodeRunner does not appear to be running."
    echo "   Please install and start CodeRunner first:"
    echo "   cd /path/to/coderunner && sudo ./install.sh"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check MCP endpoint
echo "🔍 Checking MCP endpoint..."
if curl -s http://coderunner.local:8222/mcp > /dev/null 2>&1; then
    echo "✅ MCP endpoint is accessible"
else
    echo "⚠️  Warning: MCP endpoint not accessible"
fi

echo ""
echo "📦 Plugin location: $PLUGIN_DIR"
echo ""
echo "To use this plugin with Claude Code, run:"
echo ""
echo "  cd $PLUGIN_DIR"
echo "  claude --plugin-dir ."
echo ""
echo "Or add it permanently:"
echo ""
echo "  claude add plugin $PLUGIN_DIR"
echo ""
echo "✅ Setup complete!"
