from eapy_python_sdk import Eapy

import unittest

class TestPythonSDK(unittest.TestCase):


    def setUp(self):
        self.eapy = Eapy(environment="http://127.0.0.1:5000")
        self.eapy.connect("admin@eapy.eu", "eapy2017")

        self.TEST_REPOSITORY = 23

    def tearDown(self):
        self.eapy.remove_object(self.TEST_REPOSITORY, "Teste", "TestObject")
        self.eapy.remove_object(self.TEST_REPOSITORY, "Teste", "Change name")

    def testAddUpdateRemoveObject(self):
        data = {
            "name": "TestObject",
            "key": "TestObject"
        }
        result = self.eapy.add_edit_object(self.TEST_REPOSITORY, "Teste", data)

        self.assertEquals(result["status_code"], 200)
        self.assertIsNotNone(result["results"]["id"])

        data2 = {
            "id": result["results"]["id"],
            "name": "Change name",
            "key": "TestObject"
        }

        result2 = self.eapy.add_edit_object(self.TEST_REPOSITORY, "Teste", data2)

        self.assertEquals(result2["status_code"], 200)
        self.assertEquals(result["results"]["id"], result2["results"]["id"])
        self.assertEquals(result2["results"]["name"], "Change name")

        result3 = self.eapy.remove_object(self.TEST_REPOSITORY, "Teste", "Change name")
        self.assertEquals(result3["status_code"], 200)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPythonSDK)
    unittest.TextTestRunner().run(suite)
