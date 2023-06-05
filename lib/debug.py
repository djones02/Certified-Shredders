from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *



if __name__ == '__main__':
    engine = create_engine('sqlite:///certified_shredder.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    print("This if statement is firing")

    import ipdb; ipdb.set_trace()