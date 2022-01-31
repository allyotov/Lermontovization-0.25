import logging
from lermontovization.transfiguration import process_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def hello(update, context):
    update.message.reply_text(''.join([
        'Граждане! Этот бот лермонтовизирует любой текст',
        ' путём механической замены всех прилагательных в нём ',
        'на "безумный" и "неземной".',
    ]),
    )


def lermontovizate(update, context):
    try:
        if update.message.text:
            lermontovizated_text = process_text(update.message.text)
            update.message.reply_text(text='Лермонтовизированный вариант этого текста:')
            update.message.reply_text(text=lermontovizated_text)
        else:
            update.message.reply_text(
                'Граждане! Вы не задали инетересующий вас текст!',
            )
    except Exception as exc:
        logging.exception(exc)
        update.message.reply_text(
            'Ой, у нас что-то пошло не так. Попробуйте, пожалуйста, позже.',
        )