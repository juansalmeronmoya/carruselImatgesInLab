import shutil

import requests
import time


class Bot(object):
    def __init__(self, token, path):
        self.token = token
        self.path = path
        self.last_update_time = time.time()
        self.telegram_url = 'https://api.telegram.org/'

    def updatePictures(self):
        response = requests.get(self.getUpdatesUrl()).json()
        pre_update_time = self.getLastUpdateTime()
        pictures = [res['message'] for res in response['result'] if isAPhoto(res) and isNew(res, pre_update_time)]
        for pic in pictures:
            self.downloadPicture(pic)
            if pic['date'] > self.last_update_time:
                self.last_update_time = pic['date']

    def getLastUpdateTime(self):
        return self.last_update_time

    def getUpdatesUrl(self):
        return self.telegram_url + 'bot' + self.token + '/getupdates'

    def downloadPicture(self, picture):
        print('Downloading new picture...')
        file_id = picture['photo'][-1]['file_id']
        response_file = requests.get(self.getInfoFileUrl(file_id)).json()
        response_image = requests.get(self.getImageUrl(response_file['result']['file_path']), stream=True)
        if response_image.status_code == 200:
            with open(self.path + '/' + file_id + '.jpg', 'wb') as f:
                response_image.raw.decode_content = True
                shutil.copyfileobj(response_image.raw, f)

    def getInfoFileUrl(self, file_id):
        return self.telegram_url + 'bot' + self.token + '/getfile?file_id=' + file_id

    def getImageUrl(self, image_path):
        return self.telegram_url + 'file/bot' + self.token + '/' + image_path


def isAPhoto(res):
    return 'photo' in res['message']


def isNew(res, previous_update_time):
    return res['message']['date'] > previous_update_time
