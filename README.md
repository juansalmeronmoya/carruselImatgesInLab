# Carrusel Imatges InLab FIB

### How it works
Basically is an image slideshow that downloads images from a telegram group and show them realtime.
The slideshow order is from newest to oldest. 
If a new image is sent to the group, then the slideshow restarts immediately from the newest.
Images are downloaded once and only are downloaded those added to the group while the slideshow is running (this can be changed) 

### Install
```
pipenv install
```

### Configure
You should follow these steps.
* Create a Telegram Group (use telegram web for example https://web.telegram.org/)
* Invite the bot to the group. Bot name: @inlab-2018 (if you generate a new one you have to update the bot token and permissions)


### Run
```
python slideshow.py
```
