import sqlite3
from pathlib import Path

# Database path
base_dir = Path(__file__).parent
db_path = base_dir / "database" / "opinion_ai.db"


# Database connection helper
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# Review operations
def create_review(text, stars, status="queued"):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reviews (text, stars, status)
        VALUES (?, ?, ?)
        """,
        (text, stars, status)
    )

    review_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return review_id


def update_review_status(review_id, new_status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE reviews
        SET status = ?
        WHERE id = ?
        """,
        (new_status, review_id)
    )

    conn.commit()
    conn.close()


# Category lookup
def get_category_id_by_name(category_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM categories
        WHERE name = ?
        """,
        (category_name,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return row["id"]


# Analysis result storage
def save_review_analysis(review_id, category_id, opinion):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO review_analysis (review_id, category_id, opinion)
        VALUES (?, ?, ?)
        """,
        (review_id, category_id, opinion)
    )

    conn.commit()
    conn.close()


# User lookup
def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    return user


# Dashboard summaries
def get_category_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.name AS category_name, COUNT(*) AS total
        FROM review_analysis ra
        JOIN categories c ON ra.category_id = c.id
        GROUP BY c.name
        ORDER BY total DESC
        """
    )

    results = cursor.fetchall()
    conn.close()

    return results


def get_opinion_distribution():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT opinion, COUNT(*) AS total
        FROM review_analysis
        GROUP BY opinion
        ORDER BY total DESC
        """
    )

    results = cursor.fetchall()
    conn.close()

    return results


def get_all_analysis_results():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            r.id AS review_id,
            r.text,
            r.stars,
            r.status,
            r.created_at,
            c.name AS category_name,
            ra.opinion,
            ra.analyzed_at
        FROM reviews r
        JOIN review_analysis ra ON r.id = ra.review_id
        JOIN categories c ON ra.category_id = c.id
        ORDER BY r.created_at DESC
        """
    )

    results = cursor.fetchall()
    conn.close()

    return results