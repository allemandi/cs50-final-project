from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")


@app.route("/")
@login_required
def index():
    """Show home, with all said lists"""

    valid_lists = db.execute("SELECT list_name, budget FROM list_budget WHERE user_id=:user_id ORDER BY list_name ASC",user_id=session['user_id'])
    # Query Cash of current user from user table
    valid_lists_items = db.execute("SELECT item_name, item_cost, item_num, list_budget.list_name as list_title FROM item_list JOIN list_budget ON item_list.list_name=list_budget.list_name WHERE item_list.user_id=:user_id AND list_budget.user_id=:user_id ORDER BY list_budget.list_id",user_id=session['user_id'])

    any_lists = len(valid_lists)

    # html_valid contains list name, budget, total cost of list and net value of list
    html_valid = []


    # html_list contains item names, item price, number of items, and total cost of each item type (inclusive of volume)
    html_list = []

    for row in valid_lists:
        temp_dictionary = {}
        list_cost = 0
        temp_dictionary['list_name'] = row['list_name']
        temp_dictionary['budget'] = row['budget']
        for item_row in valid_lists_items:
            if row['list_name'] == item_row['list_title']:
                list_cost += item_row['item_cost'] * item_row['item_num']
        temp_dictionary['total_cost'] = list_cost
        temp_dictionary['net_value'] = row['budget'] - list_cost
        html_valid.append(temp_dictionary)


    for row in valid_lists_items:
        # set empty dictionary each time per loop, then assign key: values pairs
        temp_dictionary = {}

        # list name
        temp_dictionary['list_name'] = row['list_title']

        temp_dictionary['item_num'] = row['item_num']
        temp_dictionary['item_name'] = row['item_name']
        temp_dictionary['item_cost'] = row['item_cost']
        temp_dictionary['item_total'] = row['item_num'] * float(row['item_cost'])


        html_list.append(temp_dictionary)


    return render_template("home.html", any_lists=any_lists, html_list=html_list, html_valid=html_valid)


@app.route("/set_budget", methods=["GET", "POST"])
@login_required
def set_budget():
    """Set budget for lists here"""

    # CREATE TABLE list_budget(list_id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, list_name TEXT NOT NULL, list_budget NUMERIC NOT NULL);



    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        selected_list = request.form.get("list_name")
        set_budget = request.form.get("set_budget")

        db.execute("UPDATE list_budget SET budget =:budget WHERE list_name=:list_name AND user_id=:user_id", budget=set_budget,list_name=selected_list,user_id=session['user_id'])

        budget_options = db.execute("SELECT list_name, budget from list_budget WHERE user_id=:user_id", user_id=session['user_id'])

        #Flash the additional cash and return to index
        flash('Budget for ' + selected_list + ' set to ' + '$' + set_budget)


        return render_template("set_budget.html", budget_options=budget_options)

    else:

        budget_options = db.execute("SELECT list_name, budget from list_budget WHERE user_id=:user_id", user_id=session['user_id'])
        return render_template("set_budget.html", budget_options=budget_options)


@app.route("/build", methods=["GET", "POST"])
@login_required
def build():

    """build list"""

    all_lists = db.execute("SELECT list_name, budget FROM list_budget WHERE user_id=:user_id ORDER BY list_name ASC",user_id=session['user_id'])


    valid_lists = db.execute("SELECT list_budget.list_name as list_name, SUM(item_num) as total_items FROM list_budget JOIN item_list on item_list.list_name = list_budget.list_name WHERE list_budget.user_id=:user_id AND item_list.user_id=:user_id GROUP BY item_list.list_name ORDER BY item_list.list_name ASC",user_id=session['user_id'])
    valid_lists_items = db.execute("SELECT item_name, item_cost, item_num, list_budget.list_name as list_title FROM item_list JOIN list_budget ON item_list.list_name = list_budget.list_name WHERE list_budget.user_id=:user_id AND item_list.user_id=:user_id ORDER BY list_budget.list_id",user_id=session['user_id'])


    # html_valid contains list name, budget, total cost of list and net value of list
    html_valid = []


    # html_list contains item names, item price, number of items, and total cost of each item type (inclusive of volume)
    html_list = []
    total_items = 0

    for row in all_lists:
        temp_dictionary = {}
        temp_dictionary['list_name'] = row['list_name']
        temp_dictionary['budget'] = row['budget']
        temp_dictionary['total_entries'] = 0
        list_cost = 0
        for item_row in valid_lists_items:
            if row['list_name'] == item_row['list_title']:
                list_cost += item_row['item_cost'] * item_row['item_num']
                temp_dictionary['total_entries'] += 1
        temp_dictionary['total_items'] = 0
        for valid_row in valid_lists:
            if row['list_name'] == valid_row['list_name']:
                temp_dictionary['total_items'] = valid_row['total_items']

        temp_dictionary['total_cost'] = list_cost
        temp_dictionary['net_value'] = row['budget'] - list_cost
        html_valid.append(temp_dictionary)


    for row in valid_lists_items:
        # set empty dictionary each time per loop, then assign key: values pairs
        temp_dictionary = {}

        # list name
        temp_dictionary['list_name'] = row['list_title']

        temp_dictionary['item_num'] = row['item_num']
        temp_dictionary['item_name'] = row['item_name']
        temp_dictionary['item_cost'] = row['item_cost']
        temp_dictionary['item_total'] = row['item_num'] * float(row['item_cost'])


        html_list.append(temp_dictionary)


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if "add_list" in request.form:

            if not request.form['new_list_name'] or not request.form['set_new_budget']:
                flash("Error: Not Added. Please complete all necessary fields")
                return redirect("/build")

            list_name = request.form['new_list_name']

            rows = db.execute("SELECT * FROM list_budget WHERE list_name=:list_name AND user_id=:user_id", list_name=list_name, user_id=session['user_id'])

            if len(rows) != 0:
                flash("Error: Already Exists, Please Use Another Name.")
                return redirect("/build")

            else:
                db.execute("INSERT INTO list_budget (user_id,list_name,budget) VALUES (:user_id,:list_name,:budget)",
                        user_id=session['user_id'],
                        list_name=request.form['new_list_name'],
                        budget=request.form['set_new_budget'])
                flash("List Added")
                return redirect("/build")

        elif "add_item" in request.form:
            if not request.form.get("list_name") or not request.form.get("item_name") or not request.form.get("item_cost") or not request.form.get("item_num"):
                flash("Error. Not Added. Please complete all necessary fields")
                return render_template("build.html", html_list=html_list,html_valid=html_valid)

            db.execute("INSERT INTO item_list (user_id,list_name,item_name,item_cost,item_num) VALUES (:user_id,:list_name,:item_name,:item_cost,:item_num)",
                    user_id=session['user_id'],
                    list_name=request.form.get("list_name"),
                    item_name=request.form.get("item_name"),
                    item_cost=request.form.get("item_cost"),
                    item_num=request.form.get("item_num"))

            flash("Item Added")
            return redirect("/build")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("build.html", html_list=html_list,html_valid=html_valid)


@app.route("/breakdown", methods=["GET", "POST"])
@login_required
def breakdown():
    """Show portfolio"""

    if request.method == "POST":

        # get breakdown from homepage
        list_name = request.form['break_value']

        list_budget_row = db.execute("SELECT budget FROM list_budget WHERE user_id=:user_id AND list_name=:list_name",user_id=session['user_id'],list_name=list_name)

        budget = list_budget_row[0]['budget']

        list_items = db.execute("SELECT item_name, item_cost, item_num FROM item_list WHERE user_id=:user_id AND list_name=:list_name",user_id=session['user_id'],list_name=list_name)

        # html list contains item names, item price, number of items, and total cost of each item type (inclusive of volume)
        html_list = []
        list_cost = 0
        unit_count = 0

        for row in list_items:
            # set empty dictionary each time per loop, then assign key: values pairs
            temp_dictionary = {}

            temp_dictionary['item_name'] = row['item_name']
            temp_dictionary['item_num'] = row['item_num']
            temp_dictionary['item_cost'] = row['item_cost']
            temp_dictionary['item_total'] = row['item_num'] * row['item_cost']
            unit_count += row['item_num']
            html_list.append(temp_dictionary)

            # keep list cost separate but still within the same loop
            list_cost += temp_dictionary['item_total']

        net_value = budget - list_cost

        # consolidate money values into list for convenient access
        money_list = []
        money_dictionary = {}
        money_dictionary['entry_count'] = len(list_items)
        money_dictionary['unit_count'] = unit_count
        money_dictionary['list_name'] = list_name
        money_dictionary['budget'] = budget
        money_dictionary['list_cost'] = list_cost
        money_dictionary['net_value'] = net_value
        money_list.append(money_dictionary)


        return render_template("breakdown.html",html_list=html_list,money_list=money_list)
    else:




        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username and password fields were submitted
        if not request.form.get("username") or not request.form.get("password"):
            flash("Fields missing. Please submit user login details")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username =:username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]


        # Redirect user to home page
        flash("Successful Login")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Logged Out")
    return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register learner"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")

        # Ensure username was submitted
        if not request.form.get("password") == request.form.get("confirmation"):
            flash("Error: Password Mismatch.")
            return redirect("/register")

        rows = db.execute("SELECT * FROM users WHERE username =:username",
                          username=username)

        # Ensure exist if username already exists
        if len(rows) == 1:
            flash("Error: Username Already Exists.")
            return redirect("/register")

        hash = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username,hash) VALUES (:username,:hash)",username=username,hash=hash)

        # Redirect user to home page
        flash("Account Registered")
        return render_template("login.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/remove_items", methods=["GET", "POST"])
@login_required
def remove_items():
    # Remove item menu

    # get all lists from sql db
    all_lists = db.execute("SELECT list_name, list_id, budget FROM list_budget WHERE user_id=:user_id ORDER BY list_name ASC",user_id=session['user_id'])

    # get all the valid lists that actually have items to remove
    valid_lists = db.execute("SELECT list_budget.list_name as list_name, SUM(item_num) as total_items FROM list_budget JOIN item_list on item_list.list_name = list_budget.list_name WHERE list_budget.user_id=:user_id AND item_list.user_id=:user_id GROUP BY item_list.list_name ORDER BY item_list.list_name ASC",user_id=session['user_id'])

    # get all valid items to remove
    valid_lists_items = db.execute("SELECT item_name, item_cost, item_num, list_budget.list_name as list_title FROM item_list JOIN list_budget ON item_list.list_name = list_budget.list_name WHERE list_budget.user_id=:user_id AND item_list.user_id=:user_id ORDER BY list_budget.list_id",user_id=session['user_id'])


    # html_valid contains list name, budget, total cost of list and net value of list
    html_valid = []


    # html_list contains item names, item price, number of items, and total cost of each item type (inclusive of volume)
    html_list = []
    total_items = 0

    # consolidate all_lists with valid lists and item lists for the general list information
    for row in all_lists:
        temp_dictionary = {}
        temp_dictionary['list_name'] = row['list_name']
        temp_dictionary['list_id'] = row['list_id']
        temp_dictionary['budget'] = row['budget']
        temp_dictionary['total_entries'] = 0
        list_cost = 0
        for item_row in valid_lists_items:
            if row['list_name'] == item_row['list_title']:
                list_cost += item_row['item_cost'] * item_row['item_num']
                temp_dictionary['total_entries'] += 1
        temp_dictionary['total_items'] = 0
        for valid_row in valid_lists:
            if row['list_name'] == valid_row['list_name']:
                temp_dictionary['total_items'] = valid_row['total_items']

        temp_dictionary['total_cost'] = list_cost
        temp_dictionary['net_value'] = row['budget'] - list_cost
        html_valid.append(temp_dictionary)



    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if "remove_list" in request.form:

            list_to_remove = request.form.get("list_to_remove")

            # Query database for list
            rows = db.execute("SELECT * FROM list_budget WHERE list_id=:list_id AND user_id=:user_id", list_id=list_to_remove, user_id=session['user_id'])

            # Ensure doubly that selected list exists
            if len(rows) != 1:
                flash("Please Select Valid List.")
                return redirect("/remove_items")

            # if so, delete from list_budget and item_list

            else:
                db.execute("DELETE from item_list WHERE list_name=:list_name AND user_id=:user_id",list_name=rows[0]['list_name'],user_id=session['user_id'])
                db.execute("DELETE from list_budget WHERE list_id=:list_id AND user_id=:user_id",list_id=list_to_remove,user_id=session['user_id'])

                flash("List Removed.")
                return redirect("/remove_items")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("remove_items.html",html_valid=html_valid)



@app.route("/remove_true", methods=["GET", "POST"])
@login_required
def remove_true():

    # This route appears once a specific list has been selected from the remove_items menu
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if "remove_items" in request.form:

            list_name = request.form['remove_items']

            list_budget_row = db.execute("SELECT budget FROM list_budget WHERE user_id=:user_id AND list_name=:list_name",user_id=session['user_id'],list_name=list_name)
            budget = list_budget_row[0]['budget']
            list_items = db.execute("SELECT item_id, item_name, item_cost, item_num FROM item_list WHERE user_id=:user_id AND list_name=:list_name",user_id=session['user_id'],list_name=list_name)

            # html list contains item names, item price, number of items, and total cost of each item type (inclusive of volume)
            html_list = []
            list_cost = 0

            for row in list_items:
                # set empty dictionary each time per loop, then assign key: values pairs
                temp_dictionary = {}
                temp_dictionary['item_id'] = row['item_id']
                temp_dictionary['item_name'] = row['item_name']
                temp_dictionary['item_num'] = row['item_num']
                temp_dictionary['item_cost'] = row['item_cost']
                temp_dictionary['item_total'] = row['item_num'] * row['item_cost']
                html_list.append(temp_dictionary)

                # keep list cost separate but still within the same loop
                list_cost += temp_dictionary['item_total']


            net_value = budget - list_cost

            # consolidate money values into list for convenient access
            money_list = []
            money_dictionary = {}
            money_dictionary['list_name'] = list_name
            money_dictionary['budget'] = budget
            money_dictionary['list_cost'] = list_cost
            money_dictionary['net_value'] = net_value
            money_list.append(money_dictionary)

            return render_template("remove_true.html",html_list=html_list,money_list=money_list)
        elif "remove_selection" in request.form:

            item_id = request.form.get("item_id")

            # Query database for list
            rows = db.execute("SELECT item_name FROM item_list WHERE item_id=:item_id AND user_id=:user_id", item_id=item_id, user_id=session['user_id'])



            # Ensure doubly that selected list exists
            if len(rows) != 1:
                flash("Error: Not Removed. Please Select Valid Item.")
                return redirect("/remove_items")


            else:
                item_name = rows[0]["item_name"]

                db.execute("DELETE from item_list WHERE item_id=:item_id AND user_id=:user_id",item_id=item_id,user_id=session['user_id'])

                flash("Removed: " + item_name)
                return redirect("/remove_items")

        else:
            return redirect("/remove_items")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return redirect("/remove_items")



