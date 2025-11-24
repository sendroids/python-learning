# This script introduces classes and objects
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(self.name, "says hello!")

dog = Animal("Buddy")
dog.speak()