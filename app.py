from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)

def validate_author_data(data):
    """This helper function checks for the validity of data by making sure
        it has the required attributes"""
    if "name" not in data or "birthdate" not in data:
        return False
    return True


@app.route('/add_author', methods=['GET', 'POST'])
def add_authors():
    """This method adds authors to the database by rendering an HTML page connected through Flask app"""
    if request.method == "POST":
        new_author = request.get_json()

        if not validate_author_data(new_author):
            return "Invalid author data", 400

        # Creating an author object from the new_author dictionary
        author = Author(
            author_name = new_author["name"],
            birth_date = new_author["birthdate"],
            date_of_death = new_author.get("date_of_death")  # optional parameter so have to use .get to avoid key error
        )

        # Adding and commiting to the database session
        db.session.add(author)
        db.session.commit()

        return "Author added successfully!", 201

    return render_template('add_author.html')

# Creating the tables with SQLAlchemy, only needed to run once, then can be commented out
"""with app.app_context():
  db.create_all()"""
