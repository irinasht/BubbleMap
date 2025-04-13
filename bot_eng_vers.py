import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes
)
from playwright.async_api import async_playwright
import os
import base64 
import requests
from pycoingecko import CoinGeckoAPI

import openai
from openai import OpenAI
from datetime import datetime

import os
from dotenv import load_dotenv


# Load params from .env
load_dotenv()
TOKEN = os.getenv('TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# Get BubbleMap screenshot
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



# Get information about image via OpenAI
async def analyze_image(filename: str, chain: str) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)

    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')


    response = client.chat.completions.create(
        model= "gpt-4.5-preview-2025-02-27",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Analyze the provided Bubble Map of the {chain.upper()} token and give detailed recommendations. Highlight any risks and advantages if present. Please ensure your response fits within Telegram bot's character limit."},
                    {"type": "image_url",
                     "image_url": {
                         "url": f"data:image/png;base64,{encoded_string}"
                     }},
                ],
            }
        ],
        max_tokens=500,
    )


    return response.choices[0].message.content



# Available blockchains and their API identifiers
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


# --- Start menu function ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '👋 Hello! Select a blockchain for the Bubble Map:',
        reply_markup=blockchain_menu()
    )

# -- Keyboard ---
def blockchain_menu():
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f'chain_{code}')]
        for name, code in BLOCKCHAINS.items()
    ]
    return InlineKeyboardMarkup(keyboard)


# --- Blockchain selection handler ---
async def blockchain_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chain_code = query.data.split('_')[1]
    context.user_data['selected_chain'] = chain_code

    await query.message.reply_text(
        f'✅ Blockchain selected: {chain_code.upper()}\nPlease send the token address:'
    )

# --- Fetch token info ---
def get_token_info(chain, token):
    cg = CoinGeckoAPI()

    chain_ids = {
        'eth': 'ethereum',
        'bsc': 'binance-smart-chain',
        'poly': 'polygon-pos',
        'ftm': 'fantom',
        'avax': 'avalanche',
        'arbi': 'arbitrum-one',
        'cro': 'cronos',
        'base': 'base',
        'sol': 'solana'
    }

    try:
        cg_data = cg.get_coin_info_from_contract_address_by_id(
            id=chain_ids.get(chain, 'ethereum'), contract_address=token
        )

        url = "https://api-legacy.bubblemaps.io/map-metadata"
        params = {"chain": chain, "token": token}
        response = requests.get(url, params=params).json()

        return {
            'name': cg_data['name'],
            'price': cg_data['market_data']['current_price']['usd'],
            'market_cap': cg_data['market_data']['market_cap']['usd'],
            'volume_24h': cg_data['market_data']['total_volume']['usd'],
            'decentralisation_score': response.get('decentralisation_score', 'N/A')
        }

    except Exception as e:
        return {'error': str(e)}

# -- All logic with messages --
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'selected_chain' not in context.user_data:
        await update.message.reply_text('Please select a blockchain first using the /start command.')
        return

    token = update.message.text.strip()
    chain = context.user_data['selected_chain']

    if len(token) < 20 or len(token) > 60:
        await update.message.reply_text('⚠️ This does not look like a valid token address. Please try again.')
        return

    token_info = get_token_info(chain, token)

    if 'error' in token_info or not token_info.get('name'):
        await update.message.reply_text("⚠️ Unfortunately, there's no token info available from the API.")
    else:
        info_text = (
            f"📌 **Token Information:**\n"
            f"Name: {token_info['name']}\n"
            f"Price: ${token_info['price']}\n"
            f"Market Cap: ${token_info['market_cap']}\n"
            f"24h Volume: ${token_info['volume_24h']}\n"
            f"Decentralization Score: {token_info['decentralisation_score']}\n"
        )
        await update.message.reply_text(info_text)

    # message about starting generation
    msg = await update.message.reply_text('🚀 Generating Bubble Map, please wait (~40 sec)...')

    try:
        screenshot_filename = await get_screenshot(token, chain)

        with open(screenshot_filename, 'rb') as photo:
            await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo)

        # message about starting generation recommendations
        await msg.edit_text('🕒 Generating recommendations, please wait...')

        analysis_result = await analyze_image(screenshot_filename, chain)

        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"📝 **Token Analysis:**\n{analysis_result}\n\n✅ Done! What would you like to do next?",
            reply_markup=repeat_menu(chain)
        )

    except Exception as e:
        await msg.edit_text(f'❌ Error: {e}')




# --- Repeat scenario ---
def repeat_menu(chain):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 New token (different blockchain)", callback_data="new_chain")],
        [InlineKeyboardButton(f"🔁 New token ({chain.upper()})", callback_data=f"repeat_{chain}")]
    ])

async def repeat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "new_chain":
        
        await query.message.reply_text(
            '👋 Select a blockchain for the Bubble Map:',
            reply_markup=blockchain_menu()
        )
    elif data.startswith("repeat_"):
        chain_code = data.split('_')[1]
        context.user_data['selected_chain'] = chain_code
        await query.message.reply_text(f'🔁 Blockchain {chain_code.upper()} selected again.\nPlease send the new token address:')



# --- Main bot launch function ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(blockchain_choice, pattern='^chain_'))
    app.add_handler(CallbackQueryHandler(repeat_handler, pattern='^(new_chain|repeat_)'))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("✅ Bot successfully launched...")
    app.run_polling()
