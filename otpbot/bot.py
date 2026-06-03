from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "8503833146:AAGTxc25xG6k2AaELY3pAutWRDV5kMPNs1k"
CHANNEL = "@otpgrup42"

user_numbers = {}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)

        if member.status not in ["member", "administrator", "creator"]:
            raise Exception()

    except:

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
        return

    await main_menu(update, context)

# MAIN MENU
async def main_menu(update, context):

    buttons = [
        [
            InlineKeyboardButton("🆓 FREE NUMBER", callback_data="free")
        ],
        [
            InlineKeyboardButton("📦 STOCK", callback_data="stock"),
            InlineKeyboardButton("💰 BALANCE", callback_data="balance")
        ],
        [
            InlineKeyboardButton("👥 REFER", callback_data="refer")
        ]
    ]

    text = "🔥 OTP BOT PANEL"

    if hasattr(update, "callback_query"):

        await update.callback_query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    else:

        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# VERIFY
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:

        member = await context.bot.get_chat_member(CHANNEL, user_id)

        if member.status in ["member", "administrator", "creator"]:

            await main_menu(update, context)

        else:

            await query.answer(
                "Join channel first",
                show_alert=True
            )

    except:

        await query.answer(
            "Join channel first",
            show_alert=True
        )

# FREE NUMBER
async def free(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

# COUNTRY
async def country(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    buttons = [
        [
            InlineKeyboardButton(
                "🇧🇩 Bangladesh",
                callback_data="bd"
            )
        ],
        [
            InlineKeyboardButton(
                "🇮🇩 Indonesia",
                callback_data="id"
            )
        ]
    ]

    await query.message.edit_text(
        "Select Country",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# NUMBER SHOW
async def numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    nums = [
        f"+62831{random.randint(1000000,9999999)}",
        f"+62832{random.randint(1000000,9999999)}",
        f"+62833{random.randint(1000000,9999999)}"
    ]

    buttons = []

    for n in nums:

        buttons.append([
            InlineKeyboardButton(
                n,
                callback_data=f"num_{n}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            "🔄 REFRESH",
            callback_data="refresh"
        )
    ])

    await query.message.edit_text(
        "Select Number",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# SELECT NUMBER
async def select_number(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    number = query.data.replace("num_", "")

    user_numbers[query.from_user.id] = number

    await query.message.edit_text(
        f"✅ Selected:\n{number}\n\nWaiting for OTP..."
    )

# REFRESH
async def refresh(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await numbers(update, context)

# BUTTON HANDLER
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = update.callback_query.data

    if data == "verify":

        await verify(update, context)

    elif data == "free":

        await free(update, context)

    elif data in ["facebook", "whatsapp"]:

        await country(update, context)

    elif data in ["bd", "id"]:

        await numbers(update, context)

    elif data.startswith("num_"):

        await select_number(update, context)

    elif data == "refresh":

        await refresh(update, context)

# RUN BOT
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("BOT RUNNING...")

app.run_polling()
