import unittest
import app.application as a
import json
import asyncio


class ApplicationTestCase(unittest.TestCase):

    def test_enum(self):
        self.assertEqual(a.SystemStatus.NONE.value, 0)
        self.assertEqual(a.SystemStatus.REQUESTED.value, 1)
        self.assertEqual(a.SystemStatus.UPDATING.value, 2)
        self.assertEqual(a.SystemStatus.DONE.value, 3)
        self.assertEqual(a.SystemStatus.FAILED.value, 4)

    def test_send(self):
        si = a.SystemInterface()
        self.assertEqual(si.getStatus(), json.dumps({"status":0}))
        jsonOut = json.dumps({"node_id": 42, "system_name": "robot", "system_time": 42, "active": True})
        asyncio.run(si.sendParameters(jsonOut))
        self.assertEqual(si.getStatus(), json.dumps({"status":3}))

if __name__ == '__main__':
    unittest.main()
