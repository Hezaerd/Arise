import asyncio
import os

from Core.HezaBot import HezaBot

bot = HezaBot()


async def start():
    await bot.load_all_extensions()
    await bot.start(os.getenv("TOKEN"))


async def close():
    await bot.close()


async def main():
    await start()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected")
        asyncio.run(close())
