from flask import Flask
from models import db
from feedback import feedback_blueprint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)  # Ensure Bootstrap is applied to the app
db.init_app(app)

app.register_blueprint(feedback_bp, url_prefix='/feedback')

@app.route("/")
def home():
    return render_template("index.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
