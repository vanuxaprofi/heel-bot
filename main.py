import asyncio, json, random, time, os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "OK"
def run_w(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
def keep_alive():
    t = Thread(target=run_w)
    t.daemon = True
    t.start()

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
    await m.answer("🦶 Бот обновлен! Фото и полные названия работают.", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(Command("reset_me"))
async def reset(m: types.Message):
    d = load()
    u = str(m.from_user.id)
    if u in d:
        del d[u]
        save(d)
        await m.answer("♻️ Твой прогресс сброшен!")

@dp.message(F.text.lower() == "пятка")
async def gt(m: types.Message):
    d = load()
    u = str(m.from_user.id)
    now = time.time()
    
    if u in d and now - d[u].get('t', 0) < CD:
        rem = int(CD - (now - d[u]['t']))
        return await m.answer(f"⏳ Жди {rem} сек.")

    if u not in d: d[u] = {'inv': [], 't': 0}
    
    available = []
    for r_n, r_i in DATA.items():
        for i_n in r_i.keys():
            if i_n not in d[u]['inv']:
                available.append((r_n, i_n))

    if not available:
        return await m.answer("🏆 Ты собрал все пятки!")

    rar_key = random.choices(list(DATA.keys()), weights=CHANCES, k=1)
    poss_items = [n for n in DATA[rar_key].keys() if n not in d[u]['inv']]
    
    if not poss_items:
        rar_key, name = random.choice(available)
    else:
        name = random.choice(poss_items)

    pic = DATA[rar_key][name]
    d[u]['inv'].append(name)
    d[u]['t'] = now
    save(d)
    
    cap = f"🦶 Выпала: <b>{name}</b>\n💎 Редкость: <b>{rar_key}</b>"
    try:
        await bot.send_photo(chat_id=m.chat.id, photo=pic, caption=cap, parse_mode="HTML")
    except Exception as e:
        print(f"Ошибка фото: {e}")
        await m.answer(cap, parse_mode="HTML")

@dp.message(F.text.lower() == "инвентарь")
async def iv(m: types.Message):
    d = load()
    items = d.get(str(m.from_user.id), {}).get('inv', [])
    if not items: await m.answer("Пусто.")
    else: await m.answer("📜 Твои пятки:\n" + "\n".join([f"— {i}" for i in items]))

async def main():
    keep_alive()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
