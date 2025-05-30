---
name: Installation Help
about: Get help with ProxmoxMCP installation and setup
title: '[INSTALL] '
labels: help-wanted, installation
assignees: ''
---

## Installation Issue Description
<!-- Describe what you're trying to install/setup and what's going wrong -->

## Installation Method
<!-- Which installation method are you using? -->
- [ ] Quick Install with UV (recommended)
- [ ] Docker/Docker Compose
- [ ] Manual pip installation
- [ ] Development setup
- [ ] Other: 

## Current Step/Stage
<!-- Which step in the installation process are you stuck on? -->
- [ ] Environment setup (Python, UV, Git)
- [ ] Repository cloning
- [ ] Virtual environment creation
- [ ] Dependency installation
- [ ] Configuration file setup
- [ ] Proxmox connection testing
- [ ] MCP server startup
- [ ] Cline/IDE integration
- [ ] Other: 

## Environment Details
- **Operating System**: <!-- e.g., Ubuntu 22.04, Windows 11, macOS 13 -->
- **Python Version**: <!-- e.g., 3.10.4 (python --version) -->
- **UV Version**: <!-- e.g., 0.1.0 (uv --version) -->
- **Git Version**: <!-- e.g., 2.34.1 (git --version) -->
- **Shell**: <!-- e.g., bash, zsh, PowerShell, Command Prompt -->

## Error Messages
<!-- Include any error messages you're seeing -->
```
Paste error messages here
```

## Commands Run
<!-- Show the exact commands you've run -->
```bash
# Example:
git clone https://github.com/basher83/ProxmoxMCP.git
cd ProxmoxMCP
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Configuration Attempted
<!-- If you've tried to set up configuration, show what you have -->

### Config File Location
<!-- Where did you place your config file? -->
- [ ] `/workspaces/ProxmoxMCP/proxmox-config/config.json`
- [ ] Other location: 

### Environment Variables
<!-- Which environment variables have you set? -->
```bash
# Example:
export PROXMOX_MCP_CONFIG="proxmox-config/config.json"
# List other variables you've set
```

### Configuration File Content
<!-- Share your config file (remove sensitive tokens!) -->
```json
{
    "proxmox": {
        "host": "REDACTED",
        "port": 8006,
        "verify_ssl": false,
        "service": "PVE"
    },
    "auth": {
        "user": "REDACTED",
        "token_name": "REDACTED",
        "token_value": "REDACTED"
    }
}
```

## Proxmox Environment
- **Proxmox Version**: <!-- e.g., 7.4-3 -->
- **Proxmox Host**: <!-- e.g., Local network, VPN, Cloud -->
- **API Token Status**: 
  - [ ] Token created successfully
  - [ ] Token tested manually (e.g., with curl)
  - [ ] Token permissions verified
  - [ ] Unsure how to create token

## What You've Tried
<!-- List troubleshooting steps you've already attempted -->
- [ ] Followed the README installation guide
- [ ] Checked Python version compatibility
- [ ] Verified virtual environment activation
- [ ] Tried different config file locations
- [ ] Tested Proxmox connection manually
- [ ] Checked firewall/network connectivity
- [ ] Searched existing issues
- [ ] Other: 

## Expected Outcome
<!-- What should happen after successful installation? -->

## Current Output
<!-- What are you seeing instead? -->
```
Paste actual output here
```

## Verification Tests
<!-- Help us understand what's working and what isn't -->

### Python Environment Test
```bash
# Run this and paste the output:
python -c "import sys; print(f'Python: {sys.version}')"
python -c "import proxmox_mcp; print('ProxmoxMCP imported successfully')"
```

### Configuration Test
```bash
# Run this and paste the output (remove sensitive data):
python -c "
import os
print(f'PROXMOX_MCP_CONFIG: {os.getenv(\"PROXMOX_MCP_CONFIG\")}')
print(f'Config file exists: {os.path.exists(os.getenv(\"PROXMOX_MCP_CONFIG\", \"\"))}')
"
```

### Network Test
```bash
# Test connectivity to your Proxmox server:
ping -c 3 YOUR_PROXMOX_HOST
curl -k https://YOUR_PROXMOX_HOST:8006/api2/json/version
```

## Additional Context
<!-- Anything else that might help us help you -->

## Documentation Feedback
<!-- Was anything unclear in our installation docs? -->
- [ ] README instructions were clear
- [ ] README instructions were confusing
- [ ] Missing information: 
- [ ] Suggestions for improvement: 

## Priority Level
<!-- How urgent is this for you? -->
- [ ] Blocking - Cannot proceed at all
- [ ] High - Major impediment to progress
- [ ] Medium - Can work around but would like to resolve
- [ ] Low - Nice to have working