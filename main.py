import telebot
import vk_api
from vk_api.audio import VkAudio

bot = telebot.TeleBot('1939600760:AAFycjvXtbbFVyOonr3m3LSdgEI2Hg9jkXs')
log = ''
pas = ''
captch = ''


def captcha_handler(captcha):
    global captch
    answ = ''
    bot.reply_to(captch, f'Введите капчу: {captcha.get_url()}')

    @bot.message_handler(content_types=['text'])
    def answ(message):
        answ = message.text
        print(answ)
    return answ


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Пропиши команду /music')


@bot.message_handler(commands=['music'])
def music_message(message):
    bot.send_message(message.chat.id, 'Введи логин и пароль от аккаунта во Вконтакте через пробел')


@bot.message_handler(content_types=['text'])
def data(message):
    try:
        global log, pas, captch
        print(message)
        log = message.text.split(' ')[0]
        pas = message.text.split(' ')[1]
        print(log, pas)
        bot.send_message(message.chat.id, 'Ожидайте, время загрузки зависит от количества аудиозаписей на вашем аккаунте')
        captch = message
        vk_session = vk_api.VkApi(
            log, pas,
            captcha_handler=captcha_handler)
        vk_session.auth()
        tracks = []
        count = 0
        for track in VkAudio(vk_session).get_iter():
            count += 1
            tracks.append(f'{track.get("title")} - {track.get("artist")}')
        bot.send_message(message.chat.id, 'Список ваших аудиозаписей:')
        bot.send_message(message.chat.id, '\n\n'.join(tracks))
    except Exception:
        bot.send_message(message.chat.id, 'Неверный логин или пароль')


bot.polling()
