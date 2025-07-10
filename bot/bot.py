import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from aiohttp import web

from bot.config import BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PATH, WEBHOOK_URL

# Инициализация бота и диспетчера с памятью для FSM
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Импортируем обработчики (регистрация внутри)
from bot.handlers import appointment, other_handlers, start


async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")


async def on_shutdown(app: web.Application):
    print("Shutting down..")
    await bot.delete_webhook()
    await bot.session.close()
    await storage.close()


async def handle_webhook(request: web.Request):
    update = Update(**await request.json())
    await dp.process_update(update)
    return web.Response(text="OK")


def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host="0.0.0.0", port=8443)


if __name__ == "__main__":
    asyncio.run(main())
