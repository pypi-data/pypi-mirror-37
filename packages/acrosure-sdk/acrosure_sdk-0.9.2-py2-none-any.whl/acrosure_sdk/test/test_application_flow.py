# -*- coding: utf-8 -*-

import unittest
from ..client import AcrosureClient
from ..application import ApplicationManager

from .constants import (
    TEST_PUBLIC_KEY,
    TEST_SECRET_KEY,
    CONFIRM_APP_DATA,
)

class ApplicationFlowTestCase(unittest.TestCase):

    APP_ID = ""
    PACKAGES = []

    def setUp( self ):
        self.client = AcrosureClient(TEST_PUBLIC_KEY)
        self.application = self.client.application
    
    def test_1_instance_of_acrosure( self ):
        client = self.client
        application = self.application
        self.assertIsInstance(client, AcrosureClient)
        self.assertIsInstance(application, ApplicationManager)
    
    def test_2_create_with_empty_data( self ):
        application = self.application
        resp = application.create(CONFIRM_APP_DATA["product_id"])
        self.assertEqual(resp["status"], "ok")
        created_application = resp["data"]
        self.assertTrue(created_application)
        self.assertTrue(created_application["id"])
        self.assertEqual(created_application["status"], "INITIAL")
        self.__class__.APP_ID = created_application["id"]

    def test_3_get_application( self ):
        application = self.application
        resp = application.get(self.__class__.APP_ID)
        self.assertEqual(resp["status"], "ok")
        got_application = resp["data"]
        self.assertTrue(got_application)
        self.assertTrue(got_application["id"])
        self.assertEqual(got_application["id"], self.__class__.APP_ID)
    
    def test_4_update_application( self ):
        application = self.application
        resp = application.update( self.__class__.APP_ID, basic_data = CONFIRM_APP_DATA["basic_data"])
        self.assertEqual(resp["status"], "ok")
        updated_application = resp["data"]
        self.assertTrue(updated_application)
        self.assertTrue(updated_application["id"])
        self.assertEqual(updated_application["status"], "PACKAGE_REQUIRED")

    def test_5_get_packages( self ):
        application = self.application
        resp = application.get_packages(self.__class__.APP_ID)
        self.assertEqual(resp["status"], "ok")
        self.__class__.PACKAGES = resp["data"]
        self.assertIsInstance(self.__class__.PACKAGES, list)
        self.assertTrue(len(self.__class__.PACKAGES) > 0)
    
    def test_6_select_package( self ):
        application = self.application
        first_package = self.__class__.PACKAGES[0]
        resp = application.select_package(
            application_id = self.__class__.APP_ID,
            package_code = first_package["package_code"]
        )
        self.assertEqual(resp["status"], "ok")
        updated_application = resp["data"]
        self.assertEqual(updated_application["status"], "DATA_REQUIRED")
    
    def test_7_get_current_package( self ):
        application = self.application
        resp = application.get_package(self.__class__.APP_ID)
        self.assertEqual(resp["status"], "ok")
        current_package = resp["data"]
        self.assertIsInstance(current_package, dict)

    def test_8_update_application_with_completed_data( self ):
        application = self.application
        resp = application.update(
            self.__class__.APP_ID,
            basic_data = CONFIRM_APP_DATA["basic_data"],
            package_options = CONFIRM_APP_DATA["package_options"],
            additional_data = CONFIRM_APP_DATA["additional_data"]
        ) 
        self.assertEqual(resp["status"], "ok")
        updated_application = resp["data"]
        self.assertTrue(updated_application)
        self.assertTrue(updated_application["id"])
        self.assertEqual(updated_application["status"], "READY")
    
    def test_9_confirm_application( self ):
        admin_client = AcrosureClient(
            token = TEST_SECRET_KEY,
        )
        application = admin_client.application
        resp = application.confirm(self.__class__.APP_ID)
        confirmed_application = resp["data"]
        self.assertTrue(confirmed_application)
        self.assertTrue(confirmed_application["id"])
        self.assertEqual(confirmed_application["status"], "CONFIRMING")

if __name__ == '__main__':
    unittest.main()
