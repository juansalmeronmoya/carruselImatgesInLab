import os
import time
import wand.display
from PIL import Image
from Bot import Bot

update_freq = 10  # Seconds
change_picture_freq = 3  # Seconds
image_path = 'img/'
bot_token = '471926478:AAECF2kaSTezJH7_fhIYAzGKKw3cNXQLZ7g'

bot = Bot(bot_token, image_path)
bot.updatePictures()

images = os.listdir(image_path)
images.sort()
i = len(images)-1

#for image_counter in images:
image = Image('img/1531476664.jpg')
display(image=image)

#    https://raspberrypi.stackexchange.com/questions/18261/how-do-i-display-an-image-file-png-in-a-simple-window
