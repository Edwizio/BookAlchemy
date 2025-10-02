from flask import Flask, request, render_template, redirect, url_for, flash
from sqlalchemy import or_
from data_models import db, Author, Book
from datetime import datetime

import os
app = Flask(__name__)
app.secret_key = "supersecretkey" # to display flash messages

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
def home():
    sort_by = request.args.get("sort")  # Reading the sort parameter from HTML file

    query = Book.query.join(Author)

    # Search functionality
    search_term = request.args.get("q")
    if search_term:
        books = query.filter(
            or_(
                Book.book_title.ilike(f"%{search_term}%"),
                Author.author_name.ilike(f"%{search_term}%")
            )
        )

    # Query to get all books from the database based on sort or not options

    elif sort_by == "title":
        books = Book.query.order_by(Book.book_title).all()
    elif sort_by == "author":
        books = Book.query.join(Author).order_by(Author.author_name).all()
    else:
        books = Book.query.all()



    # Attach cover URLs
    books_with_covers = []
    for book in books:
        books_with_covers.append({
            "id": book.book_id,
            "title": book.book_title,
            "isbn": book.isbn,
            "year": book.publication_year,
            "author_name": book.author.author_name,
            "cover_url": get_cover_url(book.isbn),
        })

    return render_template('home.html', books=books_with_covers)

@app.route('/book/<int:book_id>/delete', methods = ['POST', 'DELETE'])
def delete_book(book_id):
    """This function deletes a particular book based on it's ID and if the author doesn't
    have any other book, delete the author too from the author table"""

    book = Book.query.get(book_id)

    if not book:
        flash("Book does not exist in the database.", "error")
        return redirect(url_for("home"))
    else:
        # Getting the author before deleting the book
        author = book.author

        # Deleting the book
        db.session.delete(book)
        db.session.commit()

        # Checking whether the author still has any books,if not then deleting the author too.
        if not author.books:
            db.session.delete(author)
            db.session.commit()
            flash(f"Book and its author '{author.author_name}' deleted successfully.", "success")
        else:
            flash("Book deleted successfully.", "success")
        return redirect(url_for("home"))


# Creating the tables with SQLAlchemy, only needed to run once, then can be commented out
"""with app.app_context():
  db.create_all()"""

if __name__ == "__main__":
    app.run(debug=True)