from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.theming import ThemeManager
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.segmentedcontrol import MDSegmentedControl
from kivymd.uix.segmentedcontrol import MDSegmentedControlItem

from pytube import Playlist
from pytube import YouTube

from tkinter import filedialog

import threading
import os
from http.client import IncompleteRead

Window.size = (432, 768)


class Container(GridLayout):

    def select_path(self):
        '''
        Opens File Explorer and writes the path to
        the selected folder variable.
        '''
        # Save path
        self.path = filedialog.askdirectory()
        # Unlocking button "View titles"
        self.vt.disabled = False


    def view_titles(self):
        '''
        Finding video links in a playlist and
        displaying them on the screen.
        '''
        # Clear past titles
        self.cards.clear_widgets()
        # Clear list
        self.play_list = []
        # Save titles in list
        self.play_list = Playlist(self.url.text)
        print(self.play_list)
        for video in self.play_list:
            try:
                name = MDRectangleFlatButton(text = str(YouTube(video).title),
                                            size_hint_y = None,
                                            size_hint_x = 1
                                            )
                # Add title in screen
                self.cards.add_widget(name)
            except IncompleteRead:
                # Clear list
                self.play_list = []
                # Clear past titles
                self.cards.clear_widgets()
                # Try to start again
                self.view_titles()

        # Unlocking button "download"
        self.dw.disabled = False

    def download_button(self):
        '''
        New thread
        '''
        threading.Thread(target=self.downloads).start()

    def downloads(self):
        '''
        Dowload video
        '''
        # Setting the maximum length progress bar
        self.progress_bar.max = len(self.play_list)
        for link in self.play_list:
            yt=YouTube(link)
            # Select download format
            if self.format == 'mp3':
                # Download video
                yt.streams.filter(only_audio=True).first().download(output_path = self.path)
                # save the file
                base = os.path.splitext(yt.title)
                new_file = base + '.mp3'
                # Rename file
                os.rename(yt.title + '.mp4', new_file)
                self.progress_bar.value += 1
            else:
                # Download video
                yt.streams.get_by_itag(22).download(output_path = self.path)
                self.progress_bar.value += 1



    def on_active(
        # Register segmented control
    self,
        segmented_control: MDSegmentedControl,
        segmented_item: MDSegmentedControlItem,
    ) -> None:
            # Record format in variable
            self.format = segmented_item.text


class MyApp(MDApp):
    theme_cls = ThemeManager()
    title = 'YouTube PlayList'
    def build(self):
        # Settings theme
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        Container.format = "mp4"
        return Container()

if __name__ == '__main__':
    MyApp().run()
