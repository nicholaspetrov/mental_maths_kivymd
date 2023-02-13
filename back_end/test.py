

class Test:
    def __init__(self, test_id, difficulty, duration, test_type):
        self.test_id = test_id
        self.difficulty = difficulty
        self.duration = duration
        self.test_type = test_type
        self.number_q = None
        self.number_correct_a = None

    def set_test_results(self, number_q, number_correct_a):
        self.number_q = number_q
        self.number_correct_a = number_correct_a

