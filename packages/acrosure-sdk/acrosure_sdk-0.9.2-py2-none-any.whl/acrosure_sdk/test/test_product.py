# -*- coding: utf-8 -*-

import unittest
from ..client import AcrosureClient
from ..product import ProductManager

from .constants import (
    TEST_PUBLIC_KEY,
)

class ProductTestCase(unittest.TestCase):

    PRODUCTS = []

    def setUp( self ):
        self.client = AcrosureClient(TEST_PUBLIC_KEY)
        self.product = self.client.product
    
    def test_1_instance_of_acrosure( self ):
        client = self.client
        product = self.product
        self.assertIsInstance(client, AcrosureClient)
        self.assertIsInstance(product, ProductManager)

    def test_2_list_products( self ):
        product = self.product
        resp = product.list()
        self.assertEqual(resp["status"], "ok")
        products = resp["data"]
        self.assertIsInstance(products, list)
        self.assertTrue(len(products) > 0)
        self.__class__.PRODUCTS = products
        
    def test_3_get_product_detail( self ):
        product = self.product
        product_id = self.__class__.PRODUCTS[0]["id"]
        resp = product.get(product_id)
        self.assertEqual(resp["status"], "ok")
        product_detail = resp["data"]
        self.assertIsInstance(product_detail, dict)
        self.assertEqual(product_detail["id"], product_id)

if __name__ == '__main__':
    unittest.main()
