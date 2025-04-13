import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from playwright.async_api import async_playwright
import os
import base64  # <--- добавь этот импорт наверху


import openai
from openai import OpenAI
from datetime import datetime






async def get_screenshot(token: str, chain: str) -> str:
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = os.path.join('pictures', f'{chain}_{token}_{timestamp}.png')

    chain_urls = {
        'eth': f"https://app.bubblemaps.io/eth/token/{token}",
        'bsc': f"https://app.bubblemaps.io/bsc/token/{token}",
        'ftm': f"https://app.bubblemaps.io/ftm/token/{token}",
        'avax': f"https://app.bubblemaps.io/avax/token/{token}",
        'cro': f"https://app.bubblemaps.io/cro/token/{token}",
        'arbi': f"https://app.bubblemaps.io/arbi/token/{token}",
        'poly': f"https://app.bubblemaps.io/poly/token/{token}",
        'base': f"https://app.bubblemaps.io/base/token/{token}",
        'sol': f"https://app.bubblemaps.io/sol/token/{token}",
        'sonic': f"https://app.bubblemaps.io/sonic/token/{token}"
    }

    if chain not in chain_urls:
        raise ValueError(f"Unsupported blockchain '{chain}' selected.")

    url = chain_urls[chain]

    user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            '--no-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-infobars'
        ])

        context = await browser.new_context(
            user_agent=user_agent,
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        await page.goto(url)

        await page.wait_for_timeout(15000)

        await page.evaluate('''
            () => {
                const buttons = Array.from(document.querySelectorAll('button'));
                buttons.forEach(btn => {
                    if(btn.innerText.includes('CLOSE')) btn.click();
                });
            }
        ''')

        await page.wait_for_timeout(2000)

        await page.screenshot(path=filename, full_page=True)
        await browser.close()

    return filename



openai.api_key = "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"





async def analyze_image(filename: str) -> str:
    client = OpenAI(api_key=openai.api_key)

    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    response = client.chat.completions.create(
        model= "gpt-4.5-preview-2025-02-27",
        # "gpt-4o-mini",  # <-- исправленное название модели
        # gpt-4.5-preview-2025-02-27
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Проанализируй данную bubblemap токена Solana и дай подробные рекомендации по нему. Укажи риски и плюсы, если таковые имеются. Можешь уложиться пожалуйста в длину символов, которую допускает телеграм-бот. "},
                    {"type": "image_url",
                     "image_url": {
                         "url": f"data:image/png;base64,{encoded_string}"
                     }},
                ],
            }
        ],
        max_tokens=500,
    )

    # response = client.chat.completions.create(
    # model="gpt-4o",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": [
    #                 {"type": "text", "text": "Опиши информацию на Bubblemap: укажи, какие кошельки владеют наибольшим объемом токенов, их процентные доли, степень централизации токена и возможные технические риски, которые можно определить на основании представленного изображения. Можешь уложиться пожалуйста в длину символов, которую допускает телеграм-бот"},
    #                 {"type": "image_url",
    #                 "image_url": {
    #                     "url": f"data:image/png;base64,{encoded_string}"
    #                 }},
    #             ],
    #         }
    #     ],
    #     max_tokens=500,
    # )


    return response.choices[0].message.content



# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text('Привет! Пришли мне адрес токена Solana.')


# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     token = update.message.text.strip()

#     if len(token) < 30 or len(token) > 50:
#         await update.message.reply_text('Это не похоже на корректный адрес токена Solana.')
#         return

#     msg = await update.message.reply_text('Создаю скриншот и анализирую токен, пожалуйста, подожди (~40 сек)...')

#     try:
#         screenshot_filename = await get_screenshot(token)

#         # Отправляем пользователю скриншот сразу:
#         with open(screenshot_filename, 'rb') as photo:
#             await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo)

#         # Анализируем скриншот через OpenAI API:
#         analysis_result = await analyze_image(screenshot_filename)

#         # Отправляем анализ пользователю:
#         await context.bot.send_message(chat_id=update.message.chat_id, text=f"📝 **Анализ токена:**\n{analysis_result}")

#         await msg.edit_text(f'✅ Готово! Скриншот сохранён и анализ отправлен.')
#     except Exception as e:
#         await msg.edit_text(f'❌ Ошибка: {e}')


from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes
)

# Токен Telegram-бота (получаешь у @BotFather)
TOKEN = '7693711388:AAHTBNVR_jFzHZQz3XDE2VDdZV_QFkvEHIU'

# Список доступных блокчейнов и идентификаторов API
BLOCKCHAINS = {
    'Ethereum': 'eth',
    'BSC': 'bsc',
    'Fantom': 'ftm',
    'Avalanche': 'avax',
    'Cronos': 'cro',
    'Arbitrum': 'arbi',
    'Polygon': 'poly',
    'Base': 'base',
    'Solana': 'sol',
    'Sonic': 'sonic'
}

# --- Функция стартового меню ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f'chain_{code}')]
        for name, code in BLOCKCHAINS.items()
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        '👋 Привет! Выбери блокчейн для Bubble Map:',
        reply_markup=reply_markup
    )

# --- Обработка выбора блокчейна ---
async def blockchain_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chain_code = query.data.split('_')[1]
    context.user_data['selected_chain'] = chain_code

    await query.message.reply_text(
        f'✅ Выбран блокчейн: {chain_code.upper()}\nОтправь адрес токена:'
    )

# --- Обработка токена и создание Bubble Map ---
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if 'selected_chain' not in context.user_data:
#         await update.message.reply_text('Пожалуйста, сначала выбери блокчейн через команду /start.')
#         return

#     token = update.message.text.strip()
#     chain = context.user_data['selected_chain']

#     if len(token) < 20 or len(token) > 60:
#         await update.message.reply_text('⚠️ Это не похоже на корректный адрес токена. Попробуй снова.')
#         return

#     msg = await update.message.reply_text(f'🚀 Создаю Bubble Map для {chain.upper()}...\nПодожди (~40 сек)...')

#     try:
#         screenshot_filename = await get_screenshot(token, chain)  # добавь параметр chain в свою функцию

#         # отправляем Bubble Map пользователю:
#         with open(screenshot_filename, 'rb') as photo:
#             await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo)

#         # Анализируем через OpenAI API:
#         analysis_result = await analyze_image(screenshot_filename)

#         await context.bot.send_message(
#             chat_id=update.message.chat_id,
#             text=f"📝 **Анализ токена:**\n{analysis_result}"
#         )

#         # Повторный сценарий:
#         await msg.edit_text('✅ Готово! Что дальше?',
#                             reply_markup=repeat_menu(chain))

#     except Exception as e:
#         await msg.edit_text(f'❌ Ошибка: {e}')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'selected_chain' not in context.user_data:
        await update.message.reply_text('Пожалуйста, сначала выбери блокчейн через команду /start.')
        return

    token = update.message.text.strip()
    chain = context.user_data['selected_chain']

    if len(token) < 20 or len(token) > 60:
        await update.message.reply_text('⚠️ Это не похоже на корректный адрес токена. Попробуй снова.')
        return

    msg = await update.message.reply_text(f'🚀 Создаю Bubble Map для {chain.upper()}...\nПодожди (~40 сек)...')

    try:
        screenshot_filename = await get_screenshot(token, chain)

        # отправляем Bubble Map пользователю:
        with open(screenshot_filename, 'rb') as photo:
            await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo)

        # Информируем пользователя о генерации рекомендаций
        await msg.edit_text('🕒 Происходит генерация рекомендаций, пожалуйста, подождите...')

        # Анализируем через OpenAI API:
        analysis_result = await analyze_image(screenshot_filename)

        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"📝 **Анализ токена:**\n{analysis_result}\n\n✅ Готово! Что дальше?",
            reply_markup=repeat_menu(chain)
        )

    except Exception as e:
        await msg.edit_text(f'❌ Ошибка: {e}')

# --- Повторный сценарий ---
def repeat_menu(chain):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Новый токен (другая сеть)", callback_data="new_chain")],
        [InlineKeyboardButton(f"🔁 Новый токен ({chain.upper()})", callback_data=f"repeat_{chain}")]
    ])

async def repeat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "new_chain":
        await start(update, context)
    elif data.startswith("repeat_"):
        chain_code = data.split('_')[1]
        context.user_data['selected_chain'] = chain_code
        await query.message.reply_text(f'🔁 Повторно выбран блокчейн {chain_code.upper()}\nОтправь адрес нового токена:')


# --- Основная функция запуска бота ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(blockchain_choice, pattern='^chain_'))
    app.add_handler(CallbackQueryHandler(repeat_handler, pattern='^(new_chain|repeat_)'))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("✅ Бот успешно запущен...")
    app.run_polling()




# if __name__ == '__main__':
#     app = ApplicationBuilder().token(TOKEN).build()
#     app.add_handler(CommandHandler('start', start))
#     app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

#     print("✅ Бот запущен...")
#     app.run_polling()

