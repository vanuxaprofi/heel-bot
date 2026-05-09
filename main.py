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
        "🤡 Клоунская пятка": "AgACAgIAAxkBAAID-Gn_E6OYGkahSIly7Upk6h6I2keXAAKG FWsb1ZD5SlHVO8XInLN-AQADAgADeQADOwQ",
        "🇲🇽 Мексиканская пятка": "AgACAgIAAxkBAAID_mn_F9oimGNZFPiPeunZwvsjuHBD AAktFWsb1ZD5S_PQRif6df3IAQADAgADeQADOwQ",
        "🇫🇷 Французская пятка": "AgACAgIAAxkBAAIEAmn_FCZz8u8MT60MA_kvTEaAAT77 AAJ5FWsb1ZD5S_UuZDn jRFFEjgEAAwIAA3kAAzsE",
        "📟 Голограмная пятка": "AgACAgIAAxkBAAIEBmn_FEEKvBduRVZ4-Ub10fNgscEr vAAKyFWsb1ZD5SXQ_hu5an715AQADAgADeQADOwQ",
        "🤢 Вонючая пятка": "AgACAgIAAxkBAAID1Gn_EREAATE6n6-nLD6K2arJWCA4 RgACkFWsb1ZD5S_UsLXIuYe5Zp3gEAAwIAA3kAAzsE",
        "🍓 Клубничная пятка": "AgACAgIAAxkBAAIDmmn_EhRNxi8t882Z96BD3D-ZhwFp AAK1FWsb1ZD5S_7DlOkHFuw5AQADAgADeQADOwQ",
        "⛓️ Зек пятка": "AgACAgIAAxkBAAID6Gn_EpkcaHjRrqh8q3mOIcOaiPRIAAKP FWsb1ZD5S2-1hzZcafgaAQADAgADeQADOwQ",
        "🥈 Серебряная пятка": "AgACAgIAAxkBAAIDkGn_D0GvsOp0rze9Ruv9-H92M9-J AAJeFWsb1ZD5Sz1Z9RQS6uoEAQADAgADeQADOwQ",
        "🟡 Миньон пятка": "AgACAgIAAxkBAAIDnGn_Dtd1A6Rkv23l9eW1z3fqr7gn AATPFWsb1ZD5S3_ClOLpN5CAQADAgADeQADOwQ",
        "📦 Коробка с пяткой": "AgACAgIAAxkBAAID8Gn_E2Wtbfnba_8Wu_Wtb_mfbi5YAAKjFWsb1ZD5S2mhBaMPb7TtAQADAgADeQADO",
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

WEIGHTS = [0.45, 0.25, 0.15, 0.08, 0.04, 0.02, 0.01]
RARITIES = list(DATA.keys())
TOTAL_CARDS = sum(len(v) for v in DATA.values())

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# БАЗА ДАННЫХ
conn = sqlite3.connect("game_db.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT, username TEXT, items TEXT)')
conn.commit()

def get_items(uid, n, un):
    cursor.execute("SELECT items FROM users WHERE user_id = ?", (uid,))
    r = cursor.fetchone()
    if r and r[0]: return set(r[0].split(","))
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", (uid, n, un, ""))
    conn.commit()
    return set()

def save_items(uid, n, un, items):
    cursor.execute("REPLACE INTO users VALUES (?, ?, ?, ?)", (uid, n, un, ",".join(list(items))))
    conn.commit()

# ОЖИВИТЕЛЬ
async def handle(r): return web.Response(text="Alive")
async def start_web():
    app = web.Application(); app.router.add_get("/", handle)
    runner = web.AppRunner(app); await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", 10000).start()

def get_kb():
    kb = [[KeyboardButton(text="🦶 Пятка"), KeyboardButton(text="🎒 Инвентарь")], [KeyboardButton(text="🏆 Топ игроков")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(F.photo)
async def get_id(m: Message):
    pid = m.photo[-1].file_id
    await m.answer(f"✅ **ID цієї фотографії:**\n\n`{pid}`", parse_mode="Markdown")

@dp.message(F.text == "🦶 Пятка")
async def roll(m: Message):
    uid = m.from_user.id
    inv = get_items(uid, m.from_user.full_name, m.from_user.username)
    if len(inv) >= TOTAL_CARDS:
        return await m.answer("🏆 Вы собрали все пятки! 🎉")

    res = None
    for _ in range(15):
        rar = random.choices(RARITIES, weights=WEIGHTS)[0]
        name, pid = random.choice(list(DATA[rar].items()))
        if name not in inv:
            res = (name, rar, pid)
            break
    if not res:
        rar = random.choices(RARITIES, weights=WEIGHTS)[0]
        name, pid = random.choice(list(DATA[rar].items()))
        res = (name, rar, pid)

    name, rar, pid = res
        if is_new:
        inv.add(item_name)
        save_items(user_id, message.from_user.full_name, message.from_user.username, inv)
    
    last_time[user_id] = current_time
    status = "🎒 Пятка успешно добавлена!" if is_new else "♻️ Уже есть!"
    caption = f"🎉 **Поздравляю** 🎉\n\nВам выпала • **{item_name}**\nРедкость • **{rarity}**\n\n{status}"
    
    try:
        await message.answer_photo(photo=photo_id, caption=caption, parse_mode="Markdown")
    except:
        await message.answer(caption)

@dp.message(F.text == "🎒 Инвентарь")
async def show_inventory(message: Message):
    inv = get_user_items(message.from_user.id, message.from_user.full_name, message.from_user.username)
    if not inv: return await message.answer("Пусто!")
    text = f"🎒 **Коллекция ({len(inv)}/{TOTAL_CARDS}):**\n\n" + "\n".join([f"• {i}" for i in sorted(list(inv))])
    await message.answer(text)

@dp.message(F.text == "🏆 Топ игроков")
async def show_top(message: Message):
    cursor.execute("SELECT name, username, items FROM users")
    rows = cursor.fetchall()
    if not rows: return await message.answer("Топ пуст!")
    processed = []
    for r in rows:
        count = len(r[2].split(",")) if r[2] else 0
        processed.append({"n": r[0], "u": r[1], "c": count})
    sorted_u = sorted(processed, key=lambda x: x["c"], reverse=True)
    text = "🏆 **ТОП КОЛЛЕКЦИОНЕРОВ:**\n\n"
    for i, u in enumerate(sorted_u[:10], 1):
        un = f" (@{u['u']})" if u['u'] else ""
        text += f"{i}. {u['n']}{un} — {u['c']}/{TOTAL_CARDS}\n"
    await message.answer(text, parse_mode="Markdown")

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
