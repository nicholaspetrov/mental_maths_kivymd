from loguru import logger
from kivy.clock import Clock

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image


# from back_end.database_manager import create_password_table
# from back_end.database_manager import insert_into_password_table
# from back_end.database_manager import check_login
# from back_end.database_manager import check_user_exists

from back_end.database_manager import DatabaseManager
# from back_end import authenticator

from back_end.hashing import password_to_denary
from back_end.user import User
from back_end.usertest import UserTest


class AppLayout(MDBoxLayout):
    email = StringProperty()
    password = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainApp(MDApp):
    test_settings = {}
    user_test = None
    active = True
    user = None
    user_name = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dbm = DatabaseManager()
        self.dbm.create_tables()
        self.user = User('', '')
        Builder.load_file('pages/home.kv')
        Builder.load_file('pages/account.kv')
        Builder.load_file('pages/stats.kv')
        Builder.load_file('pages/about.kv')
        Builder.load_file('pages/quiz.kv')
        Builder.load_file('pages/history.kv')
        Builder.load_file('pages/test_results.kv')
        self.screen = Builder.load_file('pages/main_app.kv')

        difficulties = ['Easy', 'Medium', 'Hard', 'Mixed']
        difficulty_items = [
            {
                "text": difficulty,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'Difficulty: {difficulty}': self.menu_callback('Difficulty', x.split(' ')[1]),
            } for difficulty in difficulties
        ]
        self.difficulty_menu = MDDropdownMenu(
            caller=self.screen.ids.difficulty_button,
            items=difficulty_items,
            position="auto",
            width_mult=2.5,
            max_height=200
        )

        operators = ['Addition +', 'Subtraction -', 'Division /', 'Multiplication *']
        operator_items = [
            {
                "text": operator,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'Operator: {operator}': self.menu_callback('Operator', x.split(' ')[2]),
            } for operator in operators
        ]
        self.operator_menu = MDDropdownMenu(
            caller=self.screen.ids.operator_button,
            items=operator_items,
            position="auto",
            width_mult=2.5,
            max_height=200
        )

        durations = ['1 min', '2 min', '5 min', '10 min']
        duration_items = [
            {
                "text": duration,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f'Duration: {duration}': self.menu_callback('Duration', x),
            } for duration in durations
        ]
        self.duration_menu = MDDropdownMenu(
            caller=self.screen.ids.duration_button,
            items=duration_items,
            position="top",
            width_mult=2.5,
            max_height=200
        )

    def reset_test_page(self):
        self.root.ids.app_screen_manager.screens[4].ids.question_label.text = "Click 'Next question' to start"
        self.root.ids.app_screen_manager.screens[4].ids.question_label.font_style = 'H4'
        self.root.ids.app_screen_manager.screens[4].ids.answer_input.text = ''
        self.root.ids.app_screen_manager.screens[4].ids.correct_progress_bar.value = 0
        self.root.ids.app_screen_manager.screens[4].ids.incorrect_progress_bar.value = 0
        self.root.ids.app_screen_manager.screens[4].ids.question_label.bold = False
        self.root.ids.app_screen_manager.screens[4].ids.user_test_progress_bar.stop()

    def stop_user_test(self, dt):
        self.reset_test_page()
        total_possible_points = 0
        correct_answers = 0
        logger.debug('Stopping the test')
        self.active = False
        self.root.ids.app_screen_manager.current = 'Test_results'
        self.user_test.calculate_score()
        print(self.user_test.user_results)
        for result in self.user_test.user_results:
            if result[1] > 0:
                correct_answers += 1
            if result[0] == 'Easy':
                total_possible_points += 1
            elif result[0] == 'Medium':
                total_possible_points += 2
            else:
                total_possible_points += 3

        questions_answered = len(self.user_test.user_results)

        time = '{:g}'.format(int(self.test_settings["Duration"])/60)
        number_of_seconds = int(self.test_settings['Duration'])
        # https://stackoverflow.com/questions/13097099/how-to-make-python-print-1-as-opposed-to-1-0

        self.root.ids.app_screen_manager.screens[6].ids.difficulty_label.text = self.test_settings['Difficulty']
        self.root.ids.app_screen_manager.screens[6].ids.operator_label.text = self.test_settings['Operator']
        self.root.ids.app_screen_manager.screens[6].ids.duration_label.text = f'{time} min'

        if questions_answered == 0:
            self.root.ids.app_screen_manager.screens[6].ids.correct_answers_label.text = '0'
            self.root.ids.app_screen_manager.screens[6].ids.speed_label.text = '0'
        else:
            if self.user_test.score < 0 or self.user_test.score == 0:
                self.root.ids.app_screen_manager.screens[6].ids.score_label.text = '0'
                self.root.ids.app_screen_manager.screens[6].ids.correct_answers_label.text = '0'
                self.root.ids.app_screen_manager.screens[6].ids.speed_label.text = '0'
            else:
                self.root.ids.app_screen_manager.screens[6].ids.score_label.text = f'{str(self.user_test.score)}/{str(total_possible_points)}'
                self.root.ids.app_screen_manager.screens[6].ids.correct_answers_label.text = f'{correct_answers}/{questions_answered}'
                self.root.ids.app_screen_manager.screens[6].ids.speed_label.text = f'{str(round(number_of_seconds/self.user_test.score, 2))} seconds per point'

    def menu_callback(self, param_name, param_value):
        if param_name == 'Duration':
            self.test_settings[param_name] = int(param_value.split(' ')[1])*60
            self.screen.ids.duration_button.set_item(param_value)
            self.duration_menu.dismiss()
        else:
            self.test_settings[param_name] = param_value
            if param_name == 'Difficulty':
                self.screen.ids.difficulty_button.set_item(f'Difficulty: {param_value}')
                self.difficulty_menu.dismiss()
            if param_name == 'Operator':
                self.screen.ids.operator_button.set_item(f'Operator: {param_value}')
                self.operator_menu.dismiss()

        print(self.test_settings)

    def build(self):
        return self.screen

    def open_menu(self):
        # For side menu
        self.root.ids.nav_drawer.set_state("open")

    def refocus_ti(self, *args):
        self.root.ids.app_screen_manager.screens[4].ids.answer_input.focus = True

    def get_next_question(self):
        # User now able to type answer into text box
        self.root.ids.app_screen_manager.screens[4].ids.answer_input.disabled = False
        if len(self.user_test.questions) > 0:
            # If this isn't the first question asked
            answer = self.root.ids.app_screen_manager.screens[4].ids.answer_input.text
            # Answer retrieved from text box
            if answer.lstrip("-").isdigit() or answer == '':
                # Validates answer input - prevents strings of letters from being inputted whilst allowing negative sign
                logger.debug(f'Storing answer: {answer}')
                # If nothing is entered (i.e. question skipped), 0 is added to result
                self.user_test.check_answer(int(answer) if len(answer) > 0 else 0)
            else:
                toast('Invalid answer')
                self.root.ids.app_screen_manager.screens[4].ids.answer_input.text = ''
                return
        else:
            # Label that displays question now made bold and increases in size
            self.root.ids.app_screen_manager.screens[4].ids.question_label.font_style = 'H3'
            self.root.ids.app_screen_manager.screens[4].ids.question_label.bold = True
            # Sets the duration of the horizontal timer progress bar on top of screen based on what was inputted in the
            # prior test construction page
            self.root.ids.app_screen_manager.screens[4].ids.user_test_progress_bar.running_duration = self.test_settings['Duration']
            # Timer + progress bar started
            self.root.ids.app_screen_manager.screens[4].ids.user_test_progress_bar.start()
            Clock.schedule_once(self.stop_user_test, self.user_test.duration)

        # Values for points gained or lost after answering the question correctly or incorrectly stored - later used for
        # displaying green and red progress bars
        current_correct = self.root.ids.app_screen_manager.screens[4].ids.correct_progress_bar.value
        current_incorrect = self.root.ids.app_screen_manager.screens[4].ids.incorrect_progress_bar.value
        if len(self.user_test.questions) > 0:
            if self.user_test.user_results[-1][1] > 0:
                # If points scored are positive, then question has been answered correctly (back in class UserTest)
                current_correct += self.user_test.user_results[-1][1]
                # Green progress bar increases accordingly by how many points was just gained
                self.root.ids.app_screen_manager.screens[4].ids.correct_progress_bar.value = current_correct
            else:
                if self.user_test.user_results[-1][1] == 0:
                    # If nothing was inputted (i.e. User has skipped question) - no points lost or gained
                    pass
                else:
                    # Red progress bar increases accordingly by how many points was just lost
                    current_incorrect += -(self.user_test.user_results[-1][1])
                    self.root.ids.app_screen_manager.screens[4].ids.incorrect_progress_bar.value = current_incorrect
        else:
            pass

        # If either progress bar fills completely, progress bar resets
        if current_correct >= 100:
            self.root.ids.app_screen_manager.screens[4].ids.correct_progress_bar.value = 0
        if current_incorrect >= 100:
            self.root.ids.app_screen_manager.screens[4].ids.incorrect_progress_bar.value = 0

        # After user submitted answer, text in input box emptied
        self.root.ids.app_screen_manager.screens[4].ids.answer_input.text = ''
        # Next question retrieved using same very method
        question = self.user_test.get_next_question()
        # Keeps focus on enter button - User essentially never has to use the mouse (just type answer and enter, then repeat)
        Clock.schedule_once(self.refocus_ti)
        logger.debug(f'Generating next question: {question}')
        # Tuple (question) replaces the "Click 'Next question' to start" in visually appealing format
        self.root.ids.app_screen_manager.screens[4].ids.question_label.text = ' '.join(map(str, question))

    def start_new_test(self):
        toast('Good luck!')
        self.reset_test_page()
        self.root.ids.app_screen_manager.screens[4].ids.answer_input.disabled = True
        # Prevents user from typing into enter box - enabled once test has officially started
        self.root.ids.app_screen_manager.screens[4].ids.question_label.font_style = 'H4'
        self.root.ids.app_screen_manager.screens[4].ids.user_test_progress_bar.value = 0

        if len(self.test_settings) < 3:
            # Making sure all test settings has been filled in
            toast('Please fill in all required fields')
            return
        else:
            logger.debug(f'Starting new test: {self.test_settings}')
            # UserTest object created based on the inputs used as attributes
            self.user_test = UserTest(
                user_id=1,
                difficulty=self.test_settings['Difficulty'],
                duration=self.test_settings['Duration'],
                question_operator=self.test_settings['Operator']
            )
            # Resets what questions were asked and results - when test is restarted/new one made and tried
            self.user_test.questions = []
            self.user_test.user_results = []

            # Directs user to actual quiz page
            self.root.ids.app_screen_manager.current = "Quiz"
            self.root.ids.app_screen_manager.transition.direction = "right"

    def on_menu_click(self, item_name):
        # When item in menu clicked, menu closes
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.app_screen_manager.current = item_name

    def exit_app(self):
        # User redirected to login when top-right exit button clicked
        self.user = None
        self.root.ids.login_screen_manager.current = "Login"
        self.root.ids.login_screen_manager.transition.direction = "right"
        self.reset_test_page()

    def clear_register_fields(self):
        self.root.ids.reg_name.text = ""
        self.root.ids.reg_email.text = ""
        self.root.ids.reg_password.text = ""
        self.root.ids.reg_confirm_password.text = ""

    def register(self, name, email, password, confirm_password):

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

        result = authenticator.signup(email=email.text, password=password.text, name=name.text)
        if result is not None:
            # User has successfully logged in
            self.user = User(
                name=name.text,
                email=email.text,
                user_id=result['localId']
            )
            self.root.ids.login_screen_manager.current = "Application"
            self.root.ids.app_screen_manager.transition.direction = "left"
            self.user_name = self.user.name
            self.clear_register_fields()
        else:
            # Checks if inputted email has already been used to register
            toast("Account already registered under email")

        # user = self.dbm.insert_user(name.text, email.text, password.text)
        # Password fed into hashing algorithm
        # if user is not None:
        #     # User has successfully logged in
        #     self.user = user
        #     self.root.ids.login_screen_manager.current = "Application"
        #     self.root.ids.app_screen_manager.transition.direction = "left"
        #     self.user_name = self.user.name
        #     self.clear_register_fields()
        # else:
        #     # Checks if inputted email has already been used to register
        #     toast("Account already registered under email")

    def clear_login_fields(self):
        # Method that clears login fields used in several scenarios (i.e. wrong password etc.)
        self.root.ids.email.text = ""
        self.root.ids.password.text = ""

    def login(self):

        # Input from text boxes assigned to individual variables
        email = self.root.ids.email.text
        password = self.root.ids.password.text

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
            self.user = User('admin', 'admin')
            self.root.ids.login_screen_manager.current = "Application"
            self.root.ids.app_screen_manager.transition.direction = "right"
            self.user_name = 'admin'
            self.clear_login_fields()
        else:
            # Runs inputted password and salt through same hashing algorithm
            self.user = self.dbm.check_login(email, password)

            if self.user is not None:
                # If hash of inputted password and hash of password in table equal
                self.root.ids.login_screen_manager.current = "Application"
                self.root.ids.app_screen_manager.current = "Home"
                self.root.ids.app_screen_manager.transition.direction = "right"
                self.user_name = self.user.name
                self.clear_login_fields()

            else:
                toast("Wrong email or password")
                self.clear_login_fields()


MainApp().run()

'''
TODO:
- "Save db file into backend python package"
- Enable update button once something has been changed in settings page
- Animation for switching screens
- Python can send emails
- RegEx for email - correct form
- https://stackoverflow.com/questions/44617793/image-size-on-kivy example of background picture
'''
