#---------------------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------------------

# Importing the necessary libraries and modules.
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from flask_restx import Api, Namespace, Resource
import retry
import json

#---------------------------------------------------------------------------------------
# Connection to the Database, Documentation Creation, and API Key Authentication
#---------------------------------------------------------------------------------------

# Defining the database access credentials.
# For security reasons, these credentials were only included in Google App Engine.
# ↓
user = ""
passw = ""
host = ""
database = ""

# Initializing Flask.
app = Flask(__name__)

# Configuring the SQLAlchemy database URI to connect to the MySQL database.
app.config["SQLALCHEMY_DATABASE_URI"] = host

# Creating the API Documentation general description.
api = Api(app, version = '2.0',
    title = 'J&M Business Data API',
    description = """
        This REST API built using Flask and Flask-Restx is intended to request and receive data from J&M MySQL database.
        """,
    contact = "joaoapinho@student.ie.edu",
    endpoint = "/api/v2"
)

# Establishing an API key for the authenticator.
# For security reasons, this key was only included in Google App Engine.
# ↓
auth_db = { 
    ''
}

# Establishing the connection with the MySQL database using the provided credentials.
@retry.retry(tries = 3, delay = 10)
def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
        connect_args = {'connect_timeout': 10})
    try: 
        conn = db.connect()
        return conn
    except Exception as e:
        return {"message": "'Internal Server Error: Database Offline"}, 500

# Defining the function for disconnecting from the MySQL database.
def disconnect(conn):
    conn.close()

#---------------------------------------------------------------------------------------
# Query Execution Function & Status Code Responses
#---------------------------------------------------------------------------------------

# Creating a function to execute all the queries.
def query_all(query):
    try:
        # Checking for the presence of "Authorization" in the request headers.
        if "Authorization" not in request.headers:
            # Returning an error response for unauthorized access.
            return json.dumps({'message': 'Authentication Error: Unauthorized Access.'}), 401
        else:
            # Extracting the token from the "Authorization" header.
            header = request.headers["Authorization"]
            token = header.split()[1]

            # Verifying if the token is present in the authentication database.
            if token not in auth_db:
                # Returning an error response for unauthorized access.
                return json.dumps({'message': 'Authentication Error: Unauthorized Access.'}), 401

        # Establishing a connection to the database.
        conn = connect()

        # Executing the query and fetching all results.
        result = conn.execute(query).fetchall()

        # Disconnecting from the database.
        disconnect(conn)

        # Returning the results as a JSON response.
        return jsonify({'result': [dict(row) for row in result]})
    
    except Exception as e:
        return json.dumps({"message": "'Internal Server Error: Database Offline"}), 500

# Defining responses for the API endpoint.
common_responses={
        200: 'Success',
        401: 'Authentication Error: Unauthorized Access',
        404: 'Resource Not Found Error: Not Found',
        500: 'Internal Server Error: Database Offline'
    }

#---------------------------------------------------------------------------------------
# Sales Namespace (Tab 1 KPIs and Charts)
#---------------------------------------------------------------------------------------

# Creating a namespace for Sales in order to isolate its endpoint groups.
sales = Namespace('Sales',
    description = 'Data related to Sales KPIs and Charts.',
    path='/api/v2')
api.add_namespace(sales)


# Create an API route for accessing the information needed to compute Sales KPIs and Charts.
# In order to avoid replication, only one endpoint was created since the information would be
# the same across all KPIs and Charts.
@sales.route("/sales/sales_data")

class select_sales(Resource):

    # Defining responses for the API endpoint.
    @api.doc(responses={**common_responses})

    # Declaring the SQL query to retrieve the sales data.
    def get(self):
        select = """
            SELECT t_dat, sales_channel_id, price, age, club_member_status
            FROM final_data
            LIMIT 900000;
            """
        # Returning the query execution function.
        return query_all(select)


#---------------------------------------------------------------------------------------
# Marketing Namespace (Tab 2 KPIs and Charts)
#---------------------------------------------------------------------------------------

# Creating a namespace for Marketing in order to isolate its endpoint groups.
marketing = Namespace('Marketing',
    description = 'Data related to Marketing KPIs and Charts.',
    path='/api/v2')
api.add_namespace(marketing)


# Create an API route for accessing the information needed to compute Marketing KPIs and Charts.
# In order to avoid replication and optimize loading times, only one endpoint was created for this tab
# since most of the information would be the same across all KPIs and Charts.
@marketing.route("/marketing/marketing_data")

class select_marketing(Resource):

    # Defining responses for the API endpoint.
    @api.doc(responses={**common_responses})

    # Declaring the SQL query to retrieve the marketing data.
    def get(self):
        select = """
            SELECT customer_id, t_dat, sales_channel_id, price, age, club_member_status, fashion_news_frequency
            FROM final_data
            LIMIT 900000;
            """
        # Returning the query execution function.
        return query_all(select)


#---------------------------------------------------------------------------------------
# Customer Preferences Namespace (Tab 3 Key Information and Charts)
#---------------------------------------------------------------------------------------

# Creating a namespace for Marketing in order to isolate its endpoint groups.
cust_pref = Namespace('Customer Preferences',
    description = 'Data related to Customer Preferences Information and Charts.',
    path='/api/v2')
api.add_namespace(cust_pref)


# Create an API route for accessing the information needed to find Customer Preferences Key Information and plot Charts.
# In order to avoid replication and optimize loading times, only one endpoint was created for this tab
# since most of the information would be the same across all Key Information and Charts.
@cust_pref.route("/cust_pref/cust_pref_data")

class select_pref(Resource):

    # Defining responses for the API endpoint.
    @api.doc(responses={**common_responses})

    # Declaring the SQL query to retrieve the customer preferences data.
    def get(self):
        select = """
            SELECT t_dat, sales_channel_id, price, age, club_member_status, article_id, product_type_name, colour_group_name
            FROM final_data
            LIMIT 900000;
            """
        # Returning the query execution function.
        return query_all(select)


#---------------------------------------------------------------------------------------
# Various Namespace (Other Useful API Endpoints, Outside the Streamlit Dashboard)
#---------------------------------------------------------------------------------------

# Creating a namespace for Various in order to isolate its endpoint groups.
various = Namespace('Various',
    description = 'Other useful endpoints outside the Streamlit Dashboard.',
    path='/api/v2')
api.add_namespace(various)

# Create an API endpoint for accessing the information of a customer based on its customer_id.
# Example to test: 00000dbacae5abe5e23885899a1fa44253a17956c6d1c3d25f88aa139fdfc657
@various.route("/various/customers/<string:id>")
@various.doc(params = {'id': 'The ID of the user'})

class select_info_id(Resource):

    # Defining responses for the API endpoint.
    @api.doc(responses={**common_responses})

    # Declaring the SQL query to retrieve the customer information data based on its id.
    def get(self, id):
        id = str(id)
        select = """
            SELECT *
            FROM customers
            WHERE customer_id = '{0}';""".format(id)
        # Returning the query execution function.
        return query_all(select)


# Create an API route for accessing the information of all customers that are club members.
@various.route("/various/customers/club-members")

class select_members(Resource):

    # Defining responses for the API endpoint.
    @api.doc(responses={**common_responses})

    # Declaring the SQL query to retrieve the customer information for all club members.
    def get(self):
        select = """
            SELECT *
            FROM customers
            WHERE club_member_status = 'ACTIVE'
            """
        # Returning the query execution function.
        return query_all(select)


# Create an API endpoint for accessing all transactions done by a customer based on its customer_id.
# Example to test: 00007d2de826758b65a93dd24ce629ed66842531df6699338c5570910a014cc2
@various.route("/various/transactions/<string:id>")
@various.doc(params = {'id': 'The ID of the user'})

class select_all_transactions_from_user(Resource):

    # Defining responses for the API endpoint.
    @api.doc(responses={**common_responses})

    # Declaring the SQL query to retrieve all transactions from a given customer based on its id.
    def get(self, id):
        id = str(id)
        select = """
            SELECT *
            FROM transactions
            WHERE customer_id = '{0}';""".format(id)
        # Returning the query execution function.
        return query_all(select)


# Create an API endpoint for accessing all article rows (limited to 50 rows).
@various.route("/various/articles")

class get_all_articles(Resource):

    # Defining responses for the API endpoint.
    @api.doc(responses={**common_responses})

    # Declaring the SQL query to retrieve the first 50 article rows.
    def get(self):
        select = """
            SELECT *
            FROM articles
            LIMIT 50;"""
        # Returning the query execution function.
        return query_all(select)

#---------------------------------------------------------------------------------------
# Run Flask
#---------------------------------------------------------------------------------------

# Running the Flask application when the Python script is executed.
if __name__ == '__main__':
    app.run(debug=True)
