from flask import Flask, render_template, request, redirect, url_for

from database import init_database
from repositories import CandidateRepository
from services import CandidateService


app = Flask(__name__)

candidate_repository = CandidateRepository()
candidate_service = CandidateService(candidate_repository)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/candidates")
def candidates():
    candidates_list = candidate_service.get_all_candidates()
    return render_template("candidates.html", candidates=candidates_list)


@app.route("/candidates/<int:candidate_id>")
def candidate_details(candidate_id):
    candidate = candidate_service.get_candidate_by_id(candidate_id)

    if candidate is None:
        return "Candidate not found", 404

    return render_template("candidate_details.html", candidate=candidate)


@app.route("/candidates/create", methods=["GET", "POST"])
def create_candidate():
    if request.method == "POST":
        candidate_service.create_candidate(request.form)
        return redirect(url_for("candidates"))

    return render_template("create_candidate.html")


@app.route("/candidates/edit/<int:candidate_id>", methods=["GET", "POST"])
def edit_candidate(candidate_id):
    candidate = candidate_service.get_candidate_by_id(candidate_id)

    if candidate is None:
        return "Candidate not found", 404

    if request.method == "POST":
        candidate_service.update_candidate(candidate_id, request.form)
        return redirect(url_for("candidates"))

    return render_template("edit_candidate.html", candidate=candidate)


@app.route("/candidates/delete/<int:candidate_id>", methods=["POST"])
def delete_candidate(candidate_id):
    candidate_service.delete_candidate(candidate_id)
    return redirect(url_for("candidates"))


if __name__ == "__main__":
    init_database()
    app.run(debug=True)