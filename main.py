from flask import Flask, request, render_template, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from random import choices
from string import ascii_letters, digits
from random import choices


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
from models import Url

def generate_short_url(length=6):
    return ''.join(choices(ascii_letters + digits, k=length))

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get url from the form
        original_url = request.form.get("url")
        # Check whether it's already stored in the db
        existing_url = Url.query.filter_by(original_url=original_url).first()

        if existing_url:
            # If it exists, use the existing short URL
            short_url = existing_url.short_url
            return render_template('index.html', short_url=existing_url.short_url)
        else:
            # Create a new URL record
            new_url = Url(
                original_url=original_url,
                short_url=generate_short_url(),
            )
            db.session.add(new_url)
            db.session.commit()
            print(f"Record added: {original_url}:{new_url.short_url}")
            return render_template('index.html', short_url=new_url.short_url)
    return render_template('index.html')

@app.route('/<string:short_url>')
def redirect_to_url(short_url):
    # Query to find shortened
    url_map = Url.query.filter_by(short_url=short_url).first()

    if url_map:
        return redirect(f"https://{url_map.original_url}")
    else:
        return abort(404)

with app.app_context():
    db.create_all()
