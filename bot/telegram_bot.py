import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from bot import commands, config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    book_bot = Updater(config.api_key, use_context=True, request_kwargs=config.proxy)

    bot_dispatcher = book_bot.dispatcher

    bot_dispatcher.add_handler(CommandHandler('start', commands.hello))
    bot_dispatcher.add_handler(MessageHandler(Filters.text, commands.lermontovizate))

    logger.info('Бот стартовал;')

    book_bot.start_polling()

    book_bot.idle()