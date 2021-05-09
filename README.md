## CS50x Final Project - Budget Lists

This project is a web-based application based on budgeting lists and items submitted by a registered user.

This is meant to be an all-purpose, general hybrid between wishlists and budgets.

The aim of this exercise is to demonstrate the concept of a visual breakdown of items, units, and prices, all consolidated across cards, tables, and brief text descriptions.

## Disclaimer

This is an application based in part on Harvard CS50x's web track distribution code, from Finance (CS50x Problem Set 8 2020).

Because of the above, the user login and registration features are mostly unmodified from my original solutions.

This application makes use of the CS50 library for Python, along with other imported dependencies as outlined in application.py and requirements.txt.

## Languages

This is an application that utilizes Python, Javascript, HTML, CSS, and SQL.

### Database

This application makes use of a database.

The database stores all list and item information submitted by the user.

Once the user is registered, the database also stores the username and the hash value of the user's password. The learner's login details are checked against the database via SQL queries.

Flask is used to set information about the user's login session. The tracked session data is passed by the server to query the database. Most commonly, this is used to differentiate between multiple registered users.

## Python Dependencies
- cs50
- Flask
- Flask-Session
- requests

## Description (How To Use)

The [Youtube video introduction and description can be found here](https://www.youtube.com/watch?v=86e4oyCQ2mM "CS50x Final Project: Budget Lists - Youtube")

### Login and Registration Pages

The user must hold valid login details for full functionality.

There is a registration option provided in the navigation bar.

If the user makes a new account by providing a username and password, they are registered to the local budget database.

Once the user enters their valid login credentials, they are able to access the main page.

All pages aside from the Login and Registration options should require a valid user login session.

### Home Page

The Home page can be accessed by click on either the website logo or the navigation bar item marked Home.

It is a landing site for any lists created by the user, containing a semi-detailed overview of existing lists.

If the user has no lists, a button option to access the Build List page should appear.

If the user has at least one list, a card should show for each available list, listing the title as the header, every available item as the body (scrollable), and the budget, cost, and net values outlined clearly as muted text.

For each available card, there should also be an Access List Breakdown button, which leads to the Breakdown page.

### Build List Page

The Build List page can be accessed by the navigation bar and has three functions.

The first is the ability to create a new list. This can be accessed by clicking on the topmost outline button, leading to a modal window with two input fields, the list title and the budget for the list. Each list name must be unique.

The second function is the ability to add items onto any existing list. A dropdown menu is provided, and any item can be added, with form control over necessary fields.

The last function is a summary of all available lists in basic card format. These summary cards provide only the most basic information, such as list title, budget, and item counts. This is a more superficial look into the lists in comparison to the Home page, allowing for a quick glance at general statistics when adding new items to the list. For every item added, the page redirects to itself, updating any changes to the summary cards.

### Breakdown Page

The Breakdown page is accessed via the Home page, by selecting a specific list. This is the most in depth page currently available to describe the selected list.

At first glance, there are a few sentences nested at the top, with a table below. Key phrases are highlighted in green or red text to emphasize the state of the current list.

Depending on a few basic conditions, the breakdown is able to state if the budget is sufficient or in deficit. If the budget is insufficient, the page provides hyperlinks for the user to remove items from the list or to change the set budget.

Beside the table, the breakdown also states the running total of entry, unit, budget, cost, and net values upfront.

### Set Budget Page

The Set Budget page, accessed via the navigation bar, simply provides all available lists in a selection menu, with an adjacent form field to input a new budget.

The only constraint for this function is that the budget cannot be set to zero or negative values.

Once the relevant values are inputted and the set budget button is selected, the page redirects to itself, where the updated budget value is shown.


### Remove Items

The Remove Items page, accessed via the nvigation bar, has a few functions.

The first is the option to select a list and permanently delete it, along with all associated item entries with the list. This can be accessed via the topmost red outline button, opening up a modal dialogue for further user confirmation, similiar to the Create New List button in the Build List page.

This page also displays summary cards, for every available list. For each list that has at least one item that can be removed, a yellow button appears on the list. Clicking it will redirect the user to a page similar to the Breakdown page, but it is also equipped with item deletion options via a selection list.

For any summary card that does not have an item to delete, the option to remove items is disabled on the card. The yellow button is instead a dull grey, and the option cannot be selected.


## Executing the application

I am aware of the below three methods for executing this application.

Of course, there should be many other methods. The below three are intended for simplicity and for those familiar with the CS50 course.

### CS50 IDE

- This project's source code was written and developed using CS50's IDE for convenience.
- Acquire CS50 IDE.
- Download project files.
- Upload the files to CS50 IDE, then simply `cd` into the project directory.
- Run the flask application via `flask run`, then open the generated URL.
- After using the application, use `CTRL + C` to terminate flask server.

### Python (Windows)

- Install Python
- Download project files into a local directory.
- Using the Command Prompt, `cd` into the local directory.
  - If this is the first time running the application in the current directory, create a one-time virtual environment `py -3 -m venv venv`.
- Activate the virtual environment `venv\Scripts\activate`.
  - If this is the first time running the application in the current directory, run `pip install -r requirements.txt` for the dependencies.
- Set the flask app environment variable for current directory by running `set FLASK_APP=application.py`.
  - This will need to be run every time the Command Prompt is closed.
  - Alternatively, just rename the application.py file to app.py to skip this step entirely.
- Run the flask applicaion via `flask run`, then open the generated URL in your browser.
- After using the application, use `CTRL + C` to terminate flask server.
  - `deactivate` in Command Prompt to deactivate the `venv`

### Replit IDE
- Clone/upload project files for repl.
- Run `pip install -r requirements.txt` for dependencies.
- Export the flask app environment variable for repl directory by running `export FLASK_APP=application.py`.
- Run flask application via `flask run --host=0.0.0.0 --port=8080`, then open the generated repl.co URL link found within the preview panel.
- Use `CTRL + C` to terminate flask server.

## Potential Contributions / Improvements

The below are potential ideas that could further improve upon this concept:

- Tidy mobile accessibility, as the HTML could use some improvement when it comes to resizing cards
- Change passwords and usernames, delete accounts functions.
- Rename lists.
- Change existing data on lists.
- Share lists with other users.
- Publically deploy the application online

## License

MIT
