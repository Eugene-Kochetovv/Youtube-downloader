from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from tkinter import filedialog
from pytube import Playlist
from pytube import YouTube


path = ''
videos = []
class Container(FloatLayout):

    def text_change(self):
        self.button_dow.text = 'Проверить'

    def select_path(self):
        global path
        path = filedialog.askdirectory()

    def select_playlist(self):
        if self.button_dow.text == 'Проверить':
            try:
                global videos
                play_list = Playlist(self.input.text)
                for video in play_list:
                    videos.append(video)
                self.button_dow.text = 'Скачать'
                for video_info in videos:
                    video_info = YouTube(video_info)
                    self.list_videos.add_widget(Label(text = video_info.title))

            except KeyError:
                pass # ДОБАВИТЬ ОКНО ОШИБКИ




        else:
            print('xun')
class MyApp(App):
    def build(self):
        return Container()

if __name__ == '__main__':
    MyApp().run()

# https://www.youtube.com/playlist?list=PLzIAGsAFM_hcOEukz8r-oSx6H-SDKJTDq
