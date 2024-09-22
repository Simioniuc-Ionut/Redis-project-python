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
    async def pop(self, key, value):
        async with self.lock:
            if value is None:
                if key in self.data:
                    return self.data.pop(key)
                else:
                    return None
            else:
                return self.data.pop(key, value)
    async def keys(self):
        async with self.lock:
            return self.data.keys()
    def __str__(self):
        return str(self.data)