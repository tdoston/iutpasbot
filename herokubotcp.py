import telebot
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import scipy.stats as st
import math
import os
from scipy.stats import norm
from PIL import Image

print("Hello World!")
bot = telebot.TeleBot("589245993:AAHZkAhgT-TdUqqGwnMZ-A1WkAOBEL7s9M4")

# main_menu
user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
user_markup.row('🎲 Evaluate the probability 📈')

user_hide = telebot.types.ReplyKeyboardMarkup(None, True)

user_dict = {}


class User:
    def __init__(self, chatID):
        self.chatID = chatID
        self.myu = None
        self.sigma = None
        self.a = None
        self.b = None
        self.flag = None


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.from_user.id, 'Welcome!', reply_markup=user_markup)


@bot.message_handler(commands=["stop"])
def handle_stop(message):
    user_hide = telebot.types.ReplyKeyboardMarkup(True, True)
    bot.send_message(message.from_user.id, ' Bye ', reply_markup=user_hide)


@bot.message_handler(content_types=["text"])
def main_menu(message):
    if message.text == '🎲 Evaluate the probability 📈':
        bot.send_message(message.chat.id, 'Evaluation of the normal distribution probability', reply_markup=user_hide)
        process_init_step(message)
    else:
        bot.send_message(message.chat.id, "Sorry! Retry again | Press /start \n%s doesn't available" % message.text)


def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def process_init_step(message):
    try:
        bot.send_message(message.from_user.id, 'Please enter values of following one by one.'
                                               '\nμ - Mean,'
                                               '\nσ - standard deviation,'
                                               '\na,b - range of function:', reply_markup=user_hide)
        msg = bot.reply_to(message, ' Enter (mean) μ')
        bot.register_next_step_handler(msg, process_myu_step)
    except Exception as e:
        bot.reply_to(message, 'Oops!')


def process_myu_step(message):
    try:
        chat_id = message.chat.id
        myu = message.text
        if not isDigit(myu):
            msg = bot.reply_to(message, 'μ should be a number. Enter a number (value of μ):')
            bot.register_next_step_handler(msg, process_myu_step)
            return
        user = User(chat_id)
        user_dict[chat_id] = user
        current_user = user_dict[chat_id]
        current_user.myu = myu
        current_user.flag = 1
        msg = bot.reply_to(message, 'Enter (standard deviation) σ')
        bot.register_next_step_handler(msg, process_sigma_step)
    except Exception as e:
        bot.reply_to(message, 'Oops!')


def process_sigma_step(message):
    try:
        chat_id = message.chat.id
        sigma = message.text
        if not isDigit(sigma):
            msg = bot.reply_to(message, 'σ should be a number. Enter a number (value of σ):')
            bot.register_next_step_handler(msg, process_sigma_step)
            return
        current_user = user_dict[chat_id]
        current_user.sigma = sigma
        msg = bot.reply_to(message, 'Enter (range a) a:')
        bot.register_next_step_handler(msg, process_a_step)
    except Exception as e:
        bot.reply_to(message, 'Oops!')


def process_a_step(message):
    try:
        chat_id = message.chat.id
        a = message.text
        if not isDigit(a):
            msg = bot.reply_to(message, ' \'a\' should be a number. Enter a number (value of \'a\'):')
            bot.register_next_step_handler(msg, process_a_step)
            return
        current_user = user_dict[chat_id]
        current_user.a = a
        msg = bot.reply_to(message, 'Enter (range b) b:')
        bot.register_next_step_handler(msg, process_b_step)
    except Exception as e:
        bot.reply_to(message, 'Oops!')


def process_b_step(message):
    try:
        chat_id = message.chat.id
        b = message.text
        if not isDigit(b):
            msg = bot.reply_to(message, ' \'b\' should be a number. Enter a number (value of \'b\'):')
            bot.register_next_step_handler(msg, process_b_step)
            return
        current_user = user_dict[chat_id]
        current_user.b = b
        bot.reply_to(message, 'You have entered followings:')
        bot.send_message(chat_id, '\n 📐 Inputs\n✔ Myu:\t' + str(current_user.myu) + '\n✔ Sigma:\t' + str(
            current_user.sigma) + '\n✔ a:\t' + str(
            current_user.a) + '\n✔ b:\t' + str(current_user.b), reply_markup=user_markup)
        bot.send_message(39920921, 'Someone ! Chat id:\t' + str(message.from_user.id))

        mu = float(current_user.myu)
        variance = float(current_user.sigma)
        a = float(current_user.a)
        b = float(current_user.b)
        z1 = (a - mu) / variance
        z2 = (b - mu) / variance
        z1area = st.norm.cdf(z1)
        z2area = st.norm.cdf(z2)
        area = z2area - z1area
        sigma = math.sqrt(variance)
        # x = np.linspace(a, b, 100)

        def draw_z_score(x, cond, mu, sigma, title):
            y = norm.pdf(x, mu, sigma)
            z = x[cond]
            plt.plot(x, y)
            plt.fill_between(z, 0, norm.pdf(z, mu, sigma))
            plt.title(title)
            plt.grid()
        x = np.arange(a-0.1*a-3, b+0.1*b+3, 0.001)
        draw_z_score(x, (a < x) & (x < b), mu, sigma, str(z1)[0:6] + '< z <' + str(z2)[0:6]
                         + '\nShaded area: ' + str(area)[0:6])
        plt.savefig("%s.png" % current_user.chatID, format="PNG")
        plt.close()
        # plt.plot(x, mlab.normpdf(x, mu, sigma))  # Probability density function
        image = Image.open("%s.png" % current_user.chatID)
        logo = Image.open('iutpasb2.png')
        new_logo = logo.resize((100, 120))
        image_copy = image.copy()
        position = ((image_copy.width - new_logo.width - 5), (image_copy.height - new_logo.height - 5))
        image_copy.paste(new_logo, position, new_logo)
        image_copy.save("%s.png" % current_user.chatID)
        bot.send_message(current_user.chatID, 'P(a <= X <= b) = ' + str(area)[0:8])
        bot.send_chat_action(current_user.chatID, 'upload_photo')
        bot.send_photo(current_user.chatID, open("%s.png" % current_user.chatID, 'rb'))
        os.remove("%s.png" % current_user.chatID)

    except Exception as e:
        bot.reply_to(message, 'Oops!')


if __name__ == '__main__':
    bot.polling(none_stop=True)

bot.polling()
