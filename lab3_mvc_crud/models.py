class Candidate:
    def __init__(
        self,
        id=None,
        full_name=None,
        email=None,
        desired_position=None,
        skills=None,
        experience=None,
        resume_url=None,
        interview_feedback=None,
        technical_score=0,
        is_recommended=False
    ):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.desired_position = desired_position
        self.skills = skills
        self.experience = experience
        self.resume_url = resume_url
        self.interview_feedback = interview_feedback
        self.technical_score = technical_score
        self.is_recommended = is_recommended