# 🚀 Bubble Map Telegram Bot – Detailed User Scenario

## 📌 Step 1: Starting Interaction

**User action:**
- Opens Telegram, starts chat with bot:
```
/start
```

**Bot response:**
```
👋 Hello! Select a blockchain for the Bubble Map:

[ Ethereum ] [ BSC ] [ Fantom ]
[ Avalanche ] [ Cronos ] [ Arbitrum ]
[ Polygon ] [ Base ] [ Solana ] [ Sonic ]
```

## 📌 Step 2: Selecting a Blockchain

**User action:**
- Selects Ethereum.

**Bot response:**
```
✅ Blockchain selected: ETH
Please send the token address:
```

## 📌 Step 3: Providing Token Address

**User action:**
- Sends token address:
```
0x1f9840a85d5af5bf1d1762f925bdaddc4201f984
```

**Bot response:**
```
📌 Token Information:
Name: Uniswap
Price: $6.25
Market Cap: $4,700,000,000
24h Volume: $150,000,000
Decentralization Score: 82

🚀 Generating Bubble Map, please wait (~40 sec)...
```

(If token info unavailable):
```
⚠️ Unfortunately, there's no token info available from the API.
🚀 Generating Bubble Map anyway, please wait (~40 sec)...
```

## 📌 Step 4: Bubble Map Generation & Analysis

**Bot automatically:**
- Generates Bubble Map screenshot, sends to user.

**Bot response (analysis):**
```
🕒 Generating recommendations, please wait...
```

**Bot sends AI-generated analysis:**
```
📝 Token Analysis:
- ✅ High decentralization (low risk of manipulation).
- ✅ Strong liquidity and active trading volume.
- ⚠️ Some concentration among top holders (be cautious).

✅ Done! What would you like to do next?

🔄 New token (different blockchain)
🔁 New token (ETH)
```

## 📌 Step 5: Repeat or Select New Blockchain

### Scenario A: Select "New token (ETH)"
```
🔁 Blockchain ETH selected again.
Please send the new token address:
```
(Repeat from Step 3)

### Scenario B: Select "New token (different blockchain)"
```
👋 Select a blockchain for the Bubble Map:

[ Ethereum ] [ BSC ] [ Fantom ]
[ Avalanche ] [ Cronos ] [ Arbitrum ]
[ Polygon ] [ Base ] [ Solana ] [ Sonic ]
```
(Repeat from Step 2)

---

## 📑 Key Highlights
- ✅ Clear and intuitive workflow
- ✅ Real-time token data and analytics
- ✅ Interactive Bubble Map visualization
- ✅ AI-powered insights and recommendations
- ✅ User-friendly repetition and navigation

