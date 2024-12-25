class Emotions:
    def __init__(self, anger: float, trust: float):
        self.anger = anger # [0, 1]
        self.trust = trust # [0, 1]

    def get_emotions_mean(self):
        return (self.anger + self.trust) / 2

    def __str__(self):
        return f'anger: {self.anger}, trust: {self.trust}'
