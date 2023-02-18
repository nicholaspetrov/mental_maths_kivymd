# from kivy.lang import Builder
# from kivy.metrics import dp
# from kivymd.app import MDApp
# from kivymd.uix.menu import MDDropdownMenu
#
#
# class Test(MDApp):
#
#     test_settings = {}
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.screen = Builder.load_file('clock_test.kv')
#
#         difficulties = ['Easy', 'Medium', 'Hard', 'Mixed']
#         difficulty_menu_items = [
#             {
#                 "viewclass": "OneLineListItem",
#                 "text": difficulty,
#                 "height": dp(56),
#                 "on_release": lambda x=f'Difficulty: {difficulty}': self.menu_callback('Difficulty', x.split(' ')[1]),
#             } for difficulty in difficulties
#         ]
#         self.difficulty_menu = MDDropdownMenu(
#             caller=self.screen.ids.difficulty_button,
#             items=difficulty_menu_items,
#             position="center",
#             width_mult=4,
#         )
#
#         operators = ['+', '-', '/', '*']
#         operator_menu_items = [
#             {
#                 "viewclass": "OneLineListItem",
#                 "text": operator,
#                 "height": dp(56),
#                 "on_release": lambda x=f'Operator: {operator}': self.menu_callback('Operator', x.split(' ')[1]),
#             } for operator in operators
#         ]
#         self.operator_menu = MDDropdownMenu(
#             caller=self.screen.ids.operator_button,
#             items=operator_menu_items,
#             position="center",
#             width_mult=4,
#         )
#
#         durations = ['1 min', '2 min', '5 min', '10 min']
#         duration_menu_items = [
#             {
#                 "viewclass": "OneLineListItem",
#                 "text": duration,
#                 "height": dp(56),
#                 "on_release": lambda x=f'Duration: {duration}': self.menu_callback('Duration', x),
#             } for duration in durations
#         ]
#         self.duration_menu = MDDropdownMenu(
#             caller=self.screen.ids.duration_button,
#             items=duration_menu_items,
#             position="center",
#             width_mult=4,
#         )
#         self.difficulty_menu.bind()
#         self.operator_menu.bind()
#         self.duration_menu.bind()
#
#     def menu_callback(self, param_name, param_value):
#         if param_name == 'Duration':
#             self.test_settings[param_name] = int(param_value.split(' ')[1])*60
#             self.screen.ids.duration_button.set_item(param_value)
#             self.duration_menu.dismiss()
#         else:
#             self.test_settings[param_name] = param_value
#             if param_name == 'Difficulty':
#                 self.screen.ids.difficulty_button.set_item(f'Difficulty: {param_value}')
#                 self.difficulty_menu.dismiss()
#             if param_name == 'Operator':
#                 self.screen.ids.operator_button.set_item(f'Operator: {param_value}')
#                 self.operator_menu.dismiss()
#
#         print(self.test_settings)
#
#     def build(self):
#         return self.screen
#
#     def exit_app(self):
#         print('hi')
#
# Test().run()
