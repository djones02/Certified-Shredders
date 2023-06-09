from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

engine = create_engine('sqlite:///certified_shredders.db')
Session = sessionmaker(bind=engine)
session = Session()

session.query(User).delete()
session.query(Spot).delete()
session.query(Review).delete()

users= [
    User(name="Eli"),
    User(name="David"),
    User(name="Cody"),
    User(name="Josh"),
    User(name="Greem"),
    User(name="Kwame"),
    User(name="Evan"),
    User(name="Michael"),
    User(name="Matt")
]

spots = [
    Spot(name="Zelie Skate Park", type="Skate", city="Zelienople", state="PA"),
    Spot(name="Reggie Wong Park", type="Skate", city="Boston", state="MA"),
    Spot(name="Lynch Family Skatepark", type="Skate", city="Boston", state="MA"),
    Spot(name="Love Park", type="Skate", city="Philadelphia", state="PA"),
    Spot(name="LA Courthouse", type="Skate", city="Los Angeles", state="CA"),
    Spot(name="Ocean City Beach", type="Surf", city="Ocean City", state="NJ"),
    Spot(name="Narragansett Beach", type="Surf", city="Narragansett", state="RI"),
    Spot(name="North Shore", type="Surf", city="Kauai", state="HI"),
    Spot(name="Venice Beach", type="Surf", city="Venice", state="FL"),
    Spot(name="Wrightsville Beach", type="Surf", city="Wrightsville Beach", state="NC")
]

reviews = [
    Review(spot_name=spots[0].name, author=users[0].name, review=5),
    Review(spot_name=spots[1].name, author=users[0].name, review=10),
    Review(spot_name=spots[2].name, author=users[0].name, review=8),
    Review(spot_name=spots[3].name, author=users[0].name, review=5),
    Review(spot_name=spots[4].name, author=users[0].name, review=9),
    Review(spot_name=spots[0].name, author=users[1].name, review=2),
    Review(spot_name=spots[1].name, author=users[1].name, review=10),
    Review(spot_name=spots[2].name, author=users[1].name, review=4),
    Review(spot_name=spots[3].name, author=users[1].name, review=6),
    Review(spot_name=spots[6].name, author=users[1].name, review=2),
    Review(spot_name=spots[8].name, author=users[5].name, review=10),
    Review(spot_name=spots[4].name, author=users[4].name, review=1)
]

session.bulk_save_objects(users)
session.bulk_save_objects(spots)
session.bulk_save_objects(reviews)
session.commit()
