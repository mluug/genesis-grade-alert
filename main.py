import telebot
import schedule
import time
import threading

import user_defined
import crawl

bot = telebot.TeleBot(user_defined.api_token())

previous_grades = ""


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'Type /grades to retrieve current grades')


@bot.message_handler(commands=['grades'])
def send_grades(message):
    if str(message.from_user.id) == str(user_defined.chat_id()):
        bot.reply_to(message, "\n".join(crawl.grades_extracted_reformat(crawl.crawl_grades())))


# undefined keyword response
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, 'Undefined command')


def check_grades_update():
    current_grades = crawl.crawl_grades()
    global previous_grades
    if previous_grades != current_grades:
        send_message("\n".join(crawl.grades_extracted_reformat(current_grades)), user_defined.chat_id())
        previous_grades = current_grades


def send_message(message_text, chat_id):
    bot.send_message(chat_id, message_text)


def bot_polling():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Error in polling: {e}")
            time.sleep(15)


# recursive method for timed checking
def check_grades_periodically():
    check_grades_update()
    threading.Timer(30, check_grades_periodically).start()


# start timed checking
check_grades_periodically()

# handles manual requests using threading - start the bot in separate thread
bot_thread = threading.Thread(target=bot_polling)
bot_thread.start()

while True:
    schedule.run_pending()
    time.sleep(1)
