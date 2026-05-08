import asyncio
import random
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

# Твои данные
API_TOKEN = '8539851697:AAFXDrjTpm58eognPpwC2SGCxBxc3VYCJY8'
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

# Хранилища (в памяти)
user_inventory = {}  # {user_id: [названия пяток]}
last_time = {}       # {user_id: время последнего использования}

@dp.message(F.text.lower() == "пятка")
async def open_card(message: Message):
    user_id = message.from_user.id
    current_time = time.time()

    # Проверка кулдауна (5 секунд)
    if user_id in last_time and current_time - last_time[user_id] < 5:
        wait_time = int(5 - (current_time - last_time[user_id]))
        return await message.answer(f"⏳ Подожди еще {wait_time} сек.")

    # Выбор редкости и случайной пятки
    rarity = random.choices(list(DATA.keys()), weights=[70, 20, 10])[0]
    item_name, photo_id = random.choice(list(DATA[rarity].items()))

    # Сохраняем в инвентарь
    if user_id not in user_inventory:
        user_inventory[user_id] = []
    user_inventory[user_id].append(item_name)
    
    last_time[user_id] = current_time

    await message.answer_photo(
        photo=photo_id,
        caption=f"🎉 Тебе выпала: **{item_name}**\nРедкость: {rarity}",
        parse_mode="Markdown"
    )

@dp.message(F.text.lower() == "инвентарь")
async def show_inventory(message: Message):
    user_id = message.from_user.id
    items = user_inventory.get(user_id, [])

    if not items:
        return await message.answer("Твой инвентарь пока пуст. Напиши 'пятка'!")

    # Считаем количество каждой пятки
    counts = {item: items.count(item) for item in set(items)}
    text = "🎒 **Твой инвентарь:**\n\n"
    for name, count in counts.items():
        text += f"• {name} — {count} шт.\n"
    
    await message.answer(text, parse_mode="Markdown")

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
