from database import get_connection


class CandidateRepository:
    def get_all(self):
        conn = get_connection()
        candidates = conn.execute("""
            SELECT * FROM candidates
            ORDER BY id DESC
        """).fetchall()
        conn.close()

        return candidates

    def get_by_id(self, candidate_id):
        conn = get_connection()
        candidate = conn.execute("""
            SELECT * FROM candidates
            WHERE id = ?
        """, (candidate_id,)).fetchone()
        conn.close()

        return candidate

    def create(self, candidate_data):
        conn = get_connection()

        conn.execute("""
            INSERT INTO candidates 
            (
                full_name, 
                email, 
                desired_position, 
                skills, 
                experience, 
                resume_url, 
                interview_feedback, 
                technical_score, 
                is_recommended
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            candidate_data["full_name"],
            candidate_data["email"],
            candidate_data["desired_position"],
            candidate_data["skills"],
            candidate_data["experience"],
            candidate_data["resume_url"],
            candidate_data["interview_feedback"],
            candidate_data["technical_score"],
            candidate_data["is_recommended"]
        ))

        conn.commit()
        conn.close()

    def update(self, candidate_id, candidate_data):
        conn = get_connection()

        conn.execute("""
            UPDATE candidates
            SET 
                full_name = ?,
                email = ?,
                desired_position = ?,
                skills = ?,
                experience = ?,
                resume_url = ?,
                interview_feedback = ?,
                technical_score = ?,
                is_recommended = ?
            WHERE id = ?
        """, (
            candidate_data["full_name"],
            candidate_data["email"],
            candidate_data["desired_position"],
            candidate_data["skills"],
            candidate_data["experience"],
            candidate_data["resume_url"],
            candidate_data["interview_feedback"],
            candidate_data["technical_score"],
            candidate_data["is_recommended"],
            candidate_id
        ))

        conn.commit()
        conn.close()

    def delete(self, candidate_id):
        conn = get_connection()

        conn.execute("""
            DELETE FROM candidates
            WHERE id = ?
        """, (candidate_id,))

        conn.commit()
        conn.close()