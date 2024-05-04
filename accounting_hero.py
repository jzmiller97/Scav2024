class guitar_hero(Quiz):
    def ask_question(self):
        question = random.choice(list(self.questions.keys()))
        answer = input(question + " ")
        self.check_answer(question, answer)

    def check_answer(self, question, user_answer):
        correct_answer = self.questions[question]
        if user_answer.lower() == correct_answer.lower():
            print("Correct!")
        else:
            print("Incorrect. The correct answer is:", correct_answer)

if __name__ == "__main__":
    quiz = CommandLineQuiz()
    while True:
        quiz.ask_question()
        play_again = input("Do you want to play again? (yes/no): ")
        if play_again.lower() != "yes":
            break