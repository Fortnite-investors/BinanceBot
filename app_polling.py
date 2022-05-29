"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import config

from parsers import command_args
from modules import p2p_converter

from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['cost'])
async def cost(message: types.Message):
    arguments = message.get_args()

    print(arguments)
    print(type(arguments))

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
''' % (
    args.base_currency, args.base_bank, result.mean_buy_price,
    args.goal_currency, args.goal_bank, result.mean_sell_price,
    args.goal_amount, args.goal_currency, result.total_price, args.base_currency))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
