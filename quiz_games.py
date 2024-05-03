from abc import ABC, abstractmethod

class Quiz(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def ask_question(self):
        pass

    @abstractmethod
    def check_answer(self, question, user_answer):
        pass
    
    @abstractmethod
    def reset(self):
        pass
    
    @abstractmethod
    def print_gamestate(self):
        pass