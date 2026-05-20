from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
import sqlite3

app = Flask(__name__)
CORS(app)

swagger = Swagger(app)

DATABASE = "cornerstone_lab.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return """
    <h1>Cornerstone Recruiting API</h1>
    <p>API для лабораторної роботи №2 працює.</p>

    <h3>Доступні посилання:</h3>
    <ul>
        <li><a href="/apidocs">Swagger documentation</a></li>
        <li><a href="/api/tables">Переглянути таблиці бази даних</a></li>
        <li><a href="/api/candidates">Список кандидатів</a></li>
        <li><a href="/api/vacancies">Список вакансій</a></li>
        <li><a href="/api/interviews">Результати інтерв'ю</a></li>
    </ul>
    """


@app.route("/api/tables", methods=["GET"])
def get_tables():
    """
    Get all database tables
    ---
    tags:
      - Database
    responses:
      200:
        description: List of database tables
    """
    conn = get_db_connection()
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    conn.close()

    return jsonify([row["name"] for row in tables])


@app.route("/api/candidates", methods=["GET"])
def get_candidates():
    """
    Get all candidates
    ---
    tags:
      - Candidates
    responses:
      200:
        description: List of candidates
    """
    conn = get_db_connection()

    try:
        candidates = conn.execute("SELECT * FROM candidates").fetchall()
        result = [dict(row) for row in candidates]
        return jsonify(result)
    except sqlite3.Error as e:
        return jsonify({
            "error": "Cannot read candidates table",
            "details": str(e),
            "hint": "Check table name using /api/tables"
        }), 500
    finally:
        conn.close()


@app.route("/api/candidates/<int:candidate_id>", methods=["GET"])
def get_candidate(candidate_id):
    """
    Get candidate by ID
    ---
    tags:
      - Candidates
    parameters:
      - name: candidate_id
        in: path
        type: integer
        required: true
        description: Candidate ID
    responses:
      200:
        description: Candidate data
      404:
        description: Candidate not found
    """
    conn = get_db_connection()

    try:
        candidate = conn.execute(
            "SELECT * FROM candidates WHERE id = ?",
            (candidate_id,)
        ).fetchone()

        if candidate is None:
            return jsonify({"error": "Candidate not found"}), 404

        return jsonify(dict(candidate))
    except sqlite3.Error as e:
        return jsonify({
            "error": "Cannot read candidate",
            "details": str(e),
            "hint": "Check table name and column id"
        }), 500
    finally:
        conn.close()


@app.route("/api/vacancies", methods=["GET"])
def get_vacancies():
    """
    Get all vacancies
    ---
    tags:
      - Vacancies
    responses:
      200:
        description: List of vacancies
    """
    conn = get_db_connection()

    try:
        vacancies = conn.execute("SELECT * FROM vacancies").fetchall()
        result = [dict(row) for row in vacancies]
        return jsonify(result)
    except sqlite3.Error as e:
        return jsonify({
            "error": "Cannot read vacancies table",
            "details": str(e),
            "hint": "Check table name using /api/tables"
        }), 500
    finally:
        conn.close()


@app.route("/api/interviews", methods=["GET"])
def get_interviews():
    """
    Get all interview results
    ---
    tags:
      - Interviews
    responses:
      200:
        description: List of interview results
    """
    conn = get_db_connection()

    try:
        interviews = conn.execute("SELECT * FROM interview_results").fetchall()
        result = [dict(row) for row in interviews]
        return jsonify(result)
    except sqlite3.Error as e:
        return jsonify({
            "error": "Cannot read interview_results table",
            "details": str(e),
            "hint": "Check table name using /api/tables"
        }), 500
    finally:
        conn.close()


@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Check API status
    ---
    tags:
      - System
    responses:
      200:
        description: API status
    """
    return jsonify({
        "status": "ok",
        "message": "Cornerstone Recruiting API is running"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)