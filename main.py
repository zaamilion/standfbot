from aiogram import types,executor,Bot,Dispatcher
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup

bot = Bot(token='5482816138:AAHzJRieWZH4SEXAfMpUV_UpnPuj8VNDgDk')
dp = Dispatcher(bot)
button1=KeyboardButton('💰ФАРМИТЬ ГОЛДУ💰')
button2=KeyboardButton('🔒Вывод🔒')
button3=KeyboardButton('💸Заработать голду💸')
menu=ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2).add(button3)
channels=['@zamstand']
markup=InlineKeyboardMarkup(row_width=1).insert(InlineKeyboardButton(text='ПРОВЕРИТЬ',callback_data='check'))
async def check_subchannel(user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(channel,user_id)
        if chat_member['status']=='left':
            await bot.send_message(user_id,'🔥БРОО, ты уже готов зарабатывать голду на халявуу???\nТогда для работы бота подпишись на каналы:\n\n'
                                           '[ПОДПИСАТЬСЯ](https://t.me/zamstand)\n',reply_markup=markup,parse_mode=types.ParseMode.MARKDOWN)
            return False
        return True
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if await check_subchannel(message.from_user.id):
        await message.answer('ТЫ УЖЕ МОЖЕШЬ ЗАРАБАТЫВАТЬ ГОЛДУ 🔥🔥🔥',reply_markup=menu)
@dp.message_handler()
async def commands(message: types.Message):
    if await check_subchannel(message.from_user.id):
        if message.text=='💰ФАРМИТЬ ГОЛДУ💰':
            await message.answer('+0.2G')
        if message.text=='🔒Вывод🔒':
            await message.answer('Для вывода необходимо написать @standadmin1')
        if message.text=='💸Заработать голду💸':
            await message.answer('Зарабатывай по 20 голды за каждого друга!\n\nПриглашай их в бота по твоей реф.ссылке и зарабатывай голду\n\nТвоя ссылка:\n https://t.me/standfbot?start='+str(message.from_user.id))
@dp.callback_query_handler(text='check')
async def check(call):
    if await check_subchannel(call.from_user.id):
        await bot.send_message(call.from_user.id,'ТЫ УЖЕ МОЖЕШЬ ЗАРАБАТЫВАТЬ ГОЛДУ 🔥🔥🔥', reply_markup=menu)
executor.start_polling(dp)
