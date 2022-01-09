from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///test_data.sqlite", echo=True)

base = declarative_base()

# creating database
class Books(base):

    __tablename__ = 'books library'
    id = Column(Integer, primary_key=True)
    book_name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    def __init__(self, id, book_name, rating):
        self.id = id
        self.book_name = book_name
        self.rating = rating


# base.metadata.create_all(engine)

# new session
Session = sessionmaker(bind=engine)
session = Session()


# adding data

# for n in range(0, 11):
#     tr = Books(n, "Harry", "frank")
#     session.add(tr)
#
# session.commit()

# query the data
#
Session = sessionmaker(bind=engine)
new_session = Session()

for data in new_session.query(Books).all():
    print(data.id, data.rating)

id = [n for n in new_session.query(Books).all()][-1].id
print(id, type(id))

# update_data
# Session = sessionmaker(bind=engine)
# n_session = Session()
#
# n_session.query(Books).filter(Books.id == 5).update({Books.rating: 4}, synchronize_session=False)
# n_session.query(Books).filter(Books.id == 6).update({Books.rating: 4}, synchronize_session='evaluate')
# n_session.query(Books).filter(Books.id == 7).update({Books.rating: 4}, synchronize_session='fetch')
# n_session.query(Books).filter(Books.id == 9).delete()
#
# n_session.commit()

# delete data