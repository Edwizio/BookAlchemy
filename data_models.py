from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Defining class Author that inherits from db.Model
class Author(db.Model):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(String)
    date_of_death = Column(String)

    def __repr__(self):
        return f"Author(id = {self.id}, name = {self.name})"

    def __str__(self):
        return f"The id {self.id} represents the author {self.name}"

