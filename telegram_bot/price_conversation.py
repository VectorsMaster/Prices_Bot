from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from req import (
    get_products,
)

CATEGORY, FILT = range(2)

async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about the category."""
    reply_keyboard = [ 
        ["المحرك"],
        ["علبة سرعة"],
        ["الميزانية والتعليق"],
        ["دارة الوقود"],
        ["دارة التبريد"],
        ["دارة التزييت"],
        ["دارة الكهرباء"],
        ["الهيكل والفرش"],
        ["اكسسوارات"],
    ]
    context.user_data['conv'] = True
    await update.message.reply_text(
        "Let me show you the prices.\n"
        "Which category are you looking for?\n"
        "Or send /cancel to stop talking to me.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Category"
        ),
    )

    return CATEGORY

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    context.user_data['category'] = update.message.text
    context.user_data['conv'] = True

    await update.message.reply_text(
        "I see! Please send me part of the product name\n"
        "Or send /cancel to stop talking to me.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return FILT

async def products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    description = update.message.text
    rep = await get_products(None ,context.user_data['category'], description)
    await update.message.reply_text(
        f"Thank you for your question about {description} from category {context.user_data['category']}"
        "\n\n"
        + rep,
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    # logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


price_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("prices", prices)],
    states={
        CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category)],
        FILT: [MessageHandler(filters.TEXT & ~filters.COMMAND, products)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
    