#---------------------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------------------

# Importing the necessary libraries and modules.
from flask import Flask, render_template, request, session, url_for, flash,redirect,abort
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine,exc
import traceback
from functools import wraps

#---------------------------------------------------------------------------------------
# Create Flask App & Connect to Database
#---------------------------------------------------------------------------------------

# Declaring the database access credentials.
# For security reasons, these credentials were only included in Google App Engine.
# ↓
user = ""
passw = ""
host = ""
database = ""

#Initializing Flask app.
app = Flask(__name__)

# Setting the secret key used by Flask to securely sign cookies and other data.
app.config['SECRET_KEY'] = 'DO_NOT_LOSE_THIS_KEY'

# Configuring the SQLAlchemy database URI to connect to the MySQL database.
app.config["SQLALCHEMY_DATABASE_URI"] = host

# Establishing the connection with the MySQL database using the provided credentials.
def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
        connect_args = {'connect_timeout': 10})
    try: 
        conn = db.connect()
        return conn
    except Exception as e:
        # The server encountered an unexpected condition that prevented it from fulfilling the request.
        return {"message": "'Internal Server Error: Database Offline"}, 500

# When utilizing SQLAlchemy, the engine's connection pool will automatically close connections that haven't 
# been utilized in a while.

#---------------------------------------------------------------------------------------
# User Session Management Utilities
#---------------------------------------------------------------------------------------

# Ensuring the user is logged in before accessing specific routes.
def login_required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Checking if 'current_user' is in the session.
        if 'current_user' not in session:
            # Redirecting the user to the login page or show an error.
            return redirect(url_for("login"))
        # Executing the wrapped function if the user is logged in.
        return func(*args, **kwargs)
    # Returning the decorated function.
    return decorated_view


# Logging in the user by adding their information to the session.
def login_user(user_id, username):
    # Storing the 'user_id' and 'username' in the session under 'current_user'.
    session['current_user'] = {'user_id': user_id,
                               'username': username}


# Logging out the user by removing their information from the session.
def logout_user():
    try:
        # Removing 'current_user' from the session.
        session.pop('current_user')
    except Exception as e:
        # Printing the exception.
        print(e)


#---------------------------------------------------------------------------------------
# Create Flask Routes
#---------------------------------------------------------------------------------------

# ------------------------
# Index Route
# ------------------------

# Creating the index route, the login page. 
@app.route("/")
@app.route("/login")
def login():
    if 'current_user' in session:
        # By redirecting, flask will yield the 302 default html status code (in this one and in the next ones).
        return redirect(url_for("catalog"))
    # Rendering the login page.
    return render_template("index.html"),200


# ------------------------
# Catalog Route
# ------------------------

# Creating the catalog route.
@app.route("/catalog")
@login_required
def catalog():
    # Rendering the catalog page.
    return render_template("catalog.html"),200
    

# ------------------------
# Handle-Login Route
# ------------------------

# Creating a handle-login route that will compare the user input credentials against the database stored data. 
@app.route("/handle-login", methods=["POST"])
def handle_login():

    # Assigning the user input credentials to a 'username' and 'password' variables.
    username = request.form['username']
    password = request.form['password']

    # Confirming in the database, using this query, if the entered user credentials are correct.
    select = f"""
    SELECT user_id, password
    FROM users
    WHERE username='{username}';
    """

    # Connecting to the users database.
    conn = connect()
    
    # Querying the database for the entered 'username'.
    response = conn.execute(select).fetchone()
    print(response)
    
    # Checking if the 'username' is in the database.
    if response is not None:

        # Scenario 1 - Yes
        # Checking if the entered 'password' matches the stored 'password' using check_password_hash function.
        check_password = check_password_hash(response[1], password)
        
        # In case the 'password' is correct, store the 'username' and 'user_id' in session and redirect to catalog route.
        if check_password != False:

            # Storing the user's 'username' and 'user_id' to create a session.
            print(username,response[0])
            login_user(response[0],username)

            # Redirecting to the catalog page.
            return redirect(url_for("catalog"))

    # Scenario 2 - No
    # Displaying an error flash message to notify the user of incorrectly entered credentials.
    flash('Incorrect username or password. Please try again.',category='danger')
    # Redirecting to the login page.
    return redirect(url_for("login"))


# ------------------------
# Registration Route
# ------------------------

# Creating a registration route, where corporate users will register themselves in the J&M web page.
@app.route("/registration")
def registration():
    if 'current_user' in session:
        return redirect(url_for("catalog"))
    # Rendering the registration page.
    return render_template("registration.html"),200


# --------------------------
# Handle-Registration Route
# --------------------------

# Creating a handle-registration route that will reject or store the user input credentials into the database.
@app.route("/handle-registration", methods=["POST"])
def handle_registration():
    # Getting the 'username' and 'password' from the submitted form.
    username = request.form.get("username")
    password = request.form.get("password")
    print(username,password)

    # Checking, using this query, if the 'username' already exists in the database.
    query = f"SELECT username FROM users WHERE username = '{username}'"
    conn = connect()
    try:
        # Executing the query.
        result = conn.execute(query).fetchone()
        print(result)
        if result:
            # Scenario 1: Yes.
            # The 'username' already exists, so render a flash message notifying the user.
            flash('The username you entered already exists, please choose another one.',category='danger')
            # Redirecting to the registration page.
            return redirect(url_for('registration'))
        
        else:
            # Scenario 2: No.
            # The 'username' does not exist, so the new user credentials will be stored into the database.
            hashed_password = generate_password_hash(password)

            # Storing the credentials using the following query.
            insert_query = f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed_password}')"

            # Executing the query.
            conn.execute(insert_query)

            # Getting the 'user_id' for the newly inserted user using the following query.
            user_query = f"SELECT user_id FROM users WHERE username = '{username}'"

            # Executing the query.
            result = conn.execute(user_query).fetchone()
            print(result)
            user_id = result[0]
            print('user id',user_id)

            # Saving the 'user_id' and 'username' in the session.
            login_user(user_id, username)

            # Redirecting to the catalog page.
            return redirect(url_for("catalog"))

    # Handling exceptions related to SQLAlchemy errors.
    except exc.SQLAlchemyError as e:
        # Printing the error message.
        print(f"error: {e}")
        # Printing the full traceback to help with debugging.
        print(traceback.format_exc())
        # Displaying an error flash message to notify the user of a possible error.
        flash('A database error occurred. Please try again later.',category='danger')
        # Redirecting the user back to the registration page.
        return redirect(url_for('registration'))

# ------------------------
# Logout Route
# ------------------------

# Creating a logout route that will return the user to the login page.
@app.route("/logout")
@login_required
def logout():

    # Killing the user's saved session.
    logout_user()

    # Redirecting to the login page.
    return redirect(url_for("login"))

# ------------------------
# Handle-404 Error Route
# ------------------------

# Creating a 404 Error route for when the user searches a page route that doesn't exist.
@app.errorhandler(404)
def handle_not_found_error(e):
    # Rendering the 404 error page.
    return render_template('404_error.html'), 404

#---------------------------------------------------------------------------------------
# Run Flask
#---------------------------------------------------------------------------------------

# Running the Flask application when the Python script is executed.
if __name__ == '__main__':
    app.run(debug=True)