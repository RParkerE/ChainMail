import socket
import json
import threading
from typing import List, Dict
import asyncio

class Node:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.peers: List[tuple] = []
        self.blockchain = None
        self.server = None

    async def start(self):
        self.server = await asyncio.start_server(
            self.handle_connection, self.host, self.port
        )
        print(f"Node listening on {self.host}:{self.port}")

    async def handle_connection(self, reader, writer):
        data = await reader.read(1024)
        message = json.loads(data.decode())

        if message["type"] == "new_block":
            await self.handle_new_block(message["data"])
        elif message["type"] == "sync_request":
            await self.handle_sync_request(writer)

    async def broadcast(self, message: Dict):
        for peer in self.peers:
            try:
                reader, writer = await asyncio.open_connection(peer[0], peer[1])
                writer.write(json.dumps(message).encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                print(f"Failed to broadcast to {peer}: {e}") 