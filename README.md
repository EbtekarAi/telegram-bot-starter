<div align="center">

<img src="https://raw.githubusercontent.com/EbtekarAi/ebtekar-ai/main/assets/logo.png" width="84">

# Ebtekar Telegram Bot Starter

**Launch your own AI assistant on Telegram in five minutes, powered by Ebtekar.**

ربات دستیار هوش مصنوعی خودتان را در پنج دقیقه روی تلگرام راه بیندازید

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/python--telegram--bot-21%2B-26A5E4?logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-7C3AED)

</div>

---

## Features / قابلیت‌ها

- 💬 Remembers the last 20 messages of each chat (in memory only)
- 🔒 Optional allowlist of Telegram user IDs, so strangers can't spend your balance
- ✂️ Long answers are split automatically to fit Telegram's 4096-character limit
- 🧹 `/start` for a welcome message · `/reset` to clear the conversation
- 🔁 A unique `Idempotency-Key` per request, and errors are logged with `x-request-id`

## Setup / راه‌اندازی

1. Create a bot with **[@BotFather](https://t.me/BotFather)** and copy its token.
   با **@BotFather** یک ربات بسازید و توکنش را کپی کنید.
2. Create an API key at **[ebtekarai.ir/developers](https://ebtekarai.ir/developers)**.
   از پنل توسعه‌دهندگان ابتکار یک کلید API بسازید.
3. Run:

```bash
git clone https://github.com/EbtekarAi/telegram-bot-starter.git
cd telegram-bot-starter
pip install -r requirements.txt

export TELEGRAM_BOT_TOKEN="123456:..."
export EBTEKAR_API_KEY="ebt_live_..."
export ALLOWED_USER_IDS="11111111"        # your own Telegram user ID (recommended)
python bot.py
```

> **Hosting / میزبانی:** run the bot on a server that can reach Telegram's API. Set the tokens as environment variables in your host's panel, and never commit them.
>
> ربات را روی سروری اجرا کنید که به API تلگرام دسترسی دارد. توکن‌ها را به‌صورت متغیر محیطی در پنل میزبان تعریف کنید و هرگز در Git قرار ندهید.

## Settings / تنظیمات

| Variable | Default | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | — | **Required.** From @BotFather |
| `EBTEKAR_API_KEY` | — | **Required.** Your `ebt_live_…` key |
| `ALLOWED_USER_IDS` | *(everyone)* | Comma-separated user IDs allowed to use the bot |
| `EBTEKAR_MODEL` | `ebtekar-smart` | Any ID from `GET /v1/models` |
| `EBTEKAR_MAX_TOKENS` | `1024` | Output cap per answer |
| `EBTEKAR_SYSTEM` | Friendly Persian assistant | The bot's personality |

## Related / مرتبط

📘 [Developer guide](https://github.com/EbtekarAi/ebtekar-ai/blob/main/docs/developers.md) · 💬 [Web chat UI](https://github.com/EbtekarAi/chat-ui) · 🍳 [Cookbook](https://github.com/EbtekarAi/ebtekar-cookbook)

<sub>MIT © Ebtekar AI</sub>
