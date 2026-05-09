import asyncio
import random
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Твои данные
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

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Хранилища в памяти (сбросятся при перезагрузке)
user_data = {}  
last_time = {}

# Клавиатура
def get_main_kb():
    kb = [
        [KeyboardButton(text="🦶 Пятка"), KeyboardButton(text="🎒 Инвентарь")],
        [KeyboardButton(text="🏆 Топ игроков")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Нажимай на кнопки, чтобы собирать коллекцию пяток!",
        reply_markup=get_main_kb()
    )

@dp.message(F.text == "🦶 Пятка")
async def open_card(message: Message):
    user_id = message.from_user.id
    current_time = time.time()

    # Проверка кулдауна (5 секунд)
    if user_id in last_time and current_time - last_time[user_id] < 5:
        wait_time = int(5 - (current_time - last_time[user_id]))
        return await message.answer(f"⏳ Подожди еще {wait_time} сек.")

    # Выбор редкости (70% - обычная, 20% - необычная, 10% - редкая)
    rarity = random.choices(list(DATA.keys()), weights=[70, 20, 10])[0]
    item_name, photo_id = random.choice(list(DATA[rarity].items()))

    # Инициализация пользователя
    if user_id not in user_data:
        user_data[user_id] = {"name": message.from_user.full_name, "items": set()}
    
    # Проверка на новинку
    is_new = item_name not in user_data[user_id]["items"]
    user_data[user_id]["items"].add(item_name)
    user_data[user_id]["name"] = message.from_user.full_name
    
    last_time[user_id] = current_time

    status = "✨ НОВАЯ В КОЛЛЕКЦИИ!" if is_new else "♻️ Такая уже есть"
    
    try:
        await message.answer_photo(
            photo=photo_id,
            caption=f"🎉 Тебе выпала: **{item_name}**\nРедкость: {rarity}\n\n*{status}*",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(f"Ошибка при отправке фото: {e}\nВыпала: {item_name}")

@dp.message(F.text == "🎒 Инвентарь")
async def show_inventory(message: Message):
    user_id = message.from_user.id
    data = user_data.get(user_id)

    if not data or not data["items"]:
        return await message.answer("Твой инвентарь пока пуст. Жми 'Пятка'!")

    text = f"🎒 **Твой инвентарь ({len(data['items'])} шт.):**\n\n"
    # Сортируем список для красоты
    for item in sorted(list(data["items"])):
        text += f"• {item}\n"
    
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text == "🏆 Топ игроков")
async def show_top(message: Message):
    if not user_data:
        return await message.answer("Топ пока пуст! Будь первым!")

    # Сортируем игроков по количеству уникальных предметов
    sorted_users = sorted(user_data.values(), key=lambda x: len(x["items"]), reverse=True)
    
    text = "🏆 **ТОП КОЛЛЕКЦИОНЕРОВ:**\n\n"
    for i, user in enumerate(sorted_users[:10], 1):
        text += f"{i}. {user['name']} — {len(user['items'])} шт.\n"
    
    await message.answer(text, parse_mode="Markdown")

async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
