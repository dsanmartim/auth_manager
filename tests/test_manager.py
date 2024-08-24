import os
import unittest
from unittest.mock import Mock, patch

import pyotp

from auth_manager.manager import OTPManager


class TestOTPManager(unittest.TestCase):
    def setUp(self):
        """Set up a fresh OTPManager instance using a test-specific JSON file."""
        self.test_file = os.path.join(
            os.path.dirname(__file__), "../data/test_services.json"
        )
        self.manager = OTPManager(data_file=self.test_file)
        self.test_uri = "otpauth://totp/TestService?secret=JBSWY3DPEHPK3PXP"
        self.manager.add_service("TestService", self.test_uri)

    def tearDown(self):
        """Clean up the test JSON file after each test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_service(self):
        """Test adding a new service and verifying its existence."""
        self.manager.add_service("NewService", self.test_uri)
        self.assertIn("NewService", self.manager.services)
        self.assertEqual(self.manager.services["NewService"], self.test_uri)

    def test_get_code(self):
        """Test generating a code for an existing service."""
        code = self.manager.get_code("TestService")
        self.assertTrue(code.isdigit())
        self.assertEqual(len(code), 6)  # OTP codes are typically 6 digits long

    def test_edit_service(self):
        """Test editing an existing service's name and URI."""
        new_uri = "otpauth://totp/UpdatedService?secret=JBSWY3DPEHPK3PXP"
        self.manager.edit_service("TestService", "UpdatedService", new_uri)
        self.assertNotIn("TestService", self.manager.services)
        self.assertIn("UpdatedService", self.manager.services)
        self.assertEqual(self.manager.services["UpdatedService"], new_uri)

    def test_delete_service(self):
        """Test deleting an existing service."""
        self.manager.delete_service("TestService")
        self.assertNotIn("TestService", self.manager.services)

    def test_get_code_for_non_existent_service(self):
        """Test generating a code for a non-existent service."""
        code = self.manager.get_code("NonExistentService")
        self.assertIsNone(code)

    def test_edit_non_existent_service(self):
        """Test editing a non-existent service (should not raise an error)."""
        new_uri = "otpauth://totp/NonExistentService?secret=JBSWY3DPEHPK3PXP"
        self.manager.edit_service("NonExistentService", "UpdatedService", new_uri)
        self.assertIn("UpdatedService", self.manager.services)
        self.assertEqual(self.manager.services["UpdatedService"], new_uri)

    def test_delete_non_existent_service(self):
        """Test deleting a non-existent service (should not raise an error)."""
        self.manager.delete_service("NonExistentService")
        # Deleting a non-existent service should simply do nothing
        self.assertNotIn("NonExistentService", self.manager.services)

    @patch("auth_manager.manager.pyotp.TOTP")
    def test_code_generation_timing(self, mock_totp):
        """Test that the code generation uses the correct timing intervals."""
        # Mock TOTP instance and method
        mock_totp_instance = Mock()
        mock_totp.return_value = mock_totp_instance
        mock_totp_instance.now.return_value = "123456"

        # Generate code and check if the mocked code is returned
        code = self.manager.get_code("TestService")
        mock_totp_instance.now.assert_called_once()
        self.assertEqual(code, "123456")


if __name__ == "__main__":
    unittest.main()
