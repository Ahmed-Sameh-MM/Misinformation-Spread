class AgentSocioEmotionalClasses:
    lowValue = 0.3
    highValue = 0.7

    def __init__(self, education: float, anger:float, trust):
        self.education = education
        self.anger = anger

        if trust is None:
            self.trust = (anger + education) / 2

        else:
            self.trust = trust

    def __str__(self):
        return f'education: {self.education}, anger({self.anger}, trust({self.trust})'


class HighEducationHighEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = super().highValue
        anger = super().highValue

        super().__init__(education, anger, None)


class LowEducationLowEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = super().lowValue
        anger = super().lowValue

        super().__init__(education, anger, None)


class HighEducationLowEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = super().highValue
        anger = super().lowValue

        super().__init__(education, anger, None)


class LowEducationHighEmotional(AgentSocioEmotionalClasses):
    def __init__(self):
        education = super().lowValue
        anger = super().highValue

        super().__init__(education, anger, None)
