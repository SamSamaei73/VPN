import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update, InputFile

API_URL = "http://127.0.0.1:8000"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    username = update.effective_user.username or "unknown"

    requests.post(
        f"{API_URL}/users",
        params={
            "telegram_id": telegram_id,
            "username": username
        }
    )

    await update.message.reply_text("User registered in VPN system")


async def new_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    user = requests.get(f"{API_URL}/users/telegram/{telegram_id}").json()

    vpn_data = requests.post(
        f"{API_URL}/create-vpn",
        params={
            "user_id": user["id"],
            "device_name": "telegram-auto-device"
        }
    ).json()

    with open(vpn_data["config_path"], "rb") as conf_file:
        await update.message.reply_document(
            document=InputFile(conf_file, filename="wireguard.conf")
        )

    with open(vpn_data["qr_path"], "rb") as qr_file:
        await update.message.reply_photo(photo=qr_file)


def main():
    TOKEN = "8723627197:AAFA5qUfIAniWOinI_pEduJx8JO6wuKNQ8Q"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("device", new_device))

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()