#!/usr/bin/env python3

from Bot import Bot

path = "./img"
bot_image_path = 'img/'
# El nombre del bot es @inlab-2018, creado por JuanjoVG
bot_token = '737784048:AAEa_H2A8uhRZtkmCIhXydExBHV5RkwUpJs'

if __name__ == "__main__":
    slide_interval = 2500

    bot = Bot(bot_token, bot_image_path)
    bot.download_all_pictures()

