#!/usr/bin/env python3
"""Display a slideshow from a list of filenames"""

import os
import tkinter

from itertools import cycle, chain
from PIL import Image, ImageTk
from Bot import Bot

path = "./img"
bot_image_path = 'img/'
bot_token = '471926478:AAECF2kaSTezJH7_fhIYAzGKKw3cNXQLZ7g'


class Slideshow(tkinter.Tk):
    """Display a slideshow from a list of filenames"""
    def __init__(self, slide_interval, bot):
        """Initialize
        
        images = a list of filename 
        slide_interval = milliseconds to display image
        """
        tkinter.Tk.__init__(self)
        self.geometry("+0+0")
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
        w_dif = self.winfo_screenwidth() - size[0] 
        h_dif = self.winfo_screenheight() - size[1]
        w_ratio = 1
        h_ratio = 1
        if w_dif < 0:
            w_ratio = size[0]/self.winfo_screenwidth()
        if h_dif < 0:
            h_ratio = size[1]/self.winfo_screenheight()
        ratio = max(w_ratio, h_ratio)
        image = image.resize((int(size[0]/ratio), int(size[1]/ratio)), Image.ANTIALIAS)
        return image

    def set_image(self):
        """Setup image to be displayed"""
        self.image_name = self.images[self.next_image_index]
        self.update_index()
        filename, ext = os.path.splitext(self.image_name)
        image = Image.open(path + '/' + self.image_name)
        image = self.resize_image(image)
        self.image = ImageTk.PhotoImage(image)
        
    def main(self):
        """Display the images"""
        self.get_images_from_disk()
        self.set_images(self.images)
        self.set_image()
        self.slide.config(image=self.image)
        self.title(self.image_name)
        #self.center()
        self.after(self.slide_interval, self.start)
    
    def start(self):
        """Start method"""
        self.main()
        bot.updatePictures()
        self.mainloop()

    def get_images_from_disk(self):
        import glob
        images = glob.glob("*.jpg")
        exts = ["jpg", "bmp", "png", "gif", "jpeg"]
        images = [fn for fn in os.listdir(path) if any(fn.endswith(ext) for ext in exts)]
        images.sort()
        if len(images) > len(self.images):
            self.images = images
            self.next_image_index = len(self.images) - 1

if __name__ == "__main__":
    slide_interval = 2500
    
    # use a list
    #images = ["image1.jpg",
              #"image2.jpeg",
              #"/home/pi/image3.gif",
              #"/home/pi/images/image4.png",
              #"images/image5.bmp"]
    
    # all the specified file types in a directory 
    # "." us the directory the script is in.
    # exts is the file extentions to use.  it can be any extention that pillow supports
    # http://pillow.readthedocs.io/en/3.3.x/handbook/image-file-formats.html
    bot = Bot(bot_token, bot_image_path)
    bot.updatePictures()

    # start the slideshow
    slideshow = Slideshow(slide_interval, bot)
    slideshow.start()