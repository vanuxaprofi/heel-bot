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
CD = 18000 # 5 часов

# --- БАЗА ПЯТОК И ССЫЛОК ---
DATA = {
    "Обычная": {
        "Сено пятка": "https://ibb.co",
        "Земляная пятка": "https://ibb.co",
        "Водяная пятка": "https://ibb.co",
        "Небесная пятка": "https://ibb.co",
        "Стеклянная пятка": "https://ibb.co",
        "Банановая пятка": "https://ibb.co",
        "Магическая пятка": "https://ibb.co",
        "Накаченая": "https://ibb.co"
    },
    "Необычная": {
        "Какашка пятка": "https://ibb.co",
        "Вонючая пятка": "https://ibb.co",
        "Клубничная пятка": "https://ibb.co",
        "Зек пятка": "https://ibb.co",
        "Серебряная пятка": "https://ibb.co",
        "Миньйон": "https://ibb.co"
    },
    "Редкая": {
        "Пикми пятка": "https://ibb.co",
        "Фурри пятка": "https://ibb.co",
        "Аниме пятка": "https://ibb.co",
        "Нарисованная пятка": "https://ibb.co",
        "Шыповая": "https://ibb.co",
        "Костянная": "https://ibb.co"
    },
    "Эпическая": {
        "Золотая пятка": "https://ibb.co",
        "Неоновая пятка": "https://ibb.co",
        "Теневая пятка": "https://ibb.co",
        "Лавовая пятка": "https://ibb.co",
        "Готическая": "https://ibb.co"
    },
    "Мифическая": {
        "Демоническая пятка": "https://ibb.co",
        "Ангельская пятка": "https://ibb.co",
        "Король пятка": "https://ibb.co",
        "Радужная пятка": "https://ibb.co"
    },
    "Легендарная": {
        "Алмазная пятка": "https://ibb.co",
        "Зевс": "https://ibb.co",
        "Мёртвая пятка": "https://ibb.co"
    },
    "Идеальные": {
        "Изумрудная пятка": "https://ibb.co",
        "Космическая пятка": "https://ibb.co"
    }
}

# Шансы выпадения
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
async def start(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="Пятка"), kb.button(text="Инвентарь")
    await m.answer("🦶 Бот обновлен! Новые пятки и фото добавлены.", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text.lower() == "пятка")
async def get_heel(m: types.Message):
    d = load()
    u = str(m.from_user.id)
    if u in d and time.time() - d[u].get('t', 0) < CD:
        r = int(CD - (time.time() - d[u]['t']))
        return await m.answer(f"⏳ Жди {r//3600}ч. {(r%3600)//60}м.")
    
    rar_list = list(DATA.keys())
    rar = random.choices(rar_list, weights=CHANCES, k=1)[0]
    name = random.choice(list(DATA[rar].keys()))
    pic = DATA[rar][name]

    if u not in d: d[u] = {'inv': [], 't': 0}
    if name not in d[u]['inv']: d[u]['inv'].append(name)
    d[u]['t'] = time.time()
    save(d)

    cap = f"🦶 Тебе выпала: <b>{name}</b>\n💎 Редкость: <b>{rar}</b>"
    await m.answer_photo(photo=pic, caption=cap, parse_mode="HTML")

@dp.message(F.text.lower() == "инвентарь")
async def inv(m: types.Message):
    d = load()
    items = d.get(str(m.from_user.id), {}).get('inv', [])
    if not items: await m.answer("Пусто.")
    else: await m.answer("📜 Коллекция:\n" + "\n".join([f"— {i}" for i in items]))

async def main():
    keep_alive()
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
