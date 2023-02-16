from kivy.clock import Clock
from back_end.usertest import UserTest


class UserTestRunner:
    active = True

    def __init__(self, user_test):
        self.user_test = user_test

    def start_user_test(self):
        Clock.schedule_once(self.stop_user_test, self.user_test.duration)
        while self.active:
            res = input(f'{self.user_test.get_next_question()}: ')
            self.user_test.check_answer(int(res) if len(res) > 0 else 0)

        self.user_test.calculate_score()
        print(self.user_test.score)

    def stop_user_test(self, dt):
        self.active = False


if __name__ == '__main__':
    test = UserTest('2', 'Easy', 5, '+')
    runner = UserTestRunner(test)
    runner.start_user_test()
