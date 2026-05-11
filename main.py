import asyncio
import random
import time
import os
import sqlite3
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# ТВОЙ ТОКЕН
API_TOKEN = "8539851697:AAHefsphF_9xArNF1wa2Qi6AT_B-0YTAn_E"

DATA = {
    "⚪ ОБЫЧНАЯ (45%)": {
        "🌾 Сено пятка": "AgACAgIAAxkBAAPlaf2Pp7k7PXrNT0d9TgjIgwKFfDoAArwTaxv04fFLE9Pz-Di4gQsBAAMCAAN5AAM7BA",
        "🌱 Земляная пятка": "AgACAgIAAxkBAAO_af2PJQUJtkxccatimHfZXuVHkx0AAqUTaxv04fFL0X9OPtULRNgBAAMCAAN5AAM7BA",
        "🧟 Зомби пятка": "AgACAgIAAxkBAAIEEmn_FMwmK6es8BSPbR_Lm5FUe5QjAAK4FWsb1ZD5S0rz0TKwGfWOAQADAgADeQADOwQ",
        "🚗 Пятка в машине": "AgACAgIAAxkBAAID6mn_E0HXgyFPtavIfRpZ1meTEoN-AAKgFWsb1ZD5S2y8K7zxxfghAQADAgADeQADOwQ",
        "🩸 Кровяная пятка": "AgACAgIAAxkBAAIEAAFp_xQkyWRcvMmppx9GAAEEucySIOwAAq8VaxvVkPlLLNVajl7uHy0BAAMCAAN5AAM7BA",
        "🌙 Ночная пятка": "AgACAgIAAxkBAAIEHGn_F63APKdLRWncq_wcHmiJh5D8AALNFWsb1ZD5S34LTqchLDTEAQADAgADeQADOwQ",
        "🌞 Дневная пятка": "AgACAgIAAxkBAAIEHmn_F7oej49TZ7E5yHtFfDtd9s9KAALOFWsb1ZD5SwKF1-lb7QRgAQADAgADeQADOwQ",
        "💧 Водяная пятка": "AgACAgIAAxkBAAID1mn_ErtLjnFoY0ceK0ZoH5TgeKkAA5UVaxvVkPlLRu8mnryTmsABAAMCAAN5AAM7BA",
        "🌬️ Небесная пятка": "AgACAgIAAxkBAAIDsGn_EICSBiM3RKbdcxYHzeCD2woiAAJ3FWsb1ZD5S-WxYxtzJmHbAQADAgADeQADOwQ",
        "🥛 Стеклянная пятка": "AgACAgIAAxkBAAIDkmn_DOFf8k_xsfkUPrCxKrMH1uwYAAJfFWsb1ZD5SxT8rLirgtg9AQADAgADeQADOwQ",
        "🍌 Банановая пятка": "AgACAgIAAxkBAAID2Gn_EsXPbjclbQ_vojegBC364Lg3AAKWFWsb1ZD5Szj9AqhodMO1AQADAgADeQADOwQ",
        "🔮 Магическая пятка": "AgACAgIAAxkBAAIDumn_Eb6e7rfobGxfplOZYbv_7eE8AAKAFWsb1ZD5S9v9Gt16pd62AQADAgADeQADOwQ",
        "💪 Накачанная пятка": "AgACAgIAAxkBAAIDtGn_EZlWMLbzG4aNXehsEP7ut-Z0AAJ8FWsb1ZD5S9B_j9bB8f6DAQADAgADeQADOwQ",
        "🧸 Плюшевая пятка": "AgACAgIAAxkBAAIEFmn_F4T3_GiR1Nk4oAl51ZcUbob6AALJFWsb1ZD5S6nAVH_ypfpMAQADAgADeQADOwQ",
        "☢️ Радиоактивная пятка": "AgACAgIAAxkBAAIEFGn_F3a-quY8EHRJvgKrZFbVhQABMQACyBVrG9WQ-UtOVEPEprm7ygEAAwIAA3kAAzsE",
        "🪵 Деревянная пятка": "AgACAgIAAxkBAAID9mn_E5n2qzGBAAE9LED2URMWj-QEpwACpxVrG9WQ-Uvx3fvfeUnwHgEAAwIAA3kAAzsE",
        "🌫️ Пятка в тумане": "AgACAgIAAxkBAAIEIGn_F8Uh4fN9xFNabDa6SZ-x8BrfAALPFWsb1ZD5S7t-XIWi8EH4AQADAgADeQADOwQ",
        "❄️ Снежная пятка": "AgACAgIAAxkBAAID6Gn_Ey5HXjmTxgwGf_9U2Urqgi6KAAKeFWsb1ZD5S-XTgpndBk9cAQADAgADeQADOwQ"},
    
        "🟢 НЕОБЫЧНАЯ (25%)": {
        "💩 Какашка пятка": "AgACAgIAAxkBAAPFaf2PPgoYWtmcoFpNxv0jaTKVJZMAAqoTaxv04fFL3v6kk9fTTEgBAAMCAAN5AAM7BA",
        "🤡 Клоунская пятка": "AgACAgIAAxkBAAIFXmn_YhXNCagUKtMUs5hsWAYSluyIAAJwE2sb1ZABSBtXMa7EX2EnAQADAgADeQADOwQ",
        "🇲🇽 Мексиканская пятка": "AgACAgIAAxkBAAIFYGn_YijdIKLflTfBinihZOJZptq2AAJxE2sb1ZABSGN06Ezh-Di7AQADAgADeQADOwQ",
        "🇫🇷 Французская пятка": "AgACAgIAAxkBAAIFYmn_YjcC_G6jEKSxJmVLaDGdfc2uAAJzE2sb1ZABSHaFAf24-Y8qAQADAgADeQADOwQ",
        "📟 Голограмная пятка": "AgACAgIAAxkBAAIFXGn_YfJP0rRk8ffzjGRX5foaBPLuAALWEWsbQEAAAUjM_jhLR0kIVgEAAwIAA3kAAzsE",
        "🤢 Вонючая пятка": "AgACAgIAAxkBAAID1Gn_EREAATE6n6-nLD6K2arJWCA4RgACkFWsb1ZD5S_UsLXIuYe5Zp3gEAAwIAA3kAAzsE",
        "🍓 Клубничная пятка": "AgACAgIAAxkBAAIFZGn_YlJNeXKkHSxJyN7ktT0rf53hAAJ1E2sb1ZABSPvDSdClMBR2AQADAgADeQADOwQ",
        "⛓️ Зек пятка": "AgACAgIAAxkBAAIFZmn_YmpTFwUV5x1F90tkb1OXlX96AAJ3E2sb1ZABSCtDrjoogOnKAQADAgADeQADOwQ",
        "🥈 Серебряная пятка": "AgACAgIAAxkBAAIDkGn_D0GvsOp0rze9Ruv9-H92M9-JAAJeFWsb1ZD5Sz1Z9RQS6uoEAQADAgADeQADOwQ",
        "🟡 Миньон пятка": "AgACAgIAAxkBAAIFaGn_Yn0XsNrv5lyT1XFZcVxQgMiVAAJ4E2sb1ZABSFid7miwmtfPAQADAgADeQADOwQ",
        "📦 Коробка с пяткой": "AgACAgIAAxkBAAIFamn_YouCT-QYnAgfTCFB207FbSw_AAJ5E2sb1ZABSIYltFqCN6MxAQADAgADeQADOwQ",
        "🧊 Ледяная пятка": "AgACAgIAAxkBAAIEMmn_ID6A2Es4E2MhErV_offnKs8fAAIeFmsb1ZD5S5VU-JhnyFMPAQADAgADeQADOwQ",
        "🌸 Цветочная пятка": "AgACAgIAAxkBAAIDhmn_CtswJ5giZuyE6wT4QvPPuR5_AAJUFWsb1ZD5S_OtiSyyNSJnAQADAgADeQADOwQ",
        "💍 Свадебная пятка": "AgACAgIAAxkBAAID5mn_EyO0HM8BN4eH0tE-VGgw3dQxAAKdFWsb1ZD5S9wUM1L44LZ4AQADAgADeQADOwQ"},
    
    "🔵 РЕДКАЯ (15%)": {
        "🎀 Пикми пятка": "AgACAgIAAxkBAAPhaf2PnXKz5ieWdDUui3Ss2GLkYP4AAroTaxv04fFLuKGCU27-HowBAAMCAAN5AAM7BA",
        "🐾 Фурри пятка": "AgACAgIAAxkBAAIDj2n_DJvAZI1yYmTi7ETMNuPloWoIAAJdFWsb1ZD5S7qH4pa_N81uAQADAgADeQADOwQ",
        "🎎 Аниме пятка": "AgACAgIAAxkBAAID2mn_Etbb9x5TXSP0kcUVP8p4gdgIAAKXFWsb1ZD5S1o9GcEaYzSaAQADAgADeQADOwQ",
        "✏️ Нарисованная пятка": "AgACAgIAAxkBAAIDsmn_EXK9W1WYn1b34ohrGHOCYXdWAAJ7FWsb1ZD5S3hds3yfLWdPAQADAgADeQADOwQ",
        "🌵 Шиповая пятка": "AgACAgIAAxkBAAIDxGn_EgoMvT-8pJe8xInio8TRc90JAAKIFWsb1ZD5Sx6pxr5qhIsvAQADAgADeQADOwQ",
        "🦴 Костяная пятка": "AgACAgIAAxkBAAIDvmn_EdeXeFQnKpc3c5Mz3Ds1LXqEAAKEFWsb1ZD5S8FM9CNMhqI1AQADAgADeQADOwQ",
        "🍫 Шоколадная пятка": "AgACAgIAAxkBAAIEGGn_F4-ow0fL1mD7OenMCEY115w4AALKFWsb1ZD5S0fBJ4g2P5YsAQADAgADeQADOwQ",
        "🍔 Жирная пятка": "AgACAgIAAxkBAAID7mn_E1k9sSVYlSc8fIJwfZkC08z2AAKiFWsb1ZD5SxzCGexoej_GAQADAgADeQADOwQ",
        "🧱 Кирпичная пятка": "AgACAgIAAxkBAAIEEGn_FIer9aQdFCfUiCOx3GdyuVR3AAK3FWsb1ZD5S9frhYxtdwABZgEAAwIAA3kAAzsE",
        "🦇 Готическая пятка": "AgACAgIAAxkBAAID0mn_EqVauVNeXcYCpSKt3ms7MxTWAAKRFWsb1ZD5S19I1tL7w6glAQADAgADeQADOwQ",
        "🏺 Египетская пятка": "AgACAgIAAxkBAAIER2n_OAdCiNJ1fDO2hayplX7wEV69AALdFmsb1ZD5S0WgBZ51p6NNAQADAgADeQADOwQ"},
    
    "🟣 ЭПИЧЕСКАЯ (8%)": {
        "🦕 Доисторическая пятка": "AgACAgIAAxkBAAIEDmn_FHIDuHJ8g9yLUs4oqYtuWan6AAK1FWsb1ZD5S6THTIczYFOcAQADAgADeQADOwQ",
        "💥 Антиматерия пятка": "AgACAgIAAxkBAAID-mn_E8geNo0lnW05fq9B-vZtsJ3EAAKrFWsb1ZD5S_ihQgvAG9yJAQADAgADeQADOwQ",
        "👊 Джоджо пятка": "AgACAgIAAxkBAAID_Gn_E9B-MJna3bsepwT-G9Y-cSa9AAKsFWsb1ZD5Sx7j_oN6_AzzAQADAgADeQADOwQ",
        "⚔️ Рыцарская пятка": "AgACAgIAAxkBAAIELmn_GF5BFvD06sQJPWMNzMzFE4G6AALYFWsb1ZD5S6iQtVMuXrWEAQADAgADeQADOwQ",
        "☀️ Солнечная пятка": "AgACAgIAAxkBAAIEKGn_GAMgXWidw_32msiGe1MpN5IAA9AVaxvVkPlLwmk3ndc9FQEBAAMCAAN5AAM7BA",
        "🌚 Лунная пятка": "AgACAgIAAxkBAAIEKmn_GBIyDEZJWzb-Ps6m4_9QZ0BbAALSFWsb1ZD5Sxgjwz_uUPQVAQADAgADeQADOwQ",
        "📜 Древняя пятка": "AgACAgIAAxkBAAIEDmn_FHIDuHJ8g9yLUs4oqYtuWan6AAK1FWsb1ZD5S6THTIczYFOcAQADAgADeQADOwQ",
        "✨ Золотая пятка": "AgACAgIAAxkBAAIDzGn_Ej5fMNPzcmpN9zvuH795saJgAAKMFWsb1ZD5S6py6qBOf8AhAQADAgADeQADOwQ",
        "🌈 Неоновая пятка": "AgACAgIAAxkBAAIDrmn_DbHI0Jqj4IsXgmrGs6J4iREMAAJnFWsb1ZD5SzZtAAFMEVVnMwEAAwIAA3kAAzsE",
        "👤 Теневая пятка": "AgACAgIAAxkBAAID5Gn_ExizvCcHapz0JFcU_tmhDOpfAAKcFWsb1ZD5S_kRM-70fq_8AQADAgADeQADOwQ",
        "🔥 Лавовая пятка": "AgACAgIAAxkBAAIDvGn_EcvvHKIqgeeeY1VxyQf7panyAAKCFWsb1ZD5S6Nlv1VtAdXFAQADAgADeQADOwQ",
        "🌌 Гравити фолз пятка": "AgACAgIAAxkBAAID4mn_EwtwCf_6dTwAAdszn7WaUH-7PwACmxVrG9WQ-UtpmdUHcfnbmAEAAwIAA3kAAzsE",
        "🌊 Подводная пятка": "AgACAgIAAxkBAAID8mn_E28DXmAeisv9AyjTY4svxGqWAAKkFWsb1ZD5S6v3dYj_UdtbAQADAgADeQADOwQ",
        "🍕 Пицца пятка": "AgACAgIAAxkBAAID9Gn_E427KoTE1WKBQhGiiMFJKTT6AAKlFWsb1ZD5S9jLZsS2gyuJAQADAgADeQADOwQ"},
    
    "🔴 МИФИЧЕСКАЯ (4%)": {
        "👹 Демоническая пятка": "AgACAgIAAxkBAAID4Gn_Ev0bSON3TUcSQ6EHpC3SseeRAAKaFWsb1ZD5SyPWO53iJqvZAQADAgADeQADOwQ",
        "😇 Ангельская пятка": "AgACAgIAAxkBAAID3Gn_EuUcieIvGWulfO1wSRJIU1wFAAKYFWsb1ZD5SzqKAAGkMIfIewEAAwIAA3kAAzsE",
        "👑 Король пятка": "AgACAgIAAxkBAAIDwmn_EfrCpPVh4kGwvkzJSoYnwgAB1AAChxVrG9WQ-Uv47f3uLJgsLwEAAwIAA3kAAzsE",
        "🏳️‍🌈 Радужная пятка": "AgACAgIAAxkBAAIDqGn_DQ4FuWv7qkFjbzjn_OUNb0HiAAJjFWsb1ZD5S9yYkliLFV_UAQADAgADeQADOwQ",
        "👽 Инопланетная пятка": "AgACAgIAAxkBAAIEDGn_FGOlrhNtDREpmrQ70Q-8Ln3hAAK0FWsb1ZD5S9Ys73tzWqnsAQADAgADeQADOwQ",
        "🧪 SCP пятка": "AgACAgIAAxkBAAIERWn_N929xS7ixp-IZYW67VmsGiE_AALaFmsb1ZD5S15tvDeldngAAQEAAwIAA3kAAzsE",
        "🎰 Казино пятка": "AgACAgIAAxkBAAIDjWn_DIQM1hllF2usp74800QVmVxhAAJcFWsb1ZD5Sx80PirvUzEUAQADAgADeQADOwQ",
        "💰 Магнат пятка": "AgACAgIAAxkBAAID7Gn_E0wdVHJyBsvIoO7tMTtoucqTAAKhFWsb1ZD5S3-vIun8qbYQAQADAgADeQADOwQ"},
    
    "🟡 ЛЕГЕНДАРНАЯ (2%)": {
        "💎 Алмазная пятка": "AgACAgIAAxkBAAID3mn_EvLdDY1r-ZvW77novm5DuhXVAAKZFWsb1ZD5S18ODlfYhh8NAQADAgADeQADOwQ",
        "⚡ Зевс пятка": "AgACAgIAAxkBAAIDtmn_EaLijTggPq-ojfCradBc21yRAAJ9FWsb1ZD5SxfNkQw-ybnuAQADAgADeQADOwQ",
        "💀 Мертвая пятка": "AgACAgIAAxkBAAIDuGn_Ea7HrThA8-StQoFK9CyPDPPgAAJ-FWsb1ZD5S9KLDcrp1tAhAQADAgADeQADOwQ",
        "🤖 Киборг пятка": "AgACAgIAAxkBAAIEGmn_F5-Rafm_lQwas5MdBusevsDjAALLFWsb1ZD5S0IbouPTTI7pAQADAgADeQADOwQ",
        "💸 Мажор пятка": "AgACAgIAAxkBAAID7Gn_E0wdVHJyBsvIoO7tMTtoucqTAAKhFWsb1ZD5S3-vIun8qbYQAQADAgADeQADOwQ"},
    
    "👑 ИДЕАЛЬНАЯ (1%)": {
        "✳️ Изумрудная пятка": "AgACAgIAAxkBAAIDymn_EjVUFFcrFDQPEQz41_4qvr9RAAKLFWsb1ZD5S7UC99SYLJ7mAQADAgADeQADOwQ",
        "🌠 Космическая пятка": "AgACAgIAAxkBAAIDwGn_EemoJ7b518KihB1fs9FBSN_UAAKFFWsb1ZD5S8yQqj3J3BwSAQADAgADeQADOwQ",
        "🌗 Полудемон-полуангел": "AgACAgIAAxkBAAIELGn_GCw9x1M6KTHO-5DA0k7R4GV2AALUFWsb1ZD5S-aa_6j-GELaAQADAgADeQADOwQ ",
        "❓ Пропавшая пятка": "AgACAgIAAxkBAAIECGn_FE09s8tp4ww0wV6N-SkRNh4QAAKzFWsb1ZD5S8x5gqxhxEe9AQADAgADeQADOwQ"}
}

RARITIES = list(DATA.keys())
WEIGHTS = [45, 25, 15, 8, 4, 2, 1]
TOTAL_CARDS = sum(len(v) for v in DATA.values())

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
class BetState(StatesGroup):
    choosing_rarity = State()
class PromoState(StatesGroup):
    waiting_for_code = State()
last_bet_time = {}
last_time = {}
last_random_time = {}
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Жми на кнопки ниже!", reply_markup=get_kb())

# БАЗА ДАННЫХ
conn = sqlite3.connect("game_db.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
               (user_id INTEGER PRIMARY KEY, 
                name TEXT, 
                username TEXT, 
                items TEXT, 
                balance INTEGER DEFAULT 0, 
                total_opens INTEGER DEFAULT 0, 
                duplicates INTEGER DEFAULT 0, 
                bet_count INTEGER DEFAULT 0)''')
conn.commit()

def get_user_data(uid, n, un):
    cursor.execute("SELECT items, balance, total_opens, duplicates, bet_count FROM users WHERE user_id = ?", (uid,))
    r = cursor.fetchone()
    if r:
        items = set(r[0].split(",")) if r[0] else set()
        return items, r[1], r[2], r[3], r[4]
    
    cursor.execute("INSERT OR IGNORE INTO users (user_id, name, username, items, balance, total_opens, duplicates, bet_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                   (uid, n, un, "", 0, 0, 0, 0))
    conn.commit()
    return set(), 0, 0, 0, 0

def update_user_stats(uid, items, balance, total_opens, duplicates, bet_count):
    cursor.execute("UPDATE users SET items = ?, balance = ?, total_opens = ?, duplicates = ?, bet_count = ? WHERE user_id = ?", 
                   (",".join(list(items)), balance, total_opens, duplicates, bet_count, uid))
    conn.commit()

# ОЖИВИТЕЛЬ
async def handle(r): return web.Response(text="Alive")
async def start_web():
    app = web.Application(); app.router.add_get("/", handle)
    runner = web.AppRunner(app); await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", 10000).start()
def get_kb():
    # Создаем список кнопок заново
    row1 = [KeyboardButton(text="🦶 Выбить пятку")]
    row2 = [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="🏪 Магазин")]
    row3 = [KeyboardButton(text="🎰 Ставки"), KeyboardButton(text="🍀 Рандомайзер")]
    row4 = [KeyboardButton(text="🎒 Инвентарь"), KeyboardButton(text="🏆 Топ игроков")]
    row5 = [KeyboardButton(text="🎁 Промокод")]
    
    # Собираем их в одну клавиатуру
    kb = ReplyKeyboardMarkup(
        keyboard=[row1, row2, row3, row4, row5],
        resize_keyboard=True
    )
    return kb
    
@dp.message(F.photo)
async def get_photo_id(message: Message):
    pid = message.photo[-1].file_id
    await message.answer(f"✅ **ID фото:**\n`{pid}`", parse_mode="Markdown")

# Настройка монет за редкость
MONEY_REWARDS = {
    "⚪ ОБЫЧНАЯ (45%)": 10,
    "🟢 НЕОБЫЧНАЯ (25%)": 20,
    "🔵 РЕДКАЯ (15%)": 50,
    "🟣 ЭПИЧЕСКАЯ (8%)": 150,
    "🔴 МИФИЧЕСКАЯ (4%)": 400,
    "🟡 ЛЕГЕНДАРНАЯ (2%)": 1000,
    "👑 ИДЕАЛЬНАЯ (1%)": 5000
}

@dp.message(F.text == "🦶 Выбить пятку")
async def open_case(message: types.Message):
    user_id = message.from_user.id
    current_time = time.time()
    
    # Кулдаун 1 секунда
    if user_id in last_time and current_time - last_time[user_id] < 1:
        return await message.answer("⏳ Подожди 1 сек.")
    
    # Получаем данные пользователя
    inv, balance, total_opens, duplicates, bet_count = get_user_data(user_id, message.from_user.full_name, message.from_user.username)
    inv = list(inv)
    
    # Выбираем редкость
    res_list = random.choices(RARITIES, weights=WEIGHTS)
    rarity = res_list[0]
    
    # Выбираем предмет
    items = list(DATA[rarity].items())
    item_name, photo_id = random.choice(items)
    reward = MONEY_REWARDS.get(rarity, 0)
    total_opens += 1
    balance += reward

        # Проверяем, есть ли уже такая пятка
    if item_name in inv:
        # Если ЕСТЬ — это повторка
        duplicates += 1
        status = f"♻️ **Повторка!**\nВыпало: {item_name}\nЗачислено: +{reward} 💰"
    else:
        # Если НЕТ — добавляем в список
        inv.append(item_name)
        status = f"✨ **НОВАЯ ПЯТКА!**\nВыпало: {item_name}\nДобавлена в коллекцию! (+{reward} 💰)"
    
    # Сохраняем статистику (теперь бесплатно)
    update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count)
    last_time[user_id] = current_time
    
        # Шансы и иконки для оформления
    chances = {"ОБЫЧНАЯ": "45%", "НЕОБЫЧНАЯ": "25%", "РЕДКАЯ": "15%", "ЭПИЧЕСКАЯ": "10%", "МИФИЧЕСКАЯ": "3%", "ЛЕГЕНДАРНАЯ": "1.5%", "ИДЕАЛЬНАЯ": "1%"}
    icons = {"ОБЫЧНАЯ": "⚪️", "НЕОБЫЧНАЯ": "🟢", "РЕДКАЯ": "🔵", "ЭПИЧЕСКАЯ": "🟣", "МИФИЧЕСКАЯ": "🔴", "ЛЕГЕНДАРНАЯ": "🟡", "ИДЕАЛЬНАЯ": "👑"}
    
    chance = chances.get(rarity, "0%")
    icon = icons.get(rarity, "⚪️")
    
    # Формируем красивый текст
    caption = (
        f"🎉 **Поздравляю** 🎉\n\n"
        f"Вам выпала • **{item_name}**\n"
        f"Редкость • {icon} **{rarity} ({chance})**\n\n"
        f"🎒 Пятка добавлена! (+{reward} 💰)\n"
        f"💰 Твой баланс: **{balance}** монет"
    )
    try:
        await message.answer_photo(photo_id, caption=caption, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"{caption}\n\n(Ошибка фото: {e})")

@dp.message(F.text == "🎒 Инвентарь")
async def show_inventory(message: Message):
        # Проверь, чтобы эта строка стояла с ОДНИМ отступом Tab от края
    inv, balance, total_opens, duplicates, bet_count = get_user_data(message.from_user.id, message.from_user.full_name, message.from_user.username)

    if not inv:
        return await message.answer("📦 Твой инвентарь пуст!")

    total_cards_count = 74 
    unique_items = sorted(list(set(inv)))
    items_list = "\n".join([f"• {item}" for item in unique_items])
    
    text = (
        f"🎒 **Коллекция ({len(unique_items)}/{total_cards_count}):**\n\n"
        f"{items_list}"
    )
    
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text == "🏆 Топ игроков")
async def show_top(message: Message):
    cursor.execute("SELECT name, items FROM users") # Убрали запрос username
    rows = cursor.fetchall()
    if not rows: return await message.answer("Топ пока пуст!")
    
    users_list = []
    for r in rows:
        name_val = str(r[0]) if r[0] else "Игрок"
        items_str = str(r[1]) if r[1] else ""
        
        # Считаем количество только если есть хоть одна пятка
        count = len(items_str.split(",")) if (items_str and items_str.strip()) else 0
        users_list.append({"n": name_val, "c": count})
    
    # Сортируем лидеров
    sorted_u = sorted(users_list, key=lambda x: x["c"], reverse=True)
    
    txt = "🏆 **ТОП КОЛЛЕКЦИОНЕРОВ:**\n\n"
    for i, u in enumerate(sorted_u[:10], 1):
        # Чистим имя от символов, которые ломают Markdown (звездочки, подчеркивания)
        safe_name = u['n'].replace("*", "").replace("_", " ").replace("[", "").replace("`", "")
        txt += f"{i}. {safe_name} — {u['c']}/{TOTAL_CARDS}\n"
    
    try:
        await message.answer(txt, parse_mode="Markdown")
    except:
        # Если всё равно ошибка — шлем без жирного шрифта
        await message.answer(txt.replace("**", ""))

# ВСТАВЛЯЙ СЮДА:
@dp.message(F.text == "👤 Профиль")
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    # ... остальной код профиля ...
    inv, balance, total_opens, duplicates, bet_coun = get_user_data(user_id, message.from_user.full_name, message.from_user.username)
    
    progress = round((len(inv) / TOTAL_CARDS) * 100, 1) if TOTAL_CARDS > 0 else 0
    
    text = (
        f"👤 **ПРОФИЛЬ ИГРОКА**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📝 **Имя:** {message.from_user.full_name}\n"
        f"💰 **Баланс:** {balance} монет\n"
        f"📊 **Прогресс:** {len(inv)}/{TOTAL_CARDS} ({progress}%)\n"
        f"🔄 **Всего открытий:** {total_opens}\n"
        f"♻️ **Повторок выпало:** {duplicates}\n"
        f"━━━━━━━━━━━━━━━"
    )

    try:
        photos = await message.from_user.get_profile_photos(limit=1)
        if photos.total_count > 0:
            await message.answer_photo(photo=photos.photos[0][-1].file_id, caption=text, parse_mode="Markdown")
        else:
            await message.answer(text, parse_mode="Markdown")
    except:
        await message.answer(text, parse_mode="Markdown")

@dp.message(F.text == "🏪 Магазин")
async def show_shop(message: Message):
    # Получаем баланс игрока
    inv, balance, total_opens, duplicates, bet_count = get_user_data(message.from_user.id, message.from_user.full_name, message.from_user.username)
    
    text = (
        f"🛒 **МАГАЗИН СУНДУКОВ**\n"
        f"💰 Твой баланс: **{balance}** монет\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📦 **Эпический сундук** — 1000 💰\n"
        f"└ *Шанс на Идеал: 1%*\n\n"
        f"💎 **Мифический сундук** — 4500 💰\n"
        f"└ *Шанс на Идеал: 5%*\n\n"
        f"👑 **Легендарный сундук** — 15000 💰\n"
        f"└ *Шанс на Идеал: 20%*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"Чтобы купить, нажми на кнопку ниже 👇"
    )
    
    # Сделаем красивые кнопки под сообщением
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Купить Эпический (1000)", callback_data="buy_epic")],
        [InlineKeyboardButton(text="Купить Мифический (4500)", callback_data="buy_mythic")],
        [InlineKeyboardButton(text="Купить Легендарный (15000)", callback_data="buy_legend")]
    ])
    
    await message.answer(text, reply_markup=ikb, parse_mode="Markdown")
@dp.callback_query(F.data.startswith("buy_"))
async def buy_chest(call: types.CallbackQuery):
    user_id = call.from_user.id
    # Получаем данные
    inv, balance, total_opens, duplicates, bet_count = get_user_data(user_id, call.from_user.full_name, call.from_user.username)
    
    # Настройки сундуков: (Цена, Шансы, Название)
    chests = {
        "buy_epic": (1000, [75, 19, 5, 1], ["🟣 ЭПИЧЕСКАЯ (8%)", "🔴 МИФИЧЕСКАЯ (4%)", "🟡 ЛЕГЕНДАРНАЯ (2%)", "👑 ИДЕАЛЬНАЯ (1%)"], "📦 Эпический"),
        "buy_mythic": (4500, [70, 25, 5], ["🔴 МИФИЧЕСКАЯ (4%)", "🟡 ЛЕГЕНДАРНАЯ (2%)", "👑 ИДЕАЛЬНАЯ (1%)"], "💎 Мифический"),
        "buy_legend": (15000, [80, 20], ["🟡 ЛЕГЕНДАРНАЯ (2%)", "👑 ИДЕАЛЬНАЯ (1%)"], "👑 Легендарный")
    }
    
    price, weights, rarities, chest_name = chests[call.data]
    
    if balance < price:
        return await call.answer("❌ Недостаточно монет!", show_alert=True)
    
    # Списываем деньги
    balance -= price
    
    # Крутим сундук
    rarity = random.choices(rarities, weights=weights)[0]
    item_name, photo_id = random.choice(list(DATA[rarity].items()))
    
    is_new = item_name not in inv
    if is_new:
        inv.add(item_name)
    else:
        duplicates += 1
    
    # Сохраняем и отвечаем
    update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count)
    
    status = "🎒 Пятка добавлена!" if is_new else "♻️ Уже была (ушла в повторки)"
    caption = f"🎁 **ОТКРЫТИЕ СУНДУКА: {chest_name}**\n\nВы выбили: **{item_name}**\nРедкость: **{rarity}**\n\n{status}\n💰 Остаток: **{balance}** монет"
    
    await call.message.answer_photo(photo=photo_id, caption=caption, parse_mode="Markdown")
    await call.answer() # Убираем "часики" с кнопки
    async def bet_menu(message: Message):
        user_id = message.from_user.id
        current_time = time.time()
        # Получаем данные (теперь их 5)
        inv, balance, total_opens, duplicates, bet_count = get_user_data(user_id, message.from_user.full_name, message.from_user.username)
    
        # Проверка на 3 попытки и КД 9 часов
        if bet_count >= 3:
            if user_id in last_bet_time and current_time - last_bet_time[user_id] < BET_COOLDOWN:
                rem = int(BET_COOLDOWN - (current_time - last_bet_time[user_id]))
                h, m = rem // 3600, (rem % 3600) // 60
                return await message.answer(f"⏳ Попытки кончились! Новые будут через {h} ч. {m} мин.")
            else:
                bet_count = 0 
                update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count)
    
        txt = f"🎰 **КАЗИНО ПЯТОК**\n💰 Баланс: {balance} монет\n🔔 Попыток: {3 - bet_count} из 3\n\nВыбери редкость:"
        
        buttons = [
            [KeyboardButton(text="⚪ ОБЫЧНАЯ (x1.5)"), KeyboardButton(text="🟢 НЕОБЫЧНАЯ (x2.5)")],
            [KeyboardButton(text="🔵 РЕДКАЯ (x5)"), KeyboardButton(text="🟣 ЭПИЧЕСКАЯ (x10)")],
            [KeyboardButton(text="🔴 МИФИЧЕСКАЯ (x20)"), KeyboardButton(text="🟡 ЛЕГЕНДАРНАЯ (x40)")],
            [KeyboardButton(text="👑 ИДЕАЛЬНАЯ (x80)")],
            [KeyboardButton(text="◀️ Назад")]
        ]
        kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        await message.answer(txt, reply_markup=kb, parse_mode="Markdown")

@dp.message(F.text == "🎰 Ставки")
async def start_bet_cmd(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    current_time = time.time()
    
    # 1. Сначала получаем данные игрока, чтобы узнать bet_count
    inv, balance, total_opens, duplicates, bet_count = get_user_data(user_id, message.from_user.full_name, message.from_user.username)

    # 2. Проверка: если 3 попытки уже использованы
    if bet_count >= 3:
        if user_id in last_bet_time and current_time - last_bet_time[user_id] < BET_COOLDOWN:
            rem = int(BET_COOLDOWN - (current_time - last_bet_time[user_id]))
            h, m = rem // 3600, (rem % 3600) // 60
            return await message.answer(f"⏳ Попытки кончились! Новые будут через {h} ч. {m} мин.")
        else:
            # Если 9 часов прошло — сбрасываем счетчик в базе
            bet_count = 0
            update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count)

    # 3. Если всё ок, показываем меню
    buttons = [
        [KeyboardButton(text="⚪ ОБЫЧНАЯ (x1.5)"), KeyboardButton(text="🟢 НЕОБЫЧНАЯ (x2.5)")],
        [KeyboardButton(text="🔵 РЕДКАЯ (x15)"), KeyboardButton(text="🟣 ЭПИЧЕСКАЯ (x10)")],
        [KeyboardButton(text="🔴 МИФИЧЕСКАЯ (x20)"), KeyboardButton(text="🟡 ЛЕГЕНДАРНАЯ (x40)")],
        [KeyboardButton(text="👑 ИДЕАЛЬНАЯ (x80)")],
        [KeyboardButton(text="◀️ Назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await state.set_state(BetState.choosing_rarity)
    await message.answer("🎰 Выбери редкость, на которую хочешь поставить:", reply_markup=kb)

@dp.message(BetState.choosing_rarity)
async def play_bet(message: types.Message, state: FSMContext):
    # Если нажата кнопка "Назад" прямо во время выбора ставки
        # Если в тексте кнопки есть слово Назад (независимо от смайликов)
        if "Назад" in message.text:
            await state.clear()
            return await back_to_main(message, state) # Обязательно с return!
 # Сразу вызываем функцию главного меню

        user_id = message.from_user.id
    
    # 1. Приводим текст кнопки к ключу из словаря DATA
        mapping = {
            "⚪ ОБЫЧНАЯ (x1.5)": "⚪ ОБЫЧНАЯ (45%)", 
            "🟢 НЕОБЫЧНАЯ (x2.5)": "🟢 НЕОБЫЧНАЯ (25%)",
            "🔵 РЕДКАЯ (x15)": "🔵 РЕДКАЯ (15%)", 
            "🟣 ЭПИЧЕСКАЯ (x10)": "🟣 ЭПИЧЕСКАЯ (8%)",
            "🔴 МИФИЧЕСКАЯ (x20)": "🔴 МИФИЧЕСКАЯ (4%)", 
            "🟡 ЛЕГЕНДАРНАЯ (x40)": "🟡 ЛЕГЕНДАРНАЯ (2%)",
            "👑 ИДЕАЛЬНАЯ (x80)": "👑 ИДЕАЛЬНАЯ (1%)"
    }
    
        user_choice = mapping.get(message.text)
    
    # Если нажато что-то левое, просим выбрать редкость
        if not user_choice:
            return await message.answer("Пожалуйста, выбери редкость кнопками ниже!")

        inv, balance, total_opens, duplicates, bet_count = get_user_data(user_id, message.from_user.full_name, message.from_user.username)
    
        if balance < 100: 
            await state.clear() # Сбрасываем режим ставки, если нет денег
            return await message.answer("❌ Мало монет!")
    
    # Коэффициенты для расчета выплаты
        coeffs = {
            "⚪ ОБЫЧНАЯ (45%)": 1.5, "🟢 НЕОБЫЧНАЯ (25%)": 2.5, 
            "🔵 РЕДКАЯ (15%)": 5.0, "🟣 ЭПИЧЕСКАЯ (8%)": 10.0, 
            "🔴 МИФИЧЕСКАЯ (4%)": 20.0, "🟡 ЛЕГЕНДАРНАЯ (2%)": 40.0, 
            "👑 ИДЕАЛЬНАЯ (1%)": 80.0
    }
    
       # 1. Списываем монеты и прибавляем попытку
        balance -= 100
        bet_count += 1 

    # 2. Если это была 3-я попытка — запускаем таймер на 9 часов
        if bet_count >= 3:
            last_bet_time[user_id] = time.time()

    # 3. Генерируем результат (твой старый код)
        res = random.choices(RARITIES, weights=WEIGHTS)[0]
    
        if res == user_choice:
            win = int(100 * coeffs[user_choice])
            balance += win
            res_txt = f"🎉 **ВЫИГРАЛ!**\nВыпало: {res}\nПриз: **{win}** 💰"
        else:
            res_txt = f"❌ **ПРОИГРАЛ**\nВыпало: {res}\nСтавка сгорела."
    
    # 4. Сохраняем всё в базу, включая новый bet_count
        update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count)
    
    # 3. Добавляем кнопку "Назад" в ответ, чтобы она не пропадала
        kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)
        await message.answer(f"{res_txt}\n\n💰 Баланс: **{balance}**", reply_markup=kb, parse_mode="Markdown")

@dp.message(F.text == "◀️ Назад")
async def back_to_main(message: types.Message, state: FSMContext):
    # Очищаем состояние, чтобы бот не ждал ставку, если мы вышли в меню
    await state.clear() 
    
    buttons = [
        [KeyboardButton(text="🕹 Выбить пятку")],
        [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="🛍 Магазин")],
        [KeyboardButton(text="🎰 Ставки"), KeyboardButton(text="🎲 Рандомайзер")],
        [KeyboardButton(text="🎒 Инвентарь"), KeyboardButton(text="⏳ Топ игроков")],
        [KeyboardButton(text="🎁 Промокод")] # Убедитесь, что тут закрыты обе скобки: ])
    ]
    
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Вы вернулись в главное меню", reply_markup=kb)

# КД для рандомайзера: 9 часов = 32400 секунд
RAND_COOLDOWN = 32400 
last_rand_time = {}
# КД для обычных ставок: 9 часов = 32400 секунд
BET_COOLDOWN = 32400 
last_bet_time = {}

@dp.message(F.text == "🍀 Рандомайзер")
async def start_randomizer_cmd(message: types.Message):
    buttons = [
        [KeyboardButton(text="💎 Ставка 100"), KeyboardButton(text="💎 Ставка 500")],
        [KeyboardButton(text="💎 Ставка 1000")],
        [KeyboardButton(text="◀️ Назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("🎰 **Рандомайзер**\n\nВыбери ставку. Можно утроить её или потерять всё.\n(КД: 9 часов)", reply_markup=kb, parse_mode="Markdown")

@dp.message(F.text.startswith("💎 Ставка"))
async def play_randomizer(message: types.Message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_rand_time and current_time - last_rand_time[user_id] < RAND_COOLDOWN:
        rem = int(RAND_COOLDOWN - (current_time - last_rand_time[user_id]))
        h, m = rem // 3600, (rem % 3600) // 60
        return await message.answer(f"⏳ Жди еще {h} ч. {m} мин.")

    try:
        bet = int(message.text.split()[-1])
    except: return

    inv, balance, total_opens, duplicates, bet_count = get_user_data(user_id, message.from_user.full_name, message.from_user.username)
    if balance < bet:
        return await message.answer(f"❌ Не хватает монет! Нужно {bet} 💰")

        # --- НОВАЯ ЛОГИКА РАНДОМА ---
    roll = random.randint(1, 10)
    
    if roll <= 4:
        multiplier = 0
        balance -= bet
        res = f"❌ **Проигрыш**\n🎲 Число: `{roll}` | Множитель: `x0`"
    elif roll == 5:
        multiplier = 1
        # Баланс не меняем (возврат)
        res = f"🤝 **Возврат**\n🎲 Число: `{roll}` | Множитель: `x1`"
    elif 6 <= roll <= 8:
        multiplier = 3
        win = bet * multiplier
        balance += win
        res = f"🔥 **Удача!**\n🎲 Число: `{roll}` | Множитель: `x3`"
    elif roll == 9:
        multiplier = 5
        win = bet * multiplier
        balance += win
        res = f"💎 **Ого!**\n🎲 Число: `{roll}` | Множитель: `x5`"
    else:  # Это если выпало 10
        multiplier = 10
        win = bet * multiplier
        balance += win
        res = f"👑 **ДЖЕКПОТ!**\n🎲 Число: `{roll}` | Множитель: `x10`"
    # ----------------------------

    last_rand_time[user_id] = current_time
    update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count)
    await message.answer(f"{res}\n💰 Баланс: **{balance}**", parse_mode="Markdown")
    
@dp.message(F.text == "🎁 Промокод")
async def promo_start_cmd(message: types.Message, state: FSMContext):
    # Говорим боту ждать ввода текста
    await state.set_state(PromoState.waiting_for_code)
    
    # Показываем только кнопку "Назад"
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Назад")]], resize_keyboard=True)
    
    await message.answer("✍️ **Введи секретный промокод:**", reply_markup=kb, parse_mode="Markdown")
    
# 1. Сам список кодов
ACTIVE_PROMOS = {
    "TOP_CARD": [1488, 2]
}

# 2. Логика проверки (вставляй СРАЗУ после promo_start_cmd)
@dp.message(PromoState.waiting_for_code)
async def check_promo_cmd(message: types.Message, state: FSMContext):
    if message.text == "◀️ Назад":
        await state.clear()
        return await back_to_main(message, state)

    code = message.text.strip()

    if code in ACTIVE_PROMOS:
        reward, limit = ACTIVE_PROMOS[code]
        
        if limit > 0:
            user_id = message.from_user.id
            inv, balance, total_opens, duplicates, bet_count = get_user_data(user_id, message.from_user.full_name, message.from_user.username)
            
            balance += reward
            ACTIVE_PROMOS[code][1] -= 1 # Уменьшаем число активаций
            
            update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count)
            
            # Внимательно проверь кавычку в конце этой строки:
            await message.answer(f"✅ **Код активирован!**\n💰 Начислено: **{reward}** монет.\nОсталось активаций: {ACTIVE_PROMOS[code]}")
            
            await state.clear()
            await back_to_main(message, state)
        else:
            await message.answer("❌ Этот код уже закончился!")
    else:
        await message.answer("❌ Неверный код! Попробуй еще раз или нажми 'Назад'.")

async def main():
    # Добавляем новые колонки в базу, если их еще нет
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN balance INTEGER DEFAULT 0")
        cursor.execute("ALTER TABLE users ADD COLUMN total_opens INTEGER DEFAULT 0")
        cursor.execute("ALTER TABLE users ADD COLUMN duplicates INTEGER DEFAULT 0")
        conn.commit()
    except:
        pass # Если колонки уже созданы, просто идем дальше
    
    await start_web()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
