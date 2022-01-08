import unittest
from app import systeminterface as si
import embeddedPy as ep
import json
import asyncio


class SystemInterfaceTestCase(unittest.TestCase):

    def setUp(self):
        self.jsonOut = json.dumps({
            "node_id": 42,
            "system_name": "robot",
            "system_time": 42,
            "active": True
        })

    def test_get_status(self):
        result = si.getStatus()
        self.assertEqual(result, json.dumps({"status": 0}))

    def test_write_success(self):
        ep.setWriteStatus(ep.EWriteStatus.NONE)
        self.assertEqual(si.getStatus(), json.dumps({"status": 0}))
        si.writeParameters(self.jsonOut)
        self.assertEqual(si.getStatus(), json.dumps({"status": 3}))

    def test_write_failures(self):
        # Fail when trying to write while updating or requesting
        ep.setWriteStatus(ep.EWriteStatus.UPDATING)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.UPDATING)
        si.writeParameters(self.jsonOut)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.FAILED)

        # Fail when json malformed
        ep.setWriteStatus(ep.EWriteStatus.NONE)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.NONE)
        si.writeParameters("}{")
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.FAILED)

        # Fail when element is missing
        ep.setWriteStatus(ep.EWriteStatus.NONE)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.NONE)
        self.jsonOut = json.dumps({
            "system_name": "robot",
            "system_time": 42,
            "active": True
        })
        si.writeParameters(self.jsonOut)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.FAILED)

        # Fail when node_id not int
        ep.setWriteStatus(ep.EWriteStatus.NONE)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.NONE)
        self.jsonOut = json.dumps({
            "node_id": 42.1,
            "system_name": "robot",
            "system_time": 42,
            "active": True
        })
        si.writeParameters(self.jsonOut)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.FAILED)

        # Fail when system_name not str
        ep.setWriteStatus(ep.EWriteStatus.NONE)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.NONE)
        self.jsonOut = json.dumps({
            "node_id": 42,
            "system_name": 42,
            "system_time": 42,
            "active": True
        })
        si.writeParameters(self.jsonOut)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.FAILED)

        # Fail when system_time not int
        ep.setWriteStatus(ep.EWriteStatus.NONE)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.NONE)
        self.jsonOut = json.dumps({
            "node_id": 42,
            "system_name": "robot",
            "system_time": 42.1,
            "active": True
        })
        si.writeParameters(self.jsonOut)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.FAILED)

        # Fail when active not bool
        ep.setWriteStatus(ep.EWriteStatus.NONE)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.NONE)
        self.jsonOut = json.dumps({
            "node_id": 42,
            "system_name": "robot",
            "system_time": 42,
            "active": "true"
        })
        si.writeParameters(self.jsonOut)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.FAILED)

        # Fail when node_id out of range
        ep.setWriteStatus(ep.EWriteStatus.NONE)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.NONE)
        self.jsonOut = json.dumps({
            "node_id": 256,
            "system_name": "robot",
            "system_time": 42,
            "active": True
        })
        si.writeParameters(self.jsonOut)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.FAILED)

        # Fail when system_time out of range
        ep.setWriteStatus(ep.EWriteStatus.NONE)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.NONE)
        self.jsonOut = json.dumps({
            "node_id": 42,
            "system_name": "robot",
            "system_time": -1,
            "active": True
        })
        si.writeParameters(self.jsonOut)
        self.assertEqual(ep.getWriteStatus(), ep.EWriteStatus.FAILED)


if __name__ == '__main__':
    unittest.main()
