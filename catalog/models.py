from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))
    categories = relationship('Category', cascade='all, delete-orphan', backref = 'user')
    items = relationship('Items', cascade='all, delete-orphan', backref = 'user')

class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('categories', cascade='all, delete'))
    items = relationship('Items', cascade='all, delete-orphan', backref = 'category')
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }
 
class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False, unique = True)
    description = Column(String(1000))
    price = Column(String(8))
    image = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', backref=backref('category', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('items', cascade='all, delete'))


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'  : self.description,
           'id'           : self.id,
           'user_id': self.user_id,
           'category_id': self.category_id,           
           'price'        : self.price,
           'image'        : self.image,
       }

