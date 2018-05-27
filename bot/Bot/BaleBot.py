from balebot.updater import Updater
from balebot.handlers import MessageHandler
from balebot.filters import TextFilter
from balebot.models.messages import TextMessage, TemplateMessage, TemplateMessageButton
import asyncio
from ...shop.models import Transaction

TOKEN = 'c45353aeb2d0e1e6c2862b2511803e14ce10201b'  # Bale messenger token
updater = Updater(token=TOKEN, loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher

bot = updater.bot


def success(response, user_data):
    print("success: ", response)
    print(user_data)


def failure(response, user_data):
    print("failure: ", response)
    print(user_data)


#@dispatcher.command_handler(["/start"])
def start(bot, update):
    message = TextMessage("سلام. به فروشگاه ما خوش اومدید!")
    message2 = TextMessage("برو ببین اومد یا نه")
    user_peer = update.get_effective_user()
    buttons = [TemplateMessageButton(text="خرید", value="test", action=1), TemplateMessageButton(text="درباره ما", value="test", action=1)]
    template = TemplateMessage(general_message=message, btn_list=buttons)
    testing = Transaction(total_price=1111, number=100, shopper='haji')
    testing.save()
    bot.send_message(template, user_peer, success_callback=success, failure_callback=failure)
    bot.send_message(message2, user_peer, success_callback=success, failure_callback=failure)
    # dispatcher.set_conversation_data(update=update, key='name', value="no_name")

test = MessageHandler(TextFilter(keywords=["hello"]), start)
dispatcher.add_handler(test)
updater.run()
