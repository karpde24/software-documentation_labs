class CandidateService:
    def __init__(self, candidate_repository):
        self.candidate_repository = candidate_repository

    def get_all_candidates(self):
        return self.candidate_repository.get_all()

    def get_candidate_by_id(self, candidate_id):
        return self.candidate_repository.get_by_id(candidate_id)

    def create_candidate(self, form_data):
        candidate_data = self._prepare_candidate_data(form_data)
        self.candidate_repository.create(candidate_data)

    def update_candidate(self, candidate_id, form_data):
        candidate_data = self._prepare_candidate_data(form_data)
        self.candidate_repository.update(candidate_id, candidate_data)

    def delete_candidate(self, candidate_id):
        self.candidate_repository.delete(candidate_id)

    def _prepare_candidate_data(self, form_data):
        return {
            "full_name": form_data.get("full_name"),
            "email": form_data.get("email"),
            "desired_position": form_data.get("desired_position"),
            "skills": form_data.get("skills"),
            "experience": form_data.get("experience"),
            "resume_url": form_data.get("resume_url"),
            "interview_feedback": form_data.get("interview_feedback"),
            "technical_score": float(form_data.get("technical_score") or 0),
            "is_recommended": 1 if form_data.get("is_recommended") == "on" else 0
        }