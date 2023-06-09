                  ==O                                      ==O                                     ==O
                   /|\/                                     /|\/                                    /|\/
          .-``'.  / |\   .'''-.                    .-``'.  / |\   .'''-.                   .-``'.  / |\   .'''-.
        .`   .`~  _/__|_ ~`.   '.               .`   .`~  _/__|_ ~`.   '.               .`   .`~  _/__|_ ~`.   '.   
    _.-'     '._   o  o   _.'     '-._      _.-'     '._   o  o   _.'     '-._      _.-'     '._   o  o   _.'     '-._             
# Certified Shredders
The Certified Shredders App is a command-line application that allows users to manage and view information about surf and skate spots, users, and reviews. The app is built using SQLAlchemy, a Python SQL toolkit and Object-Relational Mapping (ORM) library, to interact with a SQLite database. The app provides various functionalities such as adding users, adding spots, adding reviews, filtering spots, and editing/deleting reviews.


## About
The Certified Shredders App is developed by Eli Dawson and David Jones as a sample project to demonstrate the usage of SQLAlchemy and database management in a Python application. Feel free to modify and extend the app according to your needs. Happy shredding!

---

## Usage

To install and run, follow these steps:
1. Clone the repository: https://github.com/djones02/Certified-Shredders
2. Navigate to the project directory: cd relative/path/to/Certified-Shredders
3. Install the required dependencies and enter python shell: pipenv install && pipenv shell
4. Run the CLI: python cli.py

## Additional Notes
- The app uses a SQLite database named certified_shredders.db, which is created automatically when you run the app for the first time.
- The app displays data using rich text formatting, making it more visually appealing.
- The app supports various input validations and error handling to ensure smooth usage.
- The README menu option allows you to view the contents of the README.md file directly within the app.
- To exit the app, select the "Exit" option from the main menu and confirm the exit prompt.
- The app automatically commits changes to the database after adding, editing, or deleting records.


## App Functionality
Upon running the app, you will be presented with the main menu. From there, you can navigate through different options and perform various actions. Here's an overview of the available functionality:


### Main Menu
- Select User: Choose a user from the list of existing users.
- Add User: Add a new user to the system.
- View README.md: Display the README file.
- Exit: Exit the app.


### User Menu
- Select a user from the current list of users
- Back to main menu


### Spot Menu
- Add Spot: Add a new surf or skate spot to the list.
- Add Review: Add a review for a selected spot.
- View All Reviews: View all reviews that exist.
- Filter Spots: Filter spots by surf, skate, or view all spots.
- View README: Display the README file.
- Back to User Select: Go back to the user select menu.


### Review Menu
- Add Review: Add a review for a selected spot.
- Edit Review: Edit a selected review.
- Delete Review: Delete a selected review.
- View README: Display the README file.
- Back to Spot Menu: Go back to the spot menu.


--- 
