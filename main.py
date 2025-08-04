#!/usr/bin/env python3
"""
MCP Server for file analysis tools
Provides CSV and Parquet file reading capabilities to AI assistants
"""

import pandas as pd
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("file_analyzer_server")

# Base directory for data files
DATA_DIR = Path(__file__).resolve().parent / "data"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Utility functions
def read_csv_summary(filename: str) -> str:
    """Read a CSV file and return a summary."""
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return f"Error: File '{filename}' not found in data directory."
    
    try:
        df = pd.read_csv(file_path)
        columns_info = ", ".join(df.columns.tolist())
        return f"CSV file '{filename}' has {len(df)} rows and {len(df.columns)} columns. Columns: {columns_info}"
    except Exception as e:
        return f"Error reading CSV file '{filename}': {str(e)}"

def read_parquet_summary(filename: str) -> str:
    """Read a Parquet file and return a summary."""
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return f"Error: File '{filename}' not found in data directory."
    
    try:
        df = pd.read_parquet(file_path)
        columns_info = ", ".join(df.columns.tolist())
        return f"Parquet file '{filename}' has {len(df)} rows and {len(df.columns)} columns. Columns: {columns_info}"
    except Exception as e:
        return f"Error reading Parquet file '{filename}': {str(e)}"

# MCP Tools
@mcp.tool()
def list_data_files() -> str:
    """
    List all available data files in the data directory.
    Returns:
        A string listing all available data files.
    """
    files = list(DATA_DIR.glob("*"))
    if not files:
        return "No data files found in the data directory."
    
    file_list = [f.name for f in files if f.is_file()]
    return f"Available data files: {', '.join(file_list)}"

@mcp.tool()
def summarize_csv_file(filename: str) -> str:
    """
    Summarize a CSV file by reporting its number of rows and columns.
    Args:
        filename: Name of the CSV file in the /data directory (e.g., 'sample.csv')
    Returns:
        A string describing the file's dimensions and columns.
    """
    return read_csv_summary(filename)

@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    """
    Summarize a Parquet file by reporting its number of rows and columns.
    Args:
        filename: Name of the Parquet file in the /data directory (e.g., 'sample.parquet')
    Returns:
        A string describing the file's dimensions and columns.
    """
    return read_parquet_summary(filename)

@mcp.tool()
def analyze_csv_data(filename: str, operation: str = "describe") -> str:
    """
    Perform advanced analysis on a CSV file.
    Args:
        filename: Name of the CSV file (e.g., 'sample.csv')
        operation: Type of analysis ('describe', 'head', 'info', 'columns')
    Returns:
        A string with the analysis results.
    """
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return f"Error: File '{filename}' not found."
    
    try:
        df = pd.read_csv(file_path)
        
        if operation == "describe":
            return f"Statistical description of {filename}:\n{df.describe().to_string()}"
        elif operation == "head":
            return f"First 5 rows of {filename}:\n{df.head().to_string()}"
        elif operation == "info":
            info_str = f"Info for {filename}:\n"
            info_str += f"Shape: {df.shape}\n"
            info_str += f"Columns: {list(df.columns)}\n"
            info_str += f"Data types:\n{df.dtypes.to_string()}"
            return info_str
        elif operation == "columns":
            return f"Columns in {filename}: {', '.join(df.columns)}"
        else:
            return f"Unknown operation: {operation}. Available: describe, head, info, columns"
            
    except Exception as e:
        return f"Error analyzing {filename}: {str(e)}"

@mcp.tool()
def create_sample_data(filename: str, rows: int = 10) -> str:
    """
    Create a new sample dataset.
    Args:
        filename: Name for the new file (e.g., 'new_data.csv')
        rows: Number of rows to generate
    Returns:
        A confirmation message.
    """
    import random
    from datetime import datetime, timedelta
    
    try:
        # Generate sample data
        data = {
            'id': range(1, rows + 1),
            'name': [f"User_{i}" for i in range(1, rows + 1)],
            'score': [random.randint(1, 100) for _ in range(rows)],
            'category': [random.choice(['A', 'B', 'C']) for _ in range(rows)],
            'created_date': [(datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d') for _ in range(rows)]
        }
        
        df = pd.DataFrame(data)
        file_path = DATA_DIR / filename
        
        if filename.endswith('.csv'):
            df.to_csv(file_path, index=False)
        elif filename.endswith('.parquet'):
            df.to_parquet(file_path, index=False)
        else:
            return "Error: Filename must end with .csv or .parquet"
        
        return f"Created {filename} with {rows} rows and {len(df.columns)} columns."
        
    except Exception as e:
        return f"Error creating sample data: {str(e)}"

# MCP Resources
@mcp.resource("data://schema")
def get_data_schema() -> str:
    """Provide schema information for available datasets."""
    schema_info = {
        "description": "Schema information for data files",
        "supported_formats": ["CSV", "Parquet"],
        "sample_structure": {
            "id": "integer - unique identifier",
            "name": "string - user name", 
            "email": "string - email address",
            "signup_date": "date - registration date"
        }
    }
    return json.dumps(schema_info, indent=2)

if __name__ == "__main__":
    # Create sample data if it doesn't exist
    sample_csv = DATA_DIR / "sample.csv"
    if not sample_csv.exists():
        sample_data = {
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice Johnson', 'Bob Smith', 'Carol Lee', 'David Wu', 'Eva Brown'],
            'email': ['alice@example.com', 'bob@example.com', 'carol@example.com', 'david@example.com', 'eva@example.com'],
            'signup_date': ['2023-01-15', '2023-02-22', '2023-03-10', '2023-04-18', '2023-05-30']
        }
        df = pd.DataFrame(sample_data)
        df.to_csv(sample_csv, index=False)
        df.to_parquet(DATA_DIR / "sample.parquet", index=False)
        print(f"Created sample data files in {DATA_DIR}")
    
    print("Starting MCP File Analyzer Server...")
    mcp.run()