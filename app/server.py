import asyncio
import json


class Server:

    def __init__(self, address, port):
        self.address = address
        self.port = port
        asyncio.run(self.run_server())

    async def handle_client(self, reader, writer):
        print('Client connected')
        jsonOut = json.dumps({
            "node_id": 42,
            "system_name": "robot",
            "system_time": 42,
            "active": True
        })
        jsonEncode = jsonOut.encode()

        while True:
            print("Server SEND: ", jsonOut)
            writer.write(jsonEncode)
            await writer.drain()
            await asyncio.sleep(0.1)

            for i in range(20):
                sendData = "{}"
                print("Server SEND: ", sendData)
                writer.write(sendData.encode())
                await writer.drain()
                recvData = await reader.read(255)
                print("Server RECV: ", recvData.decode())
                await asyncio.sleep(0.5)

    async def run_server(self):
        server = await asyncio.start_server(
                self.handle_client,
                self.address,
                self.port
        )
        async with server:
            await server.serve_forever()


if __name__ == '__main__':
    Server('localhost', 8888)
