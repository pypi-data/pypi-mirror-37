
import asyncio

import time  
from datetime import datetime

import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def custom_sleep():  
    print('SLEEP {}\n'.format(datetime.now()))
    await asyncio.sleep(1)
async def factorial(name, number):  
    f = 1
    for i in range(2, number+1):
        print('Task {}: Compute factorial({})'.format(name, i))
        await custom_sleep()
        f *= i
    print('Task {}: factorial({}) is {}\n'.format(name, number, f))

async def main ():
    x = await factorial ("bob", 4)
    print (x)
    
if __name__ == '__main__':
    tasks = [
        asyncio.ensure_future (main ())
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))  
