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
CHANCES =

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
    await m.answer("🦶 Бот запущен! Кулдаун 5 секунд.", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(Command("reset_me"))
async def reset(m: types.Message):
    d = load()
    u = str(m.from_user.id)
    if u in d:
        del d[u]
        save(d)
        await m.answer("♻️ Прогресс сброшен!")

@dp.message(F.text.lower() == "пятка")
async def gt(m: types.Message):
    d = load()
    u = str(m.from_user.id)
    now = time.time()
    if u in d and now - d[u].get('t', 0) < CD:
        return await m.answer(f"⏳ Жди {int(CD - (now - d[u]['t']))} сек.")

    if u not in d: d[u] = {'inv': [], 't': 0}
    
    available = []
    for r_n, r_i in DATA.items():
        for i_n in r_i.keys():
            if i_n not in d[u]['inv']: available.append((r_n, i_n))

    if not available: return await m.answer("🏆 Ты собрал все пятки!")

    rar_key = random.choices(list(DATA.keys()), weights=CHANCES, k=1)[0]
    poss = [n for n in DATA[rar_key].keys() if n not in d[u]['inv']]
    if not poss: rar_key, name = random.choice(available)
    else: name = random.choice(poss)

    pic_url = DATA[rar_key][name]
    d[u]['inv'].append(name)
    d[u]['t'] = now
    save(d)
    
    # Новый формат сообщения: Название сверху, Редкость снизу
    cap = f"🦶 Тебе выпала НОВАЯ пятка: <b>{name}</b>\n💎 Редкость: <b>{rar_key}</b>"
    
    try:
        photo = URLInputFile(pic_url)
        await m.answer_photo(photo=photo, caption=cap, parse_mode="HTML")
    except:
        await m.answer(cap, parse_mode="HTML")

@dp.message(F.text.lower() == "инвентарь")
async def iv(m: types.Message):
    d = load()
    items = d.get(str(m.from_user.id), {}).get('inv', [])
    if not items: await m.answer("📦 Твой инвентарь пуст.")
    else: await m.answer("📜 Твоя коллекция:\n" + "\n".join([f"— {i}" for i in items]))

async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
