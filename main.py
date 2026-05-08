import asyncio
import random
import time
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from flask import Flask
from threading import Thread
from motor.motor_asyncio import AsyncIOMotorClient

app = Flask('')
@app.route('/')
def home(): return "OK"
def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

MONGO_URL = "mongodb+srv://vanuxaproff:fBUnXNSZJfPftMUj@cluster0.cijehiv.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGO_URL)
db = client['heel_game_database']
users_collection = db['players_data']

API_TOKEN = '8539851697:AAFXDrjTpm58eognPpwC2SGCxBxc3VYCJY8'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
COOLDOWN_TIME = 5

DATA = {
    "Обычная": {"Сено пятка": "AgACAgIAAxkBAAPlaf2Pp7k7PXrNT0d9TgjIgwKFfDoAArwTaxv04fFLE9Pz-Di4gQsBAAMCAAN5AAM7BA", "Земляная пятка": "AgACAgIAAxkBAAO_af2PJQUJtkxccatimHfZXuVHkx0AAqUTaxv04fFL0X9OPtULRNgBAAMCAAN5AAM7BA"},
    "Необычная": {"Какашка пятка": "AgACAgIAAxkBAAPFaf2PPgoYWtmcoFpNxv0jaTKVJZMAAqoTaxv04fFL3v6kk9fTTEgBAAMCAAN5AAM7BA"},
    "Редкая": {"Пикми пятка": "AgACAgIAAxkBAAPhaf2PnXKz5ieWdDUui3Ss2GLkYP4AAroTaxv04fFLuKGCU27-HowBAAMCAAN5AAM7BA"}
}
CHANCES = [60, 30, 10]

async def get_user_data(user_id):
    u_id = str(user_id)
    data = await users_collection.find_one({"_id": u_id})
    if not data:
        data = {"_id": u_id, "inv": [], "last_t": 0}
        await users_collection.insert_one(data)
    return data

@dp.message(Command("start"))
async def start(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="Пятка")
    kb.button(text="Инвентарь")
    await m.answer("🦶 Бот запущен! Скинь фото для ID.", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.photo)
async def get_photo_id(m: types.Message):
    await m.answer(f"🆔 ID фото:\n<code>{m.photo[-1].file_id}</code>", parse_mode="HTML")

@dp.message(F.text == "Пятка")
async def give_heel(m: types.Message):
    u_id = str(m.from_user.id)
    user = await get_user_data(u_id)
    now = time.time()
    if now - user.get('last_t', 0) < COOLDOWN_TIME:
        return await m.answer(f"⏳ Жди {int(COOLDOWN_TIME - (now - user['last_t']))} сек.")
    rk = random.choices(list(DATA.keys()), weights=CHANCES, k=1)[0]
    name = random.choice(list(DATA[rk].keys()))
    await users_collection.update_one({"_id": u_id}, {"$push": {"inv": name}, "$set": {"last_t": now}})
    await m.answer_photo(photo=DATA[rk][name], caption=f"🎉 Выпала: {name}\n💎 Редкость: {rk}")

@dp.message(F.text == "Инвентарь")
async def show_inv(m: types.Message):
    user = await get_user_data(m.from_user.id)
    inv = user.get('inv', [])
    await m.answer("📜 Коллекция:\n" + "\n".join([f"— {i}" for i in inv]) if inv else "📦 Пусто.")

async def main():
    Thread(target=run_web_server, daemon=True).start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
