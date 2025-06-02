#!/usr/bin/env python3
"""
Configuration encryption utility for Proxmox MCP.

This script provides a command-line interface for encrypting sensitive
values in Proxmox MCP configuration files. It helps users migrate from
plain-text tokens to encrypted tokens for enhanced security.

Usage:
    python -m proxmox_mcp.utils.encrypt_config [config_file] [options]

Examples:
    # Encrypt tokens in existing config
    python -m proxmox_mcp.utils.encrypt_config proxmox-config/config.json
    
    # Encrypt and save to specific file
    python -m proxmox_mcp.utils.encrypt_config config.json -o config.encrypted.json
    
    # Generate a new master key
    python -m proxmox_mcp.utils.encrypt_config --generate-key
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from proxmox_mcp.utils.encryption import TokenEncryption
from proxmox_mcp.config.loader import encrypt_config_file


def generate_master_key() -> None:
    """Generate and display a new master key."""
    key = TokenEncryption.generate_master_key()
    print("🔑 Generated new master key:")
    print(f"   PROXMOX_MCP_MASTER_KEY={key}")
    print()
    print("📋 To use this key:")
    print("   1. Set the environment variable in your shell:")
    print(f"      export PROXMOX_MCP_MASTER_KEY={key}")
    print("   2. Or add it to your .env file")
    print("   3. Store this key securely - you'll need it to decrypt your config!")
    print()
    print("⚠️  WARNING: Losing this key means losing access to encrypted tokens!")


def encrypt_config(config_path: str, output_path: Optional[str] = None) -> None:
    """Encrypt sensitive values in a configuration file."""
    try:
        # Check if config file exists
        if not os.path.exists(config_path):
            print(f"❌ Error: Configuration file not found: {config_path}")
            sys.exit(1)

        # Encrypt the configuration
        encrypted_path = encrypt_config_file(config_path, output_path)

        print()
        print("🔒 Configuration encrypted successfully!")
        print(f"   Original: {config_path}")
        print(f"   Encrypted: {encrypted_path}")
        print()
        print("📝 Next steps:")
        print("   1. Verify the encrypted config works:")
        print(
            f"      PROXMOX_MCP_CONFIG={encrypted_path} python -m proxmox_mcp.server --test"
        )
        print("   2. Update your environment to use the encrypted config")
        print("   3. Securely delete the original plain-text config if desired")

    except Exception as e:
        print(f"❌ Error encrypting configuration: {e}")
        sys.exit(1)


def show_encryption_status(config_path: str) -> None:
    """Show the encryption status of a configuration file."""
    try:
        if not os.path.exists(config_path):
            print(f"❌ Error: Configuration file not found: {config_path}")
            sys.exit(1)

        with open(config_path) as f:
            config_data = json.load(f)

        print(f"📄 Configuration file: {config_path}")
        print()

        # Check token encryption status
        if "auth" in config_data and "token_value" in config_data["auth"]:
            token_value = config_data["auth"]["token_value"]
            if isinstance(token_value, str) and token_value.startswith("enc:"):
                print("🔒 Token value: ENCRYPTED ✅")
            else:
                print("🔓 Token value: PLAIN TEXT ⚠️")
        else:
            print("❓ Token value: NOT FOUND")

        print()

        # Check for master key
        master_key = os.getenv("PROXMOX_MCP_MASTER_KEY")
        if master_key:
            print("🔑 Master key: SET ✅")
        else:
            print("🔑 Master key: NOT SET ⚠️")
            print("   Set PROXMOX_MCP_MASTER_KEY environment variable")

    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        sys.exit(1)


def main():
    """Main command-line interface."""
    parser = argparse.ArgumentParser(
        description="Encrypt sensitive values in Proxmox MCP configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s config.json                    # Encrypt config.json
  %(prog)s config.json -o encrypted.json  # Encrypt to specific file
  %(prog)s --generate-key                 # Generate new master key
  %(prog)s config.json --status           # Show encryption status
        """,
    )

    parser.add_argument(
        "config_file", nargs="?", help="Path to configuration file to encrypt"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output path for encrypted configuration (default: [config].encrypted.json)",
    )

    parser.add_argument(
        "--generate-key",
        action="store_true",
        help="Generate a new master key for encryption",
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show encryption status of configuration file",
    )

    args = parser.parse_args()

    # Handle generate key command
    if args.generate_key:
        generate_master_key()
        return

    # Require config file for other operations
    if not args.config_file:
        parser.error("Configuration file required (or use --generate-key)")

    # Handle status command
    if args.status:
        show_encryption_status(args.config_file)
        return

    # Handle encryption
    encrypt_config(args.config_file, args.output)


if __name__ == "__main__":
    main()
