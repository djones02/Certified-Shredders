from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///certified_shredders.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query('User').delete()
    session.query('Spot').delete()
    session.query('Review').delete()

    user1 = User(name="Eli")
    user2 = User(name="David")

    users = []
    
    session.add(user1, user2)
    session.commit()
    users.append(user1, user2)
  