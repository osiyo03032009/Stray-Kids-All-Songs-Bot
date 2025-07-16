import telebot
from telebot import types
import os

# 🔑 Telegram bot tokenini shu yerga yozing
TOKEN = '7972527080:AAGcxhA4X3iMfuKMvOrB5oEKEdCSN-FhkvA'
bot = telebot.TeleBot(TOKEN)

# 🔊 Qo'shiqlar joylashgan papka
MUSIC_FOLDER = 'songs'

# Qo'shiqlar ro'yxatini olamiz
def get_song_list():
    return [f for f in os.listdir(MUSIC_FOLDER) if f.endswith('.mp3')]

# /start yoki / bosilganda ishlaydi
@bot.message_handler(commands=['start', 'song', 'songs', 'qo\'shiq'])
def send_song_list(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    songs = get_song_list()
    for song in songs:
        markup.add(types.KeyboardButton(song))
    bot.send_message(message.chat.id, "Quyidagi qo'shiqlardan birini tanlang:", reply_markup=markup)

# Qo'shiq nomi yozilganda yoki tugma bosilganda shu qo‘shiq yuboriladi
@bot.message_handler(func=lambda message: True)
def send_audio(message):
    song_name = message.text
    file_path = os.path.join(MUSIC_FOLDER, song_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption=f"Eshitish uchun: {song_name}")
    else:
        bot.send_message(message.chat.id, "Bu nomdagi qo'shiq topilmadi. Iltimos, mavjud tugmadan foydalaning.")

# Botni ishga tushiramiz
bot.polling()
