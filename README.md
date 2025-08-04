# MCP File Analyzer: Complete Setup & Usage Guide

This guide will walk you through setting up a Model Context Protocol (MCP) server that can analyze CSV and Parquet files, and connecting it to Claude Desktop for natural language data analysis.

## 🎯 What You'll Build

A powerful data analysis tool that allows Claude to:
- 📊 Read and analyze CSV/Parquet files
- 📈 Generate statistical summaries  
- 👀 Show data previews and structure
- 🔧 Create sample datasets
- 💬 Answer natural language questions about your data

## Table of Contents

1. [What is MCP?](#what-is-mcp)
2. [Quick Start](#quick-start)
3. [Prerequisites](#prerequisites)
4. [Project Setup](#project-setup)
5. [Claude Desktop Integration](#claude-desktop-integration)
6. [Usage Examples](#usage-examples)
7. [Testing & Verification](#testing--verification)
8. [Troubleshooting](#troubleshooting)
9. [Extending the Server](#extending-the-server)
10. [Project Structure](#project-structure)

## What is MCP?

Model Context Protocol (MCP) is a standardized way to connect AI assistants like Claude to external tools and data sources. It allows you to:

- 🔐 Give Claude access to your local files (securely)
- 🛠️ Create custom tools that Claude can use
- 🔄 Build reusable AI workflows
- 🏠 Keep your data secure and local (no API keys needed!)

## Quick Start

### ⚡ For the Impatient

```bash
# Clone or create project directory
mkdir mcp-file-analyzer && cd mcp-file-analyzer

# Set up virtual environment
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install mcp>=1.0.0 pandas>=2.0.0 pyarrow>=10.0.0

# Create and test the server (copy main.py and client.py from this repo)
python main.py  # Start server (Ctrl+C to stop)
python client.py  # Test the connection

# Configure Claude Desktop (see detailed steps below)
```

## Prerequisites

Before you begin, make sure you have:

- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- **Claude Desktop** installed ([download here](https://claude.ai/download))
- **macOS, Windows, or Linux** (Claude Desktop support varies)

Check your Python version:
```bash
python3 --version  # Should be 3.8+
```

## Project Setup

### Step 1: Create Project and Virtual Environment

```bash
# Create project directory
mkdir mcp-file-analyzer
cd mcp-file-analyzer

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### Step 2: Install Dependencies

Create `requirements.txt`:
```txt
# Core dependencies for MCP File Analyzer
mcp>=1.0.0
pandas>=2.0.0
pyarrow>=10.0.0

# HTTP client dependencies (optional)
httpx>=0.27.0

# Development dependencies (optional)
# pytest>=7.0.0
# black>=23.0.0
# flake8>=6.0.0
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Create Project Files

Your project needs these core files:

1. **main.py** - The MCP server
2. **client.py** - Testing client
3. **requirements.txt** - Dependencies
4. **run_mcp_server.sh** - Launcher script for Claude Desktop
5. **claude_desktop_config.json** - Claude Desktop configuration

### Step 4: Create Helper Scripts

Create `activate_env.sh` for easy environment activation:
```bash
#!/bin/bash
echo "🚀 Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated!"
echo "📦 Installed packages:"
pip list --format=columns
echo ""
echo "🎯 Quick start commands:"
echo "  - Run MCP server: python main.py"
echo "  - Run demo client: python client.py"
echo "  - Interactive client: python client.py interactive"
```

Make it executable:
```bash
chmod +x activate_env.sh
```

## Claude Desktop Integration

### 🎯 Method 1: Direct Integration (Recommended)

#### Step 1: Create Launcher Script

Create `run_mcp_server.sh`:
```bash
#!/bin/bash
# MCP Server Launcher for Claude Desktop

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Activate the virtual environment
source .venv/bin/activate

# Run the MCP server
python main.py
```

Make it executable:
```bash
chmod +x run_mcp_server.sh
```

#### Step 2: Create Claude Desktop Configuration

Create `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "file_analyzer": {
      "command": "/ABSOLUTE/PATH/TO/YOUR/PROJECT/run_mcp_server.sh",
      "args": []
    }
  }
}
```

**Important:** Replace `/ABSOLUTE/PATH/TO/YOUR/PROJECT` with your actual project path. Get it with:
```bash
pwd  # Copy this output
```

#### Step 3: Install Configuration in Claude Desktop

Copy the configuration to Claude Desktop:

**macOS:**
```bash
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
copy claude_desktop_config.json %APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
cp claude_desktop_config.json ~/.config/claude/claude_desktop_config.json
```

#### Step 4: Restart Claude Desktop

1. **Quit Claude Desktop completely**
2. **Relaunch the application**
3. **Look for the tool icon (🔨)** in the interface

### 🌐 Method 2: HTTP Server (Alternative)

For web-based testing and debugging, you can also run an HTTP version:

```bash
# Install additional dependencies
pip install uvicorn fastapi

# Start HTTP server
python http_server.py

# Test with HTTP client
python http_client.py

# Access web interface
open http://localhost:8000/docs
```

## Usage Examples

### 🚀 Getting Started with Claude

Once integrated, try these commands in Claude Desktop:

#### Basic Commands

**Check available tools:**
```
What MCP tools do you have available?
```

**List data files:**
```
What data files do I have available?
```

**Analyze a CSV file:**
```
Can you summarize the sample.csv file?
```

#### Advanced Analysis

**Data exploration:**
```
Show me the first 5 rows of sample.csv and tell me about the data structure
```

**Statistical analysis:**
```
Give me statistical information about sample.csv - what are the data types and any interesting patterns?
```

**Create new data:**
```
Create a new CSV file called "customer_data.csv" with 50 rows of sample customer data
```

**Comprehensive analysis:**
```
List all my data files, pick the most interesting one, and give me a complete analysis including:
- File structure and dimensions
- Data types for each column  
- First few rows as examples
- Statistical summary for numeric columns
```

### 📊 Expected Results

Claude should respond with actual data from your files:

- **File summaries:** "CSV file 'sample.csv' has 5 rows and 4 columns. Columns: id, name, email, signup_date"
- **Data previews:** Formatted tables showing your actual data
- **Statistical analysis:** Mean, median, standard deviation for numeric columns
- **Data insights:** Observations about patterns in your data

### 🧪 Sample Data Included

Your MCP server automatically creates sample data:

**sample.csv:**
```csv
id,name,email,signup_date
1,Alice Johnson,alice@example.com,2023-01-15
2,Bob Smith,bob@example.com,2023-02-22
3,Carol Lee,carol@example.com,2023-03-10
4,David Wu,david@example.com,2023-04-18
5,Eva Brown,eva@example.com,2023-05-30
```

## Testing & Verification

### 🔧 Test the Server Directly

```bash
# Activate environment
source .venv/bin/activate

# Test server and client
python client.py
```

**Expected output:**
```
🚀 Starting MCP File Analyzer Client Demo
==================================================
✅ Connected to MCP server successfully!

🔧 Available tools:
  - list_data_files
  - summarize_csv_file
  - summarize_parquet_file
  - analyze_csv_data
  - create_sample_data

📂 Listing data files:
📄 Result: Available data files: sample.csv, sample.parquet

📊 Summarizing CSV file:
📄 Result: CSV file 'sample.csv' has 5 rows and 4 columns...
```

### 🎮 Interactive Mode

```bash
python client.py interactive
```

Try these commands:
- `list_files`
- `summarize sample.csv`
- `analyze sample.csv head`
- `create test_data.csv 10`

### ✅ Verify Claude Integration

In Claude Desktop, you should see:

1. **Tool icon (🔨)** in the interface
2. **Available tools** when you ask "What MCP tools do you have?"
3. **Successful responses** to data analysis questions

## Troubleshooting

### 🐛 Common Issues

#### 1. No Tool Icon in Claude Desktop

**Symptoms:** Claude Desktop starts but no MCP tools appear

**Solutions:**
```bash
# Check config file location
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Verify JSON syntax
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Test launcher script
./run_mcp_server.sh

# Check permissions
chmod +x run_mcp_server.sh
```

#### 2. "Server Not Found" Error

**Symptoms:** Claude shows error about server connection

**Solutions:**
```bash
# Verify absolute path in config
pwd  # Make sure this matches your config

# Test server independently
source .venv/bin/activate
python main.py

# Check virtual environment
which python  # Should show .venv path
```

#### 3. "Module Not Found" Error

**Symptoms:** Import errors when starting server

**Solutions:**
```bash
# Reinstall dependencies
source .venv/bin/activate
pip install -r requirements.txt

# Verify installation
pip list | grep mcp
pip list | grep pandas
pip list | grep pyarrow
```

#### 4. Tools Appear But Don't Work

**Symptoms:** Tools listed but return errors

**Solutions:**
```bash
# Check data directory
ls -la data/

# Recreate sample data
rm -rf data/
python main.py  # Will recreate sample files

# Test with client
python client.py
```

### 🔍 Debug Steps

1. **Test each component independently:**
   ```bash
   # Test server
   python main.py
   
   # Test client (in another terminal)
   python client.py
   
   # Test launcher
   ./run_mcp_server.sh
   ```

2. **Check file permissions:**
   ```bash
   ls -la *.py *.sh
   chmod +x run_mcp_server.sh
   ```

3. **Validate configuration:**
   ```bash
   # Check JSON syntax
   python -c "import json; print(json.load(open('claude_desktop_config.json')))"
   ```

4. **Check Claude Desktop logs:**
   - Look for error messages in Claude Desktop
   - Check system logs for permission issues

## Extending the Server

### 🛠️ Adding New Tools

Create custom tools with the `@mcp.tool()` decorator:

```python
@mcp.tool()
def analyze_excel_file(filename: str) -> str:
    """
    Analyze an Excel file and return summary information.
    Args:
        filename: Name of the Excel file (e.g., 'data.xlsx')
    Returns:
        A string describing the file's contents.
    """
    import pandas as pd
    file_path = DATA_DIR / filename
    
    # Read Excel file
    df = pd.read_excel(file_path)
    
    return f"Excel file '{filename}' has {len(df)} rows and {len(df.columns)} columns"
```

### 📚 Adding Resources

Provide static information to Claude:

```python
@mcp.resource("data://file-formats")
def get_supported_formats() -> str:
    """List supported file formats."""
    formats = {
        "supported_formats": ["CSV", "Parquet", "Excel", "JSON"],
        "max_file_size": "100MB",
        "encoding": "UTF-8"
    }
    return json.dumps(formats, indent=2)
```

### 🔗 Adding Database Support

Connect to databases:

```python
import sqlite3

@mcp.tool()
def query_database(query: str) -> str:
    """
    Execute a SQL query on the local database.
    Args:
        query: SQL query to execute
    Returns:
        Query results as formatted text.
    """
    conn = sqlite3.connect('data/database.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df.to_string()
```

## Project Structure

Your complete project should look like this:

```
mcp-file-analyzer/
├── .venv/                          # Virtual environment
├── data/                           # Data files (auto-created)
│   ├── sample.csv                  # Sample CSV data
│   ├── sample.parquet              # Sample Parquet data
│   └── ...                        # Your data files
├── main.py                         # MCP server (stdio)
├── client.py                       # Test client (stdio)
├── http_server.py                  # HTTP MCP server (optional)
├── http_client.py                  # HTTP test client (optional)
├── requirements.txt                # Python dependencies
├── activate_env.sh                 # Environment activation script
├── run_mcp_server.sh              # Claude Desktop launcher
├── claude_desktop_config.json     # Claude Desktop config
├── .gitignore                     # Git ignore file
└── README.md                      # This file
```

### 📁 Key Files Explained

- **main.py**: MCP server that provides file analysis tools
- **client.py**: Test client to verify server functionality
- **run_mcp_server.sh**: Launcher script for Claude Desktop integration
- **claude_desktop_config.json**: Configuration for Claude Desktop
- **requirements.txt**: Python package dependencies
- **data/**: Directory containing your data files

## Next Steps

### 🚀 After Setup

1. **Add your own data** - Copy CSV/Parquet files to the `data/` directory
2. **Experiment with Claude** - Try complex data analysis questions
3. **Create custom tools** - Build tools specific to your workflow
4. **Explore advanced features** - Add database connections, web APIs, etc.

### 💡 Ideas for Enhancement

- **Excel support** - Add tools for .xlsx files
- **Data visualization** - Generate charts and graphs
- **Database integration** - Connect to SQL databases
- **API connections** - Fetch data from web APIs
- **Machine learning** - Add prediction and analysis tools
- **File monitoring** - Watch directories for new data files

### 🔗 Useful Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop](https://claude.ai/download)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 🎉 Congratulations!

You now have a fully functional MCP server that can:

✅ Analyze CSV and Parquet files  
✅ Respond to natural language queries through Claude  
✅ Create and manipulate data files  
✅ Provide detailed statistical analysis  
✅ Work entirely offline (no API keys required!)  

**Happy data analyzing!** 📊🤖