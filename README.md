<p align="center">
  <img src="https://user-images.githubusercontent.com/114337279/230568710-9de5ffda-ff76-4f74-9762-4878a7221d52.png" alt="Small logo" width="20%">
</p>
<h3 align="center">J&M Corporate Catalog and Business Dashboard</h3>

<h2> 👁‍🗨 Overview </h2>

<p> For many companies one of their main challenges passes through keeping their employees motivated and engaged while ensuring that they still make informed decisions to drive business success. To address this need, J&M, a renowned international clothing brand, has undertaken a project to develop an exclusive employees' catalog and an interactive dashboard for top management teams.

The employees' catalog is a web page that features all the upcoming items that are set to drop in the next weeks before customers are notified. This catalog is designed to motivate employees by giving them access to exclusive information and products before they are available to the general public.

The top management team, besides the access to the catalog, has also access to a fully interactive business dashboard that provides them with important KPIs and charts to empower their teams to make more informed and performance focused decisions. This dashboard was built using Streamlit and retrieves data from a Google Cloud MySQL database through several Flask RestX API endpoints.

To ensure that only authorized employees have access to the catalog and dashboard, the project incorporates two completely different authentication methods.

The catalog was built using Flask, JS and HTML templates, while the dashboard was developed using Streamlit, Flask RestX API endpoints, and Google Cloud MySQL. 

Take a look at the video below for a detailed overview of the project's flow 🔽</p>


<h2> 💻 Technology Stack </h2>

Python, Javascript, SQL, Flask, Streamlit, Pandas, Dockers, Google App Engine, MySQL.


<h2> 📝 Project Architecture </h2>

![final_diagram](https://user-images.githubusercontent.com/114337279/230586242-e3f3ad5f-7cc6-4a00-bf53-640ecc2d1aab.png)

<h2> 🧮 Datasets </h2>

This project features three main datasets that were instrumental in analyzing the three core dimensions of the company: Sales, Marketing, and Customer Preferences. The datasets consist of data related with Customers, Transactions, and Articles, each with their own unique set of columns that were carefully selected for analysis purposes.

- **Customers Dataset:** The Customers dataset features columns such as customer_id, FN, Active, club_member_status, fashion_news_frequency, age, and postal_code. These columns provide insights into customer demographics, preferences, and behavior. By analyzing this dataset, the business can better understand their customer base and tailor the company efforts to their specific needs.

- **Transactions Dataset:** The Transactions dataset features columns such as t_dat, customer_id, article_id, price, and sales_channel_id. These columns provide insights into the company's sales performance, customer purchasing behavior, and sales channel effectiveness. By analyzing this dataset, the business can identify areas for improvement in their sales strategy and make data-driven decisions to optimize their revenue.

- **Articles Dataset:** The Articles dataset features columns such as article_id, product_code, prod_name, product_type_name, colour_group_name, department_name, index_group_name, and section_name. These columns provide insights into the company's product offering, product popularity, and customer preferences. By analyzing this dataset, the business can better understand which products are most popular among customers, which product categories have the highest demand, and which colors or styles are trending.

While the original datasets contained irrelevant or unnecessary columns, the data was aggregated into a final dataframe named "final_data," which was used for the analysis. This dataframe aggregates the relevant columns from the three original datasets. The columns included in the final dataframe are t_dat, customer_id, age, club_member_status, fashion_news_frequency, article_id, product_type_name, colour_group_name, and sales_channel_id.

<h2> 🔨 Services </h2>

<h3> Employees' Exclusive Upcoming Collection Catalog </h3>

**Demo:**

![catalog](https://user-images.githubusercontent.com/114337279/230591467-3e113662-d357-45d9-bf3a-7dea08824278.gif)

**Description:**

This Flask application provides a corporate catalog for workers to browse forthcoming store articles that are not yet publicly available. This service includes routes to: 

- **Login** - The login route handles user authentication by comparing the user's input credentials to data saved in the database. If the credentials provided are validated through the performed SQL querying, the user is logged in and forwarded to the catalog page. Otherwise, an error flash message appears, and the user is sent to the login page to try again.
- **Registration** -  Corporate users can register on the J&M website using the registration method. After the registration form is submitted, the route checks to see if the entered username already exists in the database. If this occurs, the user is advised of the problem and returned to the registration page. If the username does not already exist in the database, the new user's credentials (i.e., incremental user_id, username and hashed password) are saved, and they are instantly logged in and routed to the catalog page.
- **Catalog** - Only logged-in users may access the catalog route, which displays the company's product catalog. Users may explore the different product information, read an appreciation message left by J&M, have access to a support contact and logout.
- **Logout** - The logout route locks out the user by deleting their session data and sending them to the login page. Having logged out, the user must re-enter their credentials to access the website's protected sections.
- **Error 404 handling** - The 404 error route is a custom error page that appears when a user attempts to navigate to a non-existent website. The error notice instructs the user to return to the previous page.

Overall, this service can be seen as an alternative entry point to the Business Dashboard's Authentication Page via the Corporate Banner Section, in addition to offering a secure and exciting manner for workers to become familiar with special J&M product information.

<h3> Business Dashboard </h3>

**Demo:**

![streamlit](https://user-images.githubusercontent.com/114337279/230591489-f45869e8-2dd7-46db-88c6-396ec6a8dace.gif)

**Description:**

This Streamlit application provides a corporate dashboard for top managers to analyse and manage J&M customer, products, and transactions data in order to guide their teams into making better business decisions. This service is divided into three main components:

- 🔐 Authentication:
  
Using the streamlit authenticator package, the project implements authentication to the Streamlit dashboard. The authentication method employs a set of credentials, cookies, and a list of preauthorized email addresses saved in a config.yaml file. The password hashing.py program is used to hash plain-text passwords, which are subsequently saved in the config.yaml file.

When a user signs in, the main.py code reads the config.yaml file's credentials and displays a login form where the user may input their username and password. The streamlit authenticator library validates the user's credentials and sets a cookie to authenticate the user. In addition, depending on the authentication state, the the user will face one of three scenarios: successful authentication, authentication failure, or no details entered.

This authentication method is safe because it employs password hashing and cookie-based authentication, which prevents attackers from reading user credentials even if they get database access. Moreover, only pre-authorized email addresses are permitted to access the dashboard, further strengthening security. 
  
- 🔎 Filtering:






