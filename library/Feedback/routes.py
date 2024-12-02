from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from extensions import db
from .models import FeedbackComment
from sqlalchemy.sql import func


# Initialize the Blueprint
feedback_bp = Blueprint('feedback', __name__, template_folder='../templates')

# ------------------- Existing Comment Routes -------------------
#GUI Query1 Add a new feedback comment
@feedback_bp.route("/add", methods=["GET", "POST"])
def add_comment():
    if request.method == "POST":
        type = request.form.get("type")
        name = request.form.get("name")

        new_comment = FeedbackComment(
            type=comment_type,
            name=comment_name
        )
        
        db.session.add(new_comment)
        db.session.commit()

        # Flash a success message and redirect to the comment list page
        flash("Feedback comment added successfully!", "success")
        return redirect(url_for("feedback.view_comment"))

    return render_template("add_comment.html")

#GUI Query 2 view all feedback comments
@feedback_blueprint.route('/view_data', methods=['GET'])
def view_data():
    feedback_data = Feedback.query.all()
    feedback_list = [{"comment_id": f.comment_id, "comment_name": f.comment_name, "date": f.date, "type": f.type, "forename": f.forename, "surname": f.surname} for f in feedback_data]
    return jsonify(feedback_list), 200
#GUI Query 3 filter feedback comments
@app.route('/feedback', methods=['GET'])
def get_feedback():
    feedback_type = request.args.get('type', None)
    if feedback_type:
        comments = Feedback.query.filter_by(type=feedback_type).all()
    else:
        comments = Feedback.query.all()
    return jsonify([comment.to_dict() for comment in comments])

#GUI Query 4 sort feedback comments by date
@app.route('/feedback', methods=['GET'])
def get_feedback():
    sort_order = request.args.get('sort', 'asc')
    if sort_order == 'desc':
        comments = Feedback.query.order_by(Feedback.submission_date.desc()).all()
    else:
        comments = Feedback.query.order_by(Feedback.submission_date.asc()).all()
    return jsonify([comment.to_dict() for comment in comments])


#GUI Query 5 edit a feedback comment
@feedback_bp.route("/edit/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    # Retrieve the feedback comment by ID
    comment = feedback.query.get_or_404(comment_id)

    if request.method == "POST":
        # Update the comment's text and type based on form input
        comment.name = request.form.get("name")
        comment.type = request.form.get("type")
        db.session.commit()
        flash("Feedback comment updated successfully!", "success")
        return redirect(url_for("feedback.view_comments"))

    # Render the edit form, passing the current comment data
    return render_template("edit_comment.html", comment=comment)


#GUI QUERY 6 delete a feedback comment
@app.route('/feedback/<int:comment_id>', methods=['DELETE'])
def delete_feedback(comment_id):
    comment = feedback.query.get(comment_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('view_comment.html'))

#GUI Query 7 count feedback comments by type
@app.route('/feedback/count', methods=['GET'])
def count_feedback_by_type():
    results = db.session.query(Feedback.type, db.func.count(Feedback.id)).group_by(Feedback.type).all()
    counts = {type_: count for type_, count in results}
    return jsonify(counts)

# ------------------- New Feedback Comment Routes -------------------

#API Query1 Bulk upload feedback comments 'done'
@feedback_bp.route("/search", methods=["GET"])
def get_comments_by_phrase():
    
    phrase = request.args.get('phrase', '').strip()
    if not phrase:
        return jsonify({"error": "Phrase is required"}), 400
    books = Book.query.filter(Book.title.ilike(f"%{phrase}%")).all()
    return jsonify([{"id": book.id, "title": book.title, "author": book.author, "year": book.year} for book in books]), 200

#API Query2 Retreieve comments containing a specific phrase'done'
@feedback_blueprint.route('/search_comments', methods=['GET'])
def search_comments():
    phrase = request.args.get('phrase', 'project').strip()
    if not phrase:
        return jsonify({"error": "Please provide a phrase to search for."}), 400
    matching_comments = Feedback.query.filter(Feedback.comment.ilike(f"%{phrase}%")).all()
    results = [
        {
            "id": comment.id,
            "category": category,
            "comment": comment_name,
            "type": feedback.type,
            "date_created": feedback.date
            }
            for feedback in matching_comments
            ]
    return jsonify(results), 200


#API Query3 retrieve comments by length
@books_bp.route("/length", methods=["GET"])
def get_books_by_author_length():
    """Retrieve books where the author's name meets a minimum length."""
    min_length = request.args.get('min_length', type=int)
    if min_length is None:
        return jsonify({"error": "min_length is required"}), 400
    books = Book.query.filter(func.length(Book.author) >= min_length).all()
    return jsonify([{"id": book.id, "title": book.title, "author": book.author, "year": book.year} for book in books]), 200


#API Query4 Update multiple comments at once
@books_bp.route("/update", methods=["PUT", "PATCH"])
def update_multiple_books():
    """Batch update book information."""
    data = request.get_json()
    ids = data.get('ids', [])
    new_year = data.get('year')

    if not ids or not new_year:
        return jsonify({"error": "ids and year are required"}), 400

    books = Book.query.filter(Book.id.in_(ids)).all()
    for book in books:
        book.year = new_year
    db.session.commit()

    return jsonify({"message": f"{len(books)} books updated"}), 200


#API Query5 delete all comments of a certain type
@books_bp.route("/delete_by_author", methods=["DELETE"])
def delete_books_by_author():
    """Delete all books by a specific author."""
    author_name = request.args.get('author')
    if not author_name:
        return jsonify({"error": "author is required"}), 400

    deleted_count = Book.query.filter_by(author=author_name).delete()
    db.session.commit()

    return jsonify({"message": f"{deleted_count} books deleted"}), 200
#API Query6 get summary statistics 'done'
@feedback_blueprint.route('/summary_statistics', methods=['GET'])
def summary_statistics():
    avg_length = db.session.query(func.avg(func.length(Feedback.comment))).scalar()
    comment_types = db.session.query(Feedback.type).all()
    type_counter = Counter([t[0] for t in comment_types if t[0]]) 
    most_common_type = type_counter.most_common(1)[0][0] if type_counter else None
    comments_per_day = db.session.query(func.date(Feedback.date_created), func.count(Feedback.id)
                                        ).group_by(func.date(Feedback.date_created)).all()
    comments_per_day = [{"date": str(day[0]), "count": day[1]} for day in comments_per_day]
    summary = {
        "average_comment_length": avg_length,
        "most_common_comment_type": most_common_type,
        "comments_per_day": comments_per_day
        }
    return jsonify(summary), 200

#API Query7 archive old feedback comments