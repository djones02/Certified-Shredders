from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
import os
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.markdown import Markdown
from models import *

engine = create_engine("sqlite:///certified_shredders.db")
Session = sessionmaker(bind=engine)
session = Session()

def display_markdown(text):
    console = Console()
    console.print(Markdown(text), style='bold')

query_list_users = [user for user in session.query(User)]
query_list_spots = [spot for spot in session.query(Spot)]

def refresh_query_lists():
    global query_list_users
    global query_list_spots
    query_list_users = [user for user in session.query(User)]
    query_list_spots = [spot for spot in session.query(Spot)]

def display_table():
    table = Table(show_header=True, header_style="bold", title="Users")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Certified")
    table.add_column("Reviews")

    for user in query_list_users:
        table.add_row(f"{user.id}", f"{user.name}", f"{user.certified}", f"{user.reviews}")

    console = Console()
    console.print(table)

def display_spot_table():
    table = Table(show_header=True, header_style="bold", title="Surf & Skate Spots")
    table.add_column("ID")
    table.add_column("Nickname")
    table.add_column("Type")
    table.add_column("City")
    table.add_column("State")

    for spot in query_list_spots:
        table.add_row(f"{spot.id}", f"{spot.name}", f"{spot.type}", f"{spot.city}", f"{spot.state}")

    console = Console()
    console.print(table)

def add_user():
    session.add(User(name=input("Username: "), certified= "False", reviews=0))
    session.commit()
    refresh_query_lists()

def select_user():
    user_choice = input("Choose a user by entering the ID or enter 0 to return: ")
    while user_choice != "0":
        try:
            user_index = int(user_choice) - 1
            if 0 <= user_index <= len(query_list_users):
                selected_user = query_list_users[user_index]
                display_spot_table()
                print("Selected user: ", selected_user.name)
            else:
                print("Invalid user number. Please try again.")
        except (ValueError, IndexError):
            print("Invalid user number. Please try again.")
        user_choice = input("Choose a user by entering the ID or enter 0 to return: ")

if __name__ == "__main__":
    welcome_text = """
                      ==O 
                       /|\/ 
              .-``'.  / |\   .'''-.
            .`   .`~  _/__|_ ~`.   '.
        _.-'     '._   o  o   _.'     '-._

          Welcome to Certified Shredders!

        1. Select a user
        2. Create a new user
        3. View README
        4. Exit the App 
    """
    display_markdown(welcome_text)

    home_selection = """
        1. Select a user
        2. Create a new user
        3. View README
        4. Exit the App
    """

    choice = input("Selection: ")
    while choice != "4":
        if choice == "1":
            display_table()
            select_user()
            display_markdown(home_selection)
        elif choice == "2":
            add_user()
            display_markdown(welcome_text)
        elif choice == "3":
            os.system("python -m rich.markdown README.md")
            display_markdown(home_selection)
        else:
            print("Please select an option from the menu")
        choice = input("Selection: ")
    print("Exiting the App")
