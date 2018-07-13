import os
import time

import matplotlib.animation as animation
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from Bot import Bot

update_freq = 10  # Seconds
change_picture_freq = 3  # Seconds
image_path = 'img/'
bot_token = '471926478:AAECF2kaSTezJH7_fhIYAzGKKw3cNXQLZ7g'

bot = Bot(bot_token, image_path)
bot.updatePictures()

fig, ax = plt.subplots(figsize=(16, 9))
images = os.listdir(image_path)
images.sort()
i = len(images)-1

def updatefig(*args):
    global images, i, bot, fig
    img = mpimg.imread(image_path + images[-1])
    im = plt.imshow(img, animated=True, aspect='auto')

    if bot.getLastUpdateTime() + update_freq < time.time():
        n_images = len(images)
        bot.updatePictures()
        images = os.listdir(image_path)
        images.sort()
        if len(images) > n_images:
            i = len(images)-1

    if i < 0:
        i = len(images)-1
    im.set_array(mpimg.imread(image_path + images[i]))
    i -= 1
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=change_picture_freq * 1000, blit=True, )

## Graffic configuration

plt.axis('off')
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()

plt.show()
