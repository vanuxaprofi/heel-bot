import asyncio
import random
import time
import os
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

# Считаем общее количество уникальных пяток в игре
TOTAL_CARDS = sum(len(v) for v in DATA.values())

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
    await message.answer("🦶 Игра запущена! Собери все пятки!", reply_markup=get_main_kb())

@dp.message(F.photo)
async def get_photo_id(message: Message):
    photo_id = message.photo[-1].file_id
    await message.answer(f"✅ **ID этой фотографии:**\n\n`{photo_id}`", parse_mode="Markdown")

@dp.message(F.text == "🦶 Пятка")
async def open_card(message: Message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_time and current_time - last_time[user_id] < 5:
        wait_time = int(5 - (current_time - last_time[user_id]))
        return await message.answer(f"⏳ Подожди еще {wait_time} сек.")

    # Инициализация игрока
    if user_id not in user_data:
        user_data[user_id] = {"name": message.from_user.full_name, "username": message.from_user.username, "items": set()}
    
    user_inventory = user_data[user_id]["items"]

    # Если уже собрал всё
    if len(user_inventory) >= TOTAL_CARDS:
        return await message.answer("🏆 Вы уже собрали всю коллекцию! Вы легенда пяток! 🎉")

    # Логика выбора: пытаемся найти новую пятку за несколько попыток
    item_name, rarity, photo_id = None, None, None
    for _ in range(10): # 10 попыток найти то, чего нет
        r = random.choices(list(DATA.keys()), weights=[70, 20, 10])[0]
        name, pid = random.choice(list(DATA[r].items()))
        if name not in user_inventory:
            item_name, rarity, photo_id = name, r, pid
            break
    
    # Если за 10 попыток не нашли новую (не повезло), берем любую рандомную
    if not item_name:
        rarity = random.choices(list(DATA.keys()), weights=[70, 20, 10])[0]
        item_name, photo_id = random.choice(list(DATA[rarity].items()))

    is_new = item_name not in user_inventory
    if is_new:
        user_inventory.add(item_name)
    
    last_time[user_id] = current_time

    # Текст сообщения
    if is_new:
        status_msg = "🎒 Пятка успешно добавлена в ваш инвентарь!"
    else:
        status_msg = "♻️ Такая пятка у вас уже есть!"

    caption_text = (
        f"🎉 **Поздравляю** 🎉\n\n"
        f"Вам выпала • **{item_name}**\n"
        f"Редкость • **{rarity}**\n\n"
        f"{status_msg}"
    )

    await message.answer_photo(photo=photo_id, caption=caption_text, parse_mode="Markdown")

    # ПРОВЕРКА НА ЗАВЕРШЕНИЕ КОЛЛЕКЦИИ
    if len(user_inventory) == TOTAL_CARDS and is_new:
        await asyncio.sleep(1) # Небольшая пауза для эффекта
        await message.answer(
            f"🎊 **НЕВЕРОЯТНО!** 🎊\n\n"
            f"Вы собрали ВСЕ **{TOTAL_CARDS}** пяток! \n"
            f"Теперь вы официально — **Мастер Пяток**! 👑🦾",
            parse_mode="Markdown"
        )

@dp.message(F.text == "🎒 Инвентарь")
async def show_inventory(message: Message):
    data = user_data.get(message.from_user.id)
    if not data or not data["items"]:
        return await message.answer("Твой инвентарь пока пуст!")

    items_list = "\n".join([f"• {item}" for item in sorted(list(data["items"]))])
    await message.answer(f"🎒 **Твоя коллекция ({len(data['items'])}/{TOTAL_CARDS}):**\n\n{items_list}", parse_mode="Markdown")

@dp.message(F.text == "🏆 Топ игроков")
async def show_top(message: Message):
    if not user_data:
        return await message.answer("🏆 Топ пока пуст!")

    users = sorted(user_data.values(), key=lambda x: len(x["items"]), reverse=True)
    text = "🏆 **ТОП КОЛЛЕКЦИОНЕРОВ:**\n\n"
    for i, user in enumerate(users[:10], 1):
        un = f" (@{user['username']})" if user.get('username') else ""
        text += f"{i}. {user['name']}{un} — {len(user['items'])}/{TOTAL_CARDS}\n"
    await message.answer(text, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
