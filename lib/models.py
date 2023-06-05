from sqlalchemy import create_engine, desc, func
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///certified_shredders.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), index=True)
    certified = Column(String(), default="False")
    reviews = Column(Integer(), default=0)

    def __repr__(self):
        return f"User ID {self.id}: " \
            + f"{self.name}" \
            + f"Certified: {self.certified}" \
            + f"Reviews: {self.reviews}" 
           
class Spot(Base):
    __tablename__ = 'spots'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), index=True)
    type = Column(String())
    city = Column(String())
    state = Column(String())

    def __repr__(self):
        return f"Spot ID: {self.id}" \
            + f"{self.name}" \
            + f"{self.type}" \
            + f"City: {self.city}" \
            + f"State: {self.state}"

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    spot_name = Column(String(), ForeignKey('spots.name'))
    author = Column(String(), ForeignKey('users.name'))
    review = Column(Integer())

    def __repr__(self):
        return f"Review ID: {self.id}" \
            + f"{self.name}" \
            + f"Review: {self.review}"
