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

# --- ИНИЦИАЛИЗАЦИЯ СЕРВЕРА ДЛЯ RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "OK"

def run_web_server():
    # Render использует порт 8080 по умолчанию
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- ПОДКЛЮЧЕНИЕ К ВЕЧНОЙ БАЗЕ ДАННЫХ ---
MONGO_URL = "mongodb+srv://vanuxaproff.db.user:fBUnXNSZJfPftMUj@cluster0.cijehiv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client['heel_game_database']
users_collection = db['players_data']

# --- НАСТРОЙКИ БОТА ---
API_TOKEN = os.getenv('BOT_TOKEN', '8539851697:AAHUHFS35gMBCJ5ozf_ChQfLOhrvke68Fzs')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Время ожидания между пятками (18000 секунд = 5 часов)
COOLDOWN_TIME = 18000 

# --- СПИСОК ВСЕХ ПЯТОК ---
DATA = {
    "Обычная": {
        "Сено пятка": "AgACAgIAAxkBAAPlaf2Pp7k7PXrNT0d9TgjIgwKFfDoAArwTaxv04fFLE9Pz-Di4gQsBAAMCAAN5AAM7BA",
        "Земляная пятка": "AgACAgIAAxkBAAO_af2PJQUJtkxccatimHfZXuVHkx0AAqUTaxv04fFL0X9OPtULRNgBAAMCAAN5AAM7BA",
        "Водяная пятка": "AgACAgIAAxkBAAO3af2PDJ0Ud1YLISwNC3Q9J-oZw4gAAqETaxv04fFLn6SnJRUCkf0BAAMCAAN5AAM7BA",
        "Небесная пятка": "AgACAgIAAxkBAAPdaf2PktnAaJdY6Dh6gQkCAAFbGuBEAAK4E2sb9OHxS81YKINb9aIAAQEAAwIAA3kAAzsE",
        "Стеклянная пятка": "AgACAgIAAxkBAAPpaf2PsTPjIxZ2V-G741bpzEhbvewAAr4Taxv04fFLvHpUeY8-3sUBAAMCAAN5AAM7BA",
        "Банановая пятка": "AgACAgIAAxkBAAO1af2PBk0xS29McOFH3fAtJSnADFEAAqATaxv04fFLdQAB7DysIts2AQADAgADeQADOwQ",
        "Магическая пятка": "AgACAgIAAxkBAAPTaf2Pbi_T-NpbKLSa1m1bjQbZ5PAAArMTaxv04fFL1jnJZS0RalQBAAMCAAN5AAM7BA",
        "Накачаная пятка": "AgACAgIAAxkBAAPZaf2Phkz7x9JbOe2kNNWQdz_wR5kAArYTaxv04fFLOopOnhweLHcBAAMCAAN5AAM7BA"
    },
    "Необычная": {
        "Какашка пятка": "AgACAgIAAxkBAAPFaf2PPgoYWtmcoFpNxv0jaTKVJZMAAqoTaxv04fFL3v6kk9fTTEgBAAMCAAN5AAM7BA",
        "Вонючая пятка": "AgACAgIAAxkBAAO5af2PEWh5IiBFzoMvoxRzlpm4MEAAAqITaxv04fFLKpbFXQZ1Ir4BAAMCAAN5AAM7BA",
        "Клубничная пятка": "AgACAgIAAxkBAAPHaf2PRQIMUE8-bWkMg0J5YEbPpWIAAqwTaxv04fFLqwlQ5MU_kY4BAAMCAAN5AAM7BA",
        "Зек пятка": "AgACAgIAAxkBAAO9af2PH1t0F0smUHB21lDoBs4rCSQAAqQTaxv04fFLba30gxBVjo0BAAMCAAN5AAM7BA",
        "Серебрянная пятка": "AgACAgIAAxkBAAPnaf2PrXCMYRpNgNhNLNF7FnpGlUUAAr0Taxv04fFLGIrK63_mifgBAAMCAAN5AAM7BA",
        "Миньон пятка": "AgACAgIAAxkBAAPXaf2PgTlB3HMIaZLY21X1WcuxHGUAArUTaxv04fFLtNyF4L2a2X0BAAMCAAN5AAM7BA"
    },
    "Редкая": {
        "Пикми пятка": "AgACAgIAAxkBAAPhaf2PnXKz5ieWdDUui3Ss2GLkYP4AAroTaxv04fFLuKGCU27-HowBAAMCAAN5AAM7BA",
        "Фурри пятка": "AgACAgIAAxkBAAPraf2Pt4eysWdXU5qpzwWhK08yYOYAAr8Taxv04fFL5D-3jabfDiMBAAMCAAN5AAM7BA",
        "Аниме пятка": "AgACAgIAAxkBAAOzaf2PAUY1BbaWRiB-NDTSPaxT5i0AAp8Taxv04fFLRFBp4H059GUBAAMCAAN5AAM7BA",
        "Нарисованная пятка": "AgACAgIAAxkBAAPbaf2PjZ_SSygWK5J8cIASeDD80TMAArcTaxv04fFLK-9iWY63af8BAAMCAAN5AAM7BA",
        "Шиповая пятка": "AgACAgIAAxkBAAPJaf2PS6W9jEZSlwMflkel97Ke_rEAAq0Taxv04fFLz5T7u3QdZPgBAAMCAAN5AAM7BA",
        "Костянная пятка": "AgACAgIAAxkBAAPPaf2PXytPkfpMTQ7XNQUV4FKWZlgAArETaxv04fFLYWz6lgy9DtMBAAMCAAN5AAM7BA"
    },
    "Эпическая": {
        "Золотая пятка": "AgACAgIAAxkBAAPBaf2PMIM0-CdCO54JHVGfkPrUcvcAAqYTaxv04fFLND3LX-G6wC8BAAMCAAN5AAM7BA",
        "Неоновая пятка": "AgACAgIAAxkBAAPfaf2Pl3arZOhe5bHtnK2ujOh-SrAAArkTaxv04fFLHITPRRLD-MIBAAMCAAN5AAM7BA",
        "Теневая пятка": "AgACAgIAAxkBAAPfaf2Pl3arZOhe5bHtnK2ujOh-SrAAArkTaxv04fFLHITPRRLD-MIBAAMCAAN5AAM7BA",
        "Лавовая пятка": "AgACAgIAAxkBAAPRaf2PZuCrLqZSAAF9fBNzEqz1RvGjAAKyE2sb9OHxS81YKINb9aIAAQEAAwIAA3kAAzsE",
        "Готическая пятка": "AgACAgIAAxkBAAO7af2PF9vc85g_9rj44635pNQnLn0AAqMTaxv04fFLSYzfJvnHsUsBAAMCAAN5AAM7BA"
    },
    "Мифическая": {
        "Демоническая пятка": "AgACAgIAAxkBAAOtaf2Nq19iTXrmG-kSb2tHNEa819wAApcTaxv04fFLWrou_FctNJcBAAMCAAN5AAM7BA",
        "Ангельская пятка": "AgACAgIAAxkBAAOxaf2O_AvYJNii6fKij3-QdEfTLUAAAp4Taxv04fFLnc4Hl2h9saMBAAMCAAN5AAM7BA",
        "Король пятка": "AgACAgIAAxkBAAPLaf2PUp3dqZabYq3OtKjyuKy1odAAAq8Taxv04fFLDtZf82PfayMBAAMCAAN5AAM7BA",
        "Радужная пятка": "AgACAgIAAxkBAAPjaf2Pop47pI8nlt6_YFSmaRHKEWgAArsTaxv04fFLUyIpnQqLpmEBAAMCAAN5AAM7BA"
    },
    "Легендарная": {
        "Алмазная пятка": "AgACAgIAAxkBAAOvaf2O9RkEOXCLb5eSn2ZRi8sWFPcAAp0Taxv04fFL1rxXHlPU78MBAAMCAAN5AAM7BA",
        "Зевс": "AgACAgIAAxkBAAPXaf2PgTlB3HMIaZLY21X1WcuxHGUAArUTaxv04fFLtNyF4L2a2X0BAAMCAAN5AAM7BA",
        "Мёртвая пятка": "AgACAgIAAxkBAAPVaf2Pe21Vy9dSRMFkzLMl5EjETvcAArQTaxv04fFLUJEtsh0bKVEBAAMCAAN5AAM7BA"
    },
    "Идеальная": {
        "Изумрудная пятка": "AgACAgIAAxkBAAPFaf2PPgoYWtmcoFpNxv0jaTKVJZMAAqoTaxv04fFL3v6kk9fTTEgBAAMCAAN5AAM7BA",
        "Космическая пятка": "AgACAgIAAxkBAAPNaf2PVxVN1R51bsl8LOY15z8IcxEAArATaxv04fFLGdwh2Cx_tWgBAAMCAAN5AAM7BA"
    }
}

# ШАНСЫ ВЫПАДЕНИЯ (в процентах)
CHANCES = [45, 25, 15, 8, 4, 2, 1]

# --- ФУНКЦИИ ДЛЯ РАБОТЫ С БАЗОЙ ---
async def get_user_from_db(user_id):
    user_id_str = str(user_id)
    user_data = await users_collection.find_one({"_id": user_id_str})
    if not user_data:
        user_data = {"_id": user_id_str, "inv": [], "last_time": 0}
        await users_collection.insert_one(user_data)
    return user_data

# --- ОБРАБОТЧИКИ КОМАНД ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="Пятка")
    builder.button(text="Инвентарь")
    keyboard = builder.as_markup(resize_keyboard=True)
    
    await message.answer(
        "🦶 Добро пожаловать в игру! Пятки выпадают раз в 5 часов.\n"
        "Твой инвентарь сохраняется вечно в облаке.",
        reply_markup=keyboard
    )

@dp.message(F.text.lower() == "пятка")
async def get_heel_handler(message: types.Message):
    user_id = message.from_user.id
    user_data = await get_user_from_db(user_id)
    current_time = time.time()
    
    # Проверка времени ожидания
    if current_time - user_data.get('last_time', 0) < COOLDOWN_TIME:
        remaining = int(COOLDOWN_TIME - (current_time - user_data['last_time']))
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        return await message.answer(f"⏳ Рано! Приходи через {hours}ч. {minutes}м.")

    # Поиск пяток, которых еще нет в инвентаре
    all_heels = []
    for rarity, items in DATA.items():
        for heel_name in items.keys():
            if heel_name not in user_data['inv']:
                all_heels.append((rarity, heel_name))

    if not all_heels:
        return await message.answer("🏆 Ого! Ты собрал вообще все пятки в этой игре!")

    # Выбор редкости по шансам
    rarity_list = list(DATA.keys())
    chosen_rarity_list = random.choices(rarity_list, weights=CHANCES, k=1)
    chosen_rarity = chosen_rarity_list[0]
    
    # Выбор конкретной пятки этой редкости (только новой)
    possible_new_items = [name for name in DATA[chosen_rarity].keys() if name not in user_data['inv']]
    
    if not possible_new_items:
        # Если в этой редкости всё собрано, берем любую другую новую
        chosen_rarity, final_heel_name = random.choice(all_heels)
    else:
        final_heel_name = random.choice(possible_new_items)

    # Сохранение в базу данных
    await users_collection.update_one(
        {"_id": str(user_id)},
        {
            "$push": {"inv": final_heel_name},
            "$set": {"last_time": current_time}
        }
    )

    # Отправка результата
    photo_id = DATA[chosen_rarity][final_heel_name]
    caption_text = (
        f"🎉 Поздравляю! Вам выпала: <b>{final_heel_name}</b>\n"
        f"💎 Редкость: <b>{chosen_rarity}</b>"
    )
    
    await message.answer_photo(
        photo=photo_id,
        caption=caption_text,
        parse_mode="HTML"
    )

@dp.message(F.text.lower() == "инвентарь")
async def inventory_handler(message: types.Message):
    user_data = await get_user_from_db(message.from_user.id)
    inventory = user_data.get('inv', [])
    
    if not inventory:
        await message.answer("📦 Твой инвентарь пока пуст. Нажми «Пятка»!")
    else:
        text = "📜 <b>Твоя коллекция:</b>\n\n"
        for item in inventory:
            text += f"— {item}\n"
        await message.answer(text, parse_mode="HTML")

# --- ЗАПУСК БОТА ---
async def main():
    # Запускаем веб-сервер в отдельном потоке для Render
    Thread(target=run_web_server).start()
    
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
