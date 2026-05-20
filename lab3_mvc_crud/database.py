import sqlite3


DATABASE = "cornerstone_lab.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            desired_position TEXT,
            skills TEXT,
            experience TEXT,
            resume_url TEXT,
            interview_feedback TEXT,
            technical_score REAL,
            is_recommended INTEGER
        )
    """)

    candidates_count = conn.execute(
        "SELECT COUNT(*) FROM candidates"
    ).fetchone()[0]

    if candidates_count == 0:
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
            "Ivan Petrenko",
            "ivan.petrenko@example.com",
            "ASP.NET MVC Developer",
            "C#, ASP.NET MVC, SQL, HTML, CSS",
            "2 years of commercial experience",
            "https://example.com/resume1",
            "Good technical knowledge and strong motivation.",
            8.5,
            1
        ))

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
            "Olena Koval",
            "olena.koval@example.com",
            "Frontend Developer",
            "JavaScript, React, HTML, CSS",
            "1 year of experience",
            "https://example.com/resume2",
            "Good communication skills, needs more technical practice.",
            7.0,
            0
        ))

    conn.commit()
    conn.close()