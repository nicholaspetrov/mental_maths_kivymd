from kivy.lang import Builder
from kivymd.app import MDApp
import time


class Test(MDApp):
    def build(self):
        return Builder.load_file('clock_test.kv')

    def press_it(self):
        current = self.root.ids.my_progress_bar.value
        current += 25
        if current > 100:
            current = 0

        self.root.ids.my_progress_bar.value = current

        self.root.ids.my_label.text = f'{current} %'
        # counter = 1
        # while counter != 11:
        #     time.sleep(1)
        #     print(counter)
        #     counter += 1
        # print('10 seconds has elapsed')


Test().run()
