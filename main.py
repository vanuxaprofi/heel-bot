import asyncio
import random
import time
import os
import sqlite3
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

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
dp = Dispatcher()
last_time = {}
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Жми на кнопки ниже!", reply_markup=get_kb())


# БАЗА ДАННЫХ
conn = sqlite3.connect("game_db.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT, username TEXT, items TEXT)')
conn.commit()

def get_user_data(uid, n, un):
    cursor.execute("SELECT items, balance, total_opens, duplicates FROM users WHERE user_id = ?", (uid,))
    r = cursor.fetchone()
    if r:
        items = set(r[0].split(",")) if r[0] else set()
        return items, r[1], r[2], r[3]
    
    cursor.execute("INSERT OR IGNORE INTO users (user_id, name, username, items, balance, total_opens, duplicates) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (uid, n, un, "", 0, 0, 0))
    conn.commit()
    return set(), 0, 0, 0

def update_user_stats(uid, items, balance, total_opens, duplicates):
    cursor.execute("UPDATE users SET items = ?, balance = ?, total_opens = ?, duplicates = ? WHERE user_id = ?", 
                   (",".join(list(items)), balance, total_opens, duplicates, uid))
    conn.commit()

# ОЖИВИТЕЛЬ
async def handle(r): return web.Response(text="Alive")
async def start_web():
    app = web.Application(); app.router.add_get("/", handle)
    runner = web.AppRunner(app); await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", 10000).start()
def get_kb():
    kb = [
        [KeyboardButton(text="🦶 Пятка"), KeyboardButton(text="🎒 Инвентарь")],
        [KeyboardButton(text="🏆 Топ игроков"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="🛒 Магазин"), KeyboardButton(text="🎰 Ставки")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
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

@dp.message(F.text == "🦶 Пятка")
async def open_card(message: Message):
    try:
        user_id = message.from_user.id
        current_time = time.time()
        
        # КД 5 секунд
        if user_id in last_time and current_time - last_time[user_id] < 5:
            return await message.answer(f"⏳ Подожди {int(5 - (current_time - last_time[user_id]))} сек.")

        # Получаем данные
        inv, balance, total_opens, duplicates = get_user_data(user_id, message.from_user.full_name, message.from_user.username)
        
        # ВЫБОР РЕДКОСТИ (с проверкой индекса)
        rarity_list = random.choices(RARITIES, weights=WEIGHTS)
        if not rarity_list:
            return await message.answer("Ошибка: не удалось выбрать редкость.")
        rarity = rarity_list[0]

        # ВЫБОР КАРТЫ
        if rarity not in DATA:
            return await message.answer(f"Ошибка: категория {rarity} не найдена в DATA.")
        
        items = list(DATA[rarity].items())
        item_name, photo_id = random.choice(items)
        
        # ДЕНЬГИ И СТАТИСТИКА
        reward = MONEY_REWARDS.get(rarity, 0)
        balance += reward
        total_opens += 1
        
        is_new = item_name not in inv
        if is_new:
            inv.add(item_name)
            status = f"🎒 Пятка добавлена! (+{reward} 💰)"
        else:
            duplicates += 1
            status = f"♻️ Уже есть! Получено (+{reward} 💰)"
        
        # СОХРАНЕНИЕ
        update_user_stats(user_id, inv, balance, total_opens, duplicates)
        last_time[user_id] = current_time
        
        caption = f"🎉 **Поздравляю** 🎉\n\nВам выпала • **{item_name}**\nРедкость • **{rarity}**\n\n{status}\n💰 Твой баланс: **{balance}** монет"
        
        try:
            await message.answer_photo(photo=photo_id, caption=caption, parse_mode="Markdown")
        except Exception as e:
            await message.answer(f"{caption}\n\n(Ошибка фото: {e})")

    except Exception as e:
        await message.answer(f"❌ Произошла ошибка: {e}")

@dp.message(F.text == "🎒 Инвентарь")
async def show_inventory(message: Message):
    # Исправляем вызов функции (теперь get_user_data)
    inv, balance, total_opens, duplicates = get_user_data(message.from_user.id, message.from_user.full_name, message.from_user.username)
    
    if not inv: 
        return await message.answer("Твой инвентарь пуст!")
    
    # Собираем список предметов
    text = f"🎒 **Коллекция ({len(inv)}/{TOTAL_CARDS}):**\n\n" + "\n".join([f"• {i}" for i in sorted(list(inv))])
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
async def show_profile(message: Message):
    user_id = message.from_user.id
    inv, balance, total_opens, duplicates = get_user_data(user_id, message.from_user.full_name, message.from_user.username)
    
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

@dp.message(F.text == "🛒 Магазин")
async def show_shop(message: Message):
    # Получаем баланс игрока
    inv, balance, total_opens, duplicates = get_user_data(message.from_user.id, message.from_user.full_name, message.from_user.username)
    
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
    inv, balance, total_opens, duplicates = get_user_data(user_id, call.from_user.full_name, call.from_user.username)
    
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
    update_user_stats(user_id, inv, balance, total_opens, duplicates)
    
    status = "🎒 Пятка добавлена!" if is_new else "♻️ Уже была (ушла в повторки)"
    caption = f"🎁 **ОТКРЫТИЕ СУНДУКА: {chest_name}**\n\nВы выбили: **{item_name}**\nРедкость: **{rarity}**\n\n{status}\n💰 Остаток: **{balance}** монет"
    
    await call.message.answer_photo(photo=photo_id, caption=caption, parse_mode="Markdown")
    await call.answer() # Убираем "часики" с кнопки
@dp.message(F.text == "🎰 Ставки")
async def bet_menu(message: Message):
    user_id = message.from_user.id
    current_time = time.time()
    
    # Проверка КД 9 часов (32400 секунд)
    if user_id in last_bet_time and current_time - last_bet_time[user_id] < 32400:
        rem = int(32400 - (current_time - last_bet_time[user_id]))
        return await message.answer(f"⏳ Ставки будут доступны через {rem // 3600}ч. {(rem % 3600) // 60}мин.")

    inv, balance, total_opens, duplicates = get_user_data(user_id, message.from_user.full_name, message.from_user.username)
    
    txt = (
        f"🎰 **КАЗИНО ПЯТОК**\n💰 Баланс: **{balance}**\n\n"
        f"Ставка: **100 💰**\n"
        f"Выбери редкость (награда за риск):\n"
        f"⚪ x1.5 | 🟢 x2.5 | 🔵 x5.0\n"
        f"🟣 x10 | 🔴 x20 | 🟡 x40 | 👑 x80\n\n"
        f"⚠️ Попытка раз в 9 часов!"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        # Важно: callback_data должна СТРОГО совпадать с твоими редкостями в DATA
        bkb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⚪ Обычная", callback_data="bet_⚪ ОБЫЧНАЯ (45%)")],
            [InlineKeyboardButton(text="🟢 Необычная", callback_data="bet_🟢 НЕОБЫЧНАЯ (25%)")],
            [InlineKeyboardButton(text="🔵 Редкая", callback_data="bet_🔵 РЕДКАЯ (15%)")],
            [InlineKeyboardButton(text="🟣 Эпик", callback_data="bet_🟣 ЭПИЧЕСКАЯ (8%)")],
            [InlineKeyboardButton(text="🔴 Мифик", callback_data="bet_🔴 МИФИЧЕСКАЯ (4%)")],
            [InlineKeyboardButton(text="🟡 Легенда", callback_data="bet_🟡 ЛЕГЕНДАРНАЯ (2%)")],
            [InlineKeyboardButton(text="👑 ИДЕАЛ", callback_data="bet_👑 ИДЕАЛЬНАЯ (1%)")]
        ])
    await message.answer(txt, reply_markup=bkb, parse_mode="Markdown")

@dp.callback_query(F.data.startswith("bet_"))
async def play_bet(call: types.CallbackQuery):
    user_id = call.from_user.id
    choice = call.data.replace("bet_", "")
    inv, balance, total_opens, duplicates = get_user_data(user_id, call.from_user.full_name, call.from_user.username)
    
    if balance < 100: return await call.answer("❌ Мало монет!", show_alert=True)
    
           coeffs = {
        "⚪ ОБЫЧНАЯ (45%)": 1.5, 
        "🟢 НЕОБЫЧНАЯ (25%)": 2.5, 
        "🔵 РЕДКАЯ (15%)": 5.0,
        "🟣 ЭПИЧЕСКАЯ (8%)": 10.0, 
        "🔴 МИФИЧЕСКАЯ (4%)": 20.0, 
        "🟡 ЛЕГЕНДАРНАЯ (2%)": 40.0, 
        "👑 ИДЕАЛЬНАЯ (1%)": 80.0
    }
    
    balance -= 100
    last_bet_time[user_id] = time.time()
    res = random.choices(RARITIES, weights=WEIGHTS)[0]
    
    if res == choice:
        win = int(100 * coeffs[choice])
        balance += win
        m = f"✅ **ВЫИГРАЛ!**\nВыпала: {res}\nПриз: **{win}** 💰"
    else:
        m = f"❌ **ПРОИГРАЛ**\nВыпала: {res}\nСтавка сгорела."
    
    update_user_stats(user_id, inv, balance, total_opens, duplicates)
    await call.message.edit_text(f"{m}\n💰 Баланс: **{balance}**\n⏳ Ждем 9 часов.", parse_mode="Markdown")
    await call.answer()

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
