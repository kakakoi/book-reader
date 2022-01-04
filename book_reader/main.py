from kivy.app import App

from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty, NumericProperty

import rarfile
import os
import shutil
import glob

def listup_files(path):
    yield [os.path.abspath(p) for p in glob.glob(path)]

class ImageWidget(Widget):
    source: StringProperty
    source_files: ListProperty
    source_index_max : NumericProperty
    source_index : NumericProperty = 0
    rf = rarfile.RarFile(".rar")
    shutil.rmtree('tmp')
    rf.extractall("./tmp")
    files = listup_files('tmp/**/*.jpg')
    for f in files:
        if type(f) is list:
            files = f
    if len(files) > 0:
        source_files = sorted(files)
        source = StringProperty(source_files[0])
        source_index_max = len(source_files) -1

    def __init__(self, **kwargs):
        super(ImageWidget, self).__init__(**kwargs)
        pass

    def buttonNext(self):
        if self.source_index < self.source_index_max:
            self.source_index += 1
        self.source = self.source_files[self.source_index]
        print(self.source)

    def buttonPrev(self):
        if self.source_index > 0:
            self.source_index -= 1
        self.source = self.source_files[self.source_index]
        print(self.source)

class ReaderApp(App):
    def __init__(self, **kwargs):
        super(ReaderApp, self).__init__(**kwargs)
        self.title = "book reader"


ReaderApp().run()
