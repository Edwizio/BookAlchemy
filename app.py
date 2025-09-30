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

        return render_template("add_author.html", message="Author added successfully!")

    return render_template('add_author.html')


def validate_book_data(data):
    """This helper function checks for the validity of data by making sure
        it has the required attributes"""
    if "title" not in data or "isbn" not in data:
        return False
    return True


@app.route('/add_book', methods=['GET', 'POST'])
def add_books():
    """This method adds books to the database by rendering an HTML page connected through Flask app"""
    if request.method == "POST":
        new_book = request.get_json()

        if not validate_book_data(new_book):
            return "Invalid book data", 400

        # Linking the author's name with author_id to enter foreign key in the book table
        author_name = new_book.get("author_name")
        author = Author.query.filter_by(author_name=author_name).first()

        if not author:
            return f"Author '{author_name}' not found. Please add the author first.", 400

        # Creating a book object from the new_book dictionary
        book = Book(
            book_title = new_book["title"],
            isbn = new_book["isbn"],
            publication_year = new_book.get("publication_year"),  # optional parameter so have to use .get to avoid key error
            author_id = author.author_id
        )

        # Adding and commiting to the database session
        db.session.add(book)
        db.session.commit()

        return render_template("add_book.html", message="Book added successfully!")

    return render_template('add_book.html')

@app.route('/')
def display_home_page():

    #Query to get all books from the database
    books = Book.query.all()

    # Pass books to the template
    return render_template('home.html', books=books)


# Creating the tables with SQLAlchemy, only needed to run once, then can be commented out
"""with app.app_context():
  db.create_all()"""
