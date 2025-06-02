"""
Tests for token encryption utilities.

This module tests the TokenEncryption class functionality including:
- Token encryption and decryption
- Unique salt generation per encryption
- Backward compatibility with old format
- Error handling and validation
- Master key generation and management
"""

import os
import pytest
import base64
from unittest.mock import patch, mock_open
from proxmox_mcp.utils.encryption import TokenEncryption, encrypt_sensitive_value, decrypt_sensitive_value


class TestTokenEncryption:
    """Test cases for TokenEncryption class."""

    def test_init_with_master_key(self):
        """Test initialization with provided master key."""
        master_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=master_key)
        assert encryptor._master_key == master_key

    @patch.dict(os.environ, {"PROXMOX_MCP_MASTER_KEY": "test_key_from_env"})
    def test_init_with_env_key(self):
        """Test initialization with key from environment variable."""
        encryptor = TokenEncryption()
        assert encryptor._master_key == "test_key_from_env"

    @patch.dict(os.environ, {}, clear=True)
    @patch("builtins.print")
    def test_init_generates_new_key_when_no_env(self, mock_print):
        """Test that a new key is generated when no environment variable is set."""
        encryptor = TokenEncryption()
        assert encryptor._master_key is not None
        assert len(encryptor._master_key) > 0
        # Verify warning was printed but key was NOT exposed
        assert mock_print.called
        
        # Check that no call to print contains the actual master key
        for call_args in mock_print.call_args_list:
            printed_text = str(call_args[0][0]) if call_args[0] else ""
            # The master key should not appear in any print statement
            assert encryptor._master_key not in printed_text
        
        # Verify security messaging is included
        printed_messages = [str(call[0][0]) for call in mock_print.call_args_list if call[0]]
        security_message_found = any("SECURITY" in msg or "security" in msg for msg in printed_messages)
        assert security_message_found, "Security warning should be displayed"

    def test_encrypt_decrypt_roundtrip_new_format(self):
        """Test that encryption and decryption work correctly with new format."""
        master_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=master_key)
        
        original_token = "test-api-token-12345"
        encrypted_token = encryptor.encrypt_token(original_token)
        decrypted_token = encryptor.decrypt_token(encrypted_token)
        
        assert decrypted_token == original_token
        assert encrypted_token.startswith("enc:")
        # New format should have salt and encrypted data separated by colons
        assert encrypted_token.count(":") == 2

    def test_unique_salts_for_same_token(self):
        """Test that encrypting the same token twice generates different salts."""
        master_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=master_key)
        
        token = "test-token"
        encrypted1 = encryptor.encrypt_token(token)
        encrypted2 = encryptor.encrypt_token(token)
        
        # Both should decrypt to the same value
        assert encryptor.decrypt_token(encrypted1) == token
        assert encryptor.decrypt_token(encrypted2) == token
        
        # But should have different encrypted representations (due to unique salts)
        assert encrypted1 != encrypted2
        
        # Extract salts and verify they're different
        salt1 = encrypted1.split(":")[1]
        salt2 = encrypted2.split(":")[1]
        assert salt1 != salt2

    def test_backward_compatibility_old_format(self):
        """Test that old format tokens (without salt) can still be decrypted."""
        master_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=master_key)
        
        # Simulate an old format encrypted token (using static salt)
        original_token = "legacy-token"
        
        # Create cipher with static salt (old behavior)
        cipher = encryptor._create_cipher()  # No salt provided, uses static salt
        encrypted_bytes = cipher.encrypt(original_token.encode())
        encrypted_b64 = base64.urlsafe_b64encode(encrypted_bytes).decode()
        old_format_token = f"enc:{encrypted_b64}"
        
        # Should be able to decrypt old format
        decrypted_token = encryptor.decrypt_token(old_format_token)
        assert decrypted_token == original_token

    def test_decrypt_plain_text_token(self):
        """Test that plain text tokens (without enc: prefix) are returned as-is."""
        encryptor = TokenEncryption()
        plain_token = "plain-text-token"
        result = encryptor.decrypt_token(plain_token)
        assert result == plain_token

    def test_is_encrypted(self):
        """Test the is_encrypted method."""
        encryptor = TokenEncryption()
        
        # Test plain text token
        assert not encryptor.is_encrypted("plain-token")
        
        # Test encrypted token
        encrypted = encryptor.encrypt_token("test-token")
        assert encryptor.is_encrypted(encrypted)

    def test_migrate_plain_token(self):
        """Test migrating plain text token to encrypted format."""
        encryptor = TokenEncryption()
        
        plain_token = "plain-token"
        migrated_token = encryptor.migrate_plain_token(plain_token)
        
        # Should be encrypted
        assert migrated_token.startswith("enc:")
        assert encryptor.is_encrypted(migrated_token)
        
        # Should decrypt to original value
        assert encryptor.decrypt_token(migrated_token) == plain_token
        
        # Migrating already encrypted token should return it unchanged
        migrated_again = encryptor.migrate_plain_token(migrated_token)
        assert migrated_again == migrated_token

    def test_invalid_master_key(self):
        """Test that invalid master keys raise appropriate errors."""
        with pytest.raises(ValueError, match="Invalid master key"):
            TokenEncryption(master_key="invalid-key")

    def test_invalid_encrypted_token_format(self):
        """Test that invalid encrypted token formats raise appropriate errors."""
        encryptor = TokenEncryption()
        
        # Invalid format (too many colons)
        with pytest.raises(ValueError, match="Failed to decrypt token"):
            encryptor.decrypt_token("enc:part1:part2:part3:extra")
        
        # Invalid base64
        with pytest.raises(ValueError, match="Failed to decrypt token"):
            encryptor.decrypt_token("enc:invalid_base64:invalid_base64")

    def test_generate_master_key(self):
        """Test master key generation."""
        key1 = TokenEncryption.generate_master_key()
        key2 = TokenEncryption.generate_master_key()
        
        # Keys should be different
        assert key1 != key2
        
        # Keys should be valid base64
        assert base64.urlsafe_b64decode(key1.encode())
        assert base64.urlsafe_b64decode(key2.encode())

    def test_different_encryptors_same_master_key(self):
        """Test that different encryptor instances with same master key can decrypt each other's tokens."""
        master_key = TokenEncryption.generate_master_key()
        
        encryptor1 = TokenEncryption(master_key=master_key)
        encryptor2 = TokenEncryption(master_key=master_key)
        
        token = "shared-token"
        encrypted_by_1 = encryptor1.encrypt_token(token)
        decrypted_by_2 = encryptor2.decrypt_token(encrypted_by_1)
        
        assert decrypted_by_2 == token


class TestConvenienceFunctions:
    """Test cases for convenience functions."""

    def test_encrypt_sensitive_value(self):
        """Test encrypt_sensitive_value convenience function."""
        value = "sensitive-value"
        encrypted = encrypt_sensitive_value(value)
        
        assert encrypted.startswith("enc:")
        assert encrypted.count(":") == 2  # New format

    def test_decrypt_sensitive_value(self):
        """Test decrypt_sensitive_value convenience function."""
        value = "sensitive-value"
        encrypted = encrypt_sensitive_value(value)
        decrypted = decrypt_sensitive_value(encrypted)
        
        assert decrypted == value

    def test_convenience_functions_with_custom_encryptor(self):
        """Test convenience functions with custom encryptor."""
        master_key = TokenEncryption.generate_master_key()
        encryptor = TokenEncryption(master_key=master_key)
        
        value = "test-value"
        encrypted = encrypt_sensitive_value(value, encryptor)
        decrypted = decrypt_sensitive_value(encrypted, encryptor)
        
        assert decrypted == value


class TestSecureKeyGeneration:
    """Test cases for secure key generation features."""

    @patch.dict(os.environ, {}, clear=True)
    @patch("builtins.print")
    def test_secure_key_generation_no_key_exposure(self, mock_print):
        """Test that master key is not exposed in console output during generation."""
        encryptor = TokenEncryption()
        master_key = encryptor._master_key
        
        # Verify key was generated and works
        assert master_key is not None
        assert len(master_key) > 0
        
        # Verify the key can be used for encryption/decryption
        test_token = "test-token-value"
        encrypted = encryptor.encrypt_token(test_token)
        decrypted = encryptor.decrypt_token(encrypted)
        assert decrypted == test_token
        
        # Verify security warnings are present but key is not exposed
        printed_messages = [str(call[0][0]) for call in mock_print.call_args_list if call[0]]
        
        # Should contain security messaging
        has_security_warning = any("SECURITY" in msg or "security" in msg for msg in printed_messages)
        assert has_security_warning, "Should contain security warnings"
        
        # Should contain instructions for setting environment variable
        has_env_instruction = any("environment variable" in msg.lower() for msg in printed_messages)
        assert has_env_instruction, "Should contain environment variable instructions"
        
        # Should NOT contain the actual master key value
        key_exposed = any(master_key in msg for msg in printed_messages)
        assert not key_exposed, f"Master key should not be exposed in console output"

    @patch.dict(os.environ, {"PROXMOX_MCP_MASTER_KEY": "existing_key"})
    @patch("builtins.print")
    def test_existing_key_no_generation_warning(self, mock_print):
        """Test that no generation warning is shown when key exists in environment."""
        encryptor = TokenEncryption()
        assert encryptor._master_key == "existing_key"
        
        # Should not have printed any warning messages
        assert not mock_print.called, "Should not print warnings when key exists"

    def test_generated_key_format_and_security(self):
        """Test that generated keys have proper format and security properties."""
        key1 = TokenEncryption.generate_master_key()
        key2 = TokenEncryption.generate_master_key()
        
        # Keys should be different (randomness)
        assert key1 != key2
        
        # Keys should be valid base64
        base64.urlsafe_b64decode(key1.encode())
        base64.urlsafe_b64decode(key2.encode())
        
        # Keys should be appropriate length (32 bytes = 43-44 chars base64)
        assert 40 <= len(key1) <= 50
        assert 40 <= len(key2) <= 50