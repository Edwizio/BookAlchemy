from flask_sqlalchemy import SQLAlchemy, Column, Integer, String
from sqlalchemy import ForeignKey
from app import app
db = SQLAlchemy()

# Defining class Author that inherits from db.Model
class Author(db.Model):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String)
    birth_date = Column(String)
    date_of_death = Column(String)

    def __repr__(self):
        return f"Author(id = {self.author_id}, name = {self.author_name})"

    def __str__(self):
        return f"The id {self.author_id} represents the author {self.author_name}"

# Defining class Books
class Book(db.Model):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String)
    book_title = Column(String)
    publication_year = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))

    def __repr__(self):
        return f"Book(id = {self.book_id}, title = {self.book_title})"

    def __str__(self):
        return f"The book {self.book_id} is written by {self.author_id}"

# Creating the tables with SQLAlchemy, only needed to run once, then can be commented out
with app.app_context():
  db.create_all()
