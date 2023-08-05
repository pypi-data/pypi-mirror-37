# -*- coding: utf-8 -*-

import unittest
from ..client import AcrosureClient

from .constants import TEST_SECRET_KEY

class ClientTestCase(unittest.TestCase):

    def setUp( self ):
        self.client = AcrosureClient(TEST_SECRET_KEY)

    def test_verify_webhook_signature( self ):
        is_valid = self.client.verify_signature(
            "1b0a6f0c0986671819cd19c38e201719b0531e72dfba312ca121190ea662a97b",
            "{\"data\":\"อโครชัว!\"}"
        )
        self.assertTrue(is_valid)

if __name__ == '__main__':
    unittest.main()
