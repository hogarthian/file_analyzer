#!/bin/bash
# MCP Server Launcher for Claude Desktop
# This script activates the virtual environment and runs the MCP server

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Activate the virtual environment
source .venv/bin/activate

# Run the MCP server
python main.py