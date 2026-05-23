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
        "❄️ Снежная пятка": "AgACAgIAAxkBAAID6Gn_Ey5HXjmTxgwGf_9U2Urqgi6KAAKeFWsb1ZD5S-XTgpndBk9cAQADAgADeQADOwQ",
        "🪨 камяная пятка": "AgACAgIAAxkBAAIrQWoB8OOSDdNtdqQzrlpz1Hge_Ip5AAJxGmsb5TkQSMim2_vPsGavAQADAgADeQADOwQ"
    },
    "🟢 НЕОБЫЧНАЯ (25%)": {
        "💩 Какашка пятка": "AgACAgIAAxkBAAPFaf2PPgoYWtmcoFpNxv0jaTKVJZMAAqoTaxv04fFL3v6kk9fTTEgBAAMCAAN5AAM7BA",
        "🤡 Клоунская пятка": "AgACAgIAAxkBAAIFXmn_YhXNCagUKtMUs5hsWAYSluyIAAJwE2sb1ZABSBtXMa7EX2EnAQADAgADeQADOwQ",
        "🇲🇽 Мексиканская пятка": "AgACAgIAAxkBAAIFYGn_YijdIKLflTfBinihZOJZptq2AAJxE2sb1ZABSGN06Ezh-Di7AQADAgADeQADOwQ",
        "🇫🇷 Французская пятка": "AgACAgIAAxkBAAIFYmn_YjcC_G6jEKSxJmVLaDGdfc2uAAJzE2sb1ZABSHaFAf24-Y8qAQADAgADeQADOwQ",
        "📟 Голограмная пятка": "AgACAgIAAxkBAAIFXGn_YfJP0rRk8ffzjGRX5foaBPLuAALWEWsbQEAAAUjM_jhLR0kIVgEAAwIAA3kAAzsE",
        "🤢 Вонючая пятка": "AgACAgIAAxkBAAImo2oB67DTFQFZDSw7LK8ekLapiGLNAAI4F2sbqjIRSPx_m-8HDYtnAQADAgADeQADOwQ",
        "🍓 Клубничная пятка": "AgACAgIAAxkBAAIFZGn_YlJNeXKkHSxJyN7ktT0rf53hAAJ1E2sb1ZABSPvDSdClMBR2AQADAgADeQADOwQ",
        "⛓️ Зек пятка": "AgACAgIAAxkBAAIFZmn_YmpTFwUV5x1F90tkb1OXlX96AAJ3E2sb1ZABSCtDrjoogOnKAQADAgADeQADOwQ",
        "🥈 Серебряная пятка": "AgACAgIAAxkBAAIDkGn_D0GvsOp0rze9Ruv9-H92M9-JAAJeFWsb1ZD5Sz1Z9RQS6uoEAQADAgADeQADOwQ",
        "🟡 Миньон пятка": "AgACAgIAAxkBAAIFaGn_Yn0XsNrv5lyT1XFZcVxQgMiVAAJ4E2sb1ZABSFid7miwmtfPAQADAgADeQADOwQ",
        "📦 Коробка с пяткой": "AgACAgIAAxkBAAIFamn_YouCT-QYnAgfTCFB207FbSw_AAJ5E2sb1ZABSIYltFqCN6MxAQADAgADeQADOwQ",
        "🧊 Ледяная пятка": "AgACAgIAAxkBAAIEMmn_ID6A2Es4E2MhErV_offnKs8fAAIeFmsb1ZD5S5VU-JhnyFMPAQADAgADeQADOwQ",
        "🌸 Цветочная пятка": "AgACAgIAAxkBAAIDhmn_CtswJ5giZuyE6wT4QvPPuR5_AAJUFWsb1ZD5S_OtiSyyNSJnAQADAgADeQADOwQ",
        "💍 Свадебная пятка": "AgACAgIAAxkBAAID5mn_EyO0HM8BN4eH0tE-VGgw3dQxAAKdFWsb1ZD5S9wUM1L44LZ4AQADAgADeQADOwQ",
        "📚 Умная пятка": "AgACAgIAAxkBAAIrW2oB8PG_iZcRwK8ggcbGyxw0zKvqAAJ6Gmsb5TkQSJRU_ujXoCmmAQADAgADeQADOwQ",
        "🏳️ ластик пятка": "AgACAgIAAxkBAAIrSGoB8OjLZIiZebM5ZAABQZd8T6nbFAACeBprG-U5EEgGnmal-GtRPwEAAwIAA3kAAzsE",
        "🧦 Бомж пятка": "AgACAgIAAxkBAAIrD2oB8MGzJxlwIXrtB43hdpge9gwnAAJoGmsb5TkQSI55rXuJzgQxAQADAgADeQADOwQ",
        "🥬 растения пятка": "AgACAgIAAxkBAAIrAWoB8LnvYqJQslDOLmAP8YzJJh5cAAJmGmsb5TkQSI6qWrNbgt-xAQADAgADeQADOwQ",
        "🪩 диско пятка": "AgACAgIAAxkBAAIzFGoDmpjkpRt2upafzLaGO83m1CzgAALbFGsb5TkgSDwrC98X5lK_AQADAgADeQADOwQ"
    },
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
        "🏺 Египетская пятка": "AgACAgIAAxkBAAIER2n_OAdCiNJ1fDO2hayplX7wEV69AALdFmsb1ZD5S0WgBZ51p6NNAQADAgADeQADOwQ",
        "🏫 изучаемая пятка": "AgACAgQAAxkBAAIqX2oB79dukjXsWxr2jKgqx8p3yOftAAIXD2sbckoIUIOgYzPobOSgAQADAgADeQADOwQ",
        "🏴‍☠️ Пират пятка": "AgACAgIAAxkBAAIrUWoB8OwCesi2Vuvhl7Ni0s_ohLV9AAJ5Gmsb5TkQSBvuzDL6Y4PfAQADAgADeQADOwQ",
        "🍬 Сахарная вата": "AgACAgIAAxkBAAIsuGoB9GVlr6i83YppJ1NvyVHLAfehAAKSGmsb5TkQSA4XOFQp_gcRAQADAgADdwADOwQ",
        "🚽 Скибиди пятка": "AgACAgIAAxkBAAIrK2oB8NUBWtzAJZIWJcmkchU3UAqKAAJsGmsb5TkQSK2CbTrBHqNzAQADAgADeQADOwQ",
        "🍯 мёдовая пятка": "AgACAgIAAxkBAAIrB2oB8L0iBw3XUCNNOmfoBEsVKnTFAAJnGmsb5TkQSORnCjFQ_1S1AQADAgADeQADOwQ",
        "⚠️ Error пятка": "AgACAgIAAxkBAAItA2oB-r4nO1i-UAOyQI-4G6TrFxOZAALPGmsb5TkQSNrm9KIVCTfFAQADAgADeQADOwQ",
        "🥚 Пасхальная": "AgACAgQAAxkBAAIm2moB7NBsYpKXRVILEvd9W5iVaNUlAALJDmsbNt0RUPXWKmv3DVlxAQADAgADeQADOwQ",
        "🍭 Леденец пятка": "AgACAgIAAxkBAAIt-2oCCfukCXROINtl2fhYy7WAVekDAALeF2sbqjIRSC3U0wz81WMSAQADAgADeQADOwQ"
    },
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
        "🍕 Пицца пятка": "AgACAgIAAxkBAAID9Gn_E427KoTE1WKBQhGiiMFJKTT6AAKlFWsb1ZD5S9jLZsS2gyuJAQADAgADeQADOwQ",
        "🧇 орео пятка": "AgACAgIAAxkBAAIzEmoDmjgT0VubPnzc4yzmh_arnxK5AALaFGsb5TkgSL3Xs42BnYn1AQADAgADeQADOwQ",
        "👨‍🚀 Пятка в скафандре": "AgACAgIAAxkBAAItAWoB-VtB0x1RQiGu3_sswLUUcLb0AALMGmsb5TkQSLNDa3yTmOZ5AQADAgADeQADOwQ",
        "🟨 Пивная пятка": "AgACAgIAAxkBAAItEWoB_PVyDhPsnJZkpbPOTkbHln4jAAKmF2sbMOcRSCC6a5lU6AMeAQADAgADeQADOwQ",
        "🟧 Фанта пятка": "AgACAgIAAxkBAAItB2oB_Ley35igtONqEpZ6jR8U4QcnAALeGmsb5TkQSI0-7d6dx8c0AQADAgADeQADOwQ",
        "🟦 Пепси пятка": "AgACAgIAAxkBAAItC2oB_MblDm8LrYHJjk9IKzcszNcVAALfGmsb5TkQSIhVfyVxbjj5AQADAgADeQADOwQ",
        "🟥 Кокакольная пятка": "AgACAgIAAxkBAAItDWoB_Mtb6RmdlIA4PDQK2-nhz1y6AALgGmsb5TkQSPiojjR8aO2UAQADAgADeQADOwQ",
        "❄️ Новогодняя пятка": "AgACAgQAAxkBAAImoWoB6udzvyoOY-hM29s9xHMkW8w-AAJADmsbckoAAVAAAcrxlQ5syJsBAAMCAAN5AAM7BA",
        "💀 Хэллоувин пятка": "AgACAgQAAxkBAAIm02oB7Mv3Il2_nfpeV8vQjMM2lfFxAALIDmsbNt0RUAXPFiRJvQtIAQADAgADeQADOwQ",
        "📰 Новостная пятка": "AgACAgIAAxkBAAIt-WoCCeiv_QMHiWnc-EFhY_XnaaEyAAI8G2sb5TkQSNDhPvwIK53xAQADAgADeQADOwQ"
    },
    "🔴 МИФИЧЕСКАЯ (4%)": {
        "👹 Демоническая пятка": "AgACAgIAAxkBAAID4Gn_Ev0bSON3TUcSQ6EHpC3SseeRAAKaFWsb1ZD5SyPWO53iJqvZAQADAgADeQADOwQ",
        "😇 Ангельская пятка": "AgACAgIAAxkBAAID3Gn_EuUcieIvGWulfO1wSRJIU1wFAAKYFWsb1ZD5SzqKAAGkMIfIewEAAwIAA3kAAzsE",
        "👑 Король пятка": "AgACAgIAAxkBAAIDwmn_EfrCpPVh4kGwvkzJSoYnwgAB1AAChxVrG9WQ-Uv47f3uLJgsLwEAAwIAA3kAAzsE",
        "🏳️‍🌈 Радужная пятка": "AgACAgIAAxkBAAIDqGn_DQ4FuWv7qkFjbzjn_OUNb0HiAAJjFWsb1ZD5S9yYkliLFV_UAQADAgADeQADOwQ",
        "👽 Инопланетная пятка": "AgACAgIAAxkBAAIEDGn_FGOlrhNtDREpmrQ70Q-8Ln3hAAK0FWsb1ZD5S9Ys73tzWqnsAQADAgADeQADOwQ",
        "🧪 SCP пятка": "AgACAgIAAxkBAAIERWn_N929xS7ixp-IZYW67VmsGiE_AALaFmsb1ZD5S15tvDeldngAAQEAAwIAA3kAAzsE",
        "🎰 Казино пятка": "AgACAgIAAxkBAAIDjWn_DIQM1hllF2usp74800QVmVxhAAJcFWsb1ZD5Sx80PirvUzEUAQADAgADeQADOwQ",
        "💰 Магнат пятка": "AgACAgIAAxkBAAID7Gn_E0wdVHJyBsvIoO7tMTtoucqTAAKhFWsb1ZD5S3-vIun8qbYQAQADAgADeQADOwQ",
        "☦️ божественая пятка": "AgACAgQAAxkBAAIqU2oB77widOaawpjapTK9EkQp-snNAALPDmsbckoIUJK8c022x6dEAQADAgADeQADOwQ",
        "🦸 Геройская пятка": "AgACAgIAAxkBAAIqWmoB79CBTboXVpJzm8ue1dvp8OmsAAJXGmsb5TkQSOhtlzKY9FrjAQADAgADeQADOwQ",
        "🦹‍♀️ Злодейская пятка": "AgACAgQAAxkBAAIsK2oB8dJnqXZsuz-F5dKVN7dcIox9AALLDmsbckoIUGdD7sNatdo8AQADAgADeQADOwQ"
    },
    "🟡 ЛЕГЕНДАРНАЯ (2%)": {
        "💎 Алмазная пятка": "AgACAgIAAxkBAAID3mn_EvLdDY1r-ZvW77novm5DuhXVAAKZFWsb1ZD5S18ODlfYhh8NAQADAgADeQADOwQ",
        "⚡ Зевс пятка": "AgACAgIAAxkBAAIDtmn_EaLijTggPq-ojfCradBc21yRAAJ9FWsb1ZD5SxfNkQw-ybnuAQADAgADeQADOwQ",
        "💀 Мертвая пятка": "AgACAgIAAxkBAAIDuGn_Ea7HrThA8-StQoFK9CyPDPPgAAJ-FWsb1ZD5S9KLDcrp1tAhAQADAgADeQADOwQ",
        "🤖 Киборг пятка": "AgACAgIAAxkBAAIEGmn_F5-Rafm_lQwas5MdBusevsDjAALLFWsb1ZD5S0IbouPTTI7pAQADAgADeQADOwQ",
        "💸 Мажор пятка": "AgACAgIAAxkBAAID7Gn_E0wdVHJyBsvIoO7tMTtoucqTAAKhFWsb1ZD5S3-vIun8qbYQAQADAgADeQADOwQ"
    },
    "👑 ИДЕАЛЬНАЯ (1%)": {
        "✳️ Изумрудная пятка": "AgACAgIAAxkBAAIDymn_EjVUFFcrFDQPEQz41_4qvr9RAAKLFWsb1ZD5S7UC99SYLJ7mAQADAgADeQADOwQ",
        "🌠 Космическая пятка": "AgACAgIAAxkBAAIDwGn_EemoJ7b518KihB1fs9FBSN_UAAKFFWsb1ZD5S8yQqj3J3BwSAQADAgADeQADOwQ",
        "🌗 Полудемон-полуангел": "AgACAgIAAxkBAAIELGn_GCw9x1M6KTHO-5DA0k7R4GV2AALUFWsb1ZD5S-aa_6j-GELaAQADAgADeQADOwQ",
        "❓ Пропавшая пятка": "AgACAgIAAxkBAAIECGn_FE09s8tp4ww0wV6N-SkRNh4QAAKzFWsb1ZD5S8x5gqxhxEe9AQADAgADeQADOwQ"}
}

ALL_FEETS = {}
for rarity_key, cards in DATA.items():
    for card_name in cards.keys():
        # Бот запомнит: "Пятка соседа": "⚪ ОБЫЧНАЯ (45%)"
        ALL_FEETS[card_name] = rarity_key

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
class LimitState(StatesGroup):
    choosing_bet = State()  # Новый этап: выбор суммы
    playing = State()       # Сам раунд (Больше/Меньше)
last_bet_time = {}
last_time = {}
last_random_time = {}
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Жми на кнопки ниже!", reply_markup=get_kb())
    
# БАЗА ДАННЫХ
import os
if os.path.exists("game_db.db"):
    os.remove("game_db.db")

conn = sqlite3.connect("game_db.db", check_same_thread=False)
cursor = conn.cursor()

# 1. Создание таблицы пользователей
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
(user_id INTEGER PRIMARY KEY, 
 name TEXT, 
 username TEXT, 
 inventory TEXT DEFAULT '', 
 balance INTEGER DEFAULT 100, 
 total_opens INTEGER DEFAULT 0, 
 duplicates INTEGER DEFAULT 0, 
 bet_count INTEGER DEFAULT 0, 
 pity_counter INTEGER DEFAULT 0, 
 current_day INTEGER DEFAULT 1, 
 last_claim_date TEXT DEFAULT '')''')
conn.commit()

# 2. Одна общая таблица квестов (все квесты вместе!)
cursor.execute('''CREATE TABLE IF NOT EXISTS user_quests
(user_id INTEGER PRIMARY KEY,
 common_10 INTEGER DEFAULT 0,
 uncommon_10 INTEGER DEFAULT 0,
 rare_10 INTEGER DEFAULT 0,
 epic_10 INTEGER DEFAULT 0,
 mythic_10 INTEGER DEFAULT 0,
 legend_3 INTEGER DEFAULT 0,
 perfect_2 INTEGER DEFAULT 0,
 global_10 INTEGER DEFAULT 0,
 global_50 INTEGER DEFAULT 0,
 global_100 INTEGER DEFAULT 0,
 jackpot_hunter INTEGER DEFAULT 0,
 optovik INTEGER DEFAULT 0,
 chest_baron INTEGER DEFAULT 0,
 legend_start INTEGER DEFAULT 0,
 chest_magnat INTEGER DEFAULT 0,
 dup_10 INTEGER DEFAULT 0,
 dup_50 INTEGER DEFAULT 0,
 dup_100 INTEGER DEFAULT 0)''')
conn.commit()

def get_user_data(uid, n, un):
    # Достаем inventory вместо items, чтобы имя совпадало с таблицей users
    cursor.execute("""
        SELECT inventory, balance, total_opens, duplicates, bet_count,
               pity_counter, current_day, last_claim_date
        FROM users WHERE user_id = ?
    """, (uid,))
    r = cursor.fetchone()
    
    if r:
        raw_str = r[0] if r[0] else ""
        raw_list = [name.strip() for name in raw_str.split(",") if name.strip()]
        # Для совместимости с остальным кодом (если где-то ниже используется словарь items)
        items = {name: raw_list.count(name) for name in set(raw_list)}
        
        # Обновляем имя и юзернейм, если они изменились
        cursor.execute("UPDATE users SET name = ?, username = ? WHERE user_id = ?", (n, un, uid))
        conn.commit()
        return r[0], r[1], r[2], r[3], r[4]
        
    # Если пользователя нет в базе — создаем его с дефолтными значениями
    cursor.execute("""
        INSERT INTO users (user_id, name, username, inventory, balance, total_opens, duplicates, bet_count, pity_counter, current_day, last_claim_date)
        VALUES (?, ?, ?, '', 100, 0, 0, 0, 0, 1, '')
    """, (uid, n, un))
    conn.commit()
    return '', 100, 0, 0, 0

def get_user_game_features(uid):
    cursor.execute("SELECT pity_counter, current_day, last_claim_date FROM users WHERE user_id = ?", (uid,))
    r = cursor.fetchone()
    if r:
        return r[0], r[1], r[2]
    return 0, 1, ""

def update_user_stats(uid, items, balance, total_opens, duplicates, bet_count, pity_counter=None, current_day=None, last_claim_date=None):
    if isinstance(items, dict):
        items_str = ",".join([name for name, count in items.items() for _ in range(count)])
    else:
        items_str = ",".join(list(items))
        
    if pity_counter is None or current_day is None or last_claim_date is None:
        cursor.execute("SELECT pity_counter, current_day, last_claim_date FROM users WHERE user_id = ?", (uid,))
        res = cursor.fetchone()
        if res:
            if pity_counter is None: pity_counter = res[0]
            if current_day is None: current_day = res[1]
            if last_claim_date is None: last_claim_date = res[2]
        else:
            pity_counter, current_day, last_claim_date = 0, 1, ""

    cursor.execute("""
        UPDATE users 
        SET items = ?, balance = ?, total_opens = ?, duplicates = ?, bet_count = ?, 
            pity_counter = ?, current_day = ?, last_claim_date = ? 
        WHERE user_id = ?
    """, (items_str, balance, total_opens, duplicates, bet_count, pity_counter, current_day, last_claim_date, uid))
    conn.commit()

async def check_and_grant_quests(message, uid, inv, balance):
    # 1. Считаем уникальные карты по каждой редкости (точно так же, как в меню квестов!)
    counts = {r: 0 for r in RARITIES}
    for rarity in RARITIES:
        if rarity in DATA:
            for card in DATA[rarity].keys():
                if card in inv:  # Проверяем наличие карты в строке инвентаря
                    counts[rarity] += 1
                    
    total_unique = sum(counts.values())

    # 2. Получаем текущие статусы квестов из базы
    cursor.execute("SELECT * FROM user_quests WHERE user_id = ?", (uid,))
    q = cursor.fetchone()
    if not q:
        cursor.execute("INSERT OR IGNORE INTO user_quests (user_id) VALUES (?)", (uid,))
        conn.commit()
        cursor.execute("SELECT * FROM user_quests WHERE user_id = ?", (uid,))
        q = cursor.fetchone()

    # Маппинг статусов квестов по колонкам (индексы строго с 1 по 10)
    columns = ["common_10", "uncommon_10", "rare_10", "epic_10", "mythic_10", "legend_3", "perfect_2", "global_10", "global_50", "global_100"]
    q_status = {col: q[i+1] for i, col in enumerate(columns)}
    
    new_balance = balance
    triggered = False

    # Сетка условий: (имя_колонки, текущее_значение, цель, награда, текст)
    QUESTS_LOGIC = [
        ("common_10", counts.get("⚪ ОБЫЧНАЯ (45%)", 0), 10, 300, "Ты собрал 10 обычных карточек!\nТвоя награда: 300 монет 💰\n✨ Продолжай в том же духе, коллекция сама себя не соберет! ✨\n👣👣👣"),
        ("uncommon_10", counts.get("🟢 НЕОБЫЧНАЯ (25%)", 0), 10, 600, "Ты собрал 10 необычных карточек!\nТвоя награда: 600 монет 💰\n✨ Продолжай в том же духе, коллекция сама себя не соберет! ✨\n👣👣👣"),
        ("rare_10", counts.get("🔵 РЕДКАЯ (15%)", 0), 10, 1200, "Ты собрал 10 редких карточек!\nТвоя награда: 1 200 монет 💰\n✨ Продолжай в том же духе, коллекция сама себя не соберет! ✨\n👣👣👣"),
        ("epic_10", counts.get("🟣 ЭПИЧЕСКАЯ (8%)", 0), 10, 2500, "Ты собрал 10 эпических карточек!\nТвоя награда: 2 500 монет 💰\n✨ Продолжай в том же духе, коллекция сама себя не соберет! ✨\n👣👣👣"),
        ("mythic_10", counts.get("🔴 МИФИЧЕСКАЯ (4%)", 0), 10, 7500, "Ты собрал 10 мифических карточек!\nТвоя награда: 7 500 монет 💰\n✨ Продолжай в том же духе, коллекция сама себя не соберет! ✨\n👣👣👣"),
        ("legend_3", counts.get("🟡 ЛЕГЕНДАРНАЯ (2%)", 0), 3, 15000, "Ты собрал 3 легендарных карточки!\nТвоя награда: 15 000 монет 💰\n✨ Продолжай в том же духе, коллекция сама себя не соберет! ✨\n👣👣👣"),
        ("perfect_2", counts.get("👑 ИДЕАЛЬНАЯ (1%)", 0), 2, 25000, "Ты собрал 2 идеальных карточки!\nТвоя награда: 25 000 монет 💰\n✨ Продолжай в том же духе, коллекция сама себя не соберет! ✨\n👣👣👣"),
        # Глобальные
        ("global_10", total_unique, 10, 1500, "🏆 ГЛОБАЛЬНЫЙ КВЕСТ ВЫПОЛНЕН! 🏆\nНачало положено! Ты преодолел первые этапы и собрал 10 пяток в свою коллекцию.\nТвоя награда: 1 500 монет 💰\n✨ Твоя выдержка впечатляет. Пора прикупить сундук подороже! ✨\n👣"),
        ("global_50", total_unique, 50, 10000, "🏆 ГЛОБАЛЬНЫЙ КВЕСТ ВЫПОЛНЕН! 🏆\nНевероятная преданность делу! В твоем альбоме уже 50 пяток. Настоящий коллекционер.\nТвоя награда: 10 000 монет 💰\n✨ Это серьезный капитал. Удача на твоей стороне! ✨\n💎"),
        ("global_100", total_unique, 100, 35000, "🏆 ВЕЛИЧАЙШЕЕ ДОСТИЖЕНИЕ! 🏆\nТы сделал это! 100 ПЯТОК! 👑 Ты шел к этому результату сотни часов.\nТвоя награда: 35 000 монет 💰\n✨ Ты — легенда этого бота. Твоему терпению можно только позавидовать! ✨\n🏰")
    ]

    # 3. Проверяем условия выполнения
    for col, current, target, reward, success_text in QUESTS_LOGIC:
        if q_status[col] == 0 and current >= target:
            new_balance += reward
            triggered = True
            
            # Меняем статус квеста на выполненный (1) в базе
            cursor.execute(f"UPDATE user_quests SET {col} = 1 WHERE user_id = ?", (uid,))
            conn.commit()
            
            # Отправляем красивое сообщение
            if col.startswith("global"):
                await message.answer(success_text, parse_mode="Markdown")
            else:
                await message.answer(f"🏆 **КВЕСТ ВЫПОЛНЕН!** 🏆\n{success_text}", parse_mode="Markdown")

    # 4. Если хоть один квест сработал, обновляем баланс игрока в таблице users
    if triggered:
        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, uid))
        conn.commit()
            
    return new_balance

# ОЖИВИТЕЛЬ
async def handle(r): return web.Response(text="Alive")
async def start_web():
    app = web.Application(); app.router.add_get("/", handle)
    runner = web.AppRunner(app); await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", 10000).start()
def get_kb():
    row1 = [KeyboardButton(text="🦶 Выбить пятку")]
    row2 = [KeyboardButton(text="💰 Профиль"), KeyboardButton(text="🏪 Магазин")]
    row3 = [KeyboardButton(text="🎰 Ставки"), KeyboardButton(text="🍀 Рандомайзер")]
    row4 = [KeyboardButton(text="🎒 Инвентарь"), KeyboardButton(text="🏆 Топ игроков")]
    row5 = [KeyboardButton(text="📜 Квесты"), KeyboardButton(text="📅 Календарь")] # Теперь они вместе сбоку!
    row6 = [KeyboardButton(text="🎁 Промокод"), KeyboardButton(text="🎲 Лимит")]

    
    kb = ReplyKeyboardMarkup(
        keyboard=[row1, row2, row3, row4, row5, row6],
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

def get_smart_random_card(user_id, inv_dict, rarity, pity_counter):
    # Получаем все карты этой редкости из DATA
    all_cards = list(DATA[rarity].keys())
    
    # Разделяем карты на новые для игрока и те, что уже есть
    my_cards_in_rarity = [card for card in all_cards if card in inv_dict and inv_dict[card] > 0]
    new_cards_in_rarity = [card for card in all_cards if card not in inv_dict or inv_dict[card] == 0]
    
    # 1. Для Мифических, Легендарных и Идеальных: шанс на повторку — 0%
    if rarity in ["🔴 МИФИЧЕСКАЯ (4%)", "🟡 ЛЕГЕНДАРНАЯ (2%)", "👑 ИДЕАЛЬНАЯ (1%)"]:
        if new_cards_in_rarity:
            return random.choice(new_cards_in_rarity), True, pity_counter
        else:
            # Если игрок вдруг собрал вообще ВСЕ карты этой редкости
            return random.choice(all_cards), False, pity_counter

    # 2. Если все карты этой редкости уже открыты (Вариант А): всегда повторка
    if not new_cards_in_rarity:
        return random.choice(all_cards), False, pity_counter

    # 3. Защита от застревания: если уже выпало 3 повторки подряд, 4-я — 100% новая
    if pity_counter >= 3:
        return random.choice(new_cards_in_rarity), True, 0

    # 4. Обычный ролл 80% на новую карту / 20% на повторку
    roll = random.randint(1, 100)
    if roll <= 80:
        # Выпала новая карта
        return random.choice(new_cards_in_rarity), True, 0
    else:
        # Выпала повторка (если повторок у игрока еще нет физически — выдаем новую)
        if my_cards_in_rarity:
            return random.choice(my_cards_in_rarity), False, pity_counter + 1
        else:
            return random.choice(new_cards_in_rarity), True, 0
            
@dp.message(F.text == "🦶 Выбить пятку")
async def open_case(message: types.Message, state: FSMContext):
    await state.clear()  # Принудительно выводит игрока из любого зависшего режима ставок/рандома!
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_time and current_time - last_time[user_id] < 1:
        return await message.answer("⏳ Подожди 1 сек.")

    # Получаем базовые данные и новые игровые фичи отдельно
    inv, balance, total_opens, duplicates, bet_count = get_user_data(user_id, message.from_user.full_name, message.from_user.username)
    pity_counter, current_day, last_claim_date = get_user_game_features(user_id)

    res_list = random.choices(RARITIES, weights=WEIGHTS)
    rarity = res_list[0]

    # Крутим наш Умный Рандом!
    item_name, is_new, new_pity = get_smart_random_card(user_id, inv, rarity, pity_counter)
    pity_counter = new_pity

    base_reward = MONEY_REWARDS.get(rarity, 0)
    total_opens += 1

    if not is_new:
        duplicates += 1
        reward = base_reward * 2  # Наш х2 бонус за повторку
        status = f"♻ **Повторка!**\nЗачислено: +{reward} 💰 (х2 бонус за повторку!)"
        inv[item_name] = inv.get(item_name, 0) + 1
    else:
        reward = base_reward
        status = f"✨ **НОВАЯ ПЯТКА!**\nДобавлена в твою коллекцию! (+{reward} 💰)"
        inv[item_name] = 1

    balance += reward

    update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count, pity_counter, current_day, last_claim_date)
        # Проверяем выполнение квестов при каждом выпадении пятки
    await check_and_grant_quests(message, user_id, inv, balance)
    last_time[user_id] = current_time

    chances = {"⚪ ОБЫЧНАЯ (45%)": "45%", "🟢 НЕОБЫЧНАЯ (25%)": "25%", "🔵 РЕДКАЯ (15%)": "15%", "🟣 ЭПИЧЕСКАЯ (8%)": "8%", "🔴 МИФИЧЕСКАЯ (4%)": "4%", "🟡 ЛЕГЕНДАРНАЯ (2%)": "2%", "👑 ИДЕАЛЬНАЯ (1%)": "1%"}
    icons = {"⚪ ОБЫЧНАЯ (45%)": "⚪", "🟢 НЕОБЫЧНАЯ (25%)": "🟢", "🔵 РЕДКАЯ (15%)": "🔵", "🟣 ЭПИЧЕСКАЯ (8%)": "🟣", "🔴 МИФИЧЕСКАЯ (4%)": "🔴", "🟡 ЛЕГЕНДАРНАЯ (2%)": "🟡", "👑 ИДЕАЛЬНАЯ (1%)": "👑"}

    chance = chances.get(rarity, "")
    icon = icons.get(rarity, "")
    photo_id = DATA[rarity][item_name]

    caption = (
        f"🎉 **Поздравляю** 🎉\n\n"
        f"Вам выпала • **{item_name}**\n"
        f"Редкость • {rarity}\n\n"
        f"{status}\n"
        f"💰 Твой баланс: **{balance}** монет"
    )

    try:
        await message.answer_photo(photo_id, caption=caption, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"{caption}\n\n(Ошибка фото: {e})")

@dp.message(F.text == "🎒 Инвентарь")
async def show_inventory(message: types.Message):
    user_id = message.from_user.id
    
    # 1. Запрашиваем инвентарь игрока из базы данных
    cursor.execute("SELECT items FROM users WHERE user_id = ?", (user_id,))
    r = cursor.fetchone()
    raw_list = r[0].split(",") if r and r[0] else []
    inv = {name: raw_list.count(name) for name in set(raw_list) if name}

    if not inv:
        return await message.answer("🎒 Твой рюкзак пуст! Выбей свою первую пятку.")

    text = "🎒 **ТВОЙ ИНВЕНТАРЬ**\n\n"
    total_collection_value = 0

    # 2. Перебираем редкости и считаем прогресс сборки
    for rarity in RARITIES:
        base_price = MONEY_REWARDS.get(rarity, 0) 
        rarity_text = ""
        
        # Считаем, сколько ВСЕГО карт в этой редкости прописано в DATA
        total_cards_in_rarity = len(DATA[rarity].keys())
        # Считаем, сколько УНИКАЛЬНЫХ карт из них уже открыл игрок
        collected_unique = 0

        for card_name in DATA[rarity].keys():
            if card_name in inv and inv[card_name] > 0:
                count = inv[card_name]
                collected_unique += 1
                
                # Математика стоимости (1-я = номинал, повторки = х2)
                card_value = base_price + (base_price * 2 * (count - 1))
                total_collection_value += card_value

                # Чистый старый стиль вывода строк
                rarity_text += f"• {card_name} — {count} шт.\n"

        # Выводим заголовок редкости с указанием прогресса (например, Собрано: 4/10)
        if rarity_text:
            text += f"**{rarity}** (Собрано: {collected_unique}/{total_cards_in_rarity}):\n{rarity_text}\n"
        else:
            text += f"**{rarity}** (Собрано: 0/{total_cards_in_rarity}):\n(Пусто)\n\n"

    # Финальный итог
    text += f"💰 **Общая стоимость:** {total_collection_value} монет"
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text == "🏆 Топ игроков")
async def show_top(message: Message):
    cursor.execute("SELECT name, items FROM users") 
    rows = cursor.fetchall()
    if not rows: 
        return await message.answer("Топ пока пуст!")
        
    users_list = []
    
    for r in rows:
        name_val = str(r[0]) if r[0] else "Игрок"
        items_str = str(r[1]) if r[1] else ""
        
        if items_str and items_str.strip():
            # 1. Сначала разбиваем строку на список всех карточек игрока
            all_items = [item.strip() for item in items_str.split(",") if item.strip()]
            # 2. ИСПРАВЛЕНИЕ: Оставляем только уникальные (новые) карты с помощью set()
            count = len(set(all_items))
        else:
            count = 0
            
        users_list.append({"n": name_val, "c": count})
        
    # Сортируем лидеров по количеству именно уникальных карт
    sorted_u = sorted(users_list, key=lambda x: x["c"], reverse=True)
    
    txt = "🏆 **ТОП КОЛЛЕКЦИОНЕРОВ (ПО УНИКАЛЬНЫМ КАРТАМ):**\n\n"
    for i, u in enumerate(sorted_u[:10], 1):
        # Чистим имя от символов, ломающих разметку Markdown
        safe_name = u['n'].replace("*", "").replace("_", " ").replace("[", "").replace("`", "")
        txt += f"{i}. {safe_name} — {u['c']}/{TOTAL_CARDS} 📑\n"
        
    try:
        await message.answer(txt, parse_mode="Markdown")
    except:
        # Резервный вариант без Markdown-тегов при ошибке
        await message.answer(txt.replace("**", ""))

@dp.message(F.text == "🏪 Магазин")
async def show_shop(message: types.Message):
    # Получаем актуальный баланс
    inv, balance, total_opens, duplicates, bet_count = get_user_data(
        message.from_user.id, message.from_user.full_name, message.from_user.username
    )
    
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
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Купить Эпический (1000)", callback_data="buy_epic")],
        [InlineKeyboardButton(text="Купить Мифический (4500)", callback_data="buy_mythic")],
        [InlineKeyboardButton(text="Купить Легендарный (15000)", callback_data="buy_legend")]
    ])
    
    await message.answer(text, reply_markup=ikb, parse_mode="Markdown")

# ВСТАВЛЯЙ СЮДА:
@dp.message(F.text == "💰 Профиль")
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

@dp.callback_query(F.data.startswith("buy_"))
async def buy_chest(call: types.CallbackQuery):
    user_id = call.from_user.id
    
    # 1. Отримуємо дані гравця та фічі (pity_counter)
    inv, balance, total_opens, duplicates, bet_count = get_user_data(
        user_id, call.from_user.full_name, call.from_user.username
    )
    pity_counter, current_day, last_claim_date = get_user_game_features(user_id)
    
    chests = {
        "buy_epic": (1000, [75, 19, 5, 1], ["🟣 ЭПИЧЕСКАЯ (8%)", "🔴 МИФИЧЕСКАЯ (4%)", "🟡 ЛЕГЕНДАРНАЯ (2%)", "👑 ИДЕАЛЬНАЯ (1%)"], "Эпический"),
        "buy_mythic": (4500, [70, 25, 5], ["🔴 МИФИЧЕСКАЯ (4%)", "🟡 ЛЕГЕНДАРНАЯ (2%)", "👑 ИДЕАЛЬНАЯ (1%)"], "Мифический"),
        "buy_legend": (15000, [80, 20], ["🟡 ЛЕГЕНДАРНАЯ (2%)", "👑 ИДЕАЛЬНАЯ (1%)"], "Легендарный")
    }
    
    if call.data not in chests:
        return
        
    price, weights, rarities, chest_name = chests[call.data]
    
    if balance < price:
        return await call.answer("❌ Недостаточно монет!", show_alert=True)
        
    # 2. Логіка покупки
    balance -= price
    total_opens += 1
    
    # Вибираємо рідкість
    rarity = random.choices(rarities, weights=weights)[0]
    
    # 🔥 ВИКЛИКАЄМО ТВІЙ РОЗУМНИЙ РАНДОМ ЗАМІСТЬ ЗВИЧАЙНОГО CHOICE!
    item_name, is_new, new_pity = get_smart_random_card(user_id, inv, rarity, pity_counter)
    pity_counter = new_pity
    
    base_reward = MONEY_REWARDS.get(rarity, 0)
    photo_id = DATA[rarity][item_name]
    
    # 3. Перевірка на повторку (працюємо зі словником inv)
    if not is_new:
        duplicates += 1
        reward = base_reward * 2 # Бонус за повторку х2
        status = f"♻ **Повторка!**\nЗачислено: +{reward} 💰 (х2 бонус за повторку!)"
        inv[item_name] = inv.get(item_name, 0) + 1
    else:
        reward = base_reward
        status = f"✨ **НОВАЯ ПЯТКА!**\nДобавлена в твою коллекцию! (+{reward} 💰)"
        inv[item_name] = inv.get(item_name, 0) + 1
        
    balance += reward
    
    # 4. Збереження в базу
    update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count, pity_counter, current_day, last_claim_date)
    
    # Автоматично перевіряємо квести після відкриття сундука
    balance = await check_and_grant_quests(call.message, user_id, inv, balance)
    
    # 5. Відправка повідомлення
    caption = (
        f"🎁 **ОТКРЫТИЕ СУНДУКА: {chest_name}**\n\n"
        f"Вам выпала • **{item_name}**\n"
        f"Редкость • **{rarity}**\n\n"
        f"{status}\n"
        f"💰 Остаток: **{balance}** монет"
    )
    
    try:
        await call.message.answer_photo(photo=photo_id, caption=caption, parse_mode="Markdown")
    except Exception as e:
        await call.message.answer(f"Ошибка при отправке photo: {e}\n\n{caption}")
        
    await call.answer()

LIMIT_COOLDOWN = 32400
last_limit_time = {}

@dp.message(F.text == "🎰 Ставки")
async def start_bet_cmd(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    current_time = time.time()
    
    # 1. Сначала получаем данные игрока, чтобы узнать bet_count
    inv, balance, total_opens, duplicates, bet_count = get_user_data(user_id, message.from_user.full_name, message.from_user.username)
    pity_counter, current_day, last_claim_date = get_user_game_features(user_id)

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
        [KeyboardButton(text="◀️ Назад")] # Твоя стрелочка!
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await state.set_state(BetState.choosing_rarity)
    await message.answer("🎰 Выбери редкость, на которую хочешь поставить:", reply_markup=kb)

@dp.message(BetState.choosing_rarity)
async def play_bet(message: types.Message, state: FSMContext):
    # Если нажата кнопка "Назад" прямо во время выбора ставки
        # Если в тексте кнопки есть слово Назад (независимо от смайликов)
        if message.text == "◀️ Назад":
            await state.clear()
            return await message.answer("Вы вернулись в главное меню", reply_markup=get_kb())

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
    await state.clear()
    await message.answer("Вы вернулись в главное меню", reply_markup=get_kb())

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
        [KeyboardButton(text="◀️ Назад")] # Твоя стрелочка!
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
    "TOP_CARD": [1488, 2],
    "123": [1234567890, 3]
}

# 2. Логика проверки (вставляй СРАЗУ после promo_start_cmd)
@dp.message(PromoState.waiting_for_code)
async def check_promo_cmd(message: types.Message, state: FSMContext):
    if message.text == "◀️ Назад":
        await state.clear()
        return await message.answer("Вы вернулись в главное меню", reply_markup=get_kb())

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
        
 # --- ИГРА «ЛИМИТ» ---

def get_limit_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔽 Меньше ([2х])", callback_data="limit_less"),
            InlineKeyboardButton(text="🔼 Больше ([2х])", callback_data="limit_more")
        ]
    ])

# --- ИГРА «ЛИМИТ» С ВЫБОРОМ СТАВКИ И КД ---

def get_limit_inline_kb(multiplier=2):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"🔽 Меньше ([{multiplier}х])", callback_data="limit_less"),
            InlineKeyboardButton(text=f"🔼 Больше ([{multiplier}х])", callback_data="limit_more")
        ]
    ])

# 1. Нажатие кнопки в главном меню — открываем выбор ставки
@dp.message(F.text == "🎲 Лимит")
async def start_limit_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_time = time.time()
    
    # Получаем данные, чтобы проверить bet_count (используем твой счетчик)
    inv, balance, total_opens, duplicates, bet_count = get_user_data(
        user_id, message.from_user.full_name, message.from_user.username
    )
    
    # Проверка КД: если 3 попытки уже израсходованы
    if bet_count >= 3:
        if user_id in last_limit_time and current_time - last_limit_time[user_id] < LIMIT_COOLDOWN:
            rem = int(LIMIT_COOLDOWN - (current_time - last_limit_time[user_id]))
            h, m = rem // 3600, (rem % 3600) // 60
            return await message.answer(f"⏳ Попытки кончились! Новые в ЛИМИТ будут через {h} ч. {m} мин.")
        else:
            # Если 9 часов прошло — сбрасываем счетчик попыток в базе
            bet_count = 0
            update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count)

    # Меню выбора ставки как в Рандомайзере
    buttons = [
        [KeyboardButton(text="🎰 Ставка 100"), KeyboardButton(text="🎰 Ставка 500")],
        [KeyboardButton(text="🎰 Ставка 1000")],
        [KeyboardButton(text="◀ Назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    
    await state.set_state(LimitState.choosing_bet)
    await message.answer("🎲 **ЛИМИТ**\n\nВыбери размер твоей ставки кнопками ниже 👇", reply_markup=kb, parse_mode="Markdown")

# 2. Обработка выбранной ставки и генерация первого числа
@dp.message(LimitState.choosing_bet)
async def limit_choose_bet(message: Message, state: FSMContext):
    if message.text == "◀ Назад":
        await state.clear()
        return await message.answer("Вы вернулись в главное меню", reply_markup=get_kb())
        
    # Извлекаем сумму ставки из текста кнопки
    try:
        bet = int(message.text.split()[-1])
    except:
        return await message.answer("Пожалуйста, используй кнопки для выбора ставки!")
        
    if bet not in [100, 500, 1000]:
        return await message.answer("Неверная ставка! Выбери 100, 500 или 1000.")
        
    user_id = message.from_user.id
    inv, balance, total_opens, duplicates, bet_count = get_user_data(
        user_id, message.from_user.full_name, message.from_user.username
    )
    
    if balance < bet:
        return await message.answer(f"❌ Не хватает монет! Твой баланс: {balance} 💰")
        
    # Генерируем первое число
    start_number = random.randint(1, 100)
    
    # Сохраняем ставку и число в FSM
    await state.update_data(current_bet=bet, current_number=start_number)
    await state.set_state(LimitState.playing)
    
    text = (
        f"📊 **Игра «ЛИМИТ»**\n\n"
        f"Бот выбрал число: **[{start_number}]** 🎲\n\n"
        f"Как думаете, каким будет следующее число от [1] до [100]? 👇\n"
        f"💡 *Ваша ставка: [{bet}] монет*"
    )
    
    # Переключаем игрока на инлайн-кнопки Больше/Меньше
    await message.answer(text, reply_markup=get_limit_inline_kb(), parse_mode="Markdown")

# 3. Обработка инлайн-кнопок (Меньше / Больше)
@dp.callback_query(LimitState.playing, F.data.startswith("limit_"))
async def process_limit_choice(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    choice = call.data.replace("limit_", "")
    current_time = time.time()
    
    inv, balance, total_opens, duplicates, bet_count = get_user_data(
        user_id, call.from_user.full_name, call.from_user.username
    )
    pity_counter, current_day, last_claim_date = get_user_game_features(user_id)
    
    # Достаем данные раунда из памяти
    user_data = await state.get_data()
    bet = user_data.get("current_bet", 100)
    old_number = user_data.get("current_number")
    
    if not old_number:
        await state.clear()
        return await call.message.answer("⚠️ Сессия игры устарела. Нажмите «🎲 Лимит» снова.")
        
    if balance < bet:
        await state.clear()
        return await call.answer("❌ У вас резко уменьшился баланс!", show_alert=True)
        
    # Списываем монеты и прибавляем попытку за игру
    balance -= bet
    bet_count += 1
    
    # Если это была 3-я попытка — включаем таймер КД на 9 часов
    if bet_count >= 3:
        last_limit_time[user_id] = current_time
        
    new_number = random.randint(1, 100)
    
    is_win = False
    if choice == "more" and new_number > old_number:
        is_win = True
    elif choice == "less" and new_number < old_number:
        is_win = True
        
    if is_win:
        win_amount = bet * 2
        balance += win_amount
        result_text = (
            f"🎉 **Победа!**\n"
            f"Новое число: **[{new_number}]** 🎲\n\n"
            f"Вы угадали и забираете выигрыш **[2х]** (+{win_amount} 💰)!\n"
            f"💰 Ваш баланс: **[{balance}]** монет.\n"
            f"Осталось попыток до КД: **[{max(0, 3 - bet_count)}]**"
        )
    else:
        result_text = (
            f"😢 **Не повезло...**\n"
            f"Новое число: **[{new_number}]** 🎲\n\n"
            f"Ваша ставка **[{bet}]** монет сгорела.\n"
            f"💰 Ваш баланс: **[{balance}]** монет.\n"
            f"Осталось попыток до КД: **[{max(0, 3 - bet_count)}]**"
        )
        
    # Сохраняем новые данные в SQLite
    update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count, pity_counter, current_day, last_claim_date)
    
    # Сбрасываем стейт, возвращаем обычную клавиатуру главного меню
    await call.message.edit_text(result_text, parse_mode="Markdown")
    await call.message.answer("Вы вернулись в меню. Можете сыграть еще раз или выбрать другую вкладку.", reply_markup=get_kb())
    await state.clear()
    await call.answer()
# --- ИГРА «ЛИМИТ» С ВЫБОРОМ СТАВКИ И КД ---

def get_limit_inline_kb(multiplier=2):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"🔽 Меньше ([{multiplier}х])", callback_data="limit_less"),
            InlineKeyboardButton(text=f"🔼 Больше ([{multiplier}х])", callback_data="limit_more")
        ]
    ])

# 1. Нажатие кнопки в главном меню — открываем выбор ставки
@dp.message(F.text == "🎲 Лимит")
async def start_limit_cmd(message: Message, state: FSMContext):
    user_id = message.from_user.id
    current_time = time.time()
    
    # Получаем данные, чтобы проверить bet_count (используем твой счетчик)
    inv, balance, total_opens, duplicates, bet_count = get_user_data(
        user_id, message.from_user.full_name, message.from_user.username
    )
    
    # Проверка КД: если 3 попытки уже израсходованы
    if bet_count >= 3:
        if user_id in last_limit_time and current_time - last_limit_time[user_id] < LIMIT_COOLDOWN:
            rem = int(LIMIT_COOLDOWN - (current_time - last_limit_time[user_id]))
            h, m = rem // 3600, (rem % 3600) // 60
            return await message.answer(f"⏳ Попытки кончились! Новые в ЛИМИТ будут через {h} ч. {m} мин.")
        else:
            # Если 9 часов прошло — сбрасываем счетчик попыток в базе
            bet_count = 0
            update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count)

    # Меню выбора ставки как в Рандомайзере
    buttons = [
        [KeyboardButton(text="🎰 Ставка 100"), KeyboardButton(text="🎰 Ставка 500")],
        [KeyboardButton(text="🎰 Ставка 1000")],
        [KeyboardButton(text="◀ Назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    
    await state.set_state(LimitState.choosing_bet)
    await message.answer("🎲 **ЛИМИТ**\n\nВыбери размер твоей ставки кнопками ниже 👇", reply_markup=kb, parse_mode="Markdown")

# 2. Обработка выбранной ставки и генерация первого числа
@dp.message(LimitState.choosing_bet)
async def limit_choose_bet(message: Message, state: FSMContext):
    if message.text == "◀ Назад":
        await state.clear()
        return await message.answer("Вы вернулись в главное меню", reply_markup=get_kb())
        
    # Извлекаем сумму ставки из текста кнопки
    try:
        bet = int(message.text.split()[-1])
    except:
        return await message.answer("Пожалуйста, используй кнопки для выбора ставки!")
        
    if bet not in [100, 500, 1000]:
        return await message.answer("Неверная ставка! Выбери 100, 500 или 1000.")
        
    user_id = message.from_user.id
    inv, balance, total_opens, duplicates, bet_count = get_user_data(
        user_id, message.from_user.full_name, message.from_user.username
    )
    
    if balance < bet:
        return await message.answer(f"❌ Не хватает монет! Твой баланс: {balance} 💰")
        
    # Генерируем первое число
    start_number = random.randint(1, 100)
    
    # Сохраняем ставку и число в FSM
    await state.update_data(current_bet=bet, current_number=start_number)
    await state.set_state(LimitState.playing)
    
    text = (
        f"📊 **Игра «ЛИМИТ»**\n\n"
        f"Бот выбрал число: **[{start_number}]** 🎲\n\n"
        f"Как думаете, каким будет следующее число от [1] до [100]? 👇\n"
        f"💡 *Ваша ставка: [{bet}] монет*"
    )
    
    # Переключаем игрока на инлайн-кнопки Больше/Меньше
    await message.answer(text, reply_markup=get_limit_inline_kb(), parse_mode="Markdown")

# 3. Обработка инлайн-кнопок (Меньше / Больше)
@dp.callback_query(LimitState.playing, F.data.startswith("limit_"))
async def process_limit_choice(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    choice = call.data.replace("limit_", "")
    current_time = time.time()
    
    inv, balance, total_opens, duplicates, bet_count = get_user_data(
        user_id, call.from_user.full_name, call.from_user.username
    )
    pity_counter, current_day, last_claim_date = get_user_game_features(user_id)
    
    # Достаем данные раунда из памяти
    user_data = await state.get_data()
    bet = user_data.get("current_bet", 100)
    old_number = user_data.get("current_number")
    
    if not old_number:
        await state.clear()
        return await call.message.answer("⚠️ Сессия игры устарела. Нажмите «🎲 Лимит» снова.")
        
    if balance < bet:
        await state.clear()
        return await call.answer("❌ У вас резко уменьшился баланс!", show_alert=True)
        
    # Списываем монеты и прибавляем попытку за игру
    balance -= bet
    bet_count += 1
    
    # Если это была 3-я попытка — включаем таймер КД на 9 часов
    if bet_count >= 3:
        last_limit_time[user_id] = current_time
        
    new_number = random.randint(1, 100)
    
    is_win = False
    if choice == "more" and new_number > old_number:
        is_win = True
    elif choice == "less" and new_number < old_number:
        is_win = True
        
    if is_win:
        win_amount = bet * 2
        balance += win_amount
        result_text = (
            f"🎉 **Победа!**\n"
            f"Новое число: **[{new_number}]** 🎲\n\n"
            f"Вы угадали и забираете выигрыш **[2х]** (+{win_amount} 💰)!\n"
            f"💰 Ваш баланс: **[{balance}]** монет.\n"
            f"Осталось попыток до КД: **[{max(0, 3 - bet_count)}]**"
        )
    else:
        result_text = (
            f"😢 **Не повезло...**\n"
            f"Новое число: **[{new_number}]** 🎲\n\n"
            f"Ваша ставка **[{bet}]** монет сгорела.\n"
            f"💰 Ваш баланс: **[{balance}]** монет.\n"
            f"Осталось попыток до КД: **[{max(0, 3 - bet_count)}]**"
        )
        
    # Сохраняем новые данные в SQLite
    update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count, pity_counter, current_day, last_claim_date)
    
    # Сбрасываем стейт, возвращаем обычную клавиатуру главного меню
    await call.message.edit_text(result_text, parse_mode="Markdown")
    await call.message.answer("Вы вернулись в меню. Можете сыграть еще раз или выбрать другую вкладку.", reply_markup=get_kb())
    await state.clear()
    await call.answer()

def generate_progress_bar(current, target):
    current = min(current, target)
    percentage = current / target
    filled_blocks = int(percentage * 5)
    empty_blocks = 5 - filled_blocks
    return "▚" * filled_blocks + "░" * empty_blocks

@dp.message(F.text == "📜 Квесты")
async def show_user_quests(message: Message):
    user_id = message.from_user.id
    
    # Загружаем статы игрока
    inv, balance, total_opens, duplicates, bet_count = get_user_data(
        user_id, message.from_user.full_name, message.from_user.username
    )
    
    # Считаем количество карточек по редкостям
    counts = {r: 0 for r in RARITIES}
    for rarity in RARITIES:
        if rarity in DATA:
            for card in DATA[rarity].keys():
                if card in inv:
                    counts[rarity] += 1
    total_unique = sum(counts.values())

    # Вытягиваем все статусы квестов из базы
    cursor.execute("""
        SELECT common_10, uncommon_10, rare_10, epic_10, mythic_10, legend_3, perfect_2, 
               global_10, global_50, global_100, 
               jackpot_hunter, optovik, chest_baron, legend_start, chest_magnat, 
               dup_10, dup_50, dup_100 
        FROM user_quests WHERE user_id = ?
    """, (user_id,))
    q_row = cursor.fetchone()
    
    if not q_row:
        cursor.execute("INSERT OR IGNORE INTO user_quests (user_id) VALUES (?)", (user_id,))
        conn.commit()
        q_row = [0] * 18
        
    def get_icon(status): return "✅" if status == 1 else "⏳"

    # Переменные для редкостей
    c_common = counts.get('⚪ ОБЫЧНАЯ (45%)', 0)
    c_uncommon = counts.get('🟢 НЕОБЫЧНАЯ (25%)', 0)
    c_rare = counts.get('🔵 РЕДКАЯ (15%)', 0)
    c_epic = counts.get('🟣 ЭПИЧЕСКАЯ (8%)', 0)
    c_mythic = counts.get('🔴 МИФИЧЕСКАЯ (4%)', 0)
    c_legend = counts.get('🟡 ЛЕГЕНДАРНАЯ (2%)', 0)
    c_perfect = counts.get('👑 ИДЕАЛЬНАЯ (1%)', 0)

    text = (
        f"📜 **СПИСОК ДОСТУПНЫХ КВЕСТОВ**\n\n"
        
        f"💎 **💎 КВЕСТЫ ПО РЕДКОСТЯМ**\n"
        f"{get_icon(q_row[0])} **Обычные карточки** (10 штук) — 300 💰\n"
        f"└ Прогресс: {generate_progress_bar(c_common, 10)} ({c_common}/10)\n\n"
        f"{get_icon(q_row[1])} **Необычные карточки** (10 штук) — 600 💰\n"
        f"└ Прогресс: {generate_progress_bar(c_uncommon, 10)} ({c_uncommon}/10)\n\n"
        f"{get_icon(q_row[2])} **Редкие карточки** (10 штук) — 1 200 💰\n"
        f"└ Прогресс: {generate_progress_bar(c_rare, 10)} ({c_rare}/10)\n\n"
        f"{get_icon(q_row[3])} **Эпические карточки** (10 штук) — 2 500 💰\n"
        f"└ Прогресс: {generate_progress_bar(c_epic, 10)} ({c_epic}/10)\n\n"
        f"{get_icon(q_row[4])} **Мифические карточки** (10 штук) — 7 500 💰\n"
        f"└ Прогресс: {generate_progress_bar(c_mythic, 10)} ({c_mythic}/10)\n\n"
        f"{get_icon(q_row[5])} **Легендарные карточки** (3 штуки) — 15 000 💰\n"
        f"└ Прогресс: {generate_progress_bar(c_legend, 3)} ({c_legend}/3)\n\n"
        f"{get_icon(q_row[6])} **Идельные карточки** (2 штуки) — 25 000 💰\n"
        f"└ Прогресс: {generate_progress_bar(c_perfect, 2)} ({c_perfect}/2)\n\n"
        
        f"🛍 **🛍 МАГАЗИННЫЕ КВЕСТЫ**\n"
        f"{get_icon(q_row[11])} **Оптовик** (10 Эпик сундуков) — 2 500 💰\n"
        f"└ Прогресс: {generate_progress_bar(total_opens, 10) if not q_row[11] else '▚▚▚▚▚'} ({total_opens if not q_row[11] else 10}/10)\n\n"
        f"{get_icon(q_row[12])} **Сундучный Барон** (5 Мифик сундуков) — 6 000 💰\n"
        f"└ Прогресс: {generate_progress_bar(total_opens, 5) if not q_row[12] else '▚▚▚▚▚'} ({total_opens if not q_row[12] else 5}/5)\n\n"
        f"{get_icon(q_row[13])} **Легендарный Старт** (1 Легенда сундук) — 5 000 💰\n"
        f"└ Прогресс: {generate_progress_bar(total_opens, 1) if not q_row[13] else '▚▚▚▚▚'} ({total_opens if not q_row[13] else 1}/1)\n\n"
        f"{get_icon(q_row[14])} **Сундучный Магнат** (Потратить 20k) — 3 000 💰\n"
        f"└ Прогресс: {'▚▚▚▚▚' if q_row[14] else '░░░░░'} ({20000 if q_row[14] else 0}/20000)\n\n"
        
        f"🔄 **🔄 КВЕСТЫ НА ПОВТОРКИ**\n"
        f"♻️ {get_icon(q_row[15])} **Начало дежавю** (10 повторок) — 1 500 💰\n"
        f"└ Прогресс: {generate_progress_bar(duplicates, 10)} ({min(duplicates, 10)}/10)\n\n"
        f"🔄 {get_icon(q_row[16])} **Коллекционер дублей** (50 повторок) — 5 000 💰\n"
        f"└ Прогресс: {generate_progress_bar(duplicates, 50)} ({min(duplicates, 50)}/50)\n\n"
        f"🌀 {get_icon(q_row[17])} **Временная петля** (100 повторок) — 15 000 💰\n"
        f"└ Прогресс: {generate_progress_bar(duplicates, 100)} ({min(duplicates, 100)}/100)\n\n"
        
        f"🌍 **🌍 ГЛОБАЛЬНАЯ КОЛЛЕКЦИЯ**\n"
        f"{get_icon(q_row[7])} **Собрать 10 уникальных пяток** — 1 500 💰\n"
        f"└ Прогресс: {generate_progress_bar(total_unique, 10)} ({total_unique}/10)\n\n"
        f"{get_icon(q_row[8])} **Собрать 50 уникальных пяток** — 10 000 💰\n"
        f"└ Прогресс: {generate_progress_bar(total_unique, 50)} ({total_unique}/50)\n\n"
        f"{get_icon(q_row[9])} **Собрать 100 уникальных пяток** — 35 000 💰\n"
        f"└ Прогресс: {generate_progress_bar(total_unique, 100)} ({total_unique}/100)\n\n"
        
        f"🎰 **🎰 КВЕСТЫ КАЗИНО**\n"
        f"{get_icon(q_row[10])} **Охотник за Джекпотом** — 14 000 💰\n"
        f"└ Прогресс: {'▚▚▚▚▚' if q_row[10] else '░░░░░'} ({1 if q_row[10] else 0}/1)\n"
    )
    
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text == "📅 Календарь")
async def show_calendar_cmd(message: Message):
    DAILY_REWARDS = {
        1: 200, 2: 250, 3: 300, 4: 350, 5: 400, 6: 450, 7: 1000,
        8: 600, 9: 700, 10: 800, 11: 900, 12: 1000, 13: 1100, 14: 2500,
        15: 1300, 16: 1400, 17: 1500, 18: 1600, 19: 1700, 20: 1800, 21: 5000,
        22: 2200, 23: 2400, 24: 2600, 25: 2800, 26: 3000, 27: 3200, 28: 3500, 29: 4000, 30: 15000
    }
    try:
        user_id = message.from_user.id
        inv, balance, total_opens, duplicates, bet_count = get_user_data(
            user_id, message.from_user.full_name, message.from_user.username
        )
        
        pity_counter, current_day, last_claim_date = get_user_game_features(user_id)
        if current_day is None:
            current_day = 0

        from datetime import datetime, timedelta
        today_date = (datetime.utcnow() + timedelta(hours=3)).date()
        today_str = str(today_date)
        
        if current_day > 30 or (current_day == 30 and last_claim_date == today_str):
            txt = (
                "🏁 **КАЛЕНДАРЬ ЗАВЕРШЕН**\n\n"
                "Ты уже забрал все 30 наград и прошел путь новичка до конца. Твой стартовый бонус полностью выплачен.\n"
                "Теперь твой доход — это новые пятки, квесты и дубликаты. Посмотрим, сможешь ли ты собрать всю коллекцию до конца!"
            )
            return await message.answer(txt, parse_mode="Markdown")

        if last_claim_date == today_str:
            return await message.answer("📅 **Ежедневный бонус**\n\nВы уже забрали сегодняшнюю награду! ❌\nЗаходи завтра после 00:00 по МСК!", parse_mode="Markdown")

        new_day = current_day
        if last_claim_date:
            try:
                last_date = datetime.strptime(last_claim_date, "%Y-%m-%d").date()
                delta = today_date - last_date
                if delta.days > 1:
                    new_day = 1
                elif delta.days == 1:
                    new_day += 1
            except Exception:
                new_day = 1
        else:
            new_day = 1

        if new_day < 1: new_day = 1
        if new_day > 30: new_day = 30

        reward_coins = DAILY_REWARDS.get(new_day, 200)
        balance += reward_coins
        
        try:
            update_user_stats(user_id, inv, balance, total_opens, duplicates, bet_count, pity_counter, new_day, today_str)
        except Exception:
            cursor.execute(
                "UPDATE users SET balance = ?, current_day = ?, last_claim_date = ? WHERE user_id = ?",
                (balance, new_day, today_str, user_id)
            )
            conn.commit()
        
        if new_day == 7:
            msg = f"🏆 **НЕДЕЛЯ ПОЗАДИ!**\nТы забирал бонусы 7 дней подряд. Первая серьезная отметка достигнута!\n\n💰 Награда: {reward_coins} монет\n✨ Не останавливайся, впереди еще много интересного.\n👣"
        elif new_day == 14:
            msg = f"🏆 **ДВЕ НЕДЕЛИ В ИГРЕ!**\nТы забираешь награды уже 14 дней. Это половина пути до финала!\n\n💰 Награда: {reward_coins} монет\n✨ Твой капитал растет, как и твоя коллекция.\n💎"
        elif new_day == 21:
            msg = f"🏆 **ТРИ НЕДЕЛИ ВЕРНОСТИ!**\n21 день пролетает незаметно, когда цель близка. Осталась последняя прямая!\n\n💰 Награда: {reward_coins} монет\n✨ Совсем скоро ты заберешь главный приз.\n🔥"
        elif new_day == 30:
            msg = f"👑 **ФИНАЛЬНАЯ НАГРАДА ПОЛУЧЕНА!**\nПоздравляем! Ты прошел путь длиной в 30 дней и забрал последний бонус. Твоё упорство достойно уважения!\n\n💰 Награда: {reward_coins} монет\n🏁 Твой календарь наград завершен.\nТеперь ты — опытный коллекционер. Используй этот капитал с умом!\n✨"
        else:
            msg = f"📅 **Ежедневный бонус**\nНаграда № {new_day}/30 получена!\n\n💰 Начислено: {reward_coins} монет\nЗаходи завтра после 00:00!"

        await message.answer(msg, parse_mode="Markdown")

    except Exception as error:
        await message.answer(f"❌ Ошибка в календаре:\n`{str(error)}`", parse_mode="Markdown")

async def check_and_grant_quests(message, uid, inv, balance):
    counts = {r: 0 for r in RARITIES}
    for rarity in RARITIES:
        if rarity in DATA:
            for card in DATA[rarity].keys():
                if card in inv:
                    counts[rarity] += 1
    total_unique = sum(counts.values())

    # Берем данные игрока для проверки условий
    cursor.execute("SELECT total_opens, duplicates FROM users WHERE user_id = ?", (uid,))
    user_row = cursor.fetchone()
    total_opens = user_row[0] if user_row else 0
    user_duplicates = user_row[1] if user_row else 0

    cursor.execute("SELECT * FROM user_quests WHERE user_id = ?", (uid,))
    q = cursor.fetchone()
    if not q:
        cursor.execute("INSERT OR IGNORE INTO user_quests (user_id) VALUES (?)", (uid,))
        conn.commit()
        cursor.execute("SELECT * FROM user_quests WHERE user_id = ?", (uid,))
        q = cursor.fetchone()

    # Массив колонок (ровно 18 квестов)
    columns = [
        "common_10", "uncommon_10", "rare_10", "epic_10", "mythic_10", "legend_3", "perfect_2", 
        "global_10", "global_50", "global_100", 
        "jackpot_hunter", "optovik", "chest_baron", "legend_start", "chest_magnat", 
        "dup_10", "dup_50", "dup_100"
    ]
    q_status = {col: q[i+1] for i, col in enumerate(columns)}
    
    new_balance = balance
    triggered = False

    # ПОЛНАЯ СЕТКА ВСЕХ КВЕСТОВ (Старые + Все новые со скриншотов)
    QUESTS_LOGIC = [
        # Старые квесты по редкостям
        ("common_10", counts.get("⚪ ОБЫЧНАЯ (45%)", 0), 10, 300, "Ты собрал 10 обычных карточек!\nНаграда: 300 монет 💰"),
        ("uncommon_10", counts.get("🟢 НЕОБЫЧНАЯ (25%)", 0), 10, 600, "Ты собрал 10 необычных карточек!\nНаграда: 600 монет 💰"),
        ("rare_10", counts.get("🔵 РЕДКАЯ (15%)", 0), 10, 1200, "Ты собрал 10 редких карточек!\nНаграда: 1 200 монет 💰"),
        ("epic_10", counts.get("🟣 ЭПИЧЕСКАЯ (8%)", 0), 10, 2500, "Ты собрал 10 эпических карточек!\nНаграда: 2 500 монет 💰"),
        ("mythic_10", counts.get("🔴 МИФИЧЕСКАЯ (4%)", 0), 10, 7500, "Ты собрал 10 мифических карточек!\nНаграда: 7 500 монет 💰"),
        ("legend_3", counts.get("🟡 ЛЕГЕНДАРНАЯ (2%)", 0), 3, 15000, "Ты собрал 3 легендарных карточки!\nНаграда: 15 000 монет 💰"),
        ("perfect_2", counts.get("👑 ИДЕАЛЬНАЯ (1%)", 0), 2, 25000, "Ты собрал 2 идеальных карточки!\nНаграда: 25 000 монет 💰"),
        
        # Старые глобальные квесты
        ("global_10", total_unique, 10, 1500, "ГЛОБАЛЬНЫЙ КВЕСТ ВЫПОЛНЕН!\nТы собрал 10 уникальных пяток!\nНаграда: 1 500 монет 💰"),
        ("global_50", total_unique, 50, 10000, "ГЛОБАЛЬНЫЙ КВЕСТ ВЫПОЛНЕН!\nТы собрал 50 уникальных пяток!\nНаграда: 10 000 монет 💰"),
        ("global_100", total_unique, 100, 35000, "ВЕЛИЧАЙШЕЕ ДОСТИЖЕНИЕ!\nТы сделал это! 100 ПЯТОК! 👑\nНаграда: 35 000 монет 💰"),
        
        # НОВЫЕ КВЕСТЫ ИЗ ТВОИХ СКРИНШОТОВ
        ("jackpot_hunter", 0, 1, 14000, "Разгон от новичка до мажора! Ты поймал Джекпот x10 на минимальной ставке в [100] монет! 🎰\nТвоя награда: [14 000] монет 💰 *(Суммарно вышло ровно [15 000]!)*\n\n✨ Риск оправдался на все сто. Пора заглянуть в магазин за Легендарным сундуком! ✨"),
        ("optovik", total_opens, 10, 2500, "Ты купил [10] Эпических сундуков в магазине! 🛍\nТвоя награда: [2 500] монет 💰\n\n✨ Отличный оборот капитала. Количество обязательно перерастёт в качество! ✨"),
        ("chest_baron", total_opens, 5, 6000, "Ты открыл [5] Мифических сундуков! 🔮\nТвоя награда: [6 000] монет 💰\n\n✨ Твой изысканный вкус к кейсам вознагражден. Коллекция становится всё элитнее! ✨"),
        ("legend_start", total_opens, 1, 5000, "Ты приобрёл свой первый [1] Легендарный сундук! 👑\nТвоя награда: [5 000] монет 💰\n\n✨ Серьезный шаг в высшую лигу коллекционеров. Твои инвестиции начинают окупаться! ✨"),
        ("chest_magnat", 0, 20000, 3000, "«Сундучный Магнат»: Потратить в магазине суммарно 20k! 💳\nТвоя награда: [3 000] монет 💰"),
        
        # Квесты на повторки
        ("dup_10", user_duplicates, 10, 1500, "Ты собрал [10] повторок в режиме выбивания пяток! 🔁\nЗа каждую из них ты уже получил х2 монет, но лавка ценит твое упорство!\nТвоя награда: [1 500] монет 💰\n\n✨ Не расстраивайся из-за дубликатов, с таким кэшбэком ты быстро накопишь на сундук! ✨"),
        ("dup_50", user_duplicates, 50, 5000, "В твоем рюкзаке осело уже [50] повторных пяток! 🎒\nТвой баланс знатно разросся на х2 бонусах, но держи еще один крупный куш!\nТвоя награда: [5 000] монет 💰\n\n✨ Настоящий ветеран повторного дропа. Удача точно скоро тебе улыбнется! ✨"),
        ("dup_100", user_duplicates, 100, 15000, "Это безумие! [100] ПОВТОРНЫХ ПЯТОК! 👑\nТы собрал целую армию дубликатов и поднял миллионы на х2 монетах! За твое титаническое терпение лавка выдает королевский грант.\nТвоя награда: [15 000] монет 💰\n\n✨ Ты — абсолютная легенда повторок. Твоему везению (или невезению) можно только позавидовать! ✨")
    ]

    for col, current, target, reward, success_text in QUESTS_LOGIC:
        # Для джекпота и магната проверка идет вручную в коде, здесь пропускаем автоматику
        if col in ["jackpot_hunter", "chest_magnat"]:
            continue
            
        if q_status[col] == 0 and current >= target:
            new_balance += reward
            triggered = True
            cursor.execute(f"UPDATE user_quests SET {col} = 1 WHERE user_id = ?", (uid,))
            conn.commit()
            
            if col == "dup_100":
                await message.answer(f"🏆 **ВЕЛИЧАЙШЕЕ ДОСТИЖЕНИЕ!** 🏆\n{success_text}", parse_mode="Markdown")
            else:
                await message.answer(f"🏆 **КВЕСТ ВЫПОЛНЕН!** 🏆\n{success_text}", parse_mode="Markdown")

    if triggered:
        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, uid))
        conn.commit()
    return new_balance

async def main():
    # Добавляем новые колонки в базу для старых игроков, если их еще нет
    try: cursor.execute("ALTER TABLE users ADD COLUMN balance INTEGER DEFAULT 0")
    except: pass
    try: cursor.execute("ALTER TABLE users ADD COLUMN total_opens INTEGER DEFAULT 0")
    except: pass
    try: cursor.execute("ALTER TABLE users ADD COLUMN duplicates INTEGER DEFAULT 0")
    except: pass
    try: cursor.execute("ALTER TABLE users ADD COLUMN pity_counter INTEGER DEFAULT 0")
    except: pass
    try: cursor.execute("ALTER TABLE users ADD COLUMN current_day INTEGER DEFAULT 1")
    except: pass
    try: cursor.execute("ALTER TABLE users ADD COLUMN last_claim_date TEXT DEFAULT ''")
    except: pass
    
    conn.commit()

    await start_web()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
