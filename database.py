from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType, PasswordType
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Float, Boolean
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    """ User class - customer """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(EmailType, unique=True, nullable=False)
    password = Column(String(40), nullable=False)
    
    name = Column(String(80), nullable=False)


class Order(db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User")
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    item = relationship("Item")
    seller_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    seller = relationship("User")
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    is_complete = Column(Boolean, default=False)
    in_cart = Column(Boolean, default=True)

class Item(db.Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    img_url = Column(String(250))

class SellerItem(db.Model):
    __tablename__ = 'selleritem'
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship("Item")
    seller_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    seller = relationship("User")
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

def initialize_db():
    db.create_all()

def add_object(obj):
    db.session.add(obj)
    return obj

def save_object(obj):
    add_object(obj)
    db.session.commit()
    return obj