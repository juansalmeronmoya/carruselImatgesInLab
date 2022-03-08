#!/usr/bin/env python3

import os
import tkinter
from PIL import Image, ImageTk, ImageDraw, ImageFont
from Bot import Bot

path = "./img"
bot_image_path = 'img/'
# El nombre del bot es @inlab-2018, creado por JuanjoVG
bot_token = '737784048:AAEa_H2A8uhRZtkmCIhXydExBHV5RkwUpJs'


class Slideshow(tkinter.Tk):
    """Display a slideshow from a list of filenames"""

    def __init__(self, slide_interval, bot):
        """Initialize
        
        images = a list of filename 
        slide_interval = milliseconds to display image
        """
        tkinter.Tk.__init__(self)
        self.geometry("+0+0")
        # self.state('zoomed')
        self.slide_interval = slide_interval
        self.images = []
        self.get_images_from_disk()
        self.set_images(self.images)
        self.slide = tkinter.Label(self)
        self.slide.pack()
        self.next_image_index = len(self.images) - 1
        self.bot = bot

    def set_images(self, images):
        self.images = images

    def update_index(self):
        self.next_image_index -= 1
        if self.next_image_index < 0:
            self.next_image_index = len(self.images) - 1

    def center(self):
        """Center the slide window on the screen"""
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        self.geometry("+%d+%d" % (x, y))

    def resize_image(self, image):
        size = image.size
        w_dif = self.winfo_width() - size[0]
        h_dif = self.winfo_height() - size[1]
        w_ratio = 1
        h_ratio = 1
        if w_dif < 0:
            w_ratio = size[0] / self.winfo_width()
        if h_dif < 0:
            h_ratio = size[1] / self.winfo_height()
        ratio = max(w_ratio, h_ratio)
        final_w = int(size[0] / ratio)
        final_h = int(size[1] / ratio)
        image = image.resize((final_w, final_h), Image.ANTIALIAS)
        return image

    def set_image(self):
        """Setup image to be displayed"""
        self.image_name = self.images[self.next_image_index]
        self.update_index()
        # filename, ext = os.path.splitext(self.image_name)
        image = Image.open(path + '/' + self.image_name)
        image = self.resize_image(image)

        # draw = ImageDraw.Draw(image)
        # font = ImageFont.truetype("ariblk.ttf", 32)
        # draw.text((0, 0), "Sopar estiu 2019", (242, 144, 0), font=font)

        self.image = ImageTk.PhotoImage(image)

    def show_new_images(self):
        """Display the images"""
        bot.updatePictures()
        self.get_images_from_disk()
        self.set_images(self.images)
        self.set_image()
        self.slide.config(image=self.image)
        self.title(self.image_name)
        # self.center()
        self.after(self.slide_interval, self.show_new_images)

    def start(self):
        """Start method"""
        self.after(self.slide_interval, self.show_new_images)
        self.mainloop()

    def get_images_from_disk(self):
        exts = ["jpg", "bmp", "png", "gif", "jpeg"]
        images = [fn for fn in os.listdir(path) if any(fn.endswith(ext) for ext in exts)]
        images.sort()
        if len(images) > len(self.images):
            self.images = images
            self.next_image_index = len(self.images) - 1


if __name__ == "__main__":
    slide_interval = 2500

    bot = Bot(bot_token, bot_image_path)
    bot.updatePictures()

    # start the slideshow
    slideshow = Slideshow(slide_interval, bot)
    slideshow.start()
