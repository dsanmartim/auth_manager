import unittest
from 2fa_manager.manager import OTPManager

class TestOTPManager(unittest.TestCase):
    def test_add_and_get_code(self):
        manager = OTPManager()
        uri = 'otpauth://totp/TestService?secret=JBSWY3DPEHPK3PXP'
        manager.add_service('TestService', uri)
        code = manager.get_code('TestService')
        self.assertTrue(code.isdigit())

if __name__ == '__main__':
    unittest.main()
