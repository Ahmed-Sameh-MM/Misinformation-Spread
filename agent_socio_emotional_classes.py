from emotions import Emotions

class AgentSocioEmotionalClasses:
    def __init__(self, education: float, emotions: Emotions):
        self.education = education
        self.emotions = emotions

    def __str__(self):
        return f'education: {self.education}, emotions({self.emotions.__str__()})'

class HighEducationHighEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = 0.9

        emotions = Emotions(
            anger=0.9,
            trust=0.9,
        )

        super().__init__(education, emotions)

class LowEducationLowEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = 0.1

        emotions = Emotions(
            anger=0.1,
            trust=0.1,
        )

        super().__init__(education, emotions)

class HighEducationLowEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = 0.9

        emotions = Emotions(
            anger=0.1,
            trust=0.1,
        )

        super().__init__(education, emotions)

class LowEducationHighEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = 0.1

        emotions = Emotions(
            anger=0.9,
            trust=0.9,
        )

        super().__init__(education, emotions)
