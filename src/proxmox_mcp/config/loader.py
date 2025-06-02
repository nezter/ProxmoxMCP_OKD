"""
Configuration loading utilities for the Proxmox MCP server.

This module handles loading and validation of server configuration:
- JSON configuration file loading
- Environment variable handling
- Configuration validation using Pydantic models
- Token encryption/decryption for secure storage
- Error handling for invalid configurations

The module ensures that all required configuration is present
and valid before the server starts operation. Sensitive values
like API tokens can be stored encrypted in the configuration file.
"""

import json
import os
from typing import Optional
from .models import Config
from ..utils.encryption import TokenEncryption


def load_config(config_path: Optional[str] = None) -> Config:
    """Load and validate configuration from JSON file.

    Performs the following steps:
    1. Verifies config path is provided (from parameter or environment)
    2. Loads JSON configuration file
    3. Decrypts any encrypted tokens (if encryption is enabled)
    4. Validates required fields are present
    5. Converts to typed Config object using Pydantic

    Configuration must include:
    - Proxmox connection settings (host, port, etc.)
    - Authentication credentials (user, token)
    - Logging configuration

    Token encryption is supported by prefixing encrypted values with 'enc:'.
    The master key must be provided via PROXMOX_MCP_MASTER_KEY environment variable.

    Args:
        config_path: Path to the JSON configuration file
                    If not provided, attempts to get from PROXMOX_MCP_CONFIG environment variable

    Returns:
        Config object containing validated configuration with decrypted tokens:
        {
            "proxmox": {
                "host": "proxmox-host",
                "port": 8006,
                ...
            },
            "auth": {
                "user": "username",
                "token_name": "token-name",
                "token_value": "decrypted-token-value",  # Automatically decrypted
                ...
            },
            "logging": {
                "level": "INFO",
                ...
            }
        }

    Raises:
        ValueError: If:
                 - Config path is not provided and environment variable not set
                 - JSON is invalid
                 - Required fields are missing
                 - Field values are invalid
                 - Token decryption fails
    """
    if not config_path:
        config_path = os.environ.get("PROXMOX_MCP_CONFIG")
        if not config_path:
            raise ValueError("Config path must be provided either as parameter or via PROXMOX_MCP_CONFIG environment variable")

    try:
        with open(config_path) as f:
            config_data = json.load(f)
            if not config_data.get("proxmox", {}).get("host"):
                raise ValueError("Proxmox host cannot be empty")

            # Decrypt sensitive values if they are encrypted
            config_data = _decrypt_config_tokens(config_data)

            return Config(**config_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")
    except Exception as e:
        raise ValueError(f"Failed to load config: {e}")


def _decrypt_config_tokens(config_data: dict) -> dict:
    """Decrypt encrypted tokens in configuration data.

    Searches for encrypted values (prefixed with 'enc:') and decrypts them
    using the TokenEncryption utility. Handles backward compatibility
    with plain text tokens.

    Args:
        config_data: Raw configuration dictionary from JSON

    Returns:
        Configuration dictionary with decrypted tokens

    Raises:
        ValueError: If token decryption fails
    """
    try:
        # Only initialize encryption if we find encrypted values
        encryptor = None

        # Check and decrypt auth.token_value if encrypted
        if "auth" in config_data and "token_value" in config_data["auth"]:
            token_value = config_data["auth"]["token_value"]
            if isinstance(token_value, str) and token_value.startswith("enc:"):
                if encryptor is None:
                    encryptor = TokenEncryption()
                config_data["auth"]["token_value"] = encryptor.decrypt_token(
                    token_value
                )

        # Future: Add support for other encrypted fields here
        # e.g., database passwords, API keys, etc.

        return config_data
    except Exception as e:
        raise ValueError(f"Failed to decrypt configuration tokens: {e}")


def encrypt_config_file(config_path: str, output_path: Optional[str] = None) -> str:
    """Encrypt sensitive values in a configuration file.

    Utility function to migrate existing plain-text configuration files
    to use encrypted tokens. Creates a new configuration file with
    encrypted sensitive values.

    Args:
        config_path: Path to existing configuration file
        output_path: Optional path for encrypted config. If not provided,
                    creates a .encrypted version of the original file

    Returns:
        Path to the encrypted configuration file

    Raises:
        ValueError: If encryption fails or config is invalid
    """
    if output_path is None:
        base_path = config_path.rsplit(".", 1)[0]
        output_path = f"{base_path}.encrypted.json"

    try:
        # Load the original config
        with open(config_path) as f:
            config_data = json.load(f)

        # Initialize encryptor
        encryptor = TokenEncryption()

        # Encrypt sensitive values
        if "auth" in config_data and "token_value" in config_data["auth"]:
            token_value = config_data["auth"]["token_value"]
            if isinstance(token_value, str) and not encryptor.is_encrypted(token_value):
                config_data["auth"]["token_value"] = encryptor.encrypt_token(
                    token_value
                )

        # Write encrypted config
        with open(output_path, "w") as f:
            json.dump(config_data, f, indent=4)

        print(f"✅ Encrypted configuration saved to: {output_path}")
        print(f"🔑 Make sure to set PROXMOX_MCP_MASTER_KEY environment variable")

        return output_path
    except Exception as e:
        raise ValueError(f"Failed to encrypt configuration file: {e}")
