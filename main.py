from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request
from sqlalchemy import desc
from sqlalchemy import asc


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://urici3i0icy8cuufham5:FrtbL6FqnCsROZMWocDBkgoOeoZC7R@b81s1xhecmfxnpmteb27-postgresql.services.clever-cloud.com:50013/b81s1xhecmfxnpmteb27"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Author(db.Model):
        __tablename__ = "authors"

        author_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(), nullable=False)
        bio = db.Column(db.Text)

class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13))
    publication_year = db.Column(db.Integer())
    copies = db.Column(db.Integer(), default = 1)



@app.route("/books/filter/", methods=["GET"])
def getBooksAndAuth():
    title = request.args.get("title")
    author = request.args.get("name")
    books = []
    authors = []
    if title: # and name
        books = Book.query.filter_by(title=title) or Author.query.filter_by(name=author) # neviem ako vyjadrit podmienku aby bralo aj knihu aj autora
    elif title:
        books = Book.query.filter_by(title=title)
    elif author:
        authors = Author.query.filter_by(name=author)
    else:
        return jsonify({"Zadaj minimalne jeden parameter, title alebo name autora."}), 400

    serialized_books = [
        {"book_id": book.book_id, "title": book.title, "isbn": book.isbn, "publication_year": book.publication_year}
        for book in books
    ]

    serialized_authors = [
        {"author_id": author.author_id, "name": author.name, "bio": author.bio}
        for author in authors
    ]

    return jsonify({"books": serialized_books, "authors": serialized_authors})

@app.route("/books/findbyparameter/", methods=["GET"])
def sortByReq():
    book_id = request.args.get("book_id")
    title = request.args.get("title")
    isbn = request.args.get("isbn")
    book = []

    if book_id:
        book = Book.query.filter_by(book_id=book_id) # or Book.query.filter_by(desc(book_id=book_id))
    elif title:
        book = Book.query.filter_by(title=title)
    elif isbn:
        book = Book.query.filter_by(isbn=isbn)
    else:
        return jsonify({"Zadaj minimalne jeden parameter, title alebo name autora."}), 400

    serialized_books = [
        {"book_id": book.book_id, "title": book.title, "isbn": book.isbn, "publication_year": book.publication_year}
        for book in book
    ]
    return jsonify(serialized_books)

    #autor = Author.query.all()
    #serialized_authors = [{"author_id": author.author_id, "name": author.name, "bio": author.bio} for author in autor]
    #return jsonify(serialized_books)

    #return jsonify(title)
@app.route("/books/findbyparameterAcsDCS", methods = ["GET"])
def zradenieHoreDole():

    book = Book.query.order_by(desc(Book.title))

    serialized_books = [
        {"book_id": book.book_id, "title": book.title, "isbn": book.isbn, "publication_year": book.publication_year}
        for book in book
    ]
    return jsonify(serialized_books)

if __name__ == "__main__":
    app.run(debug=True)