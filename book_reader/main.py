from kivy.app import App

from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty, NumericProperty

from kivy.core.window import Window

import rarfile
import os
import shutil
import glob

def listup_files(path):
    yield [os.path.abspath(p) for p in glob.glob(path)]


class ImageWidget(Widget):
    source_main: StringProperty
    source_sub: StringProperty
    source_files: ListProperty
    source_index_max : NumericProperty
    view_num : NumericProperty = 2
    source_index : NumericProperty = 0
    file_path = ""
    rf = rarfile.RarFile(file_path)
    shutil.rmtree('tmp')
    rf.extractall("./tmp")
    files = listup_files('tmp/**/*.jpg')
    for f in files:
        if type(f) is list:
            files = f
    if len(files) > 0:
        source_files = sorted(files)
        source_main = StringProperty(source_files[0])
        source_sub = StringProperty(source_files[1])
        source_index_max = len(source_files) -1

    def __init__(self, **kwargs):
        super(ImageWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.next()
        elif keycode[1] == 'right':
            self.prev()
        return True

    def next(self):
        if self.source_index < self.source_index_max:
            self.source_index += self.view_num
        self.source_main = self.source_files[self.source_index]
        if self.source_index+1 < self.source_index_max:
            self.source_sub = self.source_files[self.source_index+1]
        print(self.source_main)

    def prev(self):
        if self.source_index > 0:
            self.source_index -= self.view_num
        self.source_main = self.source_files[self.source_index]
        self.source_sub = self.source_files[self.source_index+1]
        print(self.source_main)

class ReaderApp(App):
    def __init__(self, **kwargs):
        super(ReaderApp, self).__init__(**kwargs)
        self.title = "book reader"


ReaderApp().run()
