from kivy.lang import Builder
from kivymd.app import MDApp


class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('clock_test.kv')

    def build(self):
        return self.screen


Test().run()
# import kivy
#
# from kivy.uix.gridlayout import GridLayout
# from kivy.app import App
# from kivy.lang import Builder
#
# Builder.load_string('''
# # a template Butt of type Button
# [Butt@Button]
#     # ctx.'attribute_name' is used to access the
#     # attributes defined in the instance of Butt.
#     text: ctx.text
#     # below vars are constant for every instance of Butt
#     size_hint_x: None
#     width: 100
#
# <CalcApp>:
#     cols: 3
#     row_force_default: True
#     row_default_height: 50
#     pos_hint: {'center_x':.5}
#     size_hint: (None, None)
#     # size is updated whenever minimum_size is.
#     size: self.minimum_size
#     # top is updated whenever height is.
#     top: self.height
#     Butt:
#         text: '1'
#     Butt:
#         text: '2'
#     Butt:
#         text: '3'
#     Butt:
#         text: '4'
#     Butt:
#         text: '5'
#     Butt:
#         text: '2'
#     Butt:
#         text: '6'
#     Butt:
#         text: '7'
#     Butt:
#         text: '8'
#     Butt:
#         text: '9'
#     Butt:
#         text: '0'
#     Butt:
#         text: 'Enter'
# ''')
#
# class CalcApp(App, GridLayout):
#
#     def build(self):
#         return self
#
# CalcApp().run()