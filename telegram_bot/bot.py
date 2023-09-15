"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import links    
from telegram import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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

# class NotInConversationFilter(filters.BaseFilter):
#     def check_update(  # skipcq: PYL-R0201
#         self, update: Update
#     ):
#         """Checks if the specified update should be handled by this filter.

#         Args:
#             update (:class:`telegram.Update`): The update to check.

#         Returns:
#             :obj:`bool`: :obj:`True` if the update contains one of
#             :attr:`~telegram.Update.channel_post`, :attr:`~telegram.Update.message`,
#             :attr:`~telegram.Update.edited_channel_post` or
#             :attr:`~telegram.Update.edited_message`, :obj:`False` otherwise.
#         """
#         if (  # Only message updates should be handled.
#             update.channel_post
#             or update.message
#             or update.edited_channel_post
#             or update.edited_message
#         ):
#             return self.filter(update.effective_message, update)
#         return False

#     def filter(self, message, update):
#         print(message)
#         # Check if the message is not processed by the conversation handler
#         return False
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    description = update.message.text
    rep = await get_products(None, None, description)
    await update.message.reply_text(
        f"نتائج البحث"
        "\n\n"
        + rep,
    )

TOKEN = links.Token

from upload_conversation import upload_conv_handler
from price_conversation import price_conv_handler
def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    
    application = Application.builder().token(TOKEN).build()
    print("Build application...")

    application.add_handler(price_conv_handler)
    application.add_handler(upload_conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    print("Start Polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    

if __name__ == "__main__":
    main()