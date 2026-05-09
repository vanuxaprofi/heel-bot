import asyncio
import random
import time
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Токен берется из Environment Variables на Render
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

# user_data = {user_id: {"name": str, "username": str, "items": set()}}
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
    await message.answer("🦶 Добро пожаловать в коллекционер пяток!", reply_markup=get_main_kb())

@dp.message(F.text == "🦶 Пятка")
async def open_card(message: Message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_time and current_time - last_time[user_id] < 5:
        return await message.answer(f"⏳ Подожди {int(5 - (current_time - last_time[user_id]))} сек.")

    rarity = random.choices(list(DATA.keys()), weights=[70, 20, 10])[0]
    item_name, photo_id = random.choice(list(DATA[rarity].items()))

    # Сохраняем данные пользователя
    if user_id not in user_data:
        user_data[user_id] = {
            "name": message.from_user.full_name,
            "username": message.from_user.username,
            "items": set()
        }
    
    is_new = item_name not in user_data[user_id]["items"]
    if is_new:
        user_data[user_id]["items"].add(item_name)
    
    last_time[user_id] = current_time

    status = "✨ НОВАЯ!" if is_new else "♻️ Уже есть"
    
    caption_text = (
        f"Поздравляю! Вам выпало: **{item_name}**\n"
        f"Редкость: {rarity}\n\n"
        f"*{status}*\n"
        f"---"
        f"📎 ID: `{photo_id}`" # Выводит ID фото, чтобы ты мог его копировать
    )

    try:
        await message.answer_photo(photo=photo_id, caption=caption_text, parse_mode="Markdown")
    except Exception:
        await message.answer(f"🎉 Выпала: {item_name}\nРедкость: {rarity}\nID: `{photo_id}`", parse_mode="Markdown")

@dp.message(F.text == "🎒 Инвентарь")
async def show_inventory(message: Message):
    data = user_data.get(message.from_user.id)
    if not data or not data["items"]:
        return await message.answer("Твой инвентарь пуст!")

    items_list = "\n".join([f"• {item}" for item in sorted(data["items"])])
    await message.answer(f"🎒 **Твоя коллекция ({len(data['items'])}/4):**\n\n{items_list}", parse_mode="Markdown")

@dp.message(F.text == "🏆 Топ игроков")
async def show_top(message: Message):
    if not user_data:
        return await message.answer("Топ пока пуст!")

    # Сортировка по количеству уникальных пяток
    users = sorted(user_data.values(), key=lambda x: len(x["items"]), reverse=True)
    
    text = "🏆 **ТОП КОЛЛЕКЦИОНЕРОВ:**\n\n"
    for i, user in enumerate(users[:10], 1):
        username_display = f" (@{user['username']})" if user['username'] else ""
        text += f"{i}. {user['name']}{username_display} — {len(user['items'])} шт.\n"
    
    await message.answer(text, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
