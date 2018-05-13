import telegram
import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


TELEGRAM_TOKEN = "437283497:AAF_PIsNJe1AURGYKnKzHxjBKkMV7oYwOSo"
ITEM_LIST = [['http://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-11/256/honey-pot.png', 'عسل چرنوبیل قیمت 23432 تومان', 'add_chevil'],
             ['https://images.freshop.com/00073260000011/15d7f41f3e83d65cc0c087d2a0ed2d75_medium.png', 'عسل شاخ گوساله قیمت 23432 تومان', 'add_chorbil'],
             ['https://images.freshop.com/00011153146101/2ae35cb6bea7d5c5c957dc9341f45c2e_medium.png', 'عسل برگ استقدوس قیمت 23432 تومان', 'add_chibil']]
CART = "cart.json"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname) - %(message)s', level=logging.INFO)


def start(bot, update):
    keyboard = [[InlineKeyboardButton("خرید", callback_data='1')],
                [InlineKeyboardButton("درباره ما", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('در صورتی که تمایل به خرید دارید دکمه /"خرید" و برای درباره ما /"درباره ما" رو فشار بدید', reply_markup= reply_markup)


def buttons(bot, update):  # TODO : add quality assurance here and in start()
    query = update.callback_query
    if query.data == '2':
        about_us(bot, update)
    else:
        shop(bot, update)


def shop(bot, update):
    query = update.callback_query.data
    if query == '1':
        for item in ITEM_LIST:
            keyboard = [[InlineKeyboardButton("اضافه به سبد", callback_data=item[2])]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_photo(photo=item[0],
                           chat_id=update.callback_query.message.chat_id,
                           caption=item[1],
                           reply_markup=reply_markup)
    if query[0:4] == 'add_':
        cart_file = open(CART, 'w')
        cart = json.loads(CART)
        if update.callback_query.message.chat_id in cart['incomplete']:
            cart['incomplete'][update.callback_query.message.chat_id]['cart'][query[4:]] = 1
        else:
            cart['incomplete'][update.callback_query.message.chat_id] = {'cart': {query[4:]: 1}}
        cart_file.write(json.dumps(cart))
        bot.send_message(text='added', chat_id=update.callback_query.message.chat_id,
                         message_id=update.callback_query.message.message_id)


def about_us(bot, update):
    bot.send_message(text="اینجا درباره ماست!!",
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id)


def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(buttons))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()