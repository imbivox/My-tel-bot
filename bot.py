import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 🛑 ------------------ شخصی‌سازی پروفایل شما (نسخه نهایی و کامل) ------------------

TOKEN = '8646276779:AAFOR5MFv4bT5UuxH7froaqiknqIkAN5N38'
MY_ADMIN_ID = 8110790845

START_TEXT = (
    "👋 **سلام و درود! به بورد شخصی من خوش آمدی**\n\n"
    "✨ من این ربات رو ساختم تا بتونی خیلی راحت با علایق، مشخصات سیستم و پل‌های ارتباطی من آشنا بشی.\n\n"
    "👇 **از دکمه‌های زیر برای گشت‌وگذار استفاده کن:**"
)

PC_SPECS = (
    "🖥️ ─── **⚙️ مشخصات کیس من** ───\n\n"
    "🔹 **پردازنده (CPU):** `Intel Core i5 12400F`\n"
    "🔹 **کارت گرافیک (GPU):** `AMD Radeon RX 6700 XT (12GB)`\n"
    "🔹 **حافظه موقت (RAM):** `32GB DDR4 3200MHz`\n"
    "🔹 **مادربورد (Main):** `ASUS Prime H610M-A`"
)

MY_SETUP = (
    "⌨️ ─── **🎧 لوازم جانبی و ستاپ** ───\n\n"
    "🎧 **هدفون:** `GH5162 / Razer Kraken Lite`\n"
    "🖱️ **موس:** `TSCO GM790 / VXE Dragonfly R1 SE+ / Bloody R72 Ultra`\n"
    "⌨️ **کیبورد:** `Onikuma G69 / TSCO GK8162`\n"
    "🖥️ **مانیتور:** `MSI G244 E2 (180Hz)`"
)

MY_GAMES = (
    "🎮 ─── **🕹️ بازی‌های موردعلاقه من** ───\n\n"
    "🔥 این روزا بیشتر وقتم رو پای این گیم‌ها می‌ذارم:\n\n"
    "🥇 `Counter-Strike 2`\n"
    "🥈 `Elden Ring`\n"
    "🥉 `Minecraft`\n"
    "🏆 `Fortnite`"
)

ABOUT_ME = (
    "ℹ️ ─── **👤 درباره من** ───\n\n"
    "سلام، من هیرادم، ۱۵ سالمه و یه گیمر و بسکتبالیست‌ام. 🏀🎮\n"
    "این بات رو ساختم که راحت‌تر من رو بشناسی. مرسی که سر زدی! ❤️"
)

MY_LINKS = (
    "🌐 ─── **🔗 پل‌های ارتباطی با من** ───\n\n"
    "خوشحال میشم بتونیم در پلتفرم‌های دیگه هم با هم در ارتباط باشیم:\n\n"
    "👾 **دیسکورد:** `Coming Soon...`\n"
    "🎮 **استیم:** `hiradgame`\n"
    "📸 **اینستاگرام:** @hiradhamidi2"
)

PLAYLIST_URL = 'https://t.me/playlistbivox'

# 🛑 ---------------------------------------------------------------------

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎵 플레이리스트 | My Playlist", url=PLAYLIST_URL)],
        [
            InlineKeyboardButton("🖥️ PC Specs", callback_data='pcspecs'),
            InlineKeyboardButton("⌨️ My Setup", callback_data='mysetup')
        ],
        [
            InlineKeyboardButton("🎮 My Games", callback_data='mygames'),
            InlineKeyboardButton("🌐 Links", callback_data='links')
        ],
        [InlineKeyboardButton("ℹ️ About Me", callback_data='aboutme')],
        [InlineKeyboardButton("📩 ارسال پیام ناشناس به من", callback_data='contact_me')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT, reply_markup=get_main_keyboard(), parse_mode="Markdown")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'pcspecs':
        await query.edit_message_text(text=PC_SPECS, reply_markup=get_main_keyboard(), parse_mode="Markdown")
    elif query.data == 'mysetup':
        await query.edit_message_text(text=MY_SETUP, reply_markup=get_main_keyboard(), parse_mode="Markdown")
    elif query.data == 'mygames':
        await query.edit_message_text(text=MY_GAMES, reply_markup=get_main_keyboard(), parse_mode="Markdown")
    elif query.data == 'links':
        await query.edit_message_text(text=MY_LINKS, reply_markup=get_main_keyboard(), parse_mode="Markdown")
    elif query.data == 'aboutme':
        await query.edit_message_text(text=ABOUT_ME, reply_markup=get_main_keyboard(), parse_mode="Markdown")
    elif query.data == 'contact_me':
        context.user_data['waiting_for_msg'] = True
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 بازگشت به منو", callback_data='back_to_menu')]])
        await query.edit_message_text(text="✍️ **هر حرفی، انتقادی یا سخنی تو دلت هست بنویس و بفرست:**\n\n*(پیام شما کاملاً ناشناس و بدون نام برای من ارسال میشه)*", reply_markup=back_kb, parse_mode="Markdown")
    elif query.data == 'back_to_menu':
        context.user_data['waiting_for_msg'] = False
        await query.edit_message_text(text=START_TEXT, reply_markup=get_main_keyboard(), parse_mode="Markdown")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if context.user_data.get('waiting_for_msg') and user_id != MY_ADMIN_ID:
        user_msg = update.message.text
        try:
            report_text = f"📩 **پیام ناشناس جدید دریافت شد!**\n💬 __متن پیام:__\n\n{user_msg}\n\n⚠️ __برای پاسخ دادن، فقط روی همین پیام ریپلای کنید.__"
            sent_msg = await context.bot.send_message(chat_id=MY_ADMIN_ID, text=report_text, parse_mode="Markdown")

            if 'replies' not in context.bot_data:
                context.bot_data['replies'] = {}
            context.bot_data['replies'][sent_msg.message_id] = user_id

            await update.message.reply_text("✨ **پیام شما با موفقیت و به صورت ناشناس ارسال شد!**", reply_markup=get_main_keyboard(), parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text("❌ مشکلی پیش آمد. احتمالاً تنظیمات ادمین درست نیست.")
        context.user_data['waiting_for_msg'] = False

    elif user_id == MY_ADMIN_ID and update.message.reply_to_message:
        reply_id = update.message.reply_to_message.message_id
        if 'replies' in context.bot_data and reply_id in context.bot_data['replies']:
            target_user_id = context.bot_data['replies'][reply_id]
            admin_answer = update.message.text
            try:
                await context.bot.send_message(chat_id=target_user_id, text=f"📣 **پاسخ جدید از طرف صاحب ربات:**\n\n💬 {admin_answer}")
                await update.message.reply_text("✅ پاسخ شما با موفقیت برای کاربر ارسال شد.")
            except Exception as e:
                await update.message.reply_text("❌ ارسال پاسخ ناموفق بود. شاید کاربر ربات را بلاک کرده باشد.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    print("ربات کارت ویزیت لوکس روشن شد...")
    app.run_polling()

if __name__ == '__main__':
    main()
