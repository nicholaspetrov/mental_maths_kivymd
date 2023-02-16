from loguru import logger
from kivy.clock import Clock

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty

# from back_end.database_manager import create_password_table
# from back_end.database_manager import insert_into_password_table
# from back_end.database_manager import check_login
# from back_end.database_manager import check_user_exists

from back_end.database_manager import DatabaseManager

from back_end.hashing import password_to_denary
from back_end.usertest import UserTest


class AppLayout(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dbm = DatabaseManager()
        self.dbm.create_tables()
        self.user = None

    def clear_login_fields(self):
        # Method that clears login fields used in several scenarios (i.e. wrong password etc.)
        self.ids['email'].text = ""
        self.ids['password'].text = ""

    def check_data_login(self):

        # Input from text boxes assigned to individual variables
        email = self.ids['email'].text
        password = self.ids['password'].text

        # Making sure all input login fields are filled
        if email == '' and password == '':
            toast("Email and password are required")
            return

        if email == '':
            toast("Email is required ")
            return

        if password == '':
            toast("Password is required")
            return

        # Allows admin to login - privileges to be determined
        if email == "admin" and password == "admin":
            self.ids.login_screen_manager.current = "Application"
            self.ids.app_screen_manager.transition.direction = "right"

            self.clear_login_fields()
        else:
            # Checks if email inputted into login field is in database
            if not self.dbm.check_user_exists(email, password):
                # If email not in database (i.e. account not registered under this email)
                self.clear_login_fields()
                toast("Wrong email or password")
            else:
                # TODO: Make self.user = self.dbm.check_login(email, password)
                # Runs inputted password and salt through same hashing algorithm
                if self.dbm.check_login(email, password):
                    # If hash of inputted password and hash of password in table equal
                    self.ids.login_screen_manager.current = "Application"
                    self.ids.app_screen_manager.transition.direction = "right"

                    self.clear_login_fields()
                else:
                    toast("Wrong email or password")

    def clear_register_fields(self):
        self.ids['reg_name'].text = ""
        self.ids['reg_email'].text = ""
        self.ids['reg_password'].text = ""
        self.ids['reg_confirm_password'].text = ""

    def validate_reg(self, name, email, password, confirm_password):

        # Making sure all input login fields are filled
        if name.text == '':
            toast('Name required')
            # Returning nothing prevents user advancing from current page (i.e. user has to check their inputs)
            return

        if email.text == '':
            toast('Email required')
            return

        if password.text == '' or confirm_password.text == '':
            toast('Password(s) required')
            return

        if password.text != confirm_password.text:
            # No toast since message (passwords not the same) is already displayed under textfield dynamically
            return

        if len(password.text) < 6:
            # No toast since message (passwords length less than 6) is already displayed under textfield dynamically
            return

        # Passwords table created in database

        self.user = self.dbm.insert_user(name.text, email.text, password.text)
        # Password fed into hashing algorithm
        if self.user is None:
            # Checks if inputted email has already been used to register
            toast("Account already registered under email")
        else:
            # User has successfully logged in
            self.ids.login_screen_manager.current = "Application"
            self.ids.app_screen_manager.transition.direction = "left"
            self.clear_register_fields()


class MainApp(MDApp):
    test_settings = {}
    state = StringProperty("stop")
    user_test = None
    active = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('pages/home.kv')
        Builder.load_file('pages/account.kv')
        Builder.load_file('pages/stats.kv')
        Builder.load_file('pages/about.kv')
        Builder.load_file('pages/quiz.kv')
        Builder.load_file('pages/history.kv')
        self.screen = Builder.load_file('pages/main_app.kv')

        difficulties = ['Easy', 'Medium', 'Hard', 'Mixed']
        difficulty_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback('Difficulty', x),
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
                "on_release": lambda x=i: self.menu_callback('Operator', x),
            } for i in types
        ]
        self.type_menu = MDDropdownMenu(
            caller=self.screen.ids.type_button,
            items=type_items,
            position="bottom",
            width_mult=2.5,
            max_height=200
        )

        durations = ['1 min', '2 min', '5 min', '10 min']
        duration_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback('Duration', x),
            } for i in durations
        ]
        self.duration_menu = MDDropdownMenu(
            caller=self.screen.ids.duration_button,
            items=duration_items,
            position="bottom",
            width_mult=2.5,
            max_height=200
        )

    def stop_user_test(self, dt):
        logger.debug('Stopping the test')
        self.active = False
        self.root.ids.app_screen_manager.current = 'Start test'

    def menu_callback(self, param_name, param_value):
        if param_name == 'Duration':
            param_value = int(param_value.split(' ')[0]) * 60

        self.test_settings[param_name] = param_value
        output = str(self.test_settings)
        self.screen.ids.test_label.text = output

        self.duration_menu.dismiss()
        self.type_menu.dismiss()
        self.difficulty_menu.dismiss()

    def build(self):
        return self.screen

    # def build(self):
    #     # Loads kv file
    #     return Builder.load_file("main_app.kv")

    def open_menu(self):
        # For side menu
        self.root.ids.nav_drawer.set_state("open")

    # def on_state(self, instance, value):
        # {
        #     "start": self.root.ids.app_screen_manager.current_screen.ids.progress_bar.start,
        #     "stop": self.root.ids.app_screen_manager.current_screen.ids.progress_bar.stop,
        # }.get(value)()

    # def create_next_question(self):
    #     toast('Next question')

    def get_next_question(self):
        if len(self.user_test.questions) > 0:
            answer = self.root.ids.app_screen_manager.screens[4].ids.answer_input.text
            logger.debug(f'Storing answer: {answer}')
            self.user_test.check_answer(int(answer) if len(answer) > 0 else 0)
        else:
            self.root.ids.app_screen_manager.screens[4].ids.question_label.font_style = 'H3'
            self.root.ids.app_screen_manager.screens[4].ids.user_test_progress_bar.running_duration = self.test_settings['Duration']
            self.root.ids.app_screen_manager.screens[4].ids.user_test_progress_bar.start()
            Clock.schedule_once(self.stop_user_test, self.user_test.duration)

        # if self.active:
        self.root.ids.app_screen_manager.screens[4].ids.answer_input.text = ''
        question = self.user_test.get_next_question()
        logger.debug(f'Generating next question: {question}')
        self.root.ids.app_screen_manager.screens[4].ids.question_label.text = str(question)
        # else:
        #     logger.debug('Redirecting to start test after test has finished')
        #     self.root.ids.app_screen_manager.current = 'Start test'


    def start_new_test(self):
        logger.debug(f'Starting new test: {self.test_settings}')
        self.user_test = UserTest(
            user_id=1,
            difficulty=self.test_settings['Difficulty'],
            duration=self.test_settings['Duration'],
            question_operator=self.test_settings['Operator']
        )

    def on_menu_click(self, item_name):
        # When item in menu clicked, menu closes
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.app_screen_manager.current = item_name

    def exit_app(self):
        # User redirected to login when top-right exit button clicked
        self.root.ids.login_screen_manager.current = "Login"
        self.root.ids.login_screen_manager.transition.direction = "right"


MainApp().run()

'''
TODO:
- Change TopAppBar title with username or page name when logged in
- "Save db file into backend python package"
- Enable update button once something has been changed in settings page
- Change stacklayout for test creation page so that it doesn't cover topappbar
- Change toolbar during test so exit button ("end test early button") redirects user to home rather than to login page
- Dropdown listbox not menu
- Animation for switching screens
'''
