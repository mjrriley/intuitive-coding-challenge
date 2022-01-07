import asyncio
import embeddedPy
import enum
import json


class SystemStatus(enum.Enum):
    NONE = 0
    REQUESTED = 1
    UPDATING = 2
    DONE = 3
    FAILED = 4


class SystemInterface():

    def __init__(self):
        self.status = SystemStatus.NONE
        self.system = embeddedPy.getSystemInstance()
        self.lock = asyncio.Lock()

    async def sendParameters(self, paramStr):
        if self.status == SystemStatus.REQUESTED or \
           self.status == SystemStatus.UPDATING:
            return

        await self.__setStatus(SystemStatus.REQUESTED)

        try:
            y = json.loads(paramStr)
        except JSONDecodeError:
            await self.__setStatus(SystemStatus.FAILED)
            return

        if "node_id" not in y or \
            "system_name" not in y or \
            "system_time" not in y or \
            "active" not in y :
            await self.__setStatus(SystemStatus.FAILED)
            return

        if type(y["node_id"]) is not int:
            await self.__setStatus(SystemStatus.FAILED)
            return

        if type(y["system_name"]) is not str:
            await self.__setStatus(SystemStatus.FAILED)
            return

        if type(y["system_time"]) is not int:
            await self.__setStatus(SystemStatus.FAILED)
            return

        if type(y["active"]) is not bool:
            await self.__setStatus(SystemStatus.FAILED)
            return

        if y["node_id"] > 255 or y["node_id"] < 0:
            await self.__setStatus(SystemStatus.FAILED)
            return

        if y["system_time"] < 0:
            await self.__setStatus(SystemStatus.FAILED)
            return

        await self.__setStatus(SystemStatus.UPDATING)

        params = embeddedPy.SystemParameters()
        params.node_id = y["node_id"]
        params.system_name = y["system_name"]
        params.system_time = y["system_time"]
        params.active = y["active"]

        writeResult = self.system.write(params)
        if writeResult == embeddedPy.UpdateStatus.DONE:
            await self.__setStatus(SystemStatus.DONE)
        else:
            await self.__setStatus(SystemStatus.FAILED)

    async def getStatus(self):
        async with self.lock:
            s = json.dumps({"status": self.status.value})
        return s

    async def __setStatus(self, value):
        async with self.lock:
            self.status = value

async def main():
    pass

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        pass
    finally:
        loop.close()
