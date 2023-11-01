from mutagen.mp3 import MP3
import pygame
import json
import requests
from PySide2.QtCore import QFile, QStringListModel, QTimer
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication


# https://www.yeyulingfeng.com/tools/music

class Music_Download:
    def __init__(self):
        super(Music_Download, self).__init__()

        qfile = QFile('UI.ui')
        qfile.open(QFile.ReadOnly)
        qfile.close()

        self.ui = QUiLoader().load(qfile)

        self.ui.Bsearch.clicked.connect(self.get_song_list)

        self.url = 'https://www.yeyulingfeng.com/tools/music/'
        self.headers = {
            'Referer': 'https://www.yeyulingfeng.com/tools/music/?name=%E9%98%B4%E5%A4%A9%E5%BF%AB%E4%B9%90&type'
                       '=netease',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.song_list = []
        self.search_name = ""
        self.source = "netease"
        self.song_name = ""
        self.song_id = ""
        self.song_artist = ""
        self.show_list = []

    def get_song_list(self):
        self.show_list = []
        self.get_edit_text()
        data = {
            'input': self.search_name,
            'filter': 'name',
            'type': self.source,
            'page': 1,
        }
        session = requests.Session()
        session.trust_env = False
        response = session.post(url=self.url, headers=self.headers, data=data, verify=False)
        result = response.text.replace(r'\/', '/').encode().decode('unicode_escape').replace("\n", "").replace(" ", "").replace("null", "None")
        data = json.loads(result)
        self.song_list = data.get('data', [])
        print(self.song_list)
        print(type(self.song_list))
        for song in self.song_list:
            self.song_name = song.get('title')
            self.song_id = song.get('songid')
            self.song_artist = ' '.join(song.get('author'))
            self.show_list.append(self.song_name + ' - ' + self.song_artist)
        self.add_show_list()


    def get_edit_text(self):
        self.search_name = self.ui.Edit_input.text()

    def add_show_list(self):
        list_model = QStringListModel()
        list_model.setStringList(self.show_list)
        self.ui.song_list.setModel(list_model)

    def download_song(self):

        self.get_song_url()
        response = requests.get(url=self.song_url, headers=self.headers)
        self.ui.label_state.setText('正在下载' + self.song_name + '-' + self.song_artist + '.mp3')
        with open(self.song_name + '-' + self.song_artist + '.mp3', 'wb') as w:
            w.write(response.content)
        self.ui.label_state.setText('下载完成')
        self.play_song()
        self.pause_state = 1
        self.ui.label_state.setText('正在播放： ' + self.song_name + '-' + self.song_artist + '.mp3')



if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    windows = Music_Download()
    windows.ui.show()
    app.exec_()
