class Epsilon:

    def __init__(self, epsilon=0):
        self.epsilon = epsilon

    def value(self):
        return self.epsilon

    def add(self, epsilon):
        self.epsilon = epsilon

class Optimistic:

    def __init__(self, optimistic_value=0):
        self.optimistic_value = optimistic_value

    def value(self):
        return self.optimistic_value

    def add(self, optimisitc_value):
        self.optimistic_value = optimisitc_value

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
