# 🚀 Bubble Map Telegram Bot

A Telegram bot that generates screenshot bubble maps of blockchain tokens, provides comprehensive token analytics, and delivers actionable insights using [BubbleMaps.io](https://bubblemaps.io/) and OpenAI API.

---

## 🌟 Features

- ✅ Supports multiple blockchains:
  - Ethereum (ETH)
  - Binance Smart Chain (BSC)
  - Fantom (FTM)
  - Avalanche (AVAX)
  - Cronos (CRO)
  - Arbitrum (ARBI)
  - Polygon (POLY)
  - Base (BASE)
  - Solana (SOL)
  - Sonic (SONIC)

- ✅ Generates screenshot of Bubble Map.
- ✅ Provides token analysis and decentralized scoring.
- ✅ Fetches live token data (price, market cap, 24h volume) from CoinGecko.
- ✅ Clear, user-friendly Telegram interface.

---


## 📸 Demo

| Step-by-Step Process                             | Description                                         |
|--------------------------------------------------|-----------------------------------------------------|
| `/start`                                         | Start interacting with the bot                      |
| Select blockchain                                | Choose your blockchain from a user-friendly menu    |
| Enter token address                              | Provide the token contract address                  |
| Get token information and Bubble Map             | Receive detailed analytics, visualization, and insights |

---

## ⚙️ Installation Guide

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/bubblemap-telegram-bot.git
cd bubblemap-telegram-bot
```

### 2. Set up Virtual Environment (optional, but recommended)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root with your API keys:

```
TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

### 5. Run the Bot

```bash
python bot_eng_vers.py
```

---

## 🚀 Usage

- Launch bot with `/start`.
- Select the blockchain and provide the token address.
- Instantly receive token analytics, Bubble Map visualization, and recommendations.

---

## 📂 Project Structure

```
bubblemap-telegram-bot/
├── bot_eng_vers.py
├── README.md
├── requirements.txt
├── .env
├── user-scanario.md
├── pictures/ (screenshots folder, ignored by git)
└── .gitignore
```

---

## 🔑 APIs Utilized

- [BubbleMaps.io API](https://bubblemaps.io)
- [CoinGecko API](https://www.coingecko.com/en/api)
- [OpenAI API](https://platform.openai.com/docs/api-reference)

---

## 📝 Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

---

## 📄 License

MIT License