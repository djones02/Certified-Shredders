from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from helpers import *
from models import *
import os
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.markdown import Markdown

engine = create_engine('sqlite:///certified_shredders.db')
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":   

    ################# GLOBAL VARIABLES ###################
    console = Console()
    query_list_users = [user for user in session.query(User)]
    query_list_spots = [spot for spot in session.query(Spot)]
    query_list_reviews = [review for review in session.query(Review)]
    selected_user = None
    selected_spot = None

    ################# GLOBAL FUNCTIONS ##################
    def display_markdown(text):
        console.print(Markdown(text), style='bold')

    def display_readme(markdown):
        os.system('clear')
        os.system("python -m rich.markdown README.md")
        display_markdown(markdown)

    def refresh_query_lists():
        global query_list_users
        global query_list_spots
        global query_list_reviews
        query_list_users = [user for user in session.query(User)]
        query_list_spots = [spot for spot in session.query(Spot)]
        query_list_reviews = [review for review in session.query(Review)]

    def display_user_table():
        table = Table( title="Users", show_header=True, header_style="bold")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Certified")
        table.add_column("Reviews")

        for user in query_list_users:
            table.add_row(
                f"{user.id}",
                f"{user.name}",
                f"{user.certified}",
                f"{user.reviews}"
            )

        console.print(table)

    def display_spot_table():
        table = Table(title="Surf & Skate Spots", show_header=True, header_style="bold")
        table.add_column("ID")
        table.add_column("Nickname")
        table.add_column("Type")
        table.add_column("City")
        table.add_column("State")

        for spot in query_list_spots:
            table.add_row(
                f"{spot.id}",
                f"{spot.name}",
                f"{spot.type}",
                f"{spot.city}",
                f"{spot.state}"
            )
        
        console.print(table)
        print("Selected user: ", selected_user.name)

    def display_reviews_table():
        table = Table(title="All Reviews", show_header=True, header_style="bold")
        table.add_column("ID")
        table.add_column("Spot Name")
        table.add_column("Author")
        table.add_column("Review")

        for review in query_list_reviews:
            table.add_row(
                f"{review.id}",
                f"{review.spot_name}",
                f"{review.author}",
                f"{review.review}"
            )
        
        console.print(table)
        print("Selected user: ", selected_user.name)

    ################## ADDING+EDITING FUNCTIONS ######################
    def add_user():
        session.add(User(
            name=input("Username: "),
            certified= "False",
            reviews=0)
        )
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

    def select_user():
        os.system('clear')
        display_user_table()

        user_choice = input("Choose a user by entering the ID or enter 0 to retrun to main menu: ")
        
        while user_choice != "0":
            try:
                user_index = int(user_choice) - 1
                if 0 <= user_index <= len(query_list_users):
                    global selected_user
                    selected_user = query_list_users[user_index]
                    spot_menu() 
                else:
                    print("Invalid user number. Please try again.")
            except (ValueError, IndexError):
                print("Invalid user number. Please try again.")
        main_menu()

    def edit_review():
        user_input = input("Enter Review ID to edit: ")
        edited_review = input("Enter new review out of 10: ")

        review_query = session.query(Review).filter(Review.id == user_input).first()

        if int(user_input) <= 0 or int(user_input) > len(query_list_reviews):
            print("Review not found")
            return edit_review()
        if selected_user.name != review_query.author:
            os.system('clear')
            display_reviews_table()
            display_markdown(review_markdown)
            print("You are not authorized to edit this review")
            return edit_review()
        if user_input == "back":
            return review_menu()

        try:
            int(edited_review)
            if 0 < int(edited_review) and int(edited_review) <= 10:
                review_query.review = edited_review
                session.commit()
                review_menu()
            else:
                print("Review must be a number between 0 and 10")
                return edit_review()
        except:
            print("Invalid input must be a number")
            return edit_review()
        
    ####################### MENUS #######################
    def spot_menu():
        os.system('clear')
        display_spot_table()
        display_markdown(spot_markdown)

        choice = input("Selection: ")
        while choice != "6":
            if choice == "1": # ADD SURF/SKATE SPOT
                add_spot()
                spot_menu()
            elif choice == "2": # ADD REVIEW
                add_review()
            elif choice == "3": # VIEW ALL SURF/SKATE SPOTS
                spot_menu()
            elif choice == "4": # VIEW ALL REVIEWS
                review_menu()
            elif choice == "5": # VIEW README
                display_readme(spot_markdown)
            else:
                print("Please select an option from the menu")
            choice = input("Selection: ")
        select_user()

    def review_menu():
        os.system('clear')
        display_reviews_table()
        display_markdown(review_markdown)

        choice = input("Selection: ")
        while choice != "4":
            if choice == "1": # EDIT REVIEW
                edit_review()
            elif choice == "2": # VIEW ALL REVIEWS
                review_menu()
            elif choice == "3": # VIEW README
                display_readme(review_markdown)
            else:
                print("Please select an option from the menu")
            choice = input("Selection: ")
        spot_menu()

    def main_menu():
        os.system('clear')
        display_markdown(welcome_text)

        choice = input("Selection: ")

        while choice != "4":
            if choice == "1": # SELECT USER
                select_user()
            elif choice == "2": # CREATE USER
                add_user()
                main_menu()
            elif choice == "3": # VIEW README
                display_readme(home_markdown)
            else:
                print("Please select an option from the menu")
            choice = input("Selection: ")
        print("Exiting the App")
        
    ###################### APP INIT #####################
    main_menu()
