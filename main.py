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

# --- СЕРВЕР ---
app = Flask('')

@app.route('/')
def home():
    return "OK"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- БАЗА ДАННЫХ ---
MONGO_URL = "mongodb+srv://vanuxaproff.db.user:fBUnXNSZJfPftMUj@cluster0.cijehiv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client['heel_game_database']
users_collection = db['players_data']

# --- НАСТРОЙКИ БОТА ---
API_TOKEN = '8539851697:AAFXDrjTpm58eognPpwC2SGCxBxc3VYCJY8'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
COOLDOWN_TIME = 18000 

# --- СПИСОК ПЯТОК ---
DATA = {
    "Обычная": {
        "Сено пятка": "AgACAgIAAxkBAAPlaf2Pp7k7PXrNT0d9TgjIgwKFfDoAArwTaxv04fFLE9Pz-Di4gQsBAAMCAAN5AAM7BA",
        "Земляная пятка": "AgACAgIAAxkBAAO_af2PJQUJtkxccatimHfZXuVHkx0AAqUTaxv04fFL0X9OPtULRNgBAAMCAAN5AAM7BA"
    },
    "Необычная": {
        "Какашка пятка": "AgACAgIAAxkBAAPFaf2PPgoYWtmcoFpNxv0jaTKVJZMAAqoTaxv04fFL3v6kk9fTTEgBAAMCAAN5AAM7BA",
        "Вонючая пятка": "AgACAgIAAxkBAAO5af2PEWh5IiBFzoMvoxRzlpm4MEAAAqITaxv04fFLKpbFXQZ1Ir4BAAMCAAN5AAM7BA"
    },
    "Редкая": {
        "Пикми пятка": "AgACAgIAAxkBAAPhaf2PnXKz5ieWdDUui3Ss2GLkYP4AAroTaxv04fFLuKGCU27-HowBAAMCAAN5AAM7BA",
        "Фурри пятка": "AgACAgIAAxkBAAP6af2Pt4eysWdXU5qpzwWhK08yYOYAAr8Taxv04fFL5D-3jabfDiMBAAMCAAN5AAM7BA"
    },
    "Эпическая": {
        "Золотая пятка": "AgACAgIAAxkBAAPBaf2PMIM0-CdCO54JHVGfkPrUcvcAAqYTaxv04fFLND3LX-G6wC8BAAMCAAN5AAM7BA",
        "Неоновая пятка": "AgACAgIAAxkBAAPfaf2Pl3arZOhe5bHtnK2ujOh-SrAAArkTaxv04fFLHITPRRLD-MIBAAMCAAN5AAM7BA"
    },
    "Мифическая": {
        "Демоническая пятка": "AgACAgIAAxkBAAOtaf2Nq19iTXrmG-kSb2tHNEa819wAApcTaxv04fFLWrou_FctNJcBAAMCAAN5AAM7BA",
        "Ангельская пятка": "AgACAgIAAxkBAAOxaf2O_AvYJNii6fKij3-QdEfTLUAAAp4Taxv04fFLnc4Hl2h9saMBAAMCAAN5AAM7BA"
    },
    "Легендарная": {
        "Алмазная пятка": "AgACAgIAAxkBAAOvaf2O9RkEOXCLb5eSn2ZRi8sWFPcAAp0Taxv04fFL1rxXHlPU78MBAAMCAAN5AAM7BA",
        "Зевс": "AgACAgIAAxkBAAPXaf2PgTlB3HMIaZLY21X1WcuxHGUAArUTaxv04fFLtNyF4L2a2X0BAAMCAAN5AAM7BA"
    },
    "Идеальная": {
        "Изумрудная пятка": "AgACAgIAAxkBAAPFaf2PPgoYWtmcoFpNxv0jaTKVJZMAAqoTaxv04fFL3v6kk9fTTEgBAAMCAAN5AAM7BA",
        "Космическая пятка": "AgACAgIAAxkBAAPNaf2PVxVN1R51bsl8LOY15z8IcxEAArATaxv04fFLGdwh2Cx_tWgBAAMCAAN5AAM7BA"
    }
}

CHANCES = [45, 25, 15, 8, 4, 2, 1]

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
    await m.answer("🦶 Бот запущен!", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text.lower() == "пятка")
async def give_heel(m: types.Message):
    u_id = str(m.from_user.id)
    user = await get_user_data(u_id)
    now = time.time()
    
    if now - user.get('last_t', 0) < COOLDOWN_TIME:
        rem = int(COOLDOWN_TIME - (now - user['last_t']))
        return await m.answer(f"⏳ Жди {rem // 3600}ч. {(rem % 3600) // 60}м.")

    rk_key = random.choices(list(DATA.keys()), weights=CHANCES, k=1)[0]
    name = random.choice(list(DATA[rk_key].keys()))

    await users_collection.update_one(
        {"_id": u_id}, 
        {"$push": {"inv": name}, "$set": {"last_t": now}}
    )

    await m.answer_photo(
        photo=DATA[rk_key][name], 
        caption=f"🎉 Выпала: <b>{name}</b>\n💎 Редкость: <b>{rk_key}</b>", 
        parse_mode="HTML"
    )

@dp.message(F.text.lower() == "инвентарь")
async def show_inv(m: types.Message):
    user = await get_user_data(m.from_user.id)
    inv = user.get('inv', [])
    if not inv:
        await m.answer("📦 Твой инвентарь пока пуст.")
    else:
        await m.answer("📜 Твоя коллекция:\n" + "\n".join([f"— {i}" for i in inv]))

async def main():
    Thread(target=run_web_server, daemon=True).start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
