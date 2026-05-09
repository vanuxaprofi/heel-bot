import asyncio
import random
import time
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Твой токен
API_TOKEN = "8539851697:AAHefsphF_9xArNF1wa2Qi6AT_B-0YTAn_E"

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

TOTAL_CARDS = sum(len(v) for v in DATA.values())
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
user_data = {}  
last_time = {}

# --- ВЕБ-СЕРВЕР ДЛЯ ПОДДЕРЖКИ ЖИЗНИ ---
async def handle(request):
    return web.Response(text="Бот в сети!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
# --------------------------------------

def get_main_kb():
    kb = [[KeyboardButton(text="🦶 Пятка"), KeyboardButton(text="🎒 Инвентарь")], [KeyboardButton(text="🏆 Топ игроков")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("🦶 Игра запущена!", reply_markup=get_main_kb())

@dp.message(F.photo)
async def get_photo_id(message: Message):
    await message.answer(f"✅ **ID фото:**\n`{message.photo[-1].file_id}`", parse_mode="Markdown")

@dp.message(F.text == "🦶 Пятка")
async def open_card(message: Message):
    user_id = message.from_user.id
    current_time = time.time()
    if user_id in last_time and current_time - last_time[user_id] < 5:
        return await message.answer(f"⏳ Подожди {int(5 - (current_time - last_time[user_id]))} сек.")

    if user_id not in user_data:
        user_data[user_id] = {"name": message.from_user.full_name, "username": message.from_user.username, "items": set()}
    
    inv = user_data[user_id]["items"]
    if len(inv) >= TOTAL_CARDS:
        return await message.answer("🏆 Вы собрали все пятки!")

    # Шанс найти новую
    item_name, rarity, photo_id = None, None, None
    for _ in range(10):
        r = random.choices(list(DATA.keys()), weights=[70, 20, 10])[0]
        name, pid = random.choice(list(DATA[r].items()))
        if name not in inv:
            item_name, rarity, photo_id = name, r, pid
            break
    
    if not item_name:
        rarity = random.choices(list(DATA.keys()), weights=[70, 20, 10])[0]
        item_name, photo_id = random.choice(list(DATA[rarity].items()))

    is_new = item_name not in inv
    if is_new: inv.add(item_name)
    last_time[user_id] = current_time

    status = "🎒 Пятка добавлена в инвентарь!" if is_new else "♻️ Такая пятка уже есть!"
    caption = f"🎉 **Поздравляю** 🎉\n\nВам выпала • **{item_name}**\nРедкость • **{rarity}**\n\n{status}"
    
    await message.answer_photo(photo=photo_id, caption=caption, parse_mode="Markdown")
    if len(inv) == TOTAL_CARDS and is_new:
        await message.answer("🎊 **НЕВЕРОЯТНО!** 🎊\n\nВы собрали ВСЮ коллекцию! 👑")

@dp.message(F.text == "🎒 Инвентарь")
async def show_inventory(message: Message):
    data = user_data.get(message.from_user.id)
    if not data or not data["items"]: return await message.answer("Пусто!")
    items = "\n".join([f"• {i}" for i in sorted(list(data["items"]))])
    await message.answer(f"🎒 **Коллекция ({len(data['items'])}/{TOTAL_CARDS}):**\n\n{items}", parse_mode="Markdown")

@dp.message(F.text == "🏆 Топ игроков")
async def show_top(message: Message):
    if not user_data: return await message.answer("Топ пуст!")
    users = sorted(user_data.values(), key=lambda x: len(x["items"]), reverse=True)
    text = "🏆 **ТОП КОЛЛЕКЦИОНЕРОВ:**\n\n"
    for i, u in enumerate(users[:10], 1):
        un = f" (@{u['username']})" if u.get('username') else ""
        text += f"{i}. {u['name']}{un} — {len(u['items'])}/{TOTAL_CARDS}\n"
    await message.answer(text, parse_mode="Markdown")

async def main():
    await start_web_server() # Запуск "оживителя"
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
