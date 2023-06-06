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

    users= [
        User(name="Eli", certified="True"),
        User(name="David", certified="True"),
        User(name="Cody", certified="True")
    ]

    spots = [
        Spot(name="Pristine Peak", type="Surf", city="Ormond Beach", state="FL"),
        Spot(name="The Bowl", type="Skate", city="Ormond Beach", state="FL"),
        Spot(name="Lynch Family Skatepark", type="Skate", city="Boston", state="MA")
    ]

    reviews = [
        Review(spot_name=spots[0].name, author=users[1].name, review=10),
        Review(spot_name=spots[1].name, author=users[2].name, review=10),
        Review(spot_name=spots[2].name, author=users[0].name, review=10)
    ]

    session.bulk_save_objects(users)
    session.bulk_save_objects(spots)
    session.bulk_save_objects(reviews)
    session.commit()
