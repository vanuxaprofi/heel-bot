import asyncio, json, random, time, os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from flask import Flask
from threading import Thread

# --- СЕРВЕР ДЛЯ RENDER ---
app = Flask('')
@app.route('/')
def home(): return "OK"
def run_w(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
def keep_alive():
    t = Thread(target=run_w)
    t.daemon = True
    t.start()

# --- НАСТРОЙКИ ---
API_TOKEN = os.getenv('BOT_TOKEN', '8539851697:AAHUHFS35gMBCJ5ozf_ChQfLOhrvke68Fzs')
DB_FILE = 'users_data.json'
CD = 5 # Установлено 5 секунд для теста

# --- БАЗА ПЯТОК ---
DATA = {
    "Обычная": {"Сено": "https://ibb.co", "Земляная": "https://ibb.co", "Водяная": "https://ibb.co", "Небесная": "https://ibb.co", "Стекло": "https://ibb.co", "Банановая": "https://ibb.co", "Магия": "https://ibb.co", "Накаченная": "https://ibb.co"},
    "Необычная": {"Какашка": "https://ibb.co", "Вонючая": "https://ibb.co", "Клубника": "https://ibb.co", "Зек": "https://ibb.co", "Серебро": "https://ibb.co", "Миньон": "https://ibb.co"},
    "Редкая": {"Пикми": "https://ibb.co", "Фурри": "https://ibb.co", "Аниме": "https://ibb.co", "Рисованная": "https://ibb.co", "Шиповая": "https://ibb.co", "Кости": "https://ibb.co"},
    "Эпик": {"Золото": "https://ibb.co", "Неон": "https://ibb.co", "Лава": "https://ibb.co", "Готика": "https://ibb.co"},
    "Миф": {"Демон": "https://ibb.co", "Ангел": "https://ibb.co", "Король": "https://ibb.co", "Радуга": "https://ibb.co"},
    "Легенда": {"Алмаз": "https://ibb.co", "Зевс": "https://ibb.co", "Мертвая": "https://ibb.co"},
    "Идеал": {"Изумруд": "https://ibb.co", "Космос": "https://ibb.co"}
}
CHANCES = [45, 25, 15, 8, 4, 2, 1]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def load():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except: return {}
    return {}

def save(d):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False, indent=4)

@dp.message(Command("start"))
async def st(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="Пятка"), kb.button(text="Инвентарь")
    await m.answer("🦶 Бот готов к тесту! Кулдаун 5 секунд.", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(Command("reset_me"))
async def reset(m: types.Message):
    d = load()
    u = str(m.from_user.id)
    if u in d:
        del d[u]
        save(d)
        await m.answer("♻️ Инвентарь сброшен! Начинай собирать заново.")
    else:
        await m.answer("У тебя и так пусто.")

@dp.message(F.text.lower() == "пятка")
async def gt(m: types.Message):
    d = load()
    u = str(m.from_user.id)
    now = time.time()
    
    if u in d and now - d[u].get('t', 0) < CD:
        rem = int(CD - (now - d[u]['t']))
        return await m.answer(f"⏳ Жди {rem} сек.")

    if u not in d: d[u] = {'inv': [], 't': 0}
    
    # Ищем доступные пятки (без повторок)
    available = []
    for r_n, r_i in DATA.items():
        for i_n in r_i.keys():
            if i_n not in d[u]['inv']:
                available.append((r_n, i_n))

    if not available:
        return await m.answer("🏆 Ты собрал всю коллекцию!")

    # Выбираем редкость, где есть несобранные пятки
    rar_key = random.choices(list(DATA.keys()), weights=CHANCES, k=1)[0]
    poss_items = [n for n in DATA[rar_key].keys() if n not in d[u]['inv']]
    
    if not poss_items: # Если в этой редкости всё собрано, берем любую новую из других
        rar_key, name = random.choice(available)
    else:
        name = random.choice(poss_items)

    pic = DATA[rar_key][name]
    d[u]['inv'].append(name)
    d[u]['t'] = now
    save(d)
    
    cap = f"🦶 Выпала: <b>{name}</b>\n💎 Редкость: <b>{rar_key}</b>"
    try:
        await m.answer_photo(photo=pic, caption=cap, parse_mode="HTML")
    except:
        await m.answer(cap, parse_mode="HTML")

@dp.message(F.text.lower() == "инвентарь")
async def iv(m: types.Message):
    d = load()
    items = d.get(str(m.from_user.id), {}).get('inv', [])
    if not items: await m.answer("📦 Инвентарь пуст.")
    else: await m.answer("📜 Твои пятки:\n" + "\n".join([f"— {i}" for i in items]))

async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
