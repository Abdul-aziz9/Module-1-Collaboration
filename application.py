from flask import Flask, request


app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"
    

with app.app_context():
    db.create_all()
    book2 = Book(book_name="P4E", author="Freecodecamp", publisher="Dr. Chuck")
    book = Book(book_name="MieneKraft", author="Hitler", publisher="germany")
    book1 = Book(book_name="Introducing Python - Oreilly", author="Lubanovic", publisher="O'Reilly")
    #db.session.add(book)
    #db.session.add(book1)
    #db.session.add(book2)
    db.session.commit()
    print(Book.query.all())

@app.route('/')
def index():
    return "Hello!"

@app.route('/book')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {"Name": book.book_name, "Author": book.author, "Publisher": book.publisher}
        output.append(book_data)
    
    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"Name":book.book_name, "Author": book.author, "Publisher": book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json["book_name"],
                author=request.json["author"], 
                publisher=request.json["publisher"])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return {'message': "Deleted"}

