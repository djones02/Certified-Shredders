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
    User(name="Greem"),
    User(name="Kwame"),
    User(name="Evan"),
    User(name="Michael"),
    User(name="Matt")
]

spots = [
    Spot(name="Pipeline", type="Surf", city="Oahu", state="HI"),
    Spot(name="Burnside Skatepark", type="Skate", city="Portland", state="OR"),
    Spot(name="The Wedge", type="Surf", city="Newport Beach", state="CA"),
    Spot(name="Kona Skatepark", type="Skate", city="Jacksonville", state="FL"),
    Spot(name="Trestles", type="Surf", city="San Clemente", state="CA"),
    Spot(name="Stoner Skate Plaza", type="Skate", city="Los Angeles", state="CA"),
    Spot(name="Rockaway Beach", type="Surf", city="Queens", state="NY"),
    Spot(name="Bamboo Skatepark", type="Skate", city="Oklahoma City", state="OK"),
    Spot(name="Ocean Beach", type="Surf", city="San Diego", state="CA"),
    Spot(name="Venice Skatepark", type="Skate", city="Venice", state="CA"),
    Spot(name="Zelie Skate Park", type="Skate", city="Zelienople", state="PA"),
    Spot(name="Reggie Wong Park", type="Skate", city="Boston", state="MA"),
    Spot(name="Lynch Family Skatepark", type="Skate", city="Boston", state="MA"),
    Spot(name="Love Park", type="Skate", city="Philadelphia", state="PA"),
    Spot(name="LA Courthouse", type="Skate", city="Los Angeles", state="CA"),
    Spot(name="Ocean City Beach", type="Surf", city="Ocean City", state="NJ"),
    Spot(name="Narragansett Beach", type="Surf", city="Narragansett", state="RI"),
    Spot(name="North Shore", type="Surf", city="Kauai", state="HI"),
    Spot(name="Venice Beach", type="Surf", city="Venice", state="CA"),
    Spot(name="Wrightsville Beach", type="Surf", city="Wrightsville Beach", state="NC"),
    Spot(name="Brooklyn Banks", type="Skate", city="New York", state="NY"),
    Spot(name="Huntington Beach", type="Surf", city="Huntington Beach", state="CA"),
    Spot(name="Louisville Skate Park", type="Skate", city="Louisville", state="KY"),
    Spot(name="Malibu Surfrider Beach", type="Surf", city="Malibu", state="CA"),
    Spot(name="FDR Skatepark", type="Skate", city="Philadelphia", state="PA"),
    Spot(name="The Lane", type="Surf", city="Santa Cruz", state="CA"),
    Spot(name="Burnett Memorial Park", type="Skate", city="Renton", state="WA"),
    Spot(name="Cocoa Beach", type="Surf", city="Cocoa Beach", state="FL"),
    Spot(name="Lake Cunningham", type="Skate", city="San Jose", state="CA"),
    Spot(name="Jaws", type="Surf", city="Maui", state="HI")
]

reviews = [
    Review(spot_name=spots[0].name, author=users[0].name, review=5),
    Review(spot_name=spots[1].name, author=users[0].name, review=10),
    Review(spot_name=spots[2].name, author=users[0].name, review=8),
    Review(spot_name=spots[3].name, author=users[0].name, review=5),
    Review(spot_name=spots[4].name, author=users[0].name, review=9),
    Review(spot_name=spots[20].name, author=users[0].name, review=9),
    Review(spot_name=spots[11].name, author=users[0].name, review=8),
    Review(spot_name=spots[18].name, author=users[0].name, review=6),
    Review(spot_name=spots[26].name, author=users[0].name, review=10),
    Review(spot_name=spots[0].name, author=users[1].name, review=2),
    Review(spot_name=spots[1].name, author=users[1].name, review=10),
    Review(spot_name=spots[2].name, author=users[1].name, review=4),
    Review(spot_name=spots[3].name, author=users[1].name, review=6),
    Review(spot_name=spots[6].name, author=users[1].name, review=2),
    Review(spot_name=spots[6].name, author=users[1].name, review=2),
    Review(spot_name=spots[9].name, author=users[1].name, review=7),
    Review(spot_name=spots[5].name, author=users[1].name, review=6),
    Review(spot_name=spots[13].name, author=users[1].name, review=9),
    Review(spot_name=spots[8].name, author=users[5].name, review=10),
    Review(spot_name=spots[4].name, author=users[4].name, review=1),
    Review(spot_name=spots[8].name, author=users[5].name, review=10),
    Review(spot_name=spots[4].name, author=users[4].name, review=1),
    Review(spot_name=spots[17].name, author=users[6].name, review=9),
    Review(spot_name=spots[12].name, author=users[5].name, review=8),
    Review(spot_name=spots[4].name, author=users[3].name, review=6),
    Review(spot_name=spots[8].name, author=users[4].name, review=8),
    Review(spot_name=spots[10].name, author=users[2].name, review=6),
    Review(spot_name=spots[2].name, author=users[7].name, review=7),
    Review(spot_name=spots[14].name, author=users[3].name, review=9),
    Review(spot_name=spots[19].name, author=users[6].name, review=8),
    Review(spot_name=spots[22].name, author=users[2].name, review=9),
    Review(spot_name=spots[7].name, author=users[2].name, review=8),
    Review(spot_name=spots[16].name, author=users[5].name, review=9)
]

session.bulk_save_objects(users)
session.bulk_save_objects(spots)
session.bulk_save_objects(reviews)
session.commit()
