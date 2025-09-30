from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import datetime

import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_authors():
    """This method adds authors to the database by rendering an HTML page connected through Flask app"""
    if request.method == "POST":
        author_name = request.form.get("name")
        birth_date_str = request.form.get("birthdate")
        date_of_death_str = request.form.get("date_of_death")  # optional

        # checking for validation
        if not author_name or not birth_date_str:
            return render_template("add_author.html", message="Invalid author data. Name and birthdate required.")

        # Convert string to date object
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()

        # As date_of_death is optional so need to take care of case when user don't enter it
        if date_of_death_str:
            date_of_death = datetime.strptime(date_of_death_str, "%Y-%m-%d").date()
        else:
            date_of_death = None

        # Creating an author object from the new_author dictionary
        author = Author(
            author_name=author_name,
            birth_date=birth_date,
            date_of_death= date_of_death
        )

        # Adding and commiting to the database session
        db.session.add(author)
        db.session.commit()

        return render_template("add_author.html", message="Author added successfully!")

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_books():
    """This method adds books to the database by rendering an HTML page connected through Flask app"""
    if request.method == "POST":
        title = request.form.get("title")
        isbn = request.form.get("isbn")

        # Handling errors, if the optional parameters not provided
        publication_year = request.form.get("publication_year")
        if not publication_year:
           publication_year = None
        author_name = request.form.get("author_name")
        if not author_name:
            author_name = None

        # Checking for validation
        if not title or not isbn:
            return render_template("add_book.html", message="Invalid book data. Title and isbn required.")

        # Linking the author's name with author_id to enter foreign key in the book table
        author = Author.query.filter_by(author_name=author_name).first()

        if not author:
            return f"Author '{author_name}' not found. Please add the author first.", 400

        # Creating a book object from the new_book dictionary
        book = Book(
            book_title = title,
            isbn = isbn,
            publication_year = publication_year,
            author_id = author.author_id
        )

        # Adding and commiting to the database session
        db.session.add(book)
        db.session.commit()

        return render_template("add_book.html", message="Book added successfully!")

    return render_template('add_book.html')


def get_cover_url(isbn, size="M"):
    """
    This functions returns the cover image URL from Open Library for a given ISBN.
    size can be: S, M, L (small, medium, large) but we have set the default value to be M.
    """
    if not isbn:
        return None
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-{size}.jpg"

@app.route('/home')
def display_home_page():

    #Query to get all books from the database
    books = Book.query.all()

    # Attach cover URLs
    books_with_covers = []
    for book in books:
        books_with_covers.append({
            "title": book.book_title,
            "isbn": book.isbn,
            "cover_url": get_cover_url(book.isbn)
        })

    return render_template('home.html', books=books)


# Creating the tables with SQLAlchemy, only needed to run once, then can be commented out
"""with app.app_context():
  db.create_all()"""

if __name__ == "__main__":
    app.run(debug=True)