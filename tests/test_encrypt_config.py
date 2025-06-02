"""
Tests for encrypt_config utility.

This module tests the encrypt_config command-line utility including:
- Secure master key generation
- Key display security
- Interactive prompts and warnings
- Configuration encryption workflows
"""

import io
import sys
from unittest.mock import patch, MagicMock
import pytest

from proxmox_mcp.utils.encrypt_config import generate_master_key


class TestSecureKeyGeneration:
    """Test cases for secure master key generation."""

    @patch("builtins.input")
    @patch("builtins.print")
    def test_generate_master_key_secure_workflow(self, mock_print, mock_input):
        """Test that master key generation follows secure workflow."""
        # Mock user pressing Enter twice (to confirm and after storing)
        mock_input.side_effect = ["", ""]

        # Call the function
        generate_master_key()

        # Verify security warnings were displayed
        printed_calls = [str(call) for call in mock_print.call_args_list]
        security_warnings = [
            call for call in printed_calls if "SECURITY WARNING" in call
        ]
        assert len(security_warnings) > 0, "Security warning should be displayed"

        # Verify key is displayed (may appear in export command too)
        key_displays = [
            call for call in printed_calls if "PROXMOX_MCP_MASTER_KEY=" in call
        ]
        assert len(key_displays) >= 1, "Key should be displayed at least once"

        # Verify history clearing instructions are provided
        history_instructions = [call for call in printed_calls if "history -c" in call]
        assert (
            len(history_instructions) > 0
        ), "History clearing instructions should be provided"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_generate_master_key_cancellation(self, mock_print, mock_input):
        """Test that key generation can be cancelled."""
        # Mock user pressing Ctrl+C
        mock_input.side_effect = KeyboardInterrupt()

        # Should exit gracefully
        with pytest.raises(SystemExit) as exc_info:
            generate_master_key()

        assert exc_info.value.code == 0  # Clean exit

        # Verify cancellation message was displayed
        printed_calls = [str(call) for call in mock_print.call_args_list]
        cancellation_messages = [call for call in printed_calls if "cancelled" in call]
        assert len(cancellation_messages) > 0

    @patch("builtins.input")
    @patch("builtins.print")
    def test_generate_master_key_prompts_for_confirmation(self, mock_print, mock_input):
        """Test that key generation requires user confirmation."""
        mock_input.side_effect = ["", ""]  # Two confirmations needed

        generate_master_key()

        # Should be called twice: once before showing key, once after
        assert mock_input.call_count == 2

        # First call should be for display confirmation
        first_call = mock_input.call_args_list[0]
        assert "Press ENTER to display" in first_call[0][0]

        # Second call should be for storage confirmation
        second_call = mock_input.call_args_list[1]
        assert "after you have safely stored" in second_call[0][0]

    @patch("builtins.input")
    @patch("builtins.print")
    def test_security_reminders_displayed(self, mock_print, mock_input):
        """Test that appropriate security reminders are displayed."""
        mock_input.side_effect = ["", ""]

        generate_master_key()

        printed_calls = [str(call) for call in mock_print.call_args_list]
        all_output = " ".join(printed_calls)

        # Check for key security reminders
        assert "Copy it immediately" in all_output
        assert "store it securely" in all_output
        assert "Anyone with this key can decrypt" in all_output
        assert "clearing your terminal history" in all_output
        assert "Losing this key means losing access" in all_output
