import sqlalchemy
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm.session import sessionmaker

engine = create_engine('sqlite:///books_library.sqlite')

base = declarative_base()


class Books(base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    book = Column(String, nullable=False, unique=True)
    arthur = Column(String, nullable=False)
    rating = Column(Float, nullable=False)

    def __init__(self, id, book, arthur, rating):
        self.id = id
        self.book = book
        self.arthur = arthur
        self.rating = rating


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzfds'
Bootstrap(app)

# Created database
try:
    base.metadata.create_all(engine)
except:
    pass


class AddingForm(FlaskForm):
    book = StringField('Book Name', validators=[DataRequired(), Length(min=2, max=30, message='too many characters in '
                                                                                              'the book name')])
    author = StringField('Book Author', validators=[DataRequired(), Length(min=2, max=30, message= 'too many '
                                                                                                   'characters in the'
                                                                                                   ' book name')])
    rating = FloatField('Book Rating (Out of 10)',
                          validators=[DataRequired(),
                                      NumberRange(min=0, max=10, message='Invalid Rating, Rating should be in (1-10)')])
    submit = SubmitField('Add Book')


class EditForm(FlaskForm):
    edit = FloatField('Edit Rating (Out of 10)',
                        validators=[DataRequired(),
                                    NumberRange(min=0, max=10, message='Invalid Rating, Rating should be in (1-10)')])
    submit = SubmitField('Submit Rating')


@app.route('/')
def home():
    ALL_BOOKS = []

    # ADDING TO ALL BOOKS LIST
    Session = sessionmaker(engine)
    session = Session()
    for b in session.query(Books).all():
        ALL_BOOKS.append(
            {
                "id": b.id,
                "title": b.book,
                "author": b.arthur,
                "rating": b.rating
            }
        )
    return render_template('index.html', books=ALL_BOOKS, lenght=len(ALL_BOOKS))


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    form = EditForm()
    book_name, arutur = None, None
    session = sessionmaker(bind=engine)
    session = session()
    if form.validate_on_submit():
        session.query(Books).filter(Books.id == id).update({Books.rating: form.edit.data}, synchronize_session=False)
        session.commit()
        return redirect(url_for('home'))
    for data in session.query(Books).filter(Books.id == id):
        book_name, arutur = data.book, data.arthur
    return render_template("edit.html", form=form, book=book_name, author=arutur)


@app.route('/delete/<int:num>')
def delete(num):
    print(f"id to delete : {num}")
    session = sessionmaker(engine)
    session = session()
    session.query(Books).filter(Books.id==num).delete()
    session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddingForm()
    if form.validate_on_submit():
        book = form.book.data
        author = form.author.data
        rating = form.rating.data

        Session = sessionmaker(engine)
        new_session = Session()
        try:
            id = [n for n in new_session.query(Books).filter(Books.id)][-1].id
        except IndexError:
            id = 0
        data = Books(id + 1, book, author, rating)

        new_session.add(data)
        new_session.commit()

        return redirect(url_for('home'))
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
