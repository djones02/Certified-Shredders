from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os, sys
from helpers import *
from models import *
from rich.console import Console
from rich.theme import Theme
from rich.table import Table

engine = create_engine('sqlite:///certified_shredders.db')
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    ################# GLOBAL VARIABLES ###################
    theme = Theme({
        "error": "bright_red",
    })
    console = Console(theme = theme)
    surf_skate = ("Surf", "Skate")
    query_list_users = [user for user in session.query(User)]
    query_list_spots = [spot for spot in session.query(Spot)]
    query_list_reviews = [review for review in session.query(Review)]
    selected_user = None
    selected_spot = None
    clear = os.system('clear')
    surf = False
    skate = False
    all = True
    surf = "Surf"
    skate = "Skate"

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

    def handle_cert():
        for user in query_list_users:
            if user.reviews >= 5:
                user.certified = "Shredder"
    
    def commit():
        handle_cert()
        session.commit()
        refresh_query_lists()

    ################### TABLES ###################
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
        if all == True:
            for spot in query_list_spots:
                table.add_row(
                    f"{spot.id}",
                    f"{spot.name}",
                    f"{spot.type}",
                    f"{spot.city}",
                    f"{spot.state}"
                )
        elif surf == True:
            for spot in query_list_spots:
                if spot.type == "Surf":
                    table.add_row(
                        f"{spot.id}",
                        f"{spot.name}",
                        f"{spot.type}",
                        f"{spot.city}",
                        f"{spot.state}"
                    )
        elif skate == True:
            for spot in query_list_spots:
                if spot.type == "Skate":
                    table.add_row(
                        f"{spot.id}",
                        f"{spot.name}",
                        f"{spot.type}",
                        f"{spot.city}",
                        f"{spot.state}"
                    )
        console.print(table)
        print(f"Selected user: {selected_user.name}")

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
        print(f"Selected user: {selected_user.name}")

    ################## ADDING+EDITING FUNCTIONS ######################
    def add_user():
        while True:
            user_input = input("Enter username or back to return: ")
            try:
                if user_input.lower() == "back":
                    break
                for user in query_list_users:
                    if user_input.title() == user.name:
                        raise Exception
                break
            except:
                os.system('clear')
                print(welcome_markdown)
                console.print("User already exists", style="error")
                continue
        if user_input.lower() == "back":
            main_menu()
        session.add(User(name=user_input.title()))
        commit()
        select_user()

    def add_spot():
        os.system('clear')
        display_spot_table
        while True:
            spot_name_input = input("Enter spot name: ")
            try:
                if spot_name_input.lower() == "back":
                    break
                for spot in query_list_spots:
                    if spot_name_input.title() == spot.name:
                        raise Exception
                break
            except:
                os.system('clear')
                display_spot_table()
                print(spot_markdown)
                console.print("Spot already exists", style="error")
                continue
        if spot_name_input == "back":
            spot_menu()
        while True:
            type_input = input('Enter 1 for Surf or 2 for Skate: ')
            if type_input.lower() == "back":
                break
            try:
                choice_index = int(type_input) - 1
                if int(type_input) < 1 or int(type_input) > 2:
                    raise Exception
                spot_type = surf_skate[choice_index]
                break
            except:
                os.system('clear')
                display_spot_table()
                console.print("Invalid spot type", style="error")
                continue
        if type_input.lower() == "back":
            spot_menu()
        while True:
            city_input = input("Enter city: ")
            if city_input.lower() == "back":
                spot_menu()
            break
        while True:
            state_input = input("Please enter 2 letter state abbreviation: ")
            if state_input.lower() == "back":
                break
            try:
                if state_input.upper() not in state_abb:
                    raise Exception
                state_selection = state_input.upper()
                break
            except:
                os.system("clear")
                display_spot_table()
                console.print("Invalid state selection", style="error")
                continue
        if state_input.lower() == "back":
            spot_menu()
        session.add(Spot(
            name=spot_name_input.title(), 
            type=spot_type,
            city=city_input.title(),
            state=state_selection
        ))
        commit()
        spot_menu()    

    def filter_spots():
        global skate
        global surf
        global all
        skate = False
        surf = False
        all = True
        os.system('clear')
        # display_spot_table()
        while True:
            filter_selection = input('1 to see skate spots, 2 to see surf spots, 3 to see all spots: ')
            try:
                if filter_selection.lower() == "back":
                    break
                if int(filter_selection) not in (1, 2, 3):
                    raise Exception
                break
            except:
                os.system('clear')
                display_spot_table()
                console.print("Please select an option from the menu", style="error")
                continue
        if filter_selection == "back":
            spot_menu()
        if filter_selection == "1":
            skate = True
            surf = False
            all = False
            spot_menu()
        if filter_selection == "2":
            skate = False
            surf = True
            all = False
            spot_menu()
        if filter_selection == "3":
            skate = False
            surf = False
            all = True
            spot_menu()

    def add_review():
        os.system('clear')
        display_spot_table()
        while True:
            user_choice = input("Select Spot by ID: ")
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
            spot_menu()
        print(f"Selected Spot: {selected_spot.name}")
        while True:
            user_input = input('Review out of 10: ')
            if user_input.lower() == "back":
                    break
            try:
                if int(user_input) < 0 or int(user_input) > 10:
                    raise Exception
                break
            except:
                os.system("clear")
                display_spot_table()
                print(f"Selected Spot: {selected_spot.name}")
                console.print("Review must be a number between 0 and 10", style="error")
                continue
        if user_input == "back":
            spot_menu()
        session.add(Review(
            spot_name=selected_spot.name, 
            author=selected_user.name,
            review=user_input
        ))
        selected_user.reviews += 1
        commit()
        review_menu()

    def select_user():
        os.system('clear')
        display_user_table()
        while True:
            user_choice = input("Choose a user by entering the ID or enter 0 to return: ")
            try:
                if user_choice.lower() == "0":
                    break
                user_index = int(user_choice) - 1
                if user_index < 0 or user_index >= len(query_list_users):
                    raise Exception
                global selected_user
                selected_user = query_list_users[user_index]
                break
            except:
                os.system('clear')
                display_user_table()
                console.print("Invalid user number. Please try again.", style="error")
                continue
        if user_choice == "0":
            main_menu()
        spot_menu()

    def edit_review():
        os.system('clear')
        display_reviews_table()
        while True:
            user_input = input("Enter Review ID to edit or back to return: ")
            review_query = session.query(Review).filter(Review.id == user_input).first()
            try:
                if user_input.lower() == "back":
                    break
                int(user_input)
                if not review_query:
                    raise ValueError
                if selected_user.name != review_query.author:
                    raise IndexError
                break
            except ValueError:
                os.system('clear')
                display_reviews_table()
                console.print("Review not found", style="error")
                continue
            except IndexError:
                os.system('clear')
                display_reviews_table()
                console.print("You are not authorized to edit this review", style="error")
                continue
        if user_input == "back":
            review_menu()
        while True:
            edited_review = input("Enter a new review out of 10 or back to return: ")
            try:
                if edited_review.lower() == "back":
                    break
                if int(edited_review) < 0 or int(edited_review) > 10:
                    raise Exception
                break
            except:
                os.system('clear')
                display_reviews_table()
                console.print('Review must be an integer between 0 & 10', style="error")
                continue
        if user_input == "back":
            review_menu()
        review_query.review = edited_review
        commit()
        review_menu()

    def delete_review():
        os.system('clear')
        display_reviews_table()
        while True:
            user_input = input("Enter review ID to delete or back to return: ")
            try:
                if user_input.lower() == "back":
                    break
                if int(user_input) not in [review.id for review in session.query(Review)]:
                    raise ValueError
                review_query = session.query(Review).filter(Review.id == int(user_input)).first()
                if selected_user.name != review_query.author:
                    raise IndexError    
                break   
            except ValueError:
                os.system('clear')
                display_reviews_table()
                console.print("Review not found", style="error")
                continue
            except IndexError:
                os.system('clear')
                display_reviews_table()
                console.print("You are not authorized to delete this review", style="error")
                continue
        if user_input == "back":
            review_menu()
        session.delete(review_query)
        selected_user.reviews -= 1
        commit()
        review_menu()

    def exit_app():
        os.system('clear')
        console.print("Are you sure you want to exit? (Y/N):", style="error")
        while True:
            user_input = input().lower()
            try:
                if user_input not in ("y", "yes", "no", "n"):
                    raise Exception
                break
            except:
                os.system("clear")
                console.print("Invalid input. Please enter Y or N.", style="error")
                continue
        if user_input == "y" or user_input == "yes":
                os.system("clear")
                console.print('Hope to see you soon!', style="error")
                session.close()
                sys.exit()
        if user_input == "n" or user_input == "no":
                main_menu()                    

    ####################### MENUS #######################
    def readme_menu():
        user_input = input('Exit: ')
        if user_input:
            return

    def spot_menu():
        os.system('clear')
        display_spot_table()
        print(spot_markdown)
        while True:
            choice = input("Selection: ")
            try:
                if choice not in ("1", "2", "3", "4", "5", "6"):
                    raise Exception
                break
            except:
                os.system('clear')
                display_spot_table()
                print(spot_markdown)
                console.print("Please select an option from the menu", style="error")
                continue
        if choice == "1": # ADD SURF/SKATE SPOT
            add_spot()
        if choice == "2": # ADD REVIEW
            add_review()
        if choice == "3": # VIEW ALL REVIEWS
            review_menu()
        if choice == "4": # FILTER SPOTS
            filter_spots()
        if choice == "5": # VIEW README
            display_readme()
            spot_menu()
        if choice == "6": # BACK TO USER SELECT
            select_user()

    def review_menu():
        os.system('clear')
        display_reviews_table()
        print(review_markdown)
        while True:
            menu_selection = input("Selection: ")
            try:
                if menu_selection not in ("1", "2", "3", "4", "5"):
                    raise Exception
                break
            except:
                os.system('clear')
                display_reviews_table()
                print(review_markdown)
                console.print("Please select an option from the menu", style="error")
                continue
        if menu_selection == "1": # ADD REVIEW
            add_review()
        if menu_selection == "2": # EDIT REVIEW
            edit_review()
        if menu_selection == "3": # DELETE REVIEW
            delete_review()
        if menu_selection == "4": # VIEW README
            display_readme()
            review_menu()
        if menu_selection == "5": # BACK TO SPOTS
            spot_menu()

    def main_menu():
        os.system('clear')
        print(welcome_markdown)
        while True:
            menu_selection = input("Selection: ")
            try:
                if menu_selection not in ("1", "2", "3", "4"):
                    raise Exception
                break
            except:
                os.system('clear')
                print(welcome_markdown)
                console.print("Please select an option from the menu", style="error")
                continue
        if menu_selection == "1": # SELECT USER
            select_user()
        if menu_selection == "2": # CREATE USER
            add_user()
        if menu_selection == "3": # VIEW README
            display_readme()
            main_menu()
        if menu_selection == "4": # EXIT APP
            exit_app()  

    ###################### APP INIT #####################
    os.system('python seed.py')
    refresh_query_lists()
    review_amount_query()
    handle_cert()
    main_menu()