import random
from os import listdir

from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout as Box
from kivy.uix.button import Button
from kivy.app import App


class Viewer(App):
    def __init__(self):
        super().__init__()

        self.img = Image()
        self.nb = Button(size_hint=(None, None), size=(250, 100), text='Следующая')

    def build(self):
        box = Box(orientation='vertical')

        self.nb.bind(on_release=self.random_source)
        self.img.source = 'images/img_1.png'
        box.add_widget(self.img)
        self.img.add_widget(self.nb)

        return box

    def on_stop(self):
        quit()

    def random_source(self, val=None):
        try:
            self.img.source = 'images/' + random.choice(listdir('images'))
            print(self.img.source, '-')
        except:
            print('aa')


if __name__ == '__main__':
    viewer = Viewer()
    viewer.run()
