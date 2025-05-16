class ExamSubmission:
    def __init__(self, examinee: str, points: int):
        self.examinee = examinee
        self.points = points

    def __repr__(self):
        return f"ExamSubmission (examinee: {self.examinee}, points: {self.points})"
