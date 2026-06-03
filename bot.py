from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN ="8503833146:AAGN0iI4w2IF26VPZejjwTQ3AlMiQiq1EGc"
CHANNEL = "@otpgrup42"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    buttons = [
        [
            InlineKeyboardButton(
                "📢 JOIN CHANNEL",
                url=f"https://t.me/{CHANNEL.replace('@','')}"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ VERIFY",
                callback_data="verify"
            )
        ]
    ]

    await update.message.reply_text(
        "🔒 Join Channel First",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    buttons = [
        [
            InlineKeyboardButton(
                "📘 Facebook",
                callback_data="facebook"
            )
        ],
        [
            InlineKeyboardButton(
                "🟢 WhatsApp",
                callback_data="whatsapp"
            )
        ]
    ]

    await query.message.edit_text(
        "Select Category",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    data = query.data

    if data == "verify":

        await verify(update, context)

    elif data in ["facebook", "whatsapp"]:

        nums = [
            f"+62831{random.randint(1000000,9999999)}",
            f"+62832{random.randint(1000000,9999999)}",
            f"+62833{random.randint(1000000,9999999)}"
        ]

        btn = []

        for n in nums:

            btn.append([
                InlineKeyboardButton(
                    n,
                    callback_data=n
                )
            ])

        btn.append([
            InlineKeyboardButton(
                "🔄 REFRESH",
                callback_data=data
            )
        ])

        await query.message.edit_text(
            "Select Number",
            reply_markup=InlineKeyboardMarkup(btn)
        )

    else:

        await query.message.edit_text(
            f"✅ Selected Number:\n\n{data}"
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("BOT RUNNING...")

app.run_polling()
