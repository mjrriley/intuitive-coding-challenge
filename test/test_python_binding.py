import unittest
import embeddedPy as ep


class ValidateBindingTestCase(unittest.TestCase):

    def test_read(self):
        parameters = ep.getSystemStatus()
        self.assertEqual(parameters.node_id, 255)
        self.assertEqual(parameters.system_name, "")
        self.assertEqual(parameters.system_time, 0)
        self.assertFalse(parameters.active)

    def test_write(self):
        parameters = ep.SystemParameters()
        parameters.node_id = 42
        parameters.system_name = "The System"
        writeResult = ep.writeSystemParameters(parameters)

        self.assertEqual(writeResult, ep.UpdateStatus.DONE)
        readResult = ep.getSystemStatus()
        self.assertEqual(parameters.node_id, readResult.node_id)
        self.assertEqual(parameters.system_name, readResult.system_name)

    def test_update_enum(self):
        self.assertEqual(ep.UpdateStatus.DONE, 0)
        self.assertEqual(ep.UpdateStatus.FAILED, 1)

    def test_write_status_enum(self):
        self.assertEqual(ep.EWriteStatus.NONE.value, 0)
        self.assertEqual(ep.EWriteStatus.REQUESTED.value, 1)
        self.assertEqual(ep.EWriteStatus.UPDATING.value, 2)
        self.assertEqual(ep.EWriteStatus.DONE.value, 3)
        self.assertEqual(ep.EWriteStatus.FAILED.value, 4)


if __name__ == '__main__':
    unittest.main()
