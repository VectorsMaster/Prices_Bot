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
    check_password,
    upload_file,
)

PASS, EXC_FILE = range(2)

async def start_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the uploading process"""
    user = update.message.from_user

    await update.message.reply_text(
        "Hi! this is saipa parts admin bot. Please write your password to continue!\n\n"
        "Send /cancel_upload to stop talking to me.\n\n",
    )

    return PASS

async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    password = update.message.text
    print(f"User: {user}")
    print(f"Password: {password}")

    token = await check_password(password)
    print(f"Token: {token}")

    if token is not None:
        context.user_data['token'] = token
        await update.message.reply_text(
            "Your password is correct",
        )
        return EXC_FILE
    else :
        await update.message.reply_text(
            "Your password is incorrect\n\n"
            "Plese enter your password again or /skip",
        )
        return PASS

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        file = await update.message.document.get_file()
        token = context.user_data['token'] 
        print(f"file_path: {file.file_path}, token: {token}")

        response = await upload_file(file.file_path, token)
        
        if response is True:
            await update.message.reply_text(
                'The file was uploaded successfully\n\n'
                'We will process is asap and update the database',
            )
            return ConversationHandler.END
        else :
            raise RuntimeError(f"An error occurred while sending the request")
        
    except Exception as e:

        print(e)
        await update.message.reply_text(
            'An error occured!\n'
            'Please upload the file again',
        )
        return EXC_FILE

async def cancel_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    # logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


upload_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start_upload", start_upload)],
    states={
        PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password)],
        EXC_FILE: [MessageHandler(filters.Document.MimeType('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'), handle_file)],
    },
    fallbacks=[CommandHandler("cancel_upload", cancel_upload)],
)