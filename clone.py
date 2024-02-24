from telegram.ext import Updater, CommandHandler

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Bot! You can start using it now.")

def clone(update, context):
    if len(context.args) != 1:
        update.message.reply_text("Usage: /clone <token>")
        return
    clone_token = context.args[0]
    try:
        clone_updater = Updater(token=clone_token, use_context=True)
        clone_dispatcher = clone_updater.dispatcher
        clone_dispatcher.add_handler(CommandHandler('start', start))
        clone_updater.start_polling()
        update.message.reply_text("Bot successfully cloned!")
    except Exception as e:
        update.message.reply_text(f"Error cloning bot: {e}")

def main():
    updater = Updater(token='6055798094:AAEQ1wueHQJ1-r81kxO97gF0JQdbRSWY5lI', use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('clone', clone))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
