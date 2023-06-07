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
if __name__ == "__main__":
    
    os.system('clear')

    def display_markdown(text):
        console = Console()
        console.print(Markdown(text), style='bold')

    selected_user = None
    selected_spot = None
    query_list_users = [user for user in session.query(User)]
    query_list_spots = [spot for spot in session.query(Spot)]
    query_list_reviews = [review for review in session.query(Review)]

    def refresh_query_lists():
        global query_list_users
        global query_list_spots
        global query_list_reviews
        query_list_users = [user for user in session.query(User)]
        query_list_spots = [spot for spot in session.query(Spot)]
        query_list_reviews = [review for review in session.query(Review)]


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

    def display_reviews_table():
        table = Table(show_header=True, header_style="bold", title="All Reviews")
        table.add_column("ID")
        table.add_column("Spot Name")
        table.add_column("Author")
        table.add_column("Review")

        for review in query_list_reviews:
            table.add_row(f"{review.id}", f"{review.spot_name}", f"{review.author}",f"{review.review}")

        console = Console()
        console.print(table)

    def add_user():
        session.add(User(name=input("Username: "), certified= "False", reviews=0))
        session.commit()
        refresh_query_lists()

    def add_spot():
        session.add(Spot(
            name=input('Spot Name: '), 
            type=input('Surf or Skate?: '),
            city=input('City: '),
            state=input('State: ')
        ))
        session.commit()
        refresh_query_lists()
        
    def add_review():
        user_choice = input("Select Spot by ID: ")
        spot_index = int(user_choice) - 1
        if 0 <= spot_index <= len(query_list_spots):
            global selected_spot
            selected_spot = query_list_spots[spot_index]
        else:
            print("Invalid user number. Please try again.")
        session.add(Review(
            spot_name=selected_spot.name, 
            author=selected_user.name,
            review=input('Review out of 10: ')
        ))
        session.commit()
        refresh_query_lists()

    def edit_review():
        user_input = input("Enter Review Id to edit: ")
        review_query = session.query(Review).filter(Review.id == user_input).first()
        if int(user_input) <= 0 or int(user_input) > len(query_list_reviews):
            print("Review not found.")
            return edit_review()
        if selected_user.name != review_query.author:
            print("You are not authorized to edit this review.")
            return edit_review()
        if user_input == "back":
            return review_menu()
        edited_review = input("Enter new review out of 10: ")
        
        try:
            int(edited_review)
            if 0 < int(edited_review) and int(edited_review) <= 10:
                review_query.review = edited_review
                session.commit()
                os.system("clear")
                display_reviews_table()
                display_markdown(review_markdown)
            else:
                print("Review must be a number between 0 and 10")
                return edit_review()
            # edited_review = input_field
        except:
            print("Invalid input must be a number")
            return edit_review()
        # if 0 > int(input_field) or int(input_field) > 10:
        #     print("Please enter a number between 0 and 10")
        #     return edit_review()
        # else:
        #     edited_review = input_field
        # review_query.review = edited_review
        # session.commit()
        # os.system("clear")
        # display_reviews_table()
        # display_markdown(review_markdown)

    def select_user():
        user_choice = input("Choose a user by entering the ID or enter 0 to return: ")
        while user_choice != "0":
            try:
                user_index = int(user_choice) - 1
                if 0 <= user_index <= len(query_list_users):
                    global selected_user
                    selected_user = query_list_users[user_index]
                    os.system('clear')
                    display_spot_table()
                    print("Selected user: ", selected_user.name)
                    display_markdown(spot_markdown)
                    spot_menu()
                else:
                    print("Invalid user number. Please try again.")
            except (ValueError, IndexError):
                print("Invalid user number. Please try again.")
            os.system('clear') # ****************************************************
            display_table()
            user_choice = input("Choose a user by entering the ID or enter 0 to return: ")

    def spot_menu():
        choice = input("Selection: ")
        while choice != "6":
            if choice == "1":
                add_spot()
                os.system('clear')
                display_spot_table()
                display_markdown(spot_markdown)
            elif choice == "2":
                add_review()
                os.system('clear')
                display_spot_table()
                display_markdown(spot_markdown)
            elif choice == "3":
                os.system('clear')
                display_spot_table()
                display_markdown(spot_markdown)
            elif choice == "4":
                os.system('clear')
                display_reviews_table()
                display_markdown(review_markdown)
                review_menu()
                os.system('clear')
                display_spot_table()
                display_markdown(spot_markdown)
            elif choice == "5":
                os.system('clear')
                os.system("python -m rich.markdown README.md")
                display_markdown(spot_markdown)
            else:
                print("Please select an option from the menu")
            choice = input("Selection: ")
        print("Exiting the App")

    def review_menu():
        choice = input("Selection: ")
        while choice != "4":
            if choice == "1":
                edit_review()
            elif choice == "2":
                os.system('clear')
                display_reviews_table()
                display_markdown(review_markdown)
            elif choice == "3":
                os.system('clear')
                os.system("python -m rich.markdown README.md")
                display_markdown(review_markdown)
            else:
                print("Please select an option from the menu")
            choice = input("Selection: ")
        print("Exiting the App")

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

    spot_markdown = """
        1. Add Surf/Skate spot
        2. Add Review
        3. View All Surf/Skate Spots
        4. View All Reviews
        5. View README
        6. Back to User Select
    """

    review_markdown = """
        1. Edit Review
        2. View All Reviews
        3. View README
        4. Back to Spots
    """

    choice = input("Selection: ")
    while choice != "4":
        if choice == "1":
            os.system('clear')
            display_table()
            select_user()
            display_markdown(home_selection)
        elif choice == "2":
            add_user()
            os.system('clear')
            display_markdown(welcome_text)
        elif choice == "3":
            os.system("python -m rich.markdown README.md")
            display_markdown(home_selection)
        else:
            print("Please select an option from the menu")
        choice = input("Selection: ")
    print("Exiting the App")
