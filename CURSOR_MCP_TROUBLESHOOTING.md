# 🔧 Cursor MCP Tools Troubleshooting Guide

## ✅ **MCP Server Status: WORKING**

The MCP server is running correctly and all tests pass:
- ✅ **Server running** on `http://127.0.0.1:8500/mcp`
- ✅ **3 tools available**: `generate_cultural_names`, `validate_names_watchlist`, `get_cultural_context`
- ✅ **MCP protocol compliant**: JSON-RPC 2.0 with proper initialize/tools/list/tools/call methods
- ✅ **Tool schemas correct**: Proper inputSchema with type definitions

## 🔍 **Troubleshooting Steps**

### 1. **Verify MCP Server is Running**
```bash
# Check if server is responding
curl -X GET http://127.0.0.1:8500/mcp

# Or use Python
python -c "import requests; print(requests.get('http://127.0.0.1:8500/mcp').json())"
```

### 2. **Cursor MCP Configuration**

#### **Option A: Using Cursor Settings**
1. Open Cursor
2. Go to **Settings** (Ctrl/Cmd + ,)
3. Search for **"MCP"** or **"Multi-Agent Communication Protocol"**
4. Add a new MCP server with these settings:
   - **Name**: `NAME Generation Tools`
   - **URL**: `http://127.0.0.1:8500/mcp`
   - **Type**: `HTTP`

#### **Option B: Using Cursor Configuration File**
1. Open Cursor
2. Press **Ctrl/Cmd + Shift + P**
3. Type **"Preferences: Open Settings (JSON)"**
4. Add this configuration:
```json
{
  "mcp.servers": {
    "name-generation": {
      "command": "http",
      "args": ["http://127.0.0.1:8500/mcp"]
    }
  }
}
```

### 3. **Restart Cursor**
After configuring the MCP server:
1. **Close Cursor completely**
2. **Restart Cursor**
3. **Check if tools appear** in the command palette or tool list

### 4. **Check Cursor Logs**
1. Open Cursor
2. Press **Ctrl/Cmd + Shift + P**
3. Type **"Developer: Toggle Developer Tools"**
4. Check the **Console** tab for any MCP-related errors

### 5. **Alternative: Use Cursor's MCP Host Feature**
1. In Cursor, press **Ctrl/Cmd + Shift + P**
2. Type **"MCP"** to see available MCP commands
3. Look for **"MCP: Connect to Server"** or similar
4. Enter the URL: `http://127.0.0.1:8500/mcp`

## 🛠️ **Manual Testing**

If Cursor still can't see the tools, test manually:

```bash
# Test tool discovery
curl -X POST http://127.0.0.1:8500/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'

# Test tool execution
curl -X POST http://127.0.0.1:8500/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "get_cultural_context", "arguments": {"region": "Europe", "religion": "Christianity"}}}'
```

## 📋 **Available Tools**

### 1. `generate_cultural_names`
- **Purpose**: Generate culturally appropriate names
- **Parameters**: sex, age, location, occupation, race, religion, birth_year
- **Example**: Generate names for a 25-year-old male Asian Buddhist engineer from Japan

### 2. `validate_names_watchlist`
- **Purpose**: Validate names against safety patterns
- **Parameters**: names (list of name dictionaries)
- **Example**: Check if generated names contain inappropriate patterns

### 3. `get_cultural_context`
- **Purpose**: Get cultural context for regions and religions
- **Parameters**: region, religion
- **Example**: Get naming patterns for European Christianity

## 🔄 **If Still Not Working**

### **Step 1: Check Cursor Version**
- Ensure you're using the **latest version** of Cursor
- MCP support might be version-dependent

### **Step 2: Alternative MCP Client**
Try using a different MCP client to verify the server works:
```bash
# Install mcp-cli if available
pip install mcp-cli

# Or use a simple HTTP client
python -c "
import requests
response = requests.post('http://127.0.0.1:8500/mcp', 
  json={'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'})
print(response.json())
"
```

### **Step 3: Check Firewall/Antivirus**
- Ensure port 8500 is not blocked
- Check if antivirus is blocking the connection

### **Step 4: Try Different Port**
If port 8500 is blocked, modify the server to use a different port:
```python
# In strands_mcp_server.py, change:
def run_strands_mcp_server(port=8501):  # Change to 8501
```

## 📞 **Support**

If none of the above works:
1. **Check Cursor's documentation** for MCP setup
2. **Verify Cursor supports MCP** in your version
3. **Try a different MCP client** to confirm server functionality
4. **Check Cursor's GitHub issues** for MCP-related problems

## 🎯 **Expected Result**

Once working, you should see the tools in Cursor's:
- **Command palette** (Ctrl/Cmd + Shift + P)
- **Tool list** or **MCP tools** section
- **Autocomplete** when typing tool names

The tools should be callable directly from Cursor's interface with proper parameter prompts.
