<p align="center">
  <img src="https://user-images.githubusercontent.com/114337279/230568710-9de5ffda-ff76-4f74-9762-4878a7221d52.png" alt="Small logo" width="20%">
</p>
<h3 align="center">J&M Corporate Catalog and Business Dashboard</h3>

<h2> 👁‍🗨 Overview </h2>

<p> For many companies one of their main challenges passes through keeping their employees motivated and engaged while ensuring that they make informed decisions to drive business success. To address this need, J&M, a renowned international clothing brand, has undertaken a project to develop an exclusive employees' catalog and an interactive dashboard for top management teams.

The employees' catalog is a web page that features all the upcoming items that are set to drop in the next weeks before customers are notified. This catalog is designed to motivate employees by giving them access to exclusive information and products before they are available to the general public.

The top management team, besides the access to the catalog, has also access to a fully interactive business dashboard that provides them with important KPIs and charts to empower their teams to make more informed and performance focused decisions. This dashboard was built using Streamlit and retrieves data from a Google Cloud MySQL database through several Flask RestX API endpoints.

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

<h3> 👕👖 Employees' Exclusive Upcoming Collection Catalog </h3>

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

<h3> 📊 Business Dashboard </h3>

**Demo:**

![streamlit](https://user-images.githubusercontent.com/114337279/230591489-f45869e8-2dd7-46db-88c6-396ec6a8dace.gif)

**Description:**

This Streamlit application provides a corporate dashboard for top managers to analyse and manage J&M customer, products, and transactions data in order to guide their teams into making better business decisions. This service is divided into three main components:

- 🔐 **Authentication**:
  
Using the streamlit authenticator package, the project implements authentication to the Streamlit dashboard. The authentication method employs a set of credentials, cookies, and a list of preauthorized email addresses saved in a config.yaml file. The password hashing.py program is used to hash plain-text passwords, which are subsequently saved in the config.yaml file.

When a user signs in, the main.py code reads the config.yaml file's credentials and displays a login form where the user may input their username and password. The streamlit authenticator library validates the user's credentials and sets a cookie to authenticate the user. In addition, depending on the authentication state, the the user will face one of three scenarios: successful authentication, authentication failure, or no details entered.

This authentication method is safe because it employs password hashing and cookie-based authentication, which prevents attackers from reading user credentials even if they get database access. Moreover, only pre-authorized email addresses are permitted to access the dashboard, further strengthening security. 
  
- 🔎 **Filtering**:

The Streamlit's filtering section allows the user to pick and apply various filters to the data in order to better analyze and display it:

- **Time Period** - A date input filter for selecting a data range for the processed and displayed data.
- **Sales Channel Filter** -  A multiselect filter for selecting the sales channels in the different data entries.
- **Product Price** - A slider filter for selecting a price range for the acquired articles in the different entries.
- **Customer Age** - A slider filter for selecting an age range of the customers in the different data entries.
- **Club Member Status** - A multiselect filter for selecting the club member status of the diferent customers in the data.

The filtering process begins by loading datasets from API endpoints using the make_request() and load_json_to_dataframe() functions. To speed up the process, data is loaded concurrently utilizing caching and multithreading with ThreadPoolExecutor. Following data loading and filter configuration, the apply filters() function will alter the final dataframe based on the filters user input, yielding the filtered_df dataframe that will be used for computing different KPIs and plotting charts.

- 📈 **KPIs and Charts**: 

As the core of the project, the last section is focused on the KPIs and Charts that can be derived from the processed data and which will provide important insights into the performance of the business across three different areas: 

**🛒 Sales** - The Sales tab presents the performance of sales for the company and it is divided into 4 main elements:
- **Total Revenue Generated**: The total revenue generated by sales based on the selected filters.
- **Total Number of Individual Sales**: The total number of individual sales based on the selected filters.
- **Average Order Value**: The average value of each order based on the selected filters.
- **Total Revenues by Sales Channel Chart**: A bar chart that shows the total revenues generated by each sales channel (Online and Offline) over time and based on the selected filters.

**📣 Marketing** - The Marketing tab provides information into the effectiveness of the company's marketing efforts and it is divided into 3 main elements:

- **Repeat Customer Rate (RPR)**: The percentage of repeat customers based on the selected filters.
- **Fashion News Effectiveness Chart**: A bar chart that shows the percentage of revenues generated by customers who receive fashion news versus those who do not over time and based on the selected filters.
- **Customers Distribution per Fashion News Subscription Frequency Chart**: A bar chart that shows the number of customers in each frequency category for fashion news subscription based on the selected filters.

**👩🏾👨🏻Customer Preferences** - The Customer Preferences tab details the company's best-selling products and how customers prefer to purchase them, and it is divided into 4 main elements:

- **Best Selling Product Type**: The best-selling product type based on the selected filters.
- **Best Selling Product Color**: The color with the highest total revenue based on the selected filters.
- **Sales Channel Distribution Pie Chart**: A pie chart that shows the distribution of revenues among sales channels (Online and Offline) based on the selected filters.
- **Top 10 Cumulative Revenue by Product Type Heatmap Chart**: A heatmap that shows the cumulative revenue of the top 10 best-selling product types over time based on the selected filters.

<h3> 🌉 API Endpoints </h3>

**Demo:**

![api](https://user-images.githubusercontent.com/114337279/230611764-d5e4e255-1ad2-47ba-8dd6-c588a6040977.gif)

**Description:**

In order for the dashboard to operate properly, this one is dependent on a REST API service that connects to a MySQL database and provides endpoints for obtaining Sales, Marketing, and Customer Preferences data. 

Flask-Restx and Swagger are used to produce the API documentation, and an API key is created for authentication. This one is established using the custom_api_key variable and is required to be provided in the header of the request with the name WHERE_IS_YOUR_API_KEY. If the provided API key matches the custom_api_key, the request will be authorized to access the data provided by the API. If the key doesn't match, the request will be denied with an error message. 

The documentation aggregates three main namespaces: Sales, Marketing and Customer Preferences each with a single endpoint that retrieves the data required for all of the KPIs and Charts of the corresponding tabs. A Various namespace was also included with more specific and detailed queries that were not required for the dashboard, but could be useful for other tasks. 

The code connects to the MySQL database and runs a SQL query to get data from the final_data table. The results are then returned as JSON through the API endpoints, which are dependent on Flask, SQLAlchemy, and retry libraries to facilitate the connection and interaction with the database.

**Note:**

For the purpose of the project and as agreed with the project supervisor, the retrieved data that was used was an undersample of 900,000 entries (i.e., using a LIMIT of 900000 on the appropriate queries) in order to reduce loading times.

<h2> 🎯 Conclusions and Future Improvements </h2>

In sum, while motivating employees to keep working hard by giving them access to new collection pieces ahead of the market or by giving teams powerful tools and data to improve their decision making the integration of the catalog and business dashboard could resemble 2 positive events for the company's performance.

While the developed services meet the agreed project requirements, there are still some improvement opportunities that can be explored in future updates:

- **Increase the data size by expanding the number of rows from the current limit of 900,000 entries**, in order to gain access to a more comprehensive set of information
- **Incorporate predictive modeling or machine learning functionalities** to identify trends and make predictions based on the available purchase data.
- **Improve the security of the catalog registration page** by only allowing @jm-corporate.com emails to register.
- **Expand the scope and quality of the available KPIs by integrating external data** from other departments, such as costs and inventory.
