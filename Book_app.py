from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"

@app.route('/')
def index():
    return 'Hello!'

@app.route('/book')
def get_book():
    books = Book.query.all()  # Get all books from the database

    output = []
    for book in books:
        book_data = {
            'book_name': book.book_name,
            'author': book.author,
            'publisher': book.publisher
        }
        output.append(book_data)
    
    return jsonify({"book": output})

@app.route('/book/<int:id>')
def get_book_(id):
    book = Book.query.get_or_404(id)  # Fetch the book by ID
    return jsonify({'book_name': book.book_name,
                    'author': book.author,
                    'publisher': book.publisher})

@app.route('/book', methods=['POST'])
def add_book():
    book = Book(
        book_name=request.json['book_name'],
        author=request.json['author'],
        publisher=request.json['publisher']
    )
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/drinks/<id>',methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return{"error:not found"}
    db.session.delete(book)
    db.session.commit()
    return{"message received"}



if __name__ == "__main__":
    app.run(debug=True)