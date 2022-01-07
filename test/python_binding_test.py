import unittest
import embeddedPy
import app.application


class ValidateBindingTestCase(unittest.TestCase):

    def setUp(self):
        self.System = embeddedPy.getSystemInstance()

    def tearDown(self):
        self.System = None

    def test_no_constructor(self):
        with self.assertRaises(TypeError):
            embeddedPy.System()

    def test_read(self):
        parameters = self.System.read()
        self.assertEqual(parameters.node_id, 255)
        self.assertEqual(parameters.system_name, "")
        self.assertEqual(parameters.system_time, 0)
        self.assertFalse(parameters.active)

    def test_write(self):
        parameters = embeddedPy.SystemParameters()
        parameters.node_id = 42
        parameters.system_name = "The System"
        writeResult = self.System.write(parameters)

        self.assertEqual(writeResult, embeddedPy.UpdateStatus.DONE)
        readResult = self.System.read()
        self.assertEqual(parameters.node_id, readResult.node_id)
        self.assertEqual(parameters.system_name, readResult.system_name)

    def test_enum(self):
        self.assertEqual(embeddedPy.UpdateStatus.DONE, 0)
        self.assertEqual(embeddedPy.UpdateStatus.FAILED, 1)


if __name__ == '__main__':
    unittest.main()
