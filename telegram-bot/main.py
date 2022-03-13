#Стандартные Модули
from asyncio import sleep
from datetime import datetime as dt
from time import sleep
import token

# Сторонние модули
from telebot import TeleBot
from telebot.types import (CallbackQuery, InlineKeyboardMarkup,
                             InlineKeyboardButton, Message)

# Локальные Модули
import bot_token
import welcome_handler as w_handler

# Bot Initialization
bot = TeleBot(bot_token.token)

# Variables
bot.w_file = "animation"
bot.file_path = "static/happy-anime.mp4"

@bot.message_handler(commands=["start"])
def welcome(message: Message) -> None:

    if bot.w_file != "text": 
        with open(bot.file_path, "rb") as file:
            if bot.w_file == "photo":
                bot.send_photo(message.chat.id, file)
            elif bot.w_file == "sticker" or bot.w_file == "animated":
                bot.send_sticker(message.chat.id, file)
            elif bot.w_file == "animation":
                bot.send_animation(message.chat.id, file)

    msg_text = w_handler.prep_cmd_msg(message)
    
    bot.send_message(message.chat.id, msg_text)


@bot.message_handler(commands=["help"])
def help(message: Message) -> None:

    msg_text = w_handler.prep_cmd_msg(message)

    bot.send_message(message.chat.id, msg_text)



@bot.message_handler(commands=["config"])
def config(message: Message) -> None:

    config_keyboard = InlineKeyboardMarkup(row_width=2)

    photo_key = InlineKeyboardButton(text="Photo + Text",
                                     callback_data="photo")
    animation_key = InlineKeyboardButton(text="Animation + Text",
                                     callback_data="animation")
    sticker_key = InlineKeyboardButton(text="Sticker + Text",
                                     callback_data="sticker")
    text_key = InlineKeyboardButton(text="Only text",
                                     callback_data="text")

    config_keyboard.add(photo_key, animation_key, sticker_key, text_key)

    bot.send_message(message.chat.id, " {0.first_name} Select greeting type!".format(message.from_user),
                    reply_markup=config_keyboard)


def _sticker_type(message: Message) -> None:

    sticker_keyboard = InlineKeyboardMarkup(row_width=2)

    standard_key = InlineKeyboardButton(text = "Simple sticker",
                                        callback_data="standard")

    anim_key = InlineKeyboardButton(text = "animated sticker", 
                                    callback_data="animated")


    sticker_keyboard.add(standard_key, anim_key)

    bot.send_message(message.chat.id, "Choose sticker type!",
                        reply_markup=sticker_keyboard)

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call: CallbackQuery) -> None:

    bot.answer_callback_query(call.id)

    if call.data == "photo":
        bot.w_file = "photo"
        bot.file_path = "static/stick.webp"
        bot.send_message(call.message.chat.id, "Send me a photo in .JPG!")
        bot.register_next_step_handler(call.message, _change_file, call.data)
        
    if call.data == "animation":
        bot.w_file = "animation"
        bot.file_path = "static/happy-anime.mp4"
        bot.send_message(call.message.chat.id, "Send me a animation in .JPG!")
        bot.register_next_step_handler(call.message, _change_file, call.data)

    if call.data == "sticker":
        _sticker_type(call.message)


    if call.data == "text":
        bot.w_file = "text"
        bot.register_next_step_handler(call.message, 
                                    w_handler.g_change_text)


    if call.data == "standard":
        bot.w_file = "sticker"
        bot.file_path = "static/for.webp"
        bot.send_message(call.message.chat.id, "Send me a sticker in .WEBP!")
        bot.register_next_step_handler(call.message, _change_file, call.data)
        
    if call.data == "animated":
        bot.w_file = "animated"
        bot.file_path = "static/sticker.webp"
        bot.send_message(call.message.chat.id, "Send me a sticker in .TGS!")
        bot.register_next_step_handler(call.message, _change_file, call.data)



def _send_anim(call: CallbackQuery) -> None:
    with open("static/anim.webp", "rb") as sticker:
        bot.send_sticker(call.message.chat.id, sticker)

def _change_file(message: Message, call_data: str) -> None:

    w_handler.write_file(bot, message, call_data,
                         bot.file_path, bot_token.token)
    


    

bot.polling(none_stop=True, interval=0)