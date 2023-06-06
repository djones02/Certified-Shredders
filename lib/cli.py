from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.markdown import Markdown
from models import *
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///certified_shredders.db")
Session = sessionmaker(bind=engine)
session = Session()

def display_markdown(text):
    console = Console()
    console.print(Markdown(text))

def display_table():
    table = Table(show_header=True, header_style="bold")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Certified")
    table.add_column("Reviews")

    query_list_users = [user for user in session.query(User)]

    for user in query_list_users:
        table.add_row(f"{user.id}", f"{user.name}", f"{user.certified}", f"{user.reviews}")

    console = Console()
    console.print(table)

if __name__ == "__main__":
    markdown_text = """
                  ==O 
                   /|\/ 
          .-``'.  / |\   .'''-.
        .`   .`~  _/__|_ ~`.   '.
    _.-'     '._   o  o   _.'     '-._

      Welcome to Certified Shredders!

    1. Select a user
    2. Create a new user
    3. Exit the App
    """
    display_markdown(markdown_text)

    choice = input("Selection: ")
    while choice != "3":
        if choice == "1":
            display_table()
        elif choice == "2":
            print("selected")
        else:
            print("Invalid")
        choice = input("Selection: ")
    print("Exiting the App")