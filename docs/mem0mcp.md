# Mem0-MCP
[Memory Optimization for Machine Learning Models](https://github.com/mem0ai/mem0-mcp)



# How mem0-MCP is installed in this code space

I am using the cloud hosted version of mem0, which is available at https://mem0.ai/
There is a selfhosted version that can be run locally in Docker, but I am not using that at this time. I have tested it and it works great but there are extra steps needed for memory to be persistant across restarts. I will likely eventually move to this method.

```bash
cd /workspace
git clone https://github.com/mem0ai/mem0-mcp.git
cd mem0-mcp
nano .env
# Edit the .env file to set the environment variables
# For example:
# export MEM0_MCP_API_KEY=your_api_key
uv venv
source .venv/bin/activate
uv pip install -e .
uv run main.py

# Set MCP client to connect to the SSE endpoint
http://0.0.0.0:8080/sse
```
