#!/usr/bin/env python3
import asyncio
import logging
import sys
import threading
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from handlers.start import router as start_router
from handlers.payment import router as payment_router
from handlers.admin import router as admin_router
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN: raise ValueError("BOT_TOKEN не найден!")

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

# Импортируем админку
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from web_admin.app import app as admin_app

# Объединяем API и админку
app = FastAPI(title="QAZLO")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Монтируем админку на /admin
app.mount("/admin", admin_app)

@app.get("/")
async def root(): return {"status": "ok", "admin": "/admin"}

@app.get("/health")
async def health(): return {"status": "alive"}

def run_api(): uvicorn.run(app, host="0.0.0.0", port=10000, log_level="error")

# Bot
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(admin_router)
dp.include_router(start_router)
dp.include_router(payment_router)

async def main():
    logger.info("🚀 Бот + Админка запущены!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    threading.Thread(target=run_api, daemon=True).start()
    asyncio.run(main())
