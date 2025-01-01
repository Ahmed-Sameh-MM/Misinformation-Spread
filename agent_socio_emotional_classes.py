class AgentSocioEmotionalClasses:
    def __init__(self, education: float, anger:float, trust: float):
        self.education = education
        self.anger = anger
        self.trust = trust

    def __str__(self):
        return f'education: {self.education}, anger({self.anger}, trust({self.trust})'


class HighEducationHighEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = 0.9
        anger=0.9
        trust=0.9

        super().__init__(education, anger, trust)


class LowEducationLowEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = 0.1
        anger=0.1
        trust=0.1

        super().__init__(education, anger, trust)


class HighEducationLowEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = 0.9
        anger=0.1
        trust=0.1

        super().__init__(education, anger, trust)


class LowEducationHighEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = 0.1
        anger=0.9
        trust=0.9

        super().__init__(education, anger, trust)
