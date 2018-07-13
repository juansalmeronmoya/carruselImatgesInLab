#!/usr/bin/env python3
"""Display a slideshow from a list of filenames"""

import os
import tkinter

from itertools import cycle, chain
from PIL import Image, ImageTk

path = "./img"


class Slideshow(tkinter.Tk):
    """Display a slideshow from a list of filenames"""
    def __init__(self, images, slide_interval):
        """Initialize
        
        images = a list of filename 
        slide_interval = milliseconds to display image
        """
        tkinter.Tk.__init__(self)
        self.geometry("+0+0")
        self.slide_interval = slide_interval
        self.images = None
        self.set_images(images)
        self.slide = tkinter.Label(self)
        self.slide.pack()
        self.next_image_index = 0

    def set_images(self, images):
         self.images = images
    
    def update_index(self):
        self.next_image_index += 1
        if self.next_image_index == len(self.images):
            self.next_image_index = 0

    def center(self):
        """Center the slide window on the screen"""
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        self.geometry("+%d+%d" % (x, y))

    def set_image(self):
        """Setup image to be displayed"""
        self.image_name = self.images[self.next_image_index]
        self.update_index()
        filename, ext = os.path.splitext(self.image_name)
        self.image = ImageTk.PhotoImage(Image.open(path + '/' + self.image_name))
        
    def main(self):
        """Display the images"""
        new_images = get_images_from_disk()
        self.set_images(new_images)
        self.set_image()
        self.slide.config(image=self.image)
        self.title(self.image_name)
        self.center()
        self.after(self.slide_interval, self.start)
    
    def start(self):
        """Start method"""
        self.main()
        self.mainloop()

def get_images_from_disk():
    import glob
    images = glob.glob("*.jpg")
    exts = ["jpg", "bmp", "png", "gif", "jpeg"]
    images = [fn for fn in os.listdir(path) if any(fn.endswith(ext) for ext in exts)]
    return images

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
    images = get_images_from_disk()

    # start the slideshow
    slideshow = Slideshow(images, slide_interval)
    slideshow.start()