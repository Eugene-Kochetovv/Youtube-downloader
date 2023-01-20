from kivy.uix.gridlayout import GridLayout
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.app import MDApp
from tkinter import filedialog
from pytube import Playlist
from pytube import YouTube
import threading
from kivy.core.window import Window

Window.size = (480, 853)
# ПОДУМАТЬ НАД ПЕРЕДАЧЕЙ
def downloads(path, play_list, self):
    print(path)
    if path != None:
        self.progress_bar.max = len(play_list)
        print(self.progress_bar.max)
        for link in play_list:
            yt=YouTube(link)
            videos=yt.streams.first()
            videos.download()
            self.progress_bar.value += 1
            print(self.progress_bar.value)
    else:
        pass


class Container(GridLayout):
    def select_path(self):
        self.path = filedialog.askdirectory()

    def view_titles(self):
        self.cards.clear_widgets()
        self.play_list = Playlist(self.url.text)
        print(self.play_list)
        for video in self.play_list:
            card = MDRectangleFlatButton(text = str(YouTube(video).title),
                                         size_hint_y = None,
                                         size_hint_x = 1
                                         )
            self.cards.add_widget(card)

    def dow(self):
        threading.Thread(target=downloads, args=(self.path, self.play_list, self)).start()





class MyApp(MDApp):
    theme_cls = ThemeManager()
    title = 'YouTube PlayList'
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        return Container()

if __name__ == '__main__':
    MyApp().run()


# https://www.youtube.com/playlist?list=PLzIAGsAFM_hcOEukz8r-oSx6H-SDKJTDq
