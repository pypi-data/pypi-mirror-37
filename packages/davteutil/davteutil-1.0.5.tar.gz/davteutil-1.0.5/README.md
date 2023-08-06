# davteutil
This project provides convenient general-purpose functions, used by [Davte](t.me/davte) in his projects.

Please note that you need Python3.5+ to run async code

## Project folders

## Usage
```
import asyncio

from davteutil import async_get, async_post

async def main():
  url = 'http://www.google.com'
  result = await async_get(url, mode='html')
  print(result)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
