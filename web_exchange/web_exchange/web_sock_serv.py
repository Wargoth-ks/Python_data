import asyncio
import logging
import websockets
import re


from websockets.exceptions import ConnectionClosedOK

from aio_client import get_exchange

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, ws):
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws):
        
        async for message in ws:
            match = re.match(r"exchange (\d+)", message)
            if match:
                n = int(match.group(1))
                if n > 10:
                    await self.send_to_clients("You can't get data more then 10 days")
                    continue
                n_days = await get_exchange(n)
                await self.send_to_clients("\n" + str(n_day) + "\n" for n_day in n_days)
            elif message == "exchange today":
                cur_days = await get_exchange(1)
                await self.send_to_clients("\n" + str(cur_day) + "\n" for cur_day in cur_days)
            else:
                await self.send_to_clients(f"{ws}: {message}")


async def main():
    try:
        server = Server()
        async with websockets.serve(server.ws_handler, "localhost", 8081):
            await asyncio.Future()  # run forever
    except asyncio.CancelledError:
        print("Server was stopped !!!")


if __name__ == "__main__":
    asyncio.run(main())
