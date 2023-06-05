from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///certified_shredders.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(User).delete()
    session.query(Spot).delete()
    session.query(Review).delete()

    user1 = User(name="Eli", certified="True", reviews=0)
    user2 = User(name="David", certified="True", reviews=0)

    spot1 = Spot(name="Pristine Peak", type="Surf", city="Ormond Beach", state="FL")
    spot2 = Spot(name="The Bowl", type="Skate", city="Ormond Beach", state="FL")

    review1 = Review(spot_name=spot1.name, author=user1.name, review=10)
    review2 = Review(spot_name=spot2.name, author=user2.name, review=10)

    session.add_all([user1, user2])
    session.add_all([spot1, spot2])
    session.add_all([review1, review2])
    session.commit()
  