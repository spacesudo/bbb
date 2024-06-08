from db import Users, Bridge
import telebot
from telebot import types
from telebot.types import WebAppInfo
from telebot.util import antiflood, extract_arguments
import os
from dotenv import load_dotenv
import time
from func import minimum, output, exchange, exchange_status


load_dotenv()

db_users = Users()
db_bridge = Bridge()

db_users.setup()
db_bridge.setup()

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")



@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    print(message.from_user.id)
    messager = message.chat.id
    if str(messager) == "7034272819" or str(messager) == "6219754372":
        send = bot.send_message(message.chat.id,"Enter message to broadcast")
        bot.register_next_step_handler(send,sendall)
        
    else:
        bot.reply_to(message, "You're not allowed to use this command")
        
        
        
def sendall(message):
    users = db_users.get_users()
    for chatid in users:
        try:
            msg = antiflood(bot.send_message, chatid, message.text)
        except Exception as e:
            print(e)
        
    bot.send_message(message.chat.id, "done")
    

@bot.message_handler(commands=['userno'])
def userno(message):
    print(message.from_user.id)
    messager = message.chat.id
    if str(messager) == "7034272819" or str(messager) == "6219754372":
        x = db_users.get_users()
        bot.reply_to(message,f"Total bot users: {len(x)}")
    else:
        bot.reply_to(message, "admin command")
        
        
@bot.message_handler(commands=['start'])
def start(message):
    owner = message.chat.id
    db_users.add_user(owner)
    
    msg = """Welcome to Maximus Bridger Bot 

Bridge tokens from one chain to another using the most complete cross-chain brige webapp

Use the mixer to anonymously send transactions through blockchains    
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn = types.InlineKeyboardButton('Bridge', web_app=WebAppInfo(url='https://www.google.com'))
    btn1 = types.InlineKeyboardButton('Mixer', callback_data='mixer')
    markup.add(btn,btn1)
    bot.send_message(owner, msg, reply_markup=markup)
    
    

        
     
     
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    owner = call.message.chat.id
    
    if call.data == 'mixer':
        bot.delete_message(owner, call.message.message_id)
        
        msg = """Select a chain to mix and anonymously send transactions Through
        
we currently only support sol and eth.

Please Know that mixing transactions can take about an hour to get completed 
        """
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('ETH', callback_data='ethmix')
        btn2 = types.InlineKeyboardButton('SOL', callback_data='solmix')
        markup.add(btn1,btn2)
        bot.send_message(owner, msg, reply_markup=markup)
        
    elif call.data == 'cancel':
        bot.delete_message(owner, call.message.message_id)
        
    
    elif call.data == 'confirm':
        bot.delete_message(owner, call.message.message_id)
        print('yessssssssssss')
        wallet = db_bridge.get_txid(owner)
        amount = db_bridge.get_amount(owner)
        exc = exchange('eth','eth','eth','eth',amount,wallet)
        print(exc)
        payin = exc['payinAddress']
        msg = f"""Started Mixing Operation
        
Please send the amount of *{amount} eth * to
`{payin}` 
to start your transaction

Funds will automatically be transfered to
`{wallet}` 
After mixing has been completed

⚠ *Please Note that gas fees will be deducted from input amount, so take this into consideration*

*Transactions can take up to 30 minutes to get completed*

You can close this window anytime

        """
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Close ❌️', callback_data='cancel')
        markup.add(btn)
        bot.send_message(owner, msg, reply_markup=markup)
        
    elif call.data == 'ethmix':
        min = minimum('eth','eth','eth','eth')
        send = bot.send_message(owner, f"You're about to mix ETH\n\nMinimum Mix Amount is {min} ETH \n\nEnter Amount to Mix: ")
        bot.register_next_step_handler(send, ethmix)
        db_bridge.add_user(owner)
        
    elif call.data == 'solmix':
        min = minimum('sol','sol','sol','sol')
        send = bot.send_message(owner, f"You're about to mix SOL\n\nMinimum Mix Amount is {min} SOL \n\nEnter Amount to Mix: ")
        bot.register_next_step_handler(send, solmix)
        db_bridge.add_user(owner)
        
        
    elif call.data == 'confirm1':
        bot.delete_message(owner, call.message.message_id)
        print('yessssssssssss')
        wallet = db_bridge.get_txid(owner)
        amount = db_bridge.get_amount(owner)
        exc = exchange('sol','sol','sol','sol',amount,wallet)
        print(exc)
        payin = exc['payinAddress']
        msg = f"""Started Mixing Operation
        
Please send the amount of *{amount} sol * to
`{payin}` 
to start your transaction

Funds will automatically be transfered to
`{wallet}` 
After mixing has been completed

⚠ *Please Note that gas fees will be deducted from input amount, so take this into consideration*

*Transactions can take up to 30 minutes to get completed*

You can close this window anytime

        """
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Close ❌️', callback_data='cancel')
        markup.add(btn)
        bot.send_message(owner, msg, reply_markup=markup)
        
        
        
def ethmix(message):
    owner = message.chat.id
    try:
        initial = float(message.text)
        db_bridge.update_amount(initial, owner)
    except Exception as e:
        bot.send_message(message.chat.id, "Message should be a number ")
        
    min = minimum('eth','eth','eth','eth')
    if initial < min:
        s = bot.send_message(owner, "Mix amount lower than minimum amount\nPlease enter amount: ")
        bot.register_next_step_handler(s, ethmix)
    else:
        
        bot.send_message(owner, "Enter wallet to mix to: ")
        bot.register_next_step_handler(message, ether)
        
def ether(message):
    owner = message.chat.id
    amt = db_bridge.get_amount(owner)
    msg = f"Hit the confirm button to Mix *{amt}* eth to `{message.text}`"
    wallet = str(message.text)
    if wallet.startswith('0x'):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Cancel ❌', callback_data='cancel')
        bt = types.InlineKeyboardButton('Confirm ✅️', callback_data='confirm')
        markup.add(btn,bt)
        db_bridge.update_txid(wallet, owner)
        bot.send_message(owner, msg, reply_markup=markup)
    else:
        bot.send_message(owner, "Please Enter a valid ethereum recipient wallet")
        

def solmix(message):
    owner = message.chat.id
    try:
        initial = float(message.text)
        db_bridge.update_amount(initial, owner)
    except Exception as e:
        bot.send_message(message.chat.id, "Message should be a number ")
        
    min = minimum('sol','sol','sol','sol')
    if initial < min:
        s = bot.send_message(owner, "Mix amount lower than minimum amount\nPlease enter amount: ")
        bot.register_next_step_handler(s, solmix)
    else:
        
        bot.send_message(owner, "Enter wallet to mix to: ")
        bot.register_next_step_handler(message, soler)
        
def soler(message):
    owner = message.chat.id
    amt = db_bridge.get_amount(owner)
    msg = f"Hit the confirm button to Mix *{amt}* sol to `{message.text}`"
    wallet = str(message.text)
    if not wallet.startswith('0x'):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Cancel ❌', callback_data='cancel')
        bt = types.InlineKeyboardButton('Confirm ✅️', callback_data='confirm1')
        markup.add(btn,bt)
        db_bridge.update_txid(wallet, owner)
        bot.send_message(owner, msg, reply_markup=markup)
    else:
        bot.send_message(owner, "Please Enter a valid solana recipient wallet")
        
bot.infinity_polling()