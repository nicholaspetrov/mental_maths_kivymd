from kivy.lang import Builder
from kivymd.app import MDApp


class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('clock_test.kv')

    def build(self):
        return self.screen


Test().run()
