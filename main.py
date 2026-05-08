import asyncio, json, random, time, os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import URLInputFile
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
CD = 5 

DATA = {
    "Обычная": {"Сено пятка": "https://ibb.co", "Земляная пятка": "https://ibb.co", "Водяная пятка": "https://ibb.co", "Небесная пятка": "https://ibb.co", "Стеклянная пятка": "https://ibb.co", "Банановая пятка": "https://ibb.co", "Магическая пятка": "https://ibb.co", "Накаченная пятка": "https://ibb.co"},
    "Необычная": {"Какашка пятка": "https://ibb.co", "Вонючая пятка": "https://ibb.co", "Клубничная пятка": "https://ibb.co", "Зек пятка": "https://ibb.co", "Серебряная пятка": "https://ibb.co", "Миньон пятка": "https://ibb.co"},
    "Редкая": {"Пикми пятка": "https://ibb.co", "Фурри пятка": "https://ibb.co", "Аниме пятка": "https://ibb.co", "Нарисованная пятка": "https://ibb.co", "Шиповая пятка": "https://ibb.co", "Костянная пятка": "https://ibb.co"},
    "Эпическая": {"Золотая пятка": "https://ibb.co", "Неоновая пятка": "https://ibb.co", "Теневая пятка": "https://ibb.co", "Лавовая пятка": "https://ibb.co", "Готическая пятка": "https://ibb.co"},
    "Мифическая": {"Демоническая пятка": "https://ibb.co", "Ангельская пятка": "https://ibb.co", "Король пятка": "https://ibb.co", "Радужная пятка": "https://ibb.co"},
    "Легендарная": {"Алмазная пятка": "https://ibb.co", "Зевс пятка": "https://ibb.co", "Мертвая пятка": "https://ibb.co"},
    "Идеальная": {"Изумрудная пятка": "https://ibb.co", "Космическая пятка": "https://ibb.co"}
}

# ШАНСЫ ЗАПОЛНЕНЫ ВРУЧНУЮ, БОЛЬШЕ НЕ УПАДЕТ:
CH = [45, 25, 15, 8, 4, 2, 1]

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

# ЕСЛИ ПРИШЛЕШЬ ФОТО — БОТ СКАЖЕТ ЕГО ID
@dp.message(F.photo)
async def get_photo_id(m: types.Message):
    await m.answer(f"ID фото для вставки в код:\n<code>{m.photo[-1].file_id}</code>", parse_mode="HTML")

@dp.message(Command("start"))
async def st(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="Пятка"), kb.button(text="Инвентарь")
    await m.answer("🦶 Бот запущен! Жми кнопку.", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text.lower() == "пятка")
async def gt(m: types.Message):
    d = load()
    u = str(m.from_user.id)
    now = time.time()
    
    if u in d and now - d[u].get('t', 0) < CD:
        rem = int(CD - (now - d[u]['t']))
        return await m.answer(f"⏳ Жди {rem} сек.")

    if u not in d: d[u] = {'inv': [], 't': 0}
    
    avail = []
    for r_n, r_i in DATA.items():
        for i_n in r_i.keys():
            if i_n not in d[u]['inv']: avail.append((r_n, i_n))

    if not avail: return await m.answer("🏆 Коллекция собрана!")

    # ВЫБОР РЕДКОСТИ
    rk = random.choices(list(DATA.keys()), weights=CH, k=1)[0]
    ps = [n for n in DATA[rk].keys() if n not in d[u]['inv']]
    
    if not ps: rk, name = random.choice(avail)
    else: name = random.choice(ps)

    pic = DATA[rk][name]
    d[u]['inv'].append(name)
    d[u]['t'] = now
    save(d)
    
    cap = f"🦶 Тебе выпала НОВАЯ пятка: <b>{name}</b>\n💎 Редкость: <b>{rk}</b>"
    
    try:
        if pic.startswith("http"): 
            photo = URLInputFile(pic)
        else: 
            photo = pic
        await m.answer_photo(photo=photo, caption=cap, parse_mode="HTML")
    except Exception as e:
        await m.answer(cap + "\n\n⚠️ Ошибка фото! Пришли боту картинку этой пятки, чтобы получить её ID и вставить в код.", parse_mode="HTML")

@dp.message(F.text.lower() == "инвентарь")
async def iv(m: types.Message):
    d = load()
    items = d.get(str(m.from_user.id), {}).get('inv', [])
    if not items: await m.answer("Пусто.")
    else: await m.answer("📜 Коллекция:\n" + "\n".join([f"— {i}" for i in items]))

async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
