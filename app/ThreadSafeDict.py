import asyncio
import collections

class ThreadSafeDict:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.data = {}

    async def set(self, key, value):
        async with self.lock:
            self.data[key] = value

    async def get(self, key):
        async with self.lock:
            if key in self.data:
                return self.data.get(key)
            else:
                return None
    def __str__(self):
        return str(self.data)