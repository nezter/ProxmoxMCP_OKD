# 🔐 Token Encryption Guide

ProxmoxMCP now supports secure encryption of API tokens and other sensitive configuration values at rest.

## Features

- **Fernet Encryption**: Industry-standard AES 128 in CBC mode with HMAC SHA256 authentication
- **Secure Key Derivation**: PBKDF2 with salt to prevent rainbow table attacks
- **Environment-based Keys**: Master keys stored separately from encrypted data
- **Backward Compatibility**: Existing plain-text configurations continue to work
- **CLI Tools**: Easy-to-use command-line utilities for encryption management

## Quick Start

### 1. Generate a Master Key

```bash
# Generate a new master key securely
python -m src.proxmox_mcp.utils.encrypt_config --generate-key

# Follow the prompts to securely save the generated key
# Then set it as an environment variable:
export PROXMOX_MCP_MASTER_KEY="your-generated-key"
```

> **Security Note**: The key generation process now includes enhanced security measures that prevent the key from being exposed in terminal history or log files during automatic generation.

### 2. Encrypt Your Configuration

```bash
# Encrypt existing config
python -m src.proxmox_mcp.utils.encrypt_config proxmox-config/config.json

# This creates config.encrypted.json with encrypted token values
```

### 3. Use Encrypted Configuration

```bash
# Set environment variables
export PROXMOX_MCP_CONFIG="proxmox-config/config.encrypted.json"
export PROXMOX_MCP_MASTER_KEY="your-master-key"

# Run the server
python -m proxmox_mcp.server
```

## CLI Reference

### Encrypt Configuration File

```bash
# Basic encryption
python -m src.proxmox_mcp.utils.encrypt_config config.json

# Specify output file
python -m src.proxmox_mcp.utils.encrypt_config config.json -o encrypted.json
```

### Check Encryption Status

```bash
python -m src.proxmox_mcp.utils.encrypt_config config.json --status
```

### Generate Master Key

```bash
# Generate a new master key with security prompts
python -m src.proxmox_mcp.utils.encrypt_config --generate-key

# The tool will display the key once and prompt you to save it securely
# No key exposure in logs or terminal history during automatic generation
```

## Configuration Format

### Before Encryption
```json
{
  "auth": {
    "user": "root@pam",
    "token_name": "my-token",
    "token_value": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
  }
}
```

### After Encryption
```json
{
  "auth": {
    "user": "root@pam",
    "token_name": "my-token", 
    "token_value": "enc:Z0FBQUFBQm9QYjUz..."
  }
}
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PROXMOX_MCP_MASTER_KEY` | Master encryption key | Yes (for encrypted configs) |
| `PROXMOX_MCP_CONFIG` | Path to config file | Yes |

## Security Best Practices

1. **Store Keys Separately**: Never store the master key in the same location as encrypted data
2. **Use Environment Variables**: Avoid hardcoding keys in scripts or configuration files
3. **Rotate Keys Regularly**: Generate new master keys periodically and re-encrypt configurations
4. **Secure Key Storage**: Use secure key management systems in production environments
5. **Backup Safely**: Ensure encrypted backups include both data and key recovery procedures
6. **Clear Terminal History**: After key generation, consider clearing terminal history to prevent exposure
7. **Use CLI Tool**: Always use the provided CLI tool for key generation rather than manual methods

## Migration from Plain Text

Existing configurations work without changes. To migrate:

1. **Backup Current Config**: Always backup your working configuration
2. **Generate Master Key**: Create and securely store a master key
3. **Encrypt Configuration**: Use the CLI tool to encrypt sensitive values
4. **Update Environment**: Set the master key environment variable
5. **Test Thoroughly**: Verify the server starts and connects successfully
6. **Clean Up**: Securely delete plain text configuration files

## Troubleshooting

### Common Issues

**"Token decryption failed"**
- Verify `PROXMOX_MCP_MASTER_KEY` environment variable is set correctly
- Ensure the master key matches the one used for encryption

**"Config file not found"**
- Check `PROXMOX_MCP_CONFIG` environment variable points to correct file
- Verify file permissions and path accessibility

**"Invalid encrypted token format"**
- Encrypted tokens must start with `enc:` prefix
- Verify file wasn't corrupted during transfer or storage

### Debug Mode

Enable debug logging to troubleshoot encryption issues:

```bash
# Add to your config.json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

## Integration Examples

### Docker Compose

```yaml
services:
  proxmox-mcp:
    environment:
      - PROXMOX_MCP_CONFIG=/app/config/config.encrypted.json
      - PROXMOX_MCP_MASTER_KEY=${MASTER_KEY}
    volumes:
      - ./config:/app/config
```

### Systemd Service

```ini
[Service]
Environment=PROXMOX_MCP_CONFIG=/etc/proxmox-mcp/config.encrypted.json
Environment=PROXMOX_MCP_MASTER_KEY=your-master-key
ExecStart=/usr/bin/python -m proxmox_mcp.server
```

For more information, see the main [README.md](../README.md) or [security documentation](./security.md).
