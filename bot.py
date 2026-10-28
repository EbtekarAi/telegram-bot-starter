"""Ebtekar Telegram bot starter — an AI assistant bot powered by the Ebtekar Developer Gateway.

Env:  TELEGRAM_BOT_TOKEN   from @BotFather
      EBTEKAR_API_KEY      from https://ebtekarai.ir/developers
      ALLOWED_USER_IDS     optional, comma-separated Telegram user IDs (recommended: keeps your bill safe)
"""
import logging
import os
import uuid
from collections import defaultdict, deque

import anthropic
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

BASE_URL = os.environ.get("EBTEKAR_BASE_URL", "https://ebtekarai.ir/api/developer-gateway")
MODEL = os.environ.get("EBTEKAR_MODEL", "ebtekar-smart")
MAX_TOKENS = int(os.environ.get("EBTEKAR_MAX_TOKENS", "1024"))
SYSTEM = os.environ.get(
    "EBTEKAR_SYSTEM",
    "تو یک دستیار صمیمی در تلگرام هستی. کوتاه، مفید و به زبان کاربر جواب بده.",
)
ALLOWED = {int(x) for x in os.environ.get("ALLOWED_USER_IDS", "").replace(" ", "").split(",") if x}
TELEGRAM_LIMIT = 4096

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
log = logging.getLogger("ebtekar-bot")

client = anthropic.AsyncAnthropic(api_key=os.environ["EBTEKAR_API_KEY"], base_url=BASE_URL, default_headers={"User-Agent": "Ebtekar-Client/1.0"})
# Last 20 messages per chat, kept in memory only.
memory: dict[int, deque] = defaultdict(lambda: deque(maxlen=20))


def allowed(update: Update) -> bool:
    return not ALLOWED or (update.effective_user and update.effective_user.id in ALLOWED)


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "سلام! 👋 من دستیار ابتکار هستم. هر سؤالی داری بپرس.\n"
        "برای شروع گفتگوی تازه /reset را بفرست."
    )


async def reset(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    memory.pop(update.effective_chat.id, None)
    await update.message.reply_text("گفتگو پاک شد. ✨")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not allowed(update):
        await update.message.reply_text("این ربات خصوصی است.")
        return

    chat_id = update.effective_chat.id
    history = memory[chat_id]
    history.append({"role": "user", "content": update.message.text[:6000]})
    while history and history[0]["role"] != "user":  # trimmed history must start with a user turn
        history.popleft()

    await context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    try:
        resp = await client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM,
            messages=list(history),
            extra_headers={"Idempotency-Key": str(uuid.uuid4())},
        )
        answer = "".join(b.text for b in resp.content if b.type == "text").strip() or "…"
    except anthropic.APIStatusError as e:
        history.pop()
        log.warning("gateway error %s (request-id %s)", e.status_code, e.response.headers.get("x-request-id"))
        await update.message.reply_text("متأسفم، الان نتوانستم جواب بدهم. کمی بعد دوباره امتحان کن.")
        return
    except anthropic.APIConnectionError:
        history.pop()
        await update.message.reply_text("ارتباط با ابتکار برقرار نشد. دوباره امتحان کن.")
        return

    history.append({"role": "assistant", "content": answer})
    for i in range(0, len(answer), TELEGRAM_LIMIT):
        await update.message.reply_text(answer[i : i + TELEGRAM_LIMIT])


def main() -> None:
    app = Application.builder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    log.info("Bot is running with model %s", MODEL)
    app.run_polling()


if __name__ == "__main__":
    main()
