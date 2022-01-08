import asyncio
from app import systeminterface as si


class Client:

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.statusQueue = asyncio.Queue()
        self.writeQueue = asyncio.Queue()
        asyncio.run(self.run_client())

    async def handleStatusRequestQueue(self):
        while True:
            writer = await self.statusQueue.get()
            i = si.getStatus()
            print("Client SEND: ", i)
            writer.write(i.encode())

    async def handleWriteQueue(self):
        loop = asyncio.get_event_loop()
        while True:
            jsonMsg = await self.writeQueue.get()
            loop.run_in_executor(None, si.writeParameters, jsonMsg)

    async def handleServerInput(self, reader, writer):
        while not writer.is_closing():
            data = await reader.read(1024)
            dataStr = data.decode()
            if "{}" == dataStr:
                print("Client RECV: ", dataStr)
                await self.statusQueue.put(writer)
            elif data:
                print("Client RECV: ", dataStr)
                await self.writeQueue.put(dataStr)

    async def run_client(self):
        loop = asyncio.get_event_loop()

        self.statusQueue = asyncio.Queue()
        self.writeQueue = asyncio.Queue()

        try:
            reader, writer = await asyncio.open_connection(
                    self.address, self.port)
        except Exception as e:
            print(e)
            return

        await asyncio.gather(
            self.handleStatusRequestQueue(),
            self.handleWriteQueue(),
            self.handleServerInput(reader, writer)
        )


if __name__ == '__main__':
    Client('localhost', 8888)
