import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, dict_factory

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = sqlite3.connect('language.db', check_same_thread=False)
print("Connection established ..........")
cursor = db.cursor()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Make index function, this has no GET or POST method intentionally
@app.route("/")
@login_required
def index():
    # Render template of index with the information as coorilating with html names
    return render_template("index.html")


# BUY function, this has GET and POST method intentionally
@app.route("/anishgames", methods=["GET", "POST"])
@login_required
def anishgames():

    # Render template for anishgames, loads available games to chose from
    return render_template("anishgames.html")


# HISTORY function, this has no GET or POST method intentionally
@app.route("/history")
@login_required
def history():
    # Create a transactions variable from a SQL query using session user_id
    user = session["user_id"]
    print("farting.......")
    print("fart fart fart")
    print(session["user_id"])
    cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user,))
    transactions = cursor.fetchall()
    for transaction in transactions:
        print(transaction)

    # Render history html with transactions data for the current user displayed on html
    return render_template("history.html", transactions=transactions)


# HISTORY function, this has no GET or POST method intentionally
@app.route("/dictionary")
@login_required
def dictionary():
    # Create a transactions variable from a SQL query using session user_id
    cursor.execute("SELECT * FROM anishinaabemowin")
    dictionarys = cursor.fetchall()
    # for dictionary in dictionarys:
        # print(dictionary)

    # Render history html with transactions data for the current user displayed on html
    return render_template("dictionary.html", dictionarys=dictionarys)


# LOGIN function, this has GET and POST method intentionally
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
        rows = cursor.fetchall()
        print(rows)
        print(rows[0][2])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # If request method is GET, render login html
    else:
        return render_template("login.html")


# LOGOUT function, this has no GET or POST method intentionally
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# QUOTE function, this has GET and POST method intentionally
@app.route("/lessons", methods=["GET", "POST"])
@login_required
def lessons():
    return render_template("lessons.html")


# REGISTER function, this has GET and POST method intentionally
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    # if POST method, register user for site
    if request.method == "POST":
        # Create username, password, and confirmation variables to store user input from register html
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # If username is empty, give apology
        if not username:
            return apology("must provide username", 400)

        # If password is empty, give apology
        elif not password:
            return apology("must provide password", 400)

        # If confirmation is empty, give apology
        elif not confirmation:
            return apology("must confirm password", 400)

        # If password and confirmation do not match, give apology
        elif password != confirmation:
            return apology("password must match", 400)

        # Else, create rows variable
        else:
            cursor.execute("SELECT username FROM users WHERE username = ?", [request.form.get("username")])
            rows = cursor.fetchall()

            # Check if someone already has the username
            # If the length of row is great than or equal to 1, give apology
            if len(rows) >= 1:
                return apology("username already in use", 400)

            # Else, store the password as a hash of the password for encryption/security
            else:
                hash = generate_password_hash(password)

                # Remember registrant
                cursor.execute("INSERT INTO users (username, hashpass) VALUES(?, ?)", [username, hash])
                #Commit your changes in the database
                db.commit()

        # Redirect to homepage
        return redirect("/")

    # If request method is GET, render register html
    else:
        return render_template("register.html")


# SELL function, this has GET and POST method intentionally
@app.route("/anishwordle", methods=["GET", "POST"])
@login_required
def anishwordle():
    # Create user variable to store session user_id
    user = session["user_id"]
    print("farting.......")
    print("fart fart fart")
    print(session["user_id"])
    # Create rewardbalance variable and SQL query to get current rewards balance from users for current session id, pair down to number
    cursor.execute("SELECT rewards FROM users WHERE id = ?", (user,))
    rewardbalance = cursor.fetchall()
    print(rewardbalance)
    for row in rewardbalance:
        print(row)
    user_rewards = row[0]
    print("fart")
    print(user_rewards)

    # Create points_requested variable to store user input of request points to exchange
    new_reward = 10
    newrewards = user_rewards + new_reward
    print(newrewards)
    cursor.execute("UPDATE users SET rewards = ? WHERE id = ?", (newrewards, user,))
    #Commit your changes in the database
    db.commit()
    print("table updated....farted")

    # Create variables learningtype and learningmodule to pass in learning_type and learning_module
    learningtype = "Game"
    learningmodule = "Wordle"

    # Insert the new transaction into transactions SQL table with data stored in variables
    db.execute(
        "INSERT INTO transactions(user_id, learning_type, learning_module, points_acquired) VALUES(?, ?, ?, ?)",
        (user,
        learningtype,
        learningmodule,
        new_reward,)
    )
    db.commit()

    # Attempted to create word list to pass to game, will continue to work on this after submission
    # dictionarys = db.execute
    # ("SELECT word FROM anishinaabemowin WHERE length = '5'")

    # Render anishwordle template
    return render_template("anishwordle.html")


# SELL function, this has GET and POST method intentionally
@app.route("/originalman", methods=["GET", "POST"])
@login_required
def originalman():
    # Create user variable to store session user_id
    user = session["user_id"]
    print("farting.......")
    print("fart fart fart")
    print(session["user_id"])

    # Create rewardbalance variable and SQL query to get current rewards balance from users for current session id, pair down to number
    cursor.execute("SELECT rewards FROM users WHERE id = ?", (user,))
    rewardbalance = cursor.fetchall()
    print(rewardbalance)
    for row in rewardbalance:
        print(row)
    user_rewards = row[0]
    print("fart")
    print(user_rewards)

    # Create points_requested variable to store user input of request points to exchange
    new_reward = 10
    newrewards = user_rewards + new_reward
    print(newrewards)
    cursor.execute("UPDATE users SET rewards = ? WHERE id = ?", (newrewards, user,))
    #Commit your changes in the database
    db.commit()
    print("table updated....farted")

    # create learningtype and learningmodule to pass in learning_type and learning_module
    learningtype = "Game"
    learningmodule = "Originalman"

    # INSERT the new transaction into transactions SQL table with data stored in variables
    db.execute(
        "INSERT INTO transactions(user_id, learning_type, learning_module, points_acquired) VALUES(?, ?, ?, ?)",
        (user,
        learningtype,
        learningmodule,
        new_reward,)
    )
    db.commit()

    # Attempted to create word list from SQL table to pass into game, will continue to work on this after submission
    # dodems = db.execute("SELECT word FROM anishinaabemowin WHERE category = 'Dodems'")
    # miijim = db.execute("SELECT word FROM anishinaabemowin WHERE category = 'Food'")
    #clans = db.execute("SELECT translation FROM anishinaabemowin WHERE category = 'Dodems'")
    #food = db.execute("SELECT translation FROM anishinaabemowin WHERE category = 'Food'")

    # Render originalman template
    return render_template("originalman.html")


# REWARDS function, this has GET and POST method intentionally
@app.route("/rewards", methods=["GET", "POST"])
@login_required
def rewards():
    """Show reward points and exchange for ziizbaakdoons"""

    # Create user variable to store session user_id
    user = session["user_id"]
    print("farting.......")
    print("fart fart fart")
    print(session["user_id"])

    # Create rewardbalance variable and SQL query to get current rewards balance from users for current session id, pair down to number
    cursor.execute("SELECT rewards, ziizbaakdoons FROM users WHERE id = ?", (user,))
    rewardbalance = cursor.fetchall()
    print(rewardbalance)
    for row in rewardbalance:
        print(row)
    user_rewards = row[0]
    zpoints = row[1]
    print("fart")
    print(user_rewards)
    print(zpoints)

    # if POST method, exchange rewards for ziibaakdoons or exchange ziizbaakdoons for culture kits
    if request.method == "POST":
        # if request.form for points, exchange points for ziizbaakdoons
        if request.form.get("points"):
            # Create points_requested variable to store user input of request points to exchange
            points_requested = request.form.get("points")

            # If points_requested is empty, give apology
            if not points_requested:
                return apology("no reward points selected", 400)

            # If points_requested is not a digit, give apology
            if not points_requested.isdigit():
                return apology("Invalid points", 400)

            # If the user input points is a digit and is not empty, continue to exchange points
            else:
                # Create variables for rewards, newziibaakdoons, newrewards to add to SQL tables
                redeem_rewards = int(points_requested)
                newzpoints = zpoints + redeem_rewards
                newrewards = user_rewards - redeem_rewards

                # If newrewards is less than 0, give apology
                if newrewards < 0:
                    return apology("not enough rewards points", 400)

                # Else, UPDATE users rewards and ziibaakdoons in users SQL table
                else:
                    db.execute(
                        "UPDATE users SET rewards = ?, ziizbaakdoons = ? WHERE id = ?",
                        (newrewards,
                        newzpoints,
                        user,)
                    )
                    db.commit()

            # Redirect to rewards, we want to auto refresh rewards html when user makes a rewards transaction
            return redirect("/rewards")

        # if request.form for hairfeather, exchange ziizbaakdoons for kit
        elif request.form.get("hairfeather"):
            # Create variables to store learning_type, learning_module, cost, and newziibaakdoons to pass into SQL tables
            learningtype = "Rewards"
            learningmodule = "Hair Feather Kit"
            cost = 100
            newzpoints = zpoints - cost

            # If newziizbackdoons is less than 0, give apology
            if newzpoints < 0:
                return apology("not enough ziizbaakdoons", 400)

            # Else, the user input has been verified and the user has enough ziizbaakdoons to trade for kit
            else:
                # Insert transaction into transactions SQL table
                db.execute(
                    "INSERT INTO transactions(user_id, learning_type, learning_module, points_spent) VALUES(?, ?, ?, ?)",
                    (user,
                    learningtype,
                    learningmodule,
                    cost,)
                )
                db.commit()

                # Update ziizbaakdoons total for user in user SQL table
                db.execute(
                    "UPDATE users SET ziizbaakdoons = ? WHERE id = ?",
                    (newzpoints,
                    user,)
                )
                db.commit()

                # Redirect to rewards, we want to auto refresh rewards html when user makes a rewards transaction
                return redirect("/rewards")

        # if request.form for medicinebag, exchange ziizbaakdoons for kit
        elif request.form.get("medicinebag"):
            # Create variables to store learning_type, learning_module, cost, and newziibaakdoons to pass into SQL tables
            learningtype = "Rewards"
            learningmodule = "Parfleche Medicine Bag Kit"
            cost = 100
            newzpoints = zpoints - cost

            # If newziizbackdoons is less than 0, give apology
            if newzpoints < 0:
                return apology("not enough ziizbaakdoons", 400)

            # Else, the user input has been verified and the user has enough ziizbaakdoons to trade for kit
            else:
                # Insert transaction into transactions SQL table
                db.execute(
                    "INSERT INTO transactions(user_id, learning_type, learning_module, points_spent) VALUES(?, ?, ?, ?)",
                    (user,
                    learningtype,
                    learningmodule,
                    cost,)
                )
                db.commit()

                # Update ziizbaakdoons total for user in user SQL table
                db.execute(
                    "UPDATE users SET ziizbaakdoons = ? WHERE id = ?",
                    (newzpoints,
                    user,)
                )
                db.commit()

                # Redirect to rewards, we want to auto refresh rewards html when user makes a rewards transaction
                return redirect("/rewards")

        # if request.form for dreamcatcher, exchange ziizbaakdoons for kit
        elif request.form.get("dreamcatcher"):
            # Create variables to store learning_type, learning_module, cost, and newziibaakdoons to pass into SQL tables
            learningtype = "Rewards"
            learningmodule = 'Dream Catcher Kit - 6"'
            cost = 100
            newzpoints = zpoints - cost

            # If newziizbackdoons is less than 0, give apology
            if newzpoints < 0:
                return apology("not enough ziizbaakdoons", 400)

            # Else, the user input has been verified and the user has enough ziizbaakdoons to trade for kit
            else:
                # Insert transaction into transactions SQL table
                db.execute(
                    "INSERT INTO transactions(user_id, learning_type, learning_module, points_spent) VALUES(?, ?, ?, ?)",
                    (user,
                    learningtype,
                    learningmodule,
                    cost,)
                )
                db.commit()

                # Update ziizbaakdoons total for user in user SQL table
                db.execute(
                    "UPDATE users SET ziizbaakdoons = ? WHERE id = ?",
                    (newzpoints,
                    user,)
                )
                db.commit()

                # Redirect to rewards, we want to auto refresh rewards html when user makes a rewards transaction
                return redirect("/rewards")

        # if request.form for dancestick, exchange ziizbaakdoons for kit
        elif request.form.get("dancestick"):
            # Create variables to store learning_type, learning_module, cost, and newziibaakdoons to pass into SQL tables
            learningtype = "Rewards"
            learningmodule = "Deluxe Dancestick Kit"
            cost = 200
            newzpoints = zpoints - cost

            # If newziizbackdoons is less than 0, give apology
            if newzpoints < 0:
                return apology("not enough ziizbaakdoons", 400)

            # Else, the user input has been verified and the user has enough ziizbaakdoons to trade for kit
            else:
                # Insert transaction into transactions SQL table
                db.execute(
                    "INSERT INTO transactions(user_id, learning_type, learning_module, points_spent) VALUES(?, ?, ?, ?)",
                    (user,
                    learningtype,
                    learningmodule,
                    cost,)
                )
                db.commit()

                # Update ziizbaakdoons total for user in user SQL table
                db.execute(
                    "UPDATE users SET ziizbaakdoons = ? WHERE id = ?",
                    (newzpoints,
                    user,)
                )
                db.commit()

                # Redirect to rewards, we want to auto refresh rewards html when user makes a rewards transaction
                return redirect("/rewards")

        # if request.form for beadworkstarter, exchange ziizbaakdoons for kit
        elif request.form.get("beadworkstarter"):
            # Create variables to store learning_type, learning_module, cost, and newziibaakdoons to pass into SQL tables
            learningtype = "Rewards"
            learningmodule = "Beadwork Starter Kit"
            cost = 200
            newzpoints = zpoints - cost

            # If newziizbackdoons is less than 0, give apology
            if newzpoints < 0:
                return apology("not enough ziizbaakdoons", 400)

            # Else, the user input has been verified and the user has enough ziizbaakdoons to trade for kit
            else:
                # Insert transaction into transactions SQL table
                db.execute(
                    "INSERT INTO transactions(user_id, learning_type, learning_module, points_spent) VALUES(?, ?, ?, ?)",
                    (user,
                    learningtype,
                    learningmodule,
                    cost,)
                    )
                db.commit()

                # Update ziizbaakdoons total for user in user SQL table
                db.execute(
                    "UPDATE users SET ziizbaakdoons = ? WHERE id = ?",
                    (newzpoints,
                    user,)
                )
                db.commit()

                # Redirect to rewards, we want to auto refresh rewards html when user makes a rewards transaction
                return redirect("/rewards")

        # if request.form for beadloom, exchange ziizbaakdoons for kit
        elif request.form.get("beadloom"):
            # Create variables to store learning_type, learning_module, cost, and newziibaakdoons to pass into SQL tables
            learningtype = "Rewards"
            learningmodule = "Wire Bead Loom Kit"
            cost = 200
            newzpoints = zpoints - cost

            # If newziizbackdoons is less than 0, give apology
            if newzpoints < 0:
                return apology("not enough ziizbaakdoons", 400)

            # Else, the user input has been verified and the user has enough ziizbaakdoons to trade for kit
            else:
                # Insert transaction into transactions SQL table
                db.execute(
                    "INSERT INTO transactions(user_id, learning_type, learning_module, points_spent) VALUES(?, ?, ?, ?)",
                    (user,
                    learningtype,
                    learningmodule,
                    cost,)
                )
                db.commit()

                # Update ziizbaakdoons total for user in user SQL table
                db.execute(
                    "UPDATE users SET ziizbaakdoons = ? WHERE id = ?",
                    (newzpoints,
                    user,)
                )
                db.commit()

                # Redirect to rewards, we want to auto refresh rewards html when user makes a rewards transaction
                return redirect("/rewards")

    # If request method is GET, render rewards html, add user_rewards and ziibaakdoons to display on html with GET
    else:
        return render_template(
            "rewards.html", user_rewards=user_rewards, ziizbaakdoons=zpoints
        )
