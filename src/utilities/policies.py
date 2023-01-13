class Epsilon:

    def __init__(self, epsilon=0):
        self.epsilon = epsilon

    def value(self):
        return self.epsilon

    def add(self, epsilon):
        self.epsilon = epsilon

class UCB:
    def __init__(self, c=0):
        self.c = c

    def value(self):
        return self.c

    def add(self, c):
        self.c = c

class egreedyGeo:
    def __init__(self, epsilon=0):
        self.epsilon = epsilon

    def value(self):
        return self.epsilon

    def add(self, epsilon):
        self.epsilon = epsilon