from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from library.extensions import db
from .models import Feedback, Archive
from sqlalchemy.sql import func
from collections import Counter

# Initialize the Blueprint
feedback_bp = Blueprint('feedback', __name__, template_folder='../templates')

# ------------------- Existing Comment Routes -------------------
# GUI Query1 Add a new feedback comment
@feedback_bp.route("/add", methods=["GET", "POST"])
def add_comment():
    if request.method == "POST":
        comment_type = request.form.get("type")
        text = request.form.get("text")
        date = request.form.get("date")
        forename = request.form.get("forename")
        surname = request.form.get("surname")
        category = request.form.get("category")

        formatted_date = datetime.strptime(date, "%Y-%m-%d").date()

        new_comment = Feedback(
            type=comment_type,
            text=text,
            category=category,
            date=formatted_date,
            forename=forename,
            surname=surname,
        )

        db.session.add(new_comment)
        db.session.commit()

        # Flash a success message and redirect to the comment list page
        flash("Feedback comment added successfully!", "success")

        return redirect(url_for("feedback.view_comment"))

    return render_template("add_comment.html")

# GUI Query 2 view all feedback comments
@feedback_bp.route('/view_comment', methods=['GET'])
def view_comment():
    comment_type = request.args.get('Comment Type', None)
    sort_order = request.args.get('sort', 'asc')

    query = Feedback.query
    if comment_type:
        query = query.filter_by(type=comment_type)

    if sort_order == 'desc':
        feedback_data = query.order_by(Feedback.date.desc()).all()
    else:
        feedback_data = query.order_by(Feedback.date.asc()).all()

    comments = [{"id": f.id, "category": f.category, "text": f.text, "date": f.date, "type": f.type, "forename": f.forename, "surname": f.surname} for f in feedback_data]
    return render_template("view_comment.html", comments=comments, sort_order=sort_order, comment_type=comment_type)

# GUI Query 3 filter feedback comments
@feedback_bp.route('/feedback/filter', methods=['GET'])
def get_feedback():
    feedback_type = request.args.get('type', None)
    if feedback_type:
        comments = Feedback.query.filter_by(type=feedback_type).all()
    else:
        comments = Feedback.query.all()
    return jsonify([comment.to_dict() for comment in comments])

# GUI Query 4 sort feedback comments by date
@feedback_bp.route('/feedback/sort', methods=['GET'])
def get_feedback_sorted():
    sort_order = request.args.get('sort', 'asc')
    if sort_order == 'desc':
        comments = Feedback.query.order_by(Feedback.date.desc()).all()
    else:
        comments = Feedback.query.order_by(Feedback.date.asc()).all()
    return jsonify([comment.to_dict() for comment in comments])

# GUI Query 5 edit a feedback comment
@feedback_bp.route("/edit/<string:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    # Retrieve the feedback comment by ID
    comment = Feedback.query.get_or_404(comment_id)

    if request.method == "POST":
        # Update the comment's text and type based on form input
        comment.text = request.form.get("text")
        comment.type = request.form.get("type")
        db.session.commit()
        flash("Feedback comment updated successfully!", "success")
        return redirect(url_for("feedback.view_comment"))

    # Render the edit form, passing the current comment data
    return render_template("edit_comment.html", comment=comment)

# GUI QUERY 6 delete a feedback comment
@feedback_bp.route('/delete/<string:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Feedback.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash("Feedback comment deleted successfully!", "success")
    return redirect(url_for('feedback.view_comment'))

# GUI Query 7 count feedback comments by type
@feedback_bp.route('/feedback/count', methods=['GET'])
def count_feedback_by_type():
    results = db.session.query(Feedback.type, db.func.count(Feedback.id)).group_by(Feedback.type).all()
    counts = {type_: count for type_, count in results}
    return jsonify(counts)

# ------------------- New Feedback Comment Routes -------------------

# API Query1 Bulk upload feedback comments
@feedback_bp.route("/search", methods=["GET"])
def get_comments_by_phrase():
    phrase = request.args.get('phrase', '').strip()
    if not phrase:
        return jsonify({"error": "Phrase is required"}), 400
    comments = Feedback.query.filter(Feedback.title.ilike(f"%{phrase}%")).all()
    return jsonify([{"id": comment.id, "title": comment.title, "author": comment.author, "year": comment.year} for comment in comments]), 200

# API Query2 Retrieve comments containing a specific phrase
@feedback_bp.route('/search_comments', methods=['GET'])
def search_comments():
    phrase = request.args.get('phrase', 'project').strip()
    if not phrase:
        return jsonify({"error": "Please provide a phrase to search for."}), 400
    matching_comments = Feedback.query.filter(Feedback.text.ilike(f"%{phrase}%")).all()
    results = [
        {
            "id": comment.id,
            "category": comment.category,
            "text": comment.text,
            "type": comment.type,
            "date": comment.date
        }
        for comment in matching_comments
    ]
    return jsonify(results), 200

# API Query3 retrieve comments by length
@feedback_bp.route("/length", methods=["GET"])
def get_comments_by_length():
    """Retrieve comments where the text meets a minimum length."""
    min_length = request.args.get('min_length', type=int)
    if min_length is None:
        return jsonify({"error": "min_length is required"}), 400
    comments = Feedback.query.filter(func.length(Feedback.text) >= min_length).all()
    return jsonify([{"id": comment.id, "title": comment.title, "author": comment.author, "year": comment.year} for comment in comments]), 200

# API Query4 Update multiple comments at once
@feedback_bp.route("/update", methods=["PUT", "PATCH"])
def update_multiple_comments():
    data = request.get_json()
    ids = data.get('ids', [])
    new_year = data.get('year')

    if not ids or not new_year:
        return jsonify({"error": "ids and year are required"}), 400

    comments = Feedback.query.filter(Feedback.id.in_(ids)).all()
    for comment in comments:
        comment.year = new_year
    db.session.commit()

    return jsonify({"message": f"{len(comments)} comments updated"}), 200

# API Query5 delete all comments of a certain type
@feedback_bp.route("/delete_by_author", methods=["DELETE"])
def delete_comments_by_author():
    author_name = request.args.get('author')
    if not author_name:
        return jsonify({"error": "author is required"}), 400

    deleted_count = Feedback.query.filter_by(author=author_name).delete()
    db.session.commit()

    return jsonify({"message": f"{deleted_count} comments deleted"}), 200

# API Query6 get summary statistics 'done'
@feedback_bp.route('/summary_statistics', methods=['GET'])
def summary_statistics():
    avg_length = db.session.query(func.avg(func.length(Feedback.text))).scalar()
    comment_types = db.session.query(Feedback.type).all()
    type_counter = Counter([t[0] for t in comment_types if t[0]])
    most_common_type = type_counter.most_common(1)[0][0] if type_counter else None
    comments_per_day = db.session.query(func.date(Feedback.date), func.count(Feedback.id)
                                        ).group_by(func.date(Feedback.date)).all()
    comments_per_day = [{"date": str(day[0]), "count": day[1]} for day in comments_per_day]
    summary = {
        "average_comment_length": avg_length,
        "most_common_comment_type": most_common_type,
        "comments_per_day": comments_per_day
    }
    return jsonify(summary), 200

# API Query7 Archive old feedback comments
@feedback_bp.route("/archive", methods=["POST", "PUT"])
def archive_old_comments():
    data = request.get_json()
    archive_date = data.get('date')

    if not archive_date:
        return jsonify({"error": "date is required"}), 400

    try:
        archive_date = datetime.strptime(archive_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    old_comments = Feedback.query.filter(Feedback.date < archive_date).all()
    archived_count = 0

    for comment in old_comments:
        # Assuming you have an Archive model and db table to store archived comments
        archived_comment = Archive(
            type=comment.type,
            text=comment.text,
            category=comment.category,
            date=comment.date,
            forename=comment.forename,
            surname=comment.surname,
        )
        db.session.add(archived_comment)
        db.session.delete(comment)
        archived_count += 1

    db.session.commit()

    return jsonify({"message": f"{archived_count} comments archived"}), 200