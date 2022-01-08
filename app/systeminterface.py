import asyncio
import embeddedPy as ep
import json


def setWriteError(errStr):
    # print("Writing failed: ", errStr)
    ep.setWriteStatus(ep.EWriteStatus.FAILED)


def writeParameters(paramStr):
    if ep.getWriteStatus() == ep.EWriteStatus.REQUESTED or \
       ep.getWriteStatus() == ep.EWriteStatus.UPDATING:
        setWriteError("Write is currently busy")
        return

    ep.setWriteStatus(ep.EWriteStatus.REQUESTED)

    try:
        y = json.loads(paramStr)
    except json.decoder.JSONDecodeError:
        setWriteError("JSON Decode Error")
        return

    if "node_id" not in y or \
       "system_name" not in y or \
       "system_time" not in y or \
       "active" not in y:
        setWriteError("Elements missing from JSON object")
        return

    if type(y["node_id"]) is not int:
        setWriteError("node_id should be an int")
        return

    if type(y["system_name"]) is not str:
        setWriteError("system_name should be a str")
        return

    if type(y["system_time"]) is not int:
        setWriteError("system_time should be a int")
        return

    if type(y["active"]) is not bool:
        setWriteError("active should be a bool")
        return

    if y["node_id"] > 255 or y["node_id"] < 0:
        setWriteError("node_id out of range")
        return

    if y["system_time"] < 0:
        setWriteError("system_time out of range")
        return

    ep.setWriteStatus(ep.EWriteStatus.UPDATING)

    params = ep.SystemParameters()
    params.node_id = y["node_id"]
    params.system_name = y["system_name"]
    params.system_time = y["system_time"]
    params.active = y["active"]

    writeResult = ep.writeSystemParameters(params)

    if writeResult == ep.UpdateStatus.DONE:
        ep.setWriteStatus(ep.EWriteStatus.DONE)
    else:
        setWriteError("write operation to system failed")


def getStatus():
    s = json.dumps({"status": ep.getWriteStatus().value})
    return s
