import threading
import random
from typing import Optional
from dnd_duolingo import read_spreadsheet_to_set
from quiz_games import Quiz
import sys

OPERATIONS: set[str] = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "x", "/", "=", "."}

def print_intro():
    print("\033[1;37;40m _____________________")
    print("|  _________________  |")
    print("| | \033[1;38;5;208mAccounting Hero\033[0m | |")
    print("| |_________________| |")
    print("|  ___ ___ ___   ___  |")
    print("| | 7 | 8 | 9 | | \033[1;32;40m+\033[1;37;40m | |")
    print("| |___|___|___| |___| |")
    print("| | 4 | 5 | 6 | | \033[1;32;40m-\033[1;37;40m | |")
    print("| |___|___|___| |___| |")
    print("| | 1 | 2 | 3 | | \033[1;32;40mx\033[1;37;40m | |")
    print("| |___|___|___| |___| |")
    print("| | . | 0 | = | | \033[1;32;40m/\033[1;37;40m | |")
    print("| |___|___|___| |___| |")
    print("|_____________________|")
    print("\033[0m")
    print("\033[1;33mLedger this layout if you wish to be profitable!\033[0m")

def get_input_within_time_limit(prompt: str, time_limit: float, insults: set[str]) -> Optional[str]:
    print(prompt)
    
    def read_input():
        global user_input
        user_input = input()
    
    input_thread = threading.Thread(target=read_input)
    input_thread.start()
    input_thread.join(time_limit)
    
    if input_thread.is_alive():
        insult: str = random.choice(list(insults))
        print("\n" + insult)
        input_thread.join()
        return None
    else:
        return user_input
    
def display(curr_set: set[str], window: int):
    print("┏━━━━━━━━━━━┓")
    print("┃" + create_string_with_padding(str(window), 11) + "┃")
    print("┃" + block("1", curr_set) + "┃" + block("2", curr_set) + "┃" + block("3", curr_set) + "┃" + block("+", curr_set) + "┃")
    print("┃" + block("4", curr_set) + "┃" + block("5", curr_set) + "┃" + block("6", curr_set) + "┃" + block("-", curr_set) + "┃")
    print("┃" + block("7", curr_set) + "┃" + block("8", curr_set) + "┃" + block("9", curr_set) + "┃" + block("x", curr_set) + "┃")
    print("┃" + block(".", curr_set) + "┃" + block("0", curr_set) + "┃" + block("=", curr_set) + "┃" + block("/", curr_set) + "┃")
    print("┗━━━━━━━━━━━┛")

def block(poss_str: str, test_set: set[str]) -> str:
    if any(item == poss_str for item in test_set):
        return "\033[31m▄▄\033[0m"
    else:
        return "▄▄"

def create_string_with_padding(num: str, length: int):
    num_length: int = len(num)
    return "\033[32m" + ' ' * (length - num_length) + str(num) + "\033[0m"

class accounting_hero(Quiz):
    time_insults: set[str]
    praise_set: set[str]
    insult_set: set[str]
    time_limit: float
    time_init: float
    score: int
    high_score: int
    self_oper: set[str]

    def __init__(self, timings: set[str], praises: set[str], insults: set[str], time: float):
        self.time_insults = timings
        self.praise_set = praises
        self.insult_set = insults
        self.time_limit = time
        self.time_init = time
        self.score = 0
        self.high_score = 0
        self.oper_set = OPERATIONS

    def ask_question(self):
        curr_set: set[str] = set()
        for i in range(3):
            curr_set.add(random.choice(list(self.oper_set)))
        display(curr_set, self.score)
        print(curr_set)
        answer = get_input_within_time_limit("What operations were used?", self.time_limit, self.time_insults)
        self.check_answer(curr_set, answer)

    def check_answer(self, question, user_answer):
        if user_answer is not None and question == set(user_answer):
            self.score += abs(int(self.time_init - self.time_limit + 1))
            self.time_limit += random.gauss(mu=0.0, sigma=1.0)
            print(random.choice(list(self.praise_set)))
        else:
            self.score += -1 * abs(int(self.time_init - self.time_limit + 1))
            self.time_limit += random.gauss(mu=-1.0, sigma=1.0)
            print(random.choice(list(self.insult_set)))

    def print_gamestate(self):
        print("Current score: " + str(self.score) + ". High score: " + str(self.high_score) + ". Time limit: " + str(self.time_limit) + ".")

    def reset(self) -> None:
        self.score = 0
        self.time_limit = self.time_init
    

if __name__ == "__main__":
    print_intro()
    time_insults: set[str] = {"Too slow for the Big Four."} # read_spreadsheet_to_set("time_insults.xlsx")
    acc_praises: set[str] = {"Christmas Bonus?"} # read_spreadsheet_to_set("acc_praises.xlsx")
    acc_insults: set[str] = {"Where did you go to college? Northwestern?"} # read_spreadsheet_to_set("acc_insults.xlsx")
    quiz: "accounting_hero" = accounting_hero(time_insults, acc_praises, acc_insults, int(sys.argv[1]))
    while True:
        quiz.print_gamestate()
        quiz.ask_question()
        if quiz.time_limit <= 0:
            if quiz.score > quiz.high_score:
                quiz.high_score = quiz.score
            play_again: str = input("Re-install Excel? (yes/no): ")
            if play_again.lower() != "yes":
                quiz.reset()
            else:
                break