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
    theme = Theme({
        "error": "red"
    })
    console = Console(theme = theme)
    query_list_users = [user for user in session.query(User)]
    query_list_spots = [spot for spot in session.query(Spot)]
    query_list_reviews = [review for review in session.query(Review)]
    selected_user = None
    selected_spot = None

    ################# GLOBAL FUNCTIONS ##################
    def display_readme():
        os.system('clear')
        os.system("python -m rich.markdown README.md")
        readme_menu()

        
    def refresh_query_lists():
        global query_list_users
        global query_list_spots
        global query_list_reviews
        query_list_users = [user for user in session.query(User)]
        query_list_spots = [spot for spot in session.query(Spot)]
        query_list_reviews = [review for review in session.query(Review)]


    def review_amount_query():
        for user in query_list_users:
            review_list = len([review for review in query_list_reviews if user.name == review.author])
            user.reviews = review_list


    def review_error():
        os.system('clear')
        display_reviews_table()
        print(review_menu)


    def display_user_table():
        table = Table(
            title="Users",
            show_header=True,
            header_style="bold",
            show_lines=True
        )
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
        table = Table(
            title="Surf & Skate Spots",
            show_header=True,
            header_style="bold",
            show_lines=True
        )
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
        table = Table(
            title="All Reviews",
            show_header=True,
            header_style="bold",
            show_lines=True
        )
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
        user_input = input("Enter username or back to return: ")
        if user_input.lower() == "back":
            os.system('clear')
            print(welcome_markdown)
            main_menu()
        session.add(User(name=user_input))
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
            console.print("Invalid user number. Please try again.", style="error")
        session.add(Review(
            spot_name=selected_spot.name, 
            author=selected_user.name,
            review=input('Review out of 10: ')
            ))
        selected_user.reviews += 1
        handle_cert()
        session.commit()
        refresh_query_lists()
        review_menu()


    def handle_cert():
        for user in query_list_users:
            if user.reviews > 5:
                user.certified = "True"


    def select_user():
        user_choice = input("Choose a user by entering the ID or enter back to return: ")
        
        try:
            if user_choice.lower() == "back":
                os.system('clear')
                print(welcome_markdown)
                main_menu()

            user_index = int(user_choice) - 1
            
            if 0 <= user_index <= len(query_list_users):
                global selected_user
                selected_user = query_list_users[user_index]
                os.system('clear')
                spot_menu() 
        except:
            os.system('clear')
            display_user_table()
            console.print("Invalid user number. Please try again.", style="error")
            select_user()

            
    def edit_review():
        user_input = input("Enter Review ID to edit or back to return: ")
        review_query = session.query(Review).filter(Review.id == user_input).first()
        if user_input.lower() == "back":
            review_menu()
            return
        try:
            if int(user_input) <= 0 or int(user_input) > len(query_list_reviews):
                console.print("Review not found", style="error")
                edit_review()
            if selected_user.name != review_query.author:
                review_error()
                console.print("You are not authorized to edit this review", style="error")
                edit_review()
        except:
            review_error()
            console.print("Invalid input must be a Review ID", style="error")
            edit_review()
        edited_review = input("Enter new review out of 10 or back to return: ")
        if edited_review.lower() == "back":
            review_menu()
            return
        try:
            int(edited_review)
            if 0 < int(edited_review) and int(edited_review) <= 10:
                review_query.review = edited_review
                session.commit()
                review_menu()
        except:
            review_error()
            console.print("Invalid review must be a number between 0 and 10", style="error")
            edit_review()


    def delete_review():
        user_input = input("Enter review ID to delete or back to return: ")
        if user_input.lower() == "back":
            review_menu()
            return
        review_query = session.query(Review).filter(Review.id == user_input).first()
        if review_query:
            if selected_user.name != review_query.author:
                review_error()
                console.print("You are not authorized to delete this review", style="error")
                delete_review()
            else:
                session.delete(review_query)
                session.commit()
                selected_user.reviews -= 1
                refresh_query_lists()
                review_menu()
        else:
            review_error()
            console.print("Review not found", style="error")
            delete_review()
    
        
    ####################### MENUS #######################
    def readme_menu():
        user_input = input('Exit: ')
        if user_input:
            return
    

    def spot_menu():
        display_spot_table()
        print(spot_markdown)
        choice = input("Selection: ")
        if choice == "1": # ADD SURF/SKATE SPOT
            add_spot()
            os.system('clear')
            spot_menu()
        elif choice == "2": # ADD REVIEW
            add_review()
        elif choice == "3": # VIEW ALL REVIEWS
            review_menu()
        elif choice == "4": # VIEW README
            display_readme()
            os.system('clear')
            spot_menu()
        elif choice == "5":
            os.system('clear')
            display_user_table()
            select_user()
        else:
            os.system('clear')
            console.print("Please select an option from the menu", style="error")
            spot_menu()


    def review_menu():
        os.system('clear')
        display_reviews_table()
        print(review_markdown)
        choice = input("Selection: ")
        
        if choice =="1":
            os.system('clear')
            display_spot_table()
            
            add_review()
        elif choice == "2": # EDIT REVIEW
            edit_review()
        elif choice == "3": # VIEW ALL REVIEWS
            delete_review()
        elif choice == "4":
            display_readme()
            review_menu()
        elif choice == "5":
            os.system('clear')
            spot_menu()
        else:
            os.system('clear')
            console.print("Please select an option from the menu", style="error")
            review_menu()


    def main_menu():
        choice = input("Selection: ")
        if choice == "1": # SELECT USER
            os.system('clear')
            display_user_table()
            select_user()
        elif choice == "2": # CREATE USER
            add_user()
            os.system('clear')
            display_user_table()
            select_user()
        elif choice == "3": # VIEW README
            display_readme()
            os.system('clear')
            print(welcome_markdown)
            main_menu()
        elif choice == "4":
            os.system('clear')
            console.print("Exiting the App", style="error")
            exit()
        else:
            os.system('clear')
            print(welcome_markdown)
            console.print("Please select an option from the menu", style="error")
            main_menu()
            


    ###################### APP INIT #####################
    refresh_query_lists()
    review_amount_query()
    handle_cert()
    os.system('clear')
    print(welcome_markdown)
    main_menu()