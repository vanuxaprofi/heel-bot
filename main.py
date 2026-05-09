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
    "⚪ ОБЫЧНАЯ": {
        "🌾 Сено пятка": "AgACAgIAAxkBAAPlaf2Pp7k7PXrNT0d9TgjIgwKFfDoAArwTaxv04fFLE9Pz-Di4gQsBAAMCAAN5AAM7BA",
        "🌱 Земляная пятка": "AgACAgIAAxkBAAO_af2PJQUJtkxccatimHfZXuVHkx0AAqUTaxv04fFL0X9OPtULRNgBAAMCAAN5AAM7BA",
        "💧 Водяная пятка": "AgACAgIAAxkBAAID1mn_ErtLjnFoY0ceK0ZoH5TgeKkAA5UVaxvVkPlLRu8mnryTmsABAAMCAAN5AAM7BA",
        "🌬️ Небесная пятка": "AgACAgIAAxkBAAIDsGn_EICSBiM3RKbdcxYHzeCD2woiAAJ3FWsb1ZD5S-WxYxtzJmHbAQADAgADeQADOwQ",
        "🥛 Стеклянная пятка": "AgACAgIAAxkBAAIDsGn_EICSBiM3RKbdcxYHzeCD2woiAAJ3FWsb1ZD5S-WxYxtzJmHbAQADAgADeQADOwQ",
        "🍌 Банановая пятка": "AgACAgIAAxkBAAID2Gn_EsXPbjclbQ_vojegBC364Lg3AAKWFWsb1ZD5Szj9AqhodMO1AQADAgADeQADOwQ",
        "🔮 Магическая пятка": "AgACAgIAAxkBAAIDumn_Eb6e7rfobGxfplOZYbv_7eE8AAKAFWsb1ZD5S9v9Gt16pd62AQADAgADeQADOwQ",
        "💪 Накачанная пятка": "AgACAgIAAxkBAAIDtGn_EZlWMLbzG4aNXehsEP7ut-Z0AAJ8FWsb1ZD5S9B_j9bB8f6DAQADAgADeQADOwQ",
        "🧸 Плюшевая пятка": "AgACAgIAAxkBAAIEFmn_F4T3_GiR1Nk4oAl51ZcUbob6AALJFWsb1ZD5S6nAVH_ypfpMAQADAgADeQADOwQ",
        "☢️ Радиоактивная пятка": "AgACAgIAAxkBAAIEFGn_F3a-quY8EHRJvgKrZFbVhQABMQACyBVrG9WQ-UtOVEPEprm7ygEAAwIAA3kAAzsE
",
        "🪵 Деревянная пятка": "AgACAgIAAxkBAAID9mn_E5n2qzGBAAE9LED2URMWj-QEpwACpxVrG9WQ-Uvx3fvfeUnwHgEAAwIAA3kAAzsE",
        "🌫️ Пятка в тумане": "AgACAgIAAxkBAAIEIGn_F8Uh4fN9xFNabDa6SZ-x8BrfAALPFWsb1ZD5S7t-XIWi8EH4AQADAgADeQADOwQ",
        "❄️ Снежная пятка": "AgACAgIAAxkBAAID6Gn_Ey5HXjmTxgwGf_9U2Urqgi6KAAKeFWsb1ZD5S-XTgpndBk9cAQADAgADeQADOwQ"
    },
    "🟢 НЕОБЫЧНАЯ": {
        "💩 Какашка пятка": "AgACAgIAAxkBAAPFaf2PPgoYWtmcoFpNxv0jaTKVJZMAAqoTaxv04fFL3v6kk9fTTEgBAAMCAAN5AAM7BA",
        "🤢 Вонючая пятка": "AgACAgIAAxkBAAID1Gn_ErEAAT68h6-mLD8K2arJWCA4RgACkhVrG9WQ-UsiX3uYe6Zp3gEAAwIAA3kAAzsE",
        "🍓 Клубничная пятка": "AgACAgIAAxkBAAIDxmn_EhRNxlBtB82Z968OJD-ZhmfpAAKJFWsb1ZD5S_7D1Okhfuw5AQADAgADeQADOwQ",
        "⛓️ Зек пятка": "AgACAgIAAxkBAAID0Gn_EpkcaHjRrqH8q2nCIeOaiPRUAAKPFWsb1ZD5S2-ihZzcaFgaAQADAgADeQADOwQ",
        "🥈 Серебряная пятка": "AgACAgIAAxkBAAIDkWn_DOGvpOsOrze9Ruv9-W92M9-JAAJeFWsb1ZD5SzlZ9RQSeuoEAQADAgADeQADOwQ",
        "🟡 Миньон пятка": "AgACAgIAAxkBAAIDb2n_BtDlA6Rkv23l9eWlz3fqr7gnAAIPFWsb1ZD5S3_CiOLpN5CRAQADAgADeQADOwQ",
        "📦 Коробка с пяткой": "AgACAgIAAxkBAAID8Gn_E2Wtbfnba_8Wu_Wtb_mfbi5YAAKjFWsb1ZD5S2mhBaMPb7TtAQADAgADeQADOwQ",
        "🧊 Ледяная пятка": "AgACAgIAAxkBAAIEMmn_ID6A2Es4E2MhErV_offnKs8fAAIeFmsb1ZD5S5VU-JhnyFMPAQADAgADeQADOwQ",
        "🌸 Цветочная пятка": "AgACAgIAAxkBAAIDhmn_CtswJ5giZuyE6wT4QvPPuR5_AAJUFWsb1ZD5S_OtiSyyNSJnAQADAgADeQADOwQ",
        "💍 Свадебная пятка": "AgACAgIAAxkBAAID5mn_EyO0HM8BN4eH0tE-VGgw3dQxAAKdFWsb1ZD5S9wUM1L44LZ4AQADAgADeQADOwQ"
    },
    "🔵 РЕДКАЯ": {
        "🎀 Пикми пятка": "AgACAgIAAxkBAAPhaf2PnXKz5ieWdDUui3Ss2GLkYP4AAroTaxv04fFLuKGCU27-HowBAAMCAAN5AAM7BA",
        "🐾 Фурри пятка": "AgACAgIAAxkBAAIDj2n_DJvAZI1yYmTi7ETMNuPloWoIAAJdFWsb1ZD5S7qH4pa_N81uAQADAgADeQADOwQ",
        "🎎 Аниме пятка": "AgACAgIAAxkBAAID2mn_Etbb9x5TXSP0kcUVP8p4gdgIAAKXFWsb1ZD5S1o9GcEaYzSaAQADAgADeQADOwQ",
        "✏️ Нарисованная пятка": "AgACAgIAAxkBAAIDsmn_EXK9W1WYn1b34ohrGHOCYXdWAAJ7FWsb1ZD5S3hds3yfLWdPAQADAgADeQADOwQ
",
        "🌵 Шиповая пятка": "AgACAgIAAxkBAAIDxGn_EgoMvT-8pJe8xInio8TRc90JAAKIFWsb1ZD5Sx6pxr5qhIsvAQADAgADeQADOwQ",
        "🦴 Костяная пятка": "AgACAgIAAxkBAAIDvmn_EdeXeFQnKpc3c5Mz3Ds1LXqEAAKEFWsb1ZD5S8FM9CNMhqI1AQADAgADeQADOwQ",
        "🍫 Шоколадная пятка": "AgACAgIAAxkBAAIEGGn_F4-ow0fL1mD7OenMCEY115w4AALKFWsb1ZD5S0fBJ4g2P5YsAQADAgADeQADOwQ",
        "🍔 Жирная пятка": "AgACAgIAAxkBAAID7mn_E1k9sSVYlSc8fIJwfZkC08z2AAKiFWsb1ZD5SxzCGexoej_GAQADAgADeQADOwQ",
        "🧱 Кирпичная пятка": "AgACAgIAAxkBAAIEEGn_FIer9aQdFCfUiCOx3GdyuVR3AAK3FWsb1ZD5S9frhYxtdwABZgEAAwIAA3kAAzsE"
    },
    "🟣 ЭПИЧЕСКАЯ": {
        "📜 Древняя пятка": "AgACAgIAAxkBAAIEDmn_FHIDuHJ8g9yLUs4oqYtuWan6AAK1FWsb1ZD5S6THTIczYFOcAQADAgADeQADOwQ",
        "✨ Золотая пятка": "AgACAgIAAxkBAAIDzGn_Ej5fMNPzcmpN9zvuH795saJgAAKMFWsb1ZD5S6py6qBOf8AhAQADAgADeQADOwQ",
        "🌈 Неоновая пятка": "AgACAgIAAxkBAAIDrmn_DbHI0Jqj4IsXgmrGs6J4iREMAAJnFWsb1ZD5SzZtAAFMEVVnMwEAAwIAA3kAAzsE",
        "👤 Теневая пятка": "AgACAgIAAxkBAAID5Gn_ExizvCcHapz0JFcU_tmhDOpfAAKcFWsb1ZD5S_kRM",
        "🔥 Лавовая пятка": "AgACAgIAAxkBAAIDvGn_EcvvHKIqgeeeY1VxyQf7panyAAKCFWsb1ZD5S6Nlv1VtAdXFAQADAgADeQADOwQ",
        "🌌 Гравити фолз пятка": "AgACAgIAAxkBAAID4mn_EwtwCf_6dTwAAdszn7WaUH-7PwACmxVrG9WQ-UtpmdUHcfnbmAEAAwIAA3kAAzsE",
        "🌊 Подводная пятка": "AgACAgIAAxkBAAID8mn_E28DXmAeisv9AyjTY4svxGqWAAKkFWsb1ZD5S6v3dYj_UdtbAQADAgADeQADOwQ",
        "🍕 Пицца пятка": "AgACAgIAAxkBAAID9Gn_E427KoTE1WKBQhGiiMFJKTT6AAKlFWsb1ZD5S9jLZsS2gyuJAQADAgADeQADOwQ"
    },
    "🔴 МИФИЧЕСКАЯ": {
        "👹 Демоническая пятка": "AgACAgIAAxkBAAID4Gn_Ev0bSON3TUcSQ6EHpC3SseeRAAKaFWsb1ZD5SyPWO53iJqvZAQADAgADeQADOwQ",
        "😇 Ангельская пятка": "AgACAgIAAxkBAAID3Gn_EuUcieIvGWulfO1wSRJIU1wFAAKYFWsb1ZD5SzqKAAGkMIfIewEAAwIAA3kAAzsE",
        "👑 Король пятка": "AgACAgIAAxkBAAIDwmn_EfrCpPVh4kGwvkzJSoYnwgAB1AAChxVrG9WQ-Uv47f3uLJgsLwEAAwIAA3kAAzsE",
        "🏳️‍🌈 Радужная пятка": "AgACAgIAAxkBAAIDqGn_DQ4FuWv7qkFjbzjn_OUNb0HiAAJjFWsb1ZD5S9yYkliLFV_UAQADAgADeQADOwQ",
        "👽 Инопланетная пятка": "AgACAgIAAxkBAAIEDGn_FGOlrhNtDREpmrQ70Q-8Ln3hAAK0FWsb1ZD5S9Ys73tzWqnsAQADAgADeQADOwQ"
    },
    "🟡 ЛЕГЕНДАРНАЯ": {
        "💎 Алмазная пятка": "AgACAgIAAxkBAAID3mn_EvLdDY1r-ZvW77novm5DuhXVAAKZFWsb1ZD5S18ODlfYhh8NAQADAgADeQADOwQ",
        "⚡ Зевс пятка": "AgACAgIAAxkBAAIDtmn_EaLijTggPq-ojfCradBc21yRAAJ9FWsb1ZD5SxfNkQw-ybnuAQADAgADeQADOwQ",
        "💀 Мертвая пятка": "AgACAgIAAxkBAAIDuGn_Ea7HrThA8-StQoFK9CyPDPPgAAJ-FWsb1ZD5S9KLDcrp1tAhAQADAgADeQADOwQ",
        "🤖 Киборг пятка": "AgACAgIAAxkBAAIEGmn_F5-Rafm_lQwas5MdBusevsDjAALLFWsb1ZD5S0IbouPTTI7pAQADAgADeQADOwQ",
        "💸 Мажор пятка": "AgACAgIAAxkBAAID7Gn_E0wdVHJyBsvIoO7tMTtoucqTAAKhFWsb1ZD5S3-vIun8qbYQAQADAgADeQADOwQ"
    },
    "👑 ИДЕАЛЬНАЯ": {
        "✳️ Изумрудная пятка": "AgACAgIAAxkBAAIDymn_EjVUFFcrFDQPEQz41_4qvr9RAAKLFWsb1ZD5S7UC99SYLJ7mAQADAgADeQADOwQ",
        "🌠 Космическая пятка": "AgACAgIAAxkBAAIDwGn_EemoJ7b518KihB1fs9FBSN_UAAKFFWsb1ZD5S8yQqj3J3BwSAQADAgADeQADOwQ",
        "🌗 Полудемон-полуангел": "AgACAgIAAxkBAAIELGn_GCw9x1M6KTHO-5DA0k7R4GV2AALUFWsb1ZD5S-aa_6j-GELaAQADAgADeQADOwQ ",
        "❓ Пропавшая пятка": "AgACAgIAAxkBAAIECGn_FE09s8tp4ww0wV6N-SkRNh4QAAKzFWsb1ZD5S8x5gqxhxEe9AQADAgADeQADOwQ"
    }
}

# ШАНСЫ (ВЕСА)
WEIGHTS = [45, 25, 15, 8, 4, 2, 1]
RARITIES = list(DATA.keys())
TOTAL_CARDS = sum(len(v) for v in DATA.values())

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- БАЗА ДАННЫХ (SQLite) ---
conn = sqlite3.connect("game_db.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT, username TEXT, items TEXT)')
conn.commit()

def get_items(uid, n, un):
    cursor.execute("SELECT items FROM users WHERE user_id = ?", (uid,))
    r = cursor.fetchone()
    if r: return set(r[0].split(",")) if r[0] else set()
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", (uid, n, un, ""))
    conn.commit()
    return set()

def save_items(uid, n, un, items):
    cursor.execute("REPLACE INTO users VALUES (?, ?, ?, ?)", (uid, n, un, ",".join(list(items))))
    conn.commit()

# --- ВЕБ-СЕРВЕР (ДЛЯ RENDER) ---
async def handle(r): return web.Response(text="Heel Bot Alive")
async def start_web():
    app = web.Application(); app.router.add_get("/", handle)
    runner = web.AppRunner(app); await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", 10000).start()

def get_kb():
    kb = [[KeyboardButton(text="🦶 Пятка"), KeyboardButton(text="🎒 Инвентарь")], [KeyboardButton(text="🏆 Топ игроков")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def start(m: Message):
    await m.answer(f"🦶 Игра запущена! В коллекции {TOTAL_CARDS} пяток. Соберешь все?", reply_markup=get_kb())

@dp.message(F.photo)
async def get_id(m: Message):
    pid = m.photo[-1].file_id
    await m.answer(f"✅ **ID этой фотографии:**\n\n`{pid}`", parse_mode="Markdown")

@dp.message(F.text == "🦶 Пятка")
async def roll(m: Message):
    uid = m.from_user.id
    name_user = m.from_user.full_name
    user_n = m.from_user.username
    inv = get_items(uid, name_user, user_n)
    
    if len(inv) >= TOTAL_CARDS:
        return await m.answer("🏆 Вы собрали АБСОЛЮТНО ВСЕ пятки! Вы — Король Пяток! 🎉")

    # Пытаемся выбить новую (10 попыток)
    res = None
    for _ in range(10):
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
    is_new = name not in inv
    if is_new:
        inv.add(name)
        save_items(uid, name_user, user_n, inv)
    
    status_msg = "🎒 Пятка успешно добавлена в ваш инвентарь!" if is_new else "♻️ Такая пятка у вас уже есть!"
    
    cap = (f"🎉 **Поздравляю** 🎉\n\n"
           f"Вам выпала • **{name}**\n"
           f"Редкость • **{rar}**\n\n"
           f"{status_msg}")
    
    try:
        await m.answer_photo(photo=pid, caption=cap, parse_mode="Markdown")
    except:
        await m.answer(f"🎉 **Поздравляю** 🎉\n\nВам выпала • **{name}**\nРедкость • **{rar}**\n\n(Фото еще не добавлено)")

    if len(inv) == TOTAL_CARDS and is_new:
        await m.answer("🎊 **НЕВЕРОЯТНО!** Вы собрали ВСЮ коллекцию! 👑🦾")

@dp.message(F.text == "🎒 Инвентарь")
async def inv_cmd(m: Message):
    inv = get_items(m.from_user.id, m.from_user.full_name, m.from_user.username)
    if not inv: return await m.answer("Твой инвентарь пуст!")
    txt = f"🎒 **Твоя коллекция ({len(inv)}/{TOTAL_CARDS}):**\n\n" + "\n".join([f"• {i}" for i in sorted(list(inv))])
    await m.answer(txt)

@dp.message(F.text == "🏆 Топ игроков")
async def top_cmd(m: Message):
    cursor.execute("SELECT name, username, items FROM users")
    rows = cursor.fetchall()
    if not rows: return await m.answer("Топ пока пуст!")
    
    users_list = []
    for r in rows:
        count = len(r[2].split(",")) if r[2] else 0
        users_list.append({"n": r[0], "u": r[1], "c": count})
    
    sorted_u = sorted(users_list, key=lambda x: x["c"], reverse=True)
    txt = "🏆 **ТОП КОЛЛЕКЦИОНЕРОВ:**\n\n"
    for i, u in enumerate(sorted_u[:10], 1):
        un = f" (@{u['u']})" if u['u'] else ""
        txt += f"{i}. {u['n']}{un} — {u['c']}/{TOTAL_CARDS}\n"
    await m.answer(txt)

async def main():
    await start_web()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
