import asyncio
import random
import time
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Код берет токен из настроек Render (раздел Environment), чтобы он не "протух"
API_TOKEN = os.getenv 8539851697:AAHefsphF_9xArNF1wa2Qi6AT_B-0YTAn_E

DATA = {
    "Обычная": {
        "Сено пятка": "AgACAgIAAxkBAAPlaf2Pp7k7PXrNT0d9TgjIgwKFfDoAArwTaxv04fFLE9Pz-Di4gQsBAAMCAAN5AAM7BA",
        "Земляная пятка": "AgACAgIAAxkBAAO_af2PJQUJtkxccatimHfZXuVHkx0AAqUTaxv04fFL0X9OPtULRNgBAAMCAAN5AAM7BA"
    },
    "Необычная": {
        "Какашка пятка": "AgACAgIAAxkBAAPFaf2PPgoYWtmcoFpNxv0jaTKVJZMAAqoTaxv04fFL3v6kk9fTTEgBAAMCAAN5AAM7BA"
    },
    "Редкая": {
        "Пикми пятка": "AgACAgIAAxkBAAPhaf2PnXKz5ieWdDUui3Ss2GLkYP4AAroTaxv04fFLuKGCU27-HowBAAMCAAN5AAM7BA"
    }
}

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_data = {}  
last_time = {}

def get_main_kb():
    kb = [
        [KeyboardButton(text="🦶 Пятка"), KeyboardButton(text="🎒 Инвентарь")],
        [KeyboardButton(text="🏆 Топ игроков")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Нажимай на кнопки:", reply_markup=get_main_kb())

@dp.message(F.text == "🦶 Пятка")
async def open_card(message: Message):
    user_id = message.from_user.id
    current_time = time.time()
    if user_id in last_time and current_time - last_time[user_id] < 5:
        return await message.answer(f"⏳ Подожди {int(5 - (current_time - last_time[user_id]))} сек.")

    rarity = random.choices(list(DATA.keys()), weights=[70, 20, 10])[0]
    item_name, photo_id = random.choice(list(DATA[rarity].items()))

    if user_id not in user_data:
        user_data[user_id] = {"name": message.from_user.full_name, "items": set()}
    
    is_new = item_name not in user_data[user_id]["items"]
    user_data[user_id]["items"].add(item_name)
    last_time[user_id] = current_time
    
    status = "✨ НОВАЯ!" if is_new else "♻️ Уже есть"
    try:
        await message.answer_photo(photo=photo_id, caption=f"🎉 **{item_name}** ({rarity})\n\n*{status}*", parse_mode="Markdown")
    except Exception:
        await message.answer(f"🎉 Выпала: {item_name} ({rarity})")

@dp.message(F.text == "🎒 Инвентарь")
async def show_inventory(message: Message):
    data = user_data.get(message.from_user.id)
    if not data or not data["items"]: return await message.answer("Пусто!")
    text = "🎒 Инвентарь:\n" + "\n".join([f"• {i}" for i in sorted(data["items"])])
    await message.answer(text)

@dp.message(F.text == "🏆 Топ игроков")
async def show_top(message: Message):
    if not user_data: return await message.answer("Топ пуст!")
    users = sorted(user_data.values(), key=lambda x: len(x["items"]), reverse=True)
    text = "🏆 ТОП:\n" + "\n".join([f"{i+1}. {u['name']} — {len(u['items'])}" for i, u in enumerate(users[:10])])
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
