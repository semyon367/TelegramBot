from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from core.handlers.basic import get_start, get_photo, get_hello
from core.filters.iscontact import IsTrueContact
from core.handlers.contact import get_fake_contact, get_true_contact
import asyncio
import logging
from core.settings import settings
from aiogram.filters import Command
from core.utils.commands import set_commands
from core.handlers.basic import get_location, get_inline
from core.handlers.callback import select_macbook
from core.utils.callbackdata import MacInfo
from core.handlers.pay import order, pre_checkout_query, succesful_payment, shipping_check
from core.middlewares.counter import CounterMiddleware
from core.middlewares.officehours import OfficeHoursMiddleware
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.appschedulermiddleware import SchedulerMiddleware
import psycopg_pool
from core.handlers import form
from core.utils.statesform import StepsForm
from apscheduler.schedulers.asyncio import  AsyncIOScheduler
from core.handlers import apched
from datetime import datetime, timedelta
from core.handlers import send_media
from aiogram.utils.chat_action import ChatActionMiddleware
from core.middlewares.example_chat_action_middleware import ExampleChatActionMiddleware
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен!')


def create_pool():
    return psycopg_pool.AsyncConnectionPool(f"host=127.0.0.1 port=5432 dbname=users user=postgres password=gbcpgeam98 "
                                            f"connect_timeout=60")


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                                "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    pool_connect = create_pool()
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone='Asia/Irkutsk')
    scheduler.add_job(apched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
                      kwargs={'bot': bot})
    scheduler.add_job(apched.send_message_cron, trigger='cron', hour=datetime.now().hour,
                      minute=datetime.now().minute + 1, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(apched.send_message_interval, trigger='interval', seconds=60, kwargs={'bot': bot})
    scheduler.start()


    dp.update.middleware.register(DbSession(pool_connect))
    dp.message.middleware.register(CounterMiddleware())
    # dp.update.middleware.register(OfficeHoursMiddleware())
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.message.middleware.register(ChatActionMiddleware())
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(send_media.get_audio, Command(commands='audio'))
    dp.message.register(send_media.get_document, Command(commands='document'))
    dp.message.register(send_media.get_media_group, Command(commands='mediagroup'))
    dp.message.register(send_media.get_photo, Command(commands='photo'))
    dp.message.register(send_media.get_sticker, Command(commands='sticker'))
    dp.message.register(send_media.get_video, Command(commands='video'))
    dp.message.register(send_media.get_video_note, Command(commands='video_note'))
    dp.message.register(send_media.get_voice, Command(commands='voice'))


    dp.message.register(form.get_form, Command(commands='form'))
    dp.message.register(form.get_name, StepsForm.GET_NAME)
    dp.message.register(form.get_last_name, StepsForm.GET_LAST_NAME)
    dp.message.register(form.get_age, StepsForm.GET_AGE)

    dp.message.register(order, Command(commands='pay'))
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.message.register(succesful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    dp.shipping_query.register(shipping_check)
    dp.message.register(get_inline, Command(commands='inline'))
    dp.callback_query.register(select_macbook, MacInfo.filter(F.model == 'pro'))
    dp.message.register(get_location, F.location)
    dp.message.register(get_hello, F.text == 'Привет')
    dp.message.register(get_true_contact, F.contact, IsTrueContact())
    dp.message.register(get_fake_contact, F.contact)
    dp.message.register(get_photo, F.photo)
    dp.message.register(get_start, Command(commands=['start', 'run']))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())
