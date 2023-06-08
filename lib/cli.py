from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from helpers import *
from models import *
import os
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.markdown import Markdown
import sys
import ipdb
from seed import *

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
    surf_skate = ("Surf", "Skate") ###########################################################
    state_abb = (
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 
    'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 
    'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 
    'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    )
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
        # print(review_markdown)

    def handle_cert():
        for user in query_list_users:
            if user.reviews > 5:
                user.certified = "Shredder"


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
        while True:
            user_input = input("Enter username or back to return: ")
            if user_input.lower() == "back":
                break
            for user in query_list_users:
                if user_input.title() == user.name:
                    os.system('clear')
                    print(welcome_markdown)
                    console.print("User already exists", style="error")
                    main_menu()
            break
        if user_input.lower() == "back":
            os.system('clear')
            print(welcome_markdown)
            main_menu()
        
        session.add(User(name=user_input.title()))
        session.commit()
        refresh_query_lists()
        os.system('clear')
        display_user_table()
        select_user()

    def add_spot():
        while True:
            spot_name_input = input("Enter spot name: ")
            if spot_name_input.lower() == "back":
                break
            for spot in query_list_spots:
                if spot_name_input.title() == spot.name:
                    os.system('clear')
                    display_spot_table()
                    print(spot_markdown)
                    console.print("Spot already exists", style="error")
                    spot_menu()
            break
        
        if spot_name_input == "back":
            os.system('clear')
            display_spot_table()
            print(spot_markdown)
            spot_menu()

        while True:
            type_input = input('Enter 1 for Surf or 2 for Skate or back to return: ')
            if type_input.lower() == "back":
                break
            try:
                choice_index = int(type_input) - 1
                if int(type_input) < 1 or int(type_input) > 2:
                    raise ValueError()
                spot_type = surf_skate[choice_index]
                break
            except (ValueError, IndexError):
                os.system('clear')
                display_spot_table()
                console.print("Invalid spot type", style="error")
                continue
        if type_input.lower() == "back":

            os.system('clear')
            display_spot_table()
            print(spot_markdown)
            spot_menu()

        while True:
            city_input = input("Enter city: ")
            if city_input.lower() == "back":
                break
            else:
                break
        if city_input == "back":
            os.system('clear')
            display_spot_table()
            print(spot_markdown)
            spot_menu()

        while True:
            state_input = input("Please enter 2 letter state abbreviation: ")
            if state_input.lower() == "back":
                break
            try:
                if state_input.upper() not in state_abb:
                    raise ValueError
                state_selection = state_input.upper()
                break
            except ValueError:
                os.system("clear")
                display_spot_table()
                console.print("Invalid state selection", style="error")
                continue
        if state_input.lower() == "back":
            os.system('clear')
            display_spot_table()
            print(spot_markdown)
            spot_menu()

        session.add(Spot(
            name=spot_name_input.title(), 
            type=spot_type,
            city=city_input.title(),
            state=state_selection
        ))
        session.commit()
        refresh_query_lists()
        
            
        os.system('clear')
        display_spot_table()
        print(spot_markdown)
        spot_menu()
        


    def add_review():
        while True:
            user_choice = input("Select Spot by ID or enter back to return: ")
            
            if user_choice.lower() == "back":
                    break
            
            try:
                spot_index = int(user_choice) - 1

                if spot_index < 0 or spot_index >= len(query_list_spots):
                    raise ValueError
                
                global selected_spot
                selected_spot = query_list_spots[spot_index]

                selected_spot_reviews = [review.author for review in query_list_reviews if review.spot_name == selected_spot.name]

                if selected_user.name in selected_spot_reviews:
                    raise IndexError

                break
            except ValueError:
                os.system("clear")
                display_spot_table()
                console.print("Invalid spot ID. Please try again", style="error")
                continue
            except IndexError:
                os.system("clear")
                display_spot_table()
                console.print("You already wrote a review for this spot", style="error")
                continue

        if user_choice == "back":
            os.system('clear')
            display_spot_table()
            print(spot_markdown)
            spot_menu()

        while True:
            user_input = input('Review out of 10: ')
            if user_input.lower() == "back":
                    break
            
            try:
                if int(user_input) < 0 or int(user_input) > 10:
                    raise ValueError

                break
            except:
                os.system("clear")
                display_spot_table()
                console.print("Review must be a number between 0 and 10", style="error")
                continue
        if user_input == "back":
            os.system('clear')
            display_spot_table()
            print(spot_markdown)
            spot_menu()

        session.add(Review(
                        spot_name=selected_spot.name, 
                        author=selected_user.name,
                        review=user_input
                        ))
        selected_user.reviews += 1
        handle_cert()
        session.commit()
        refresh_query_lists()
        display_reviews_table
        print(review_markdown)
        review_menu()



 

    def select_user():
            
            while True:
                user_choice = input("Choose a user by entering the ID or enter back to return: ")
                    
                if user_choice.lower() == "back":
                    break
                
                try:
                    user_index = int(user_choice) - 1
                    if user_index < 0 or user_index >= len(query_list_users):
                        raise ValueError()
                    global selected_user
                    selected_user = query_list_users[user_index]
                    break
                except ValueError:
                    os.system('clear')
                    display_user_table()
                    console.print("Invalid user number. Please try again.", style="error")
                    continue 

            if user_choice == "back":
                os.system('clear')
                print(welcome_markdown)
                main_menu()
            else:
                os.system('clear')
                display_spot_table()
                print(spot_markdown)
                spot_menu()
         
    def edit_review():
        os.system('clear')
        display_reviews_table()

        while True:
            user_input = input("Enter Review ID to edit or back to return: ")
            review_query = session.query(Review).filter(Review.id == user_input).first()

            if user_input.lower() == "back":
                break

            try:
                int(user_input)
                
                if not review_query:
                    raise ValueError

                if selected_user.name != review_query.author:
                    raise IndexError
                
                break

            except ValueError:
                review_error()
                console.print("Review not found", style="error")
                continue
            except IndexError:
                review_error()
                console.print("You are not authorized to edit this review", style="error")
                continue
        if user_input == "back":
            os.system('clear')
            display_reviews_table
            print(review_markdown)
            review_menu()

        while True:
            edited_review = input("Enter a new review out of 10 or back to return: ")

            if edited_review.lower() == "back":
                break

            try:
                if int(edited_review) < 0 or int(edited_review) > 10:
                    raise ValueError
                
                break
            except:
                review_error()
                console.print('Review must be an integer between 0 & 10', style="error")
                continue

        if user_input == "back":
            os.system('clear')
            display_reviews_table
            print(review_markdown)
            review_menu()
        review_query.review = edited_review
        session.commit()
        review_menu()

    def delete_review():
        os.system('clear')
        display_reviews_table()
        while True:
            user_input = input("Enter review ID to delete or back to return: ")
            
            
            if user_input.lower() == "back":
                break

            try:
                
                if int(user_input) not in [review.id for review in session.query(Review)]:
                    raise ValueError
                
                review_query = session.query(Review).filter(Review.id == int(user_input)).first()
                
                if selected_user.name != review_query.author:
                    raise IndexError
                
                
                break   
            except ValueError:
                review_error()
                console.print("Review not found", style="error")
                continue
            except IndexError:
                review_error()
                console.print("You are not authorized to delete this review", style="error")
                continue
        if user_input == "back":
            os.system('clear')
            display_reviews_table
            print(review_markdown)
            review_menu()
        
        session.delete(review_query)
        session.commit()
        selected_user.reviews -= 1
        refresh_query_lists()
        review_menu()



    def exit_app():
        console.print("Are you sure you want to exit? (Y/N):", style="error")
        user_input = input().lower()

        if user_input == "y" or user_input == "yes":
            os.system("clear")
            console.print('Hope to see you soon!', style="error")
            session.close()
            sys.exit()
        elif user_input == "n" or user_input == "no":
            os.system("clear")
            print(welcome_markdown)
            main_menu()
        else:
            os.system("clear")
            console.print("Invalid input. Please enter Y or N.", style="error")
            exit_app()
        
    ####################### MENUS #######################
    def readme_menu():
        user_input = input('Exit: ')
        if user_input:
            return


    def spot_menu():
        # display_spot_table()
        # print(spot_markdown)
        choice = input("Selection: ")
        if choice == "1": # ADD SURF/SKATE SPOT
            add_spot()
        elif choice == "2": # ADD REVIEW
            os.system('clear')
            display_spot_table()
            add_review()
        elif choice == "3": # VIEW ALL REVIEWS
            review_menu()
        elif choice == "4": # VIEW README
            display_readme()
            os.system('clear')
            display_spot_table()
            print(spot_markdown)
            spot_menu()
        elif choice == "5":
            os.system('clear')
            display_user_table()
            select_user()
        else:
            os.system('clear')
            display_spot_table()
            print(spot_markdown)
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
            display_spot_table()
            print(spot_markdown)
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
            exit_app()
        else:
            os.system('clear')
            print(welcome_markdown)
            console.print("Please select an option from the menu", style="error")
            main_menu()
            


    ###################### APP INIT #####################
    os.system('python seed.py')
    refresh_query_lists()
    review_amount_query()
    handle_cert()
    os.system('clear')
    print(welcome_markdown)
    main_menu()