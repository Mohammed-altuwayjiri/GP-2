from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

from analysis import analyze_review
from db import (
    create_review,
    update_review_status,
    get_category_id_by_name,
    save_review_analysis,
    get_user_by_email,
    get_category_summary,
    get_opinion_distribution,
    get_all_analysis_results,
)

# Flask app setup
app = Flask(__name__)
app.secret_key = "change-this-secret-key"


# Session helper
def is_logged_in():
    return "user_id" in session


# Public pages
@app.route("/")
def home():
    return render_template("review.html")


# Review submission flow
@app.route("/reviews", methods=["POST"])
def submit_review():
    text = request.form.get("text", "").strip()
    stars = request.form.get("stars", "").strip()

    if not text:
        flash("Review text is required.", "error")
        return redirect(url_for("home"))

    try:
        stars = int(stars)
        if stars < 1 or stars > 5:
            raise ValueError
    except ValueError:
        flash("Stars must be a number between 1 and 5.", "error")
        return redirect(url_for("home"))

    review_id = create_review(text, stars)
    result = analyze_review(text)

    category_name = result["category"]
    opinion = result["opinion"]

    category_id = get_category_id_by_name(category_name)

    if category_id is None:
        flash("Predicted category was not found in database.", "error")
        return redirect(url_for("home"))

    save_review_analysis(review_id, category_id, opinion)
    update_review_status(review_id, "processed")

    flash("Review submitted and analyzed successfully.", "success")
    return redirect(url_for("home"))


# Login flow
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    if not email or not password:
        flash("Email and password are required.", "error")
        return redirect(url_for("login"))

    user = get_user_by_email(email)

    if user is None or not check_password_hash(user["password_hash"], password):
        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    session["user_id"] = user["id"]
    session["user_email"] = user["email"]
    session["user_type"] = user["user_type"]

    flash("Login successful.", "success")
    return redirect(url_for("dashboard"))


# Protected dashboard
@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        flash("Please log in first.", "error")
        return redirect(url_for("login"))

    category_summary = get_category_summary()
    opinion_distribution = get_opinion_distribution()
    results = get_all_analysis_results()

    return render_template(
        "dashboard.html",
        category_summary=category_summary,
        opinion_distribution=opinion_distribution,
        results=results,
        user_email=session.get("user_email"),
        user_type=session.get("user_type"),
    )


# Logout flow
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))


# Run development server
if __name__ == "__main__":
    app.run(debug=True)