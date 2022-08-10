import aiogram.types
mail=False
import config as cfg
import markup as nav
from db import *
from aiogram import types,executor,Bot,Dispatcher
bot = Bot(token=cfg.token)
dp=Dispatcher(bot)
dtb=DataBase('database.db')
async def check_subchannel(channels,user_id):
    for channel in channels:
        if channel!='':
            try:
                chat_member= await bot.get_chat_member(channel,user_id)
                if chat_member['status']=='left':
                    return False
            except:
                continue
    return True
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if await check_subchannel(cfg.channels,message.from_user.id):
        if not(dtb.get_user(message.from_user.id)):
            if message.text[7:]!='':
                dtb.add_user(message.from_user.id,int(message.text[7:]))
                referals=dtb.user_referals(int(message.text[7:]))+1
                dtb.add_referal(int(message.text[7:]),referals)
                money= dtb.user_money(int(message.text[7:]))+10
                dtb.set_money(int(message.text[7:]),10,money)
                await bot.send_message(int(message.text[7:]),'🔔За приглашение друга вы получаете 10 C')
                if dtb.user_referals(int(message.text[7:]))==10:
                    dtb.set_level(int(message.text[7:]),'⚙Silver')
                if dtb.user_referals(int(message.text[7:])) == 25:
                    dtb.set_level(int(message.text[7:]), '👑Gold')
                if dtb.user_referals(int(message.text[7:])) == 50:
                    dtb.set_level(int(message.text[7:]), '💎Platinum')
            else:
                dtb.add_user(message.from_user.id,None)
        await message.answer('Добро пожаловать в БОТ КЛИКЕР ГОЛДЫ🏆\n\n💰Здесь вы можете заработать голды кликая или приглашая друзей',reply_markup=nav.main_markup)
    else:
        await message.answer(cfg.submessage,reply_markup=nav.channles_markup,parse_mode=aiogram.types.ParseMode.MARKDOWN)
@dp.message_handler()
async def botz(message: types.Message):
    global mail
    if await check_subchannel(cfg.channels, message.from_user.id):
        if message.text=='💸Фармить голду💸':
            await message.answer('💥 +1 C')
            clicks= dtb.clicks(message.from_user.id)+1
            dtb.add_click(message.from_user.id,clicks)
            money=dtb.user_money(message.from_user.id)+1
            dtb.set_money(message.from_user.id,money)
        if message.text=='📒Баланс голды':
            await message.answer('💰Ваш баланс: '+str(dtb.user_money(message.from_user.id)))
        if message.text=='📦Вывод голды':
            if dtb.user_money(message.from_user.id)<1000:
                await message.answer('Вывод доступен от 1000C')
            elif dtb.user_level(message.from_user.id)!='💎Platinum':
                await message.answer('🔒ВЫВОД С НЕДОСТУПЕН🔒\n\nДля вывода С необходим уровень 💎Platinum\nЧтобы повысить уровень,приглашайте друзей по реферальной ссылке в ПРОФИЛЕ')
            else:
                await message.answer('Для вывода напишите @standadmin1')
        if message.text=='👤Профиль':
            await message.answer('💾Профиль ' + message.from_user.username + '\n\nВаш уровень: ' +str(dtb.user_level(message.from_user.id))+ '\n\nВаша реферальная ссылка:' + '\nhttps://t.me/standfbot?start=' + str(message.from_user.id))
        if message.text=='/subtext':
            await message.answer(cfg.submessage)
        if message.text.split()[0]=='/editsubtext':
            cfg.submessage=message.text[13:]
            await message.answer(cfg.submessage)
        if message.text.split()[0]=='/cadd':
            cfg.channels.append(message.text.split()[1])
            await message.answer('Канал успешно добавлен')
        if message.text.split()[0]=='/cremove':
            cfg.channels.remove(message.text.split()[1])
            await message.answer('Канал успешно удален')
        if message.text=='/mail_on':
            if message.from_user.id==1143219768:
                mail=True
                await message.answer('Рассылка успешно включена')
        elif mail==True:
            if message.from_user.id==1143219768:
                users=dtb.all_users()
                counter=0
                for user in users:
                    try:
                        await message.forward(user[0])
                        counter+=1
                    except:
                        continue
                mail=False
                await message.answer('Рассылка проведена,количество получателей:'+str(counter))
    else:
        await message.answer(cfg.submessage,reply_markup=nav.channles_markup,parse_mode=aiogram.types.ParseMode.MARKDOWN)
@dp.message_handler(content_types=aiogram.types.ContentType.PHOTO)
async def mail_photo(message: types.Message):
    global mail
    if mail==True:
        if message.from_user.id==1143219768:
            users = dtb.all_users()
            counter = 0
            for user in users:
                try:
                    await message.forward(user[0])
                    counter += 1
                except:
                    continue
            mail = False
            await message.answer('Рассылка проведена,количество получателей:' + str(counter))
@dp.callback_query_handler(text='checksubchannel')
async def sub(message):
    if await check_subchannel(cfg.channels,message.from_user.id):
        if not(dtb.get_user(message.from_user.id)):
            if message.message.text[7:]!='':
                dtb.add_user(message.from_user.id,int(message.message.text[7:]))
                referals=dtb.user_referals(int(message.message.text[7:]))+1
                dtb.add_referal(int(message.message.text[7:]),referals)
                money= dtb.user_money(int(message.message.text[7:]))+10
                dtb.set_money(int(message.message.text[7:]),10,money)
                await bot.send_message(int(message.message.text[7:]),'🔔За приглашение друга вы получаете 10 C')
                if dtb.user_referals(int(message.message.text[7:]))==10:
                    dtb.set_level(int(message.message.text[7:]),'⚙Silver')
                if dtb.user_referals(int(message.message.text[7:])) == 25:
                    dtb.set_level(int(message.message.text[7:]), '👑Gold')
                if dtb.user_referals(int(message.message.text[7:])) == 50:
                    dtb.set_level(int(message.message.text[7:]), '💎Platinum')
            else:
                dtb.add_user(message.from_user.id,None)
        await bot.send_message(message.from_user.id,'Добро пожаловать в БОТ КЛИКЕР ГОЛДЫ🏆\n\n💰Здесь вы можете заработать голды кликая или приглашая друзей',reply_markup=nav.main_markup)
    else:
        await bot.send_message(message.from_user.id,cfg.submessage,reply_markup=nav.channles_markup,parse_mode=aiogram.types.ParseMode.MARKDOWN)
if __name__=='__main__':
    executor.start_polling(dp)