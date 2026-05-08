import asyncio, random, time, os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from flask import Flask
from threading import Thread
from motor.motor_asyncio import AsyncIOMotorClient

app = Flask('')
bot = Bot(token=os.getenv('BOT_TOKEN','8539851697:AAHUHFS35gMBCJ5ozf_ChQfLOhrvke68Fzs'))
dp = Dispatcher()

# БАЗА ДАННЫХ
MONGO_URL = "mongodb+srv://vanuxaproff.db.user:fBUnXNSZJfPftMUj@cluster0.cijehiv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client['heel_game']
users_col = db['players']

@app.route('/')
def h(): return "OK"
def run_w(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

CD = 18000 

DATA = {
    "Обычная": {"Сено пятка": "AgACAgIAAxkBAAPlaf2Pp7k7PXrNT0d9TgjIgwKFfDoAArwTaxv04fFLE9Pz-Di4gQsBAAMCAAN5AAM7BA", "Земляная пятка": "AgACAgIAAxkBAAO_af2PJQUJtkxccatimHfZXuVHkx0AAqUTaxv04fFL0X9OPtULRNgBAAMCAAN5AAM7BA", "Водяная пятка": "AgACAgIAAxkBAAO3af2PDJ0Ud1YLISwNC3Q9J-oZw4gAAqETaxv04fFLn6SnJRUCkf0BAAMCAAN5AAM7BA", "Небесная пятка": "AgACAgIAAxkBAAPdaf2PktnAaJdY6Dh6gQkCAAFbGuBEAAK4E2sb9OHxS81YKINb9aIAAQEAAwIAA3kAAzsE", "Стеклянная пятка": "AgACAgIAAxkBAAPpaf2PsTPjIxZ2V-G741bpzEhbvewAAr4Taxv04fFLvHpUeY8-3sUBAAMCAAN5AAM7BA", "Банановая пятка": "AgACAgIAAxkBAAO1af2PBk0xS29McOFH3fAtJSnADFEAAqATaxv04fFLdQAB7DysIts2AQADAgADeQADOwQ", "Магическая пятка": "AgACAgIAAxkBAAPTaf2Pbi_T-NpbKLSa1m1bjQbZ5PAAArMTaxv04fFL1jnJZS0RalQBAAMCAAN5AAM7BA", "Накачаная пятка": "AgACAgIAAxkBAAPZaf2Phkz7x9JbOe2kNNWQdz_wR5kAArYTaxv04fFLOopOnhweLHcBAAMCAAN5AAM7BA"},
    "Необычная": {"Какашка пятка": "AgACAgIAAxkBAAPFaf2PPgoYWtmcoFpNxv0jaTKVJZMAAqoTaxv04fFL3v6kk9fTTEgBAAMCAAN5AAM7BA", "Вонючая пятка": "AgACAgIAAxkBAAO5af2PEWh5IiBFzoMvoxRzlpm4MEAAAqITaxv04fFLKpbFXQZ1Ir4BAAMCAAN5AAM7BA", "Клубничная пятка": "AgACAgIAAxkBAAPHaf2PRQIMUE8-bWkMg0J5YEbPpWIAAqwTaxv04fFLqwlQ5MU_kY4BAAMCAAN5AAM7BA", "Зек пятка": "AgACAgIAAxkBAAO9af2PH1t0F0smUHB21lDoBs4rCSQAAqQTaxv04fFLba30gxBVjo0BAAMCAAN5AAM7BA", "Серебрянная пятка": "AgACAgIAAxkBAAPnaf2PrXCMYRpNgNhNLNF7FnpGlUUAAr0Taxv04fFLGIrK63_mifgBAAMCAAN5AAM7BA", "Миньон пятка": "AgACAgIAAxkBAAPXaf2PgTlB3HMIaZLY21X1WcuxHGUAArUTaxv04fFLtNyF4L2a2X0BAAMCAAN5AAM7BA"},
    "Редкая": {"Пикми пятка": "AgACAgIAAxkBAAPhaf2PnXKz5ieWdDUui3Ss2GLkYP4AAroTaxv04fFLuKGCU27-HowBAAMCAAN5AAM7BA", "Фурри пятка": "AgACAgIAAxkBAAPraf2Pt4eysWdXU5qpzwWhK08yYOYAAr8Taxv04fFL5D-3jabfDiMBAAMCAAN5AAM7BA", "Аниме пятка": "AgACAgIAAxkBAAOzaf2PAUY1BbaWRiB-NDTSPaxT5i0AAp8Taxv04fFLRFBp4H059GUBAAMCAAN5AAM7BA", "Нарисованная пятка": "AgACAgIAAxkBAAPbaf2PjZ_SSygWK5J8cIASeDD80TMAArcTaxv04fFLK-9iWY63af8BAAMCAAN5AAM7BA", "Шиповая пятка": "AgACAgIAAxkBAAPJaf2PS6W9jEZSlwMflkel97Ke_rEAAq0Taxv04fFLz5T7u3QdZPgBAAMCAAN5AAM7BA", "Костянная пятка": "AgACAgIAAxkBAAPPaf2PXytPkfpMTQ7XNQUV4FKWZlgAArETaxv04fFLYWz6lgy9DtMBAAMCAAN5AAM7BA"},
    "Эпическая": {"Золотая пятка": "AgACAgIAAxkBAAPBaf2PMIM0-CdCO54JHVGfkPrUcvcAAqYTaxv04fFLND3LX-G6wC8BAAMCAAN5AAM7BA", "Неоновая пятка": "AgACAgIAAxkBAAPfaf2Pl3arZOhe5bHtnK2ujOh-SrAAArkTaxv04fFLHITPRRLD-MIBAAMCAAN5AAM7BA", "Теневая пятка": "AgACAgIAAxkBAAPfaf2Pl3arZOhe5bHtnK2ujOh-SrAAArkTaxv04fFLHITPRRLD-MIBAAMCAAN5AAM7BA", "Лавовая пятка": "AgACAgIAAxkBAAPRaf2PZuCrLqZSAAF9fBNzEqz1RvGjAAKyE2sb9OHxS81YKINb9aIAAQEAAwIAA3kAAzsE", "Готическая пятка": "AgACAgIAAxkBAAO7af2PF9vc85g_9rj44635pNQnLn0AAqMTaxv04fFLSYzfJvnHsUsBAAMCAAN5AAM7BA"},
    "Мифическая": {"Демоническая пятка": "AgACAgIAAxkBAAOtaf2Nq19iTXrmG-kSb2tHNEa819wAApcTaxv04fFLWrou_FctNJcBAAMCAAN5AAM7BA", "Ангельская пятка": "AgACAgIAAxkBAAOxaf2O_AvYJNii6fKij3-QdEfTLUAAAp4Taxv04fFLnc4Hl2h9saMBAAMCAAN5AAM7BA", "Король пятка": "AgACAgIAAxkBAAPLaf2PUp3dqZabYq3OtKjyuKy1odAAAq8Taxv04fFLDtZf82PfayMBAAMCAAN5AAM7BA", "Радужная пятка": "AgACAgIAAxkBAAPjaf2Pop47pI8nlt6_YFSmaRHKEWgAArsTaxv04fFLUyIpnQqLpmEBAAMCAAN5AAM7BA"},
    "Легендарная": {"Алмазная пятка": "AgACAgIAAxkBAAOvaf2O9RkEOXCLb5eSn2ZRi8sWFPcAAp0Taxv04fFL1rxXHlPU78MBAAMCAAN5AAM7BA", "Зевс": "AgACAgIAAxkBAAPXaf2PgTlB3HMIaZLY21X1WcuxHGUAArUTaxv04fFLtNyF4L2a2X0BAAMCAAN5AAM7BA", "Мёртвая пятка": "AgACAgIAAxkBAAPVaf2Pe21Vy9dSRMFkzLMl5EjETvcAArQTaxv04fFLUJEtsh0bKVEBAAMCAAN5AAM7BA"},
    "Идеальная": {"Изумрудная пятка": "AgACAgIAAxkBAAPFaf2PPgoYWtmcoFpNxv0jaTKVJZMAAqoTaxv04fFL3v6kk9fTTEgBAAMCAAN5AAM7BA", "Космическая пятка": "AgACAgIAAxkBAAPNaf2PVxVN1R51bsl8LOY15z8IcxEAArATaxv04fFLGdwh2Cx_tWgBAAMCAAN5AAM7BA"}
}

async def get_db_user(uid):
    u = await users_col.find_one({"_id": uid})
    if not u:
        u = {"_id": uid, "inv": [], "t": 0}
        await users_col.insert_one(u)
    return u

@dp.message(Command("start"))
async def st(m: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="Пятка"), kb.button(text="Инвентарь")
    await m.answer("🦶 Бот запущен! Пятки выпадают раз в 5 часов.", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text.lower() == "пятка")
async def gt(m: types.Message):
    uid = str(m.from_user.id)
    u_data = await get_db_user(uid)
    now = time.time()
    
    if now - u_data.get('t', 0) < CD:
        rem = int(CD - (now - u_data['t']))
        return await m.answer(f"⏳ Рано! Жди {rem // 3600}ч. {(rem % 3600) // 60}м.")

    avail = [(r, i) for r, items in DATA.items() for i in items if i not in u_data['inv']]
    if not avail: return await m.answer("🏆 Коллекция уже собрана!")

    # ВЫБОР: Обыч(45%), Необыч(25%), Редк(15%), Эпик(8%), Миф(4%), Лег(2%), Идеал(1%)
    rk = random.choices(list(DATA.keys()), weights=, k=1)
    
    ps = [n for n in DATA[rk].keys() if n not in u_data['inv']]
    if not ps: rk, name = random.choice(avail)
    else: name = random.choice(ps)

    await users_col.update_one({"_id": uid}, {"$push": {"inv": name}, "$set": {"t": now}})
    msg = f"🎉 Поздравляю! Вам выпала: <b>{name}</b>\n💎 Редкость: <b>{rk}</b>"
    await m.answer_photo(photo=DATA[rk][name], caption=msg, parse_mode="HTML")

@dp.message(F.text.lower() == "инвентарь")
async def iv(m: types.Message):
    u_data = await get_db_user(str(m.from_user.id))
    inv = u_data.get('inv', [])
    if not inv: await m.answer("📦 Твой инвентарь пуст.")
    else: await m.answer("📜 Твоя коллекция:\n" + "\n".join([f"— {i}" for i in inv]))

async def main():
    Thread(target=run_w).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
