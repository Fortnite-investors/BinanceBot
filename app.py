import config
from parsers import command_args
from modules import p2p_converter

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    """Handle start command"""
    await message.reply("""
/cost GOAL_AMOUNT GOAL_CURRENCY GOAL_BANK BASE_CURRENCY BASE_BANK - выводит стоимость конвертации рублей в определнную валюту через USDT p2p
/help - помощь по командам
    """)


@dp.message_handler(commands=['chat_id'])
async def chat_id(message: types.Message):
    await message.reply(message.chat.id)


@dp.message_handler(commands=['cost'])
async def cost(message: types.Message):
    arguments = message.get_args()

    try:
        args = command_args.CostArgs(arguments)
        result = await p2p_converter.module.calc_convert_price(
            args.goal_amount, args.goal_currency, args.goal_bank, args.base_currency,
            args.base_bank
        )
    except (p2p_converter.exceptions.ConvertError, command_args.ParseError) as exc:
        await message.reply(str(exc))
    else:
        await message.reply(
'''
Цена покупки USDT за фиат %s с %s: %s
Цена продажи USDT за %s на %s: %s
Итоговая стоимость %s %s - %s %s
Итоговый курс 1 %s - %s %s
''' % (
    args.base_currency, args.base_bank, result.mean_buy_price,
    args.goal_currency, args.goal_bank, result.mean_sell_price,
    args.goal_amount, args.goal_currency, result.total_price, args.base_currency,
    args.goal_currency, result.total_rate, args.base_currency))




async def on_startup(app):
    """Simple hook for aiohttp application which manages webhook"""
    await bot.delete_webhook()
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp):
    pass


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_URL_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)
