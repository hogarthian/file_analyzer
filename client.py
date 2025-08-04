#!/usr/bin/env python3
"""
MCP Client for testing the file analyzer server
Demonstrates how to programmatically interact with MCP tools
"""

import asyncio
import json
import sys
from pathlib import Path
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

class MCPFileAnalyzerClient:
    """A client for interacting with the MCP file analyzer server."""
    
    def __init__(self, server_script_path: str = "main.py"):
        self.server_script_path = server_script_path
        self.session = None
    
    async def connect(self):
        """Connect to the MCP server."""
        server_params = StdioServerParameters(
            command="python",
            args=[self.server_script_path],
            env=None
        )
        
        try:
            self.stdio_client = stdio_client(server_params)
            self.read, self.write = await self.stdio_client.__aenter__()
            self.session = ClientSession(self.read, self.write)
            await self.session.__aenter__()
            
            # Initialize the session
            await self.session.initialize()
            print("✅ Connected to MCP server successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to MCP server: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from the MCP server."""
        try:
            if self.session:
                await self.session.__aexit__(None, None, None)
            if hasattr(self, 'stdio_client'):
                await self.stdio_client.__aexit__(None, None, None)
            print("✅ Disconnected from MCP server")
        except Exception as e:
            print(f"⚠️ Error during disconnect: {e}")
    
    async def list_tools(self):
        """List all available tools from the server."""
        try:
            response = await self.session.list_tools()
            print("🔧 Available tools:")
            for tool in response.tools:
                print(f"  - {tool.name}: {tool.description}")
            return response.tools
        except Exception as e:
            print(f"❌ Error listing tools: {e}")
            return []
    
    async def list_resources(self):
        """List all available resources from the server."""
        try:
            response = await self.session.list_resources()
            print("📚 Available resources:")
            for resource in response.resources:
                print(f"  - {resource.uri}: {resource.description}")
            return response.resources
        except Exception as e:
            print(f"❌ Error listing resources: {e}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: dict = None):
        """Call a specific tool with arguments."""
        if arguments is None:
            arguments = {}
        
        try:
            print(f"🔧 Calling tool: {tool_name} with args: {arguments}")
            response = await self.session.call_tool(tool_name, arguments)
            
            if response.content:
                for content in response.content:
                    if hasattr(content, 'text'):
                        print(f"📄 Result: {content.text}")
                    else:
                        print(f"📄 Result: {content}")
            return response
            
        except Exception as e:
            print(f"❌ Error calling tool {tool_name}: {e}")
            return None
    
    async def get_resource(self, uri: str):
        """Get a resource from the server."""
        try:
            print(f"📚 Getting resource: {uri}")
            response = await self.session.read_resource(uri)
            
            if response.contents:
                for content in response.contents:
                    if hasattr(content, 'text'):
                        print(f"📄 Resource content:\n{content.text}")
                    else:
                        print(f"📄 Resource content: {content}")
            return response
            
        except Exception as e:
            print(f"❌ Error getting resource {uri}: {e}")
            return None

async def interactive_demo():
    """Run an interactive demo of the MCP client."""
    client = MCPFileAnalyzerClient()
    
    print("🚀 Starting MCP File Analyzer Client Demo")
    print("=" * 50)
    
    # Connect to server
    if not await client.connect():
        return
    
    try:
        # List available tools
        print("\n1. Discovering available tools...")
        tools = await client.list_tools()
        
        # List available resources
        print("\n2. Discovering available resources...")
        resources = await client.list_resources()
        
        # Test basic functionality
        print("\n3. Testing basic functionality...")
        
        # List data files
        print("\n📂 Listing data files:")
        await client.call_tool("list_data_files")
        
        # Summarize CSV file
        print("\n📊 Summarizing CSV file:")
        await client.call_tool("summarize_csv_file", {"filename": "sample.csv"})
        
        # Analyze CSV data
        print("\n🔍 Analyzing CSV data (info):")
        await client.call_tool("analyze_csv_data", {"filename": "sample.csv", "operation": "info"})
        
        # Show first few rows
        print("\n👀 Showing first 5 rows:")
        await client.call_tool("analyze_csv_data", {"filename": "sample.csv", "operation": "head"})
        
        # Create sample data
        print("\n🆕 Creating new sample data:")
        await client.call_tool("create_sample_data", {"filename": "test_data.csv", "rows": 3})
        
        # Get schema resource
        print("\n📋 Getting data schema:")
        await client.get_resource("data://schema")
        
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    
    finally:
        await client.disconnect()

async def run_custom_commands():
    """Allow users to run custom commands."""
    client = MCPFileAnalyzerClient()
    
    if not await client.connect():
        return
    
    try:
        print("\n🎮 Interactive MCP Client")
        print("Available commands:")
        print("  - list_tools: Show available tools")
        print("  - list_files: List data files")
        print("  - summarize <filename>: Summarize a file")
        print("  - analyze <filename> <operation>: Analyze data")
        print("  - create <filename> <rows>: Create sample data")
        print("  - quit: Exit")
        
        while True:
            try:
                command = input("\n🤖 Enter command: ").strip()
                
                if command == "quit":
                    break
                elif command == "list_tools":
                    await client.list_tools()
                elif command == "list_files":
                    await client.call_tool("list_data_files")
                elif command.startswith("summarize"):
                    parts = command.split()
                    if len(parts) >= 2:
                        filename = parts[1]
                        if filename.endswith('.csv'):
                            await client.call_tool("summarize_csv_file", {"filename": filename})
                        elif filename.endswith('.parquet'):
                            await client.call_tool("summarize_parquet_file", {"filename": filename})
                        else:
                            print("❌ Please specify .csv or .parquet extension")
                    else:
                        print("❌ Usage: summarize <filename>")
                elif command.startswith("analyze"):
                    parts = command.split()
                    if len(parts) >= 3:
                        filename = parts[1]
                        operation = parts[2]
                        await client.call_tool("analyze_csv_data", {"filename": filename, "operation": operation})
                    else:
                        print("❌ Usage: analyze <filename> <operation>")
                elif command.startswith("create"):
                    parts = command.split()
                    if len(parts) >= 3:
                        filename = parts[1]
                        rows = int(parts[2])
                        await client.call_tool("create_sample_data", {"filename": filename, "rows": rows})
                    else:
                        print("❌ Usage: create <filename> <rows>")
                else:
                    print("❌ Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                print("\n🛑 Interrupted by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
    finally:
        await client.disconnect()

def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        asyncio.run(run_custom_commands())
    else:
        asyncio.run(interactive_demo())

if __name__ == "__main__":
    main()