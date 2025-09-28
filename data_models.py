
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Defining class Author that inherits from db.Model
class Author(db.Model):
    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_name = db.Column(db.String)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)

    def __repr__(self):
        return f"Author(id = {self.author_id}, name = {self.author_name})"

    def __str__(self):
        return f"The id {self.author_id} represents the author {self.author_name}"

# Defining class Books
class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String)
    book_title = db.Column(db.String)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.author_id"))

    def __repr__(self):
        return f"Book(id = {self.book_id}, title = {self.book_title})"

    def __str__(self):
        return f"The book {self.book_id} is written by {self.author_id}"

