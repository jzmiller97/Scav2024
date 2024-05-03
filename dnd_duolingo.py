import random
from quiz_games import Quiz
import openpyxl
import sys

def string_hearts(num_hearts) -> str:
    hearts: str = '\u001b[31m\u2764\u001b[0m '  # ANSI escape codes for red heart
    return hearts * num_hearts

def string_box(text):
    width: int = len(text) + 4
    l1: str = "\u001b[1m\u250f" + "\u2501" * width + "\u2513\u001b[0m"
    l2: str = "\u001b[1m\u2503  " + text + "  \u2503\u001b[0m"
    l3: str = "\u001b[1m\u2517" + "\u2501" * width + "\u251b\u001b[0m"
    return "\n".join((l1, l2, l3))

def read_spreadsheet_to_dict(filename):
    data_dict: dict[str, str] = {}
    try:
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active
        for row in sheet.iter_rows(values_only=True):
            key = str(row[0])
            value = str(row[1])
            data_dict[key] = value
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print("An error occurred:", e)
    return data_dict

def read_spreadsheet_to_set(filename):
    data_set: set[str] = {}
    try:
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active
        for row in sheet.iter_rows(values_only=True):
            value = str(row[0])
            data_set.add(value)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print("An error occurred:", e)
    return data_set

def print_sword_greeting():
    sword: list[str] = [
        "                 />",
        " ()            //---------------------------------------------------------(",
        "(*)OXOXOXOXOXO(*>  Greetings, adventurer. Welcome to Duolingo & Dragons.   \\",
        " ()            \\\\-----------------------------------------------------------)",
        "                 \\>"
    ]
    print("\u001b[33m")  # ANSI escape code for yellow color
    for line in sword:
        print(line)
    print("\u001b[0m")  # Reset color

questions: dict[str, str] = read_spreadsheet_to_dict
praises: set[str] = read_spreadsheet_to_set
insults: set[str] = read_spreadsheet_to_set
motivations: set[str] = read_spreadsheet_to_set

class DnD(Quiz):
    hp: int
    questions: dict[str, str]
    praises: set[str]
    insults: set[str]
    motivations: set[str]
    streak: int
    hp_max: int
    
    def __init__(self, questions: dict["str", "str"], praises: set[str], 
                 insults: set[str], motivations: set[str], hp: int) -> None:
        self.questions = questions
        self.praises = praises
        self.insults = insults
        self.motivations: motivations
        self.hp = hp
        self.hp_max = hp
        self.streak = 0
    
    def ask_question(self) -> None:
        question = random.choice(list(self.questions.keys()))
        motivation = random.choice(self.motivations)
        answer = input(question + " " + motivation + " ")
        self.check_answer(question, answer)

    def check_answer(self, question, user_answer) -> None:
        correct_answer = self.questions[question]
        if user_answer.lower() == correct_answer.lower():
            streak += 1
            if streak % 5 == 0:
                hp += 1
            print(random.choice(self.praises))
        else:
            streak = 0
            hp += -1
            print(random.choice(self.insults) + " The correct answer is:", correct_answer)
            
    def reset(self) -> None:
        self.streak = 0
        self.hp = self.hp_max
        
    def print_gamestate(self) -> None:
        print(string_box("Hit points remaining: " + string_hearts(self.hp)))
        print("Current streak: " + self.streak + ".")
        

if __name__ == "__main__":
    print_sword_greeting()
    quiz = DnD()
    while True:
        quiz.ask_question()
        if quiz.hp <= 0:
            play_again: str = input("Re-roll initiative? (yes/no): ")
        if play_again.lower() != "yes":
            quiz.reset()
        else:
            break