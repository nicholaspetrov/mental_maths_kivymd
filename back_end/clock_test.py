from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu


class Test(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('clock_test.kv')

        difficulties = ['Easy', 'Medium', 'Hard', 'Mixed']
        difficulty_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback(x),
            } for i in difficulties
        ]
        self.difficulty_menu = MDDropdownMenu(
            caller=self.screen.ids.difficulty_button,
            items=difficulty_items,
            position="bottom",
            width_mult=2.5,
            max_height=200
        )

        types = ['+', '-', '/', '*']
        type_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback(x),
            } for i in types
        ]
        self.type_menu = MDDropdownMenu(
            caller=self.screen.ids.type_button,
            items=type_items,
            position="bottom",
            width_mult=2.5,
            max_height=200
        )

        durations = ['1:00', '2:00', '5:00', '10:00']
        duration_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback(x),
            } for i in durations
        ]
        self.duration_menu = MDDropdownMenu(
            caller=self.screen.ids.duration_button,
            items=duration_items,
            position="bottom",
            width_mult=2.5,
            max_height=200
        )

    test = []

    def menu_callback(self, text_item):
        self.test.append(text_item)
        output = ', '.join(self.test)
        print(output)
        # self.ids.test_label.text = output For realtime output on screen (above start test button)

        self.duration_menu.dismiss()
        self.type_menu.dismiss()
        self.difficulty_menu.dismiss()

    def build(self):
        return self.screen


Test().run()
