import os
import shutil

import requests


class Bot(object):
    def __init__(self, token, path):
        self.token = token
        self.path = path
        self.last_download_picture_time = self.getLastDownloadedPictureTimeFromFiles()
        self.telegram_url = 'https://api.telegram.org/'

    def updatePictures(self):
        response = requests.get(self.getUpdatesUrl()).json()
        pictures = [res['message'] for res in response['result'] if self.isAPhoto(res) and self.isNew(res)]
        print(pictures)
        for pic in pictures:
            self.downloadPicture(pic)
            if pic['date'] > self.last_download_picture_time:
                self.last_download_picture_time = pic['date']

    def getLastUpdateTime(self):
        return self.last_download_picture_time

    def getUpdatesUrl(self):
        return self.telegram_url + 'bot' + self.token + '/getupdates'

    def downloadPicture(self, picture):
        print('Downloading new picture...')
        file_id = picture['photo'][-1]['file_id']
        response_file = requests.get(self.getInfoFileUrl(file_id)).json()
        response_image = requests.get(self.getImageUrl(response_file['result']['file_path']), stream=True)
        if response_image.status_code == 200:
            with open(self.path + '/' + str(picture['date']) + '.jpg', 'wb') as f:
                response_image.raw.decode_content = True
                shutil.copyfileobj(response_image.raw, f)

    def getInfoFileUrl(self, file_id):
        return self.telegram_url + 'bot' + self.token + '/getfile?file_id=' + file_id

    def getImageUrl(self, image_path):
        return self.telegram_url + 'file/bot' + self.token + '/' + image_path

    def isAPhoto(self, res):
        return 'photo' in res['message']

    def isNew(self, res):
        return res['message']['date'] > self.last_download_picture_time

    def getLastDownloadedPictureTimeFromFiles(self):
        exts = ["jpg", "bmp", "png", "gif", "jpeg"]
        images = [fn for fn in os.listdir(self.path) if any(fn.endswith(ext) for ext in exts)]
        images.sort()
        return int(os.path.splitext(images.pop())[0])
