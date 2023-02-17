from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu


class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('clock_test.kv')

        difficulties = ['Easy', 'Medium', 'Hard', 'Mixed']
        difficulty_menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": difficulty,
                "height": dp(56),
                "on_release": lambda x=f'Difficulty: {difficulty}': self.set_difficulty(x),
            } for difficulty in difficulties
        ]
        self.difficulty_menu = MDDropdownMenu(
            caller=self.screen.ids.difficulty_button,
            items=difficulty_menu_items,
            position="center",
            width_mult=4,
        )

        operators = ['+', '-', '/', '*']
        operator_menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": operator,
                "height": dp(56),
                "on_release": lambda x=f'Operator: {operator}': self.set_operator(x),
            } for operator in operators
        ]
        self.operator_menu = MDDropdownMenu(
            caller=self.screen.ids.operator_button,
            items=operator_menu_items,
            position="center",
            width_mult=4,
        )

        durations = ['1 min', '2 min', '5 min', '10 min']
        duration_menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": duration,
                "height": dp(56),
                "on_release": lambda x=f'Duration: {duration}': self.set_duration(x),
            } for duration in durations
        ]
        self.duration_menu = MDDropdownMenu(
            caller=self.screen.ids.duration_button,
            items=duration_menu_items,
            position="center",
            width_mult=4,
        )
        self.difficulty_menu.bind()
        self.operator_menu.bind()
        self.duration_menu.bind()

    def set_difficulty(self, text_item):
        self.screen.ids.difficulty_button.set_item(text_item)
        self.difficulty_menu.dismiss()

    def set_operator(self, text_item):
        self.screen.ids.operator_button.set_item(text_item)
        self.operator_menu.dismiss()

    def set_duration(self, text_item):
        self.screen.ids.duration_button.set_item(text_item)
        self.duration_menu.dismiss()

    def build(self):
        return self.screen


Test().run()
