<p align="center">
  <img src="https://user-images.githubusercontent.com/114337279/230568710-9de5ffda-ff76-4f74-9762-4878a7221d52.png" alt="Small logo" width="20%">
</p>
<h3 align="center">J&M Corporate Catalog and Business Dashboard</h3>

<h2> Overview </h2>

<p> For many companies one of their main challenges passes through keeping their employees motivated and engaged while ensuring that they still make informed decisions to drive business success. To address this need, J&M, a renowned international clothing brand, has undertaken a project to develop an exclusive employees' catalog and an interactive dashboard for top management teams.

The employees' catalog is a web page that features all the upcoming items that are set to drop in the next weeks before customers are notified. This catalog is designed to motivate employees by giving them access to exclusive information and products before they are available to the general public.

The top management team, besides the access to the catalog, has also access to a fully interactive business dashboard that provides them with important KPIs and charts to empower their teams to make more informed and performance focused decisions. This dashboard was built using Streamlit and retrieves data from a Google Cloud MySQL database through several Flask RestX API endpoints.

To ensure that only authorized employees have access to the catalog and dashboard, the project incorporates two completely different authentication methods.

The catalog was built using Flask, JS and HTML templates, while the dashboard was developed using Streamlit, Flask RestX API endpoints, and Google Cloud MySQL. 

Take a look at the video below for a detailed overview of the project's flow 🔽</p>

[Video]


<h2> Technology Stack </h2>

Python, Javascript, SQL, Flask, Streamlit, Pandas, Dockers, Google App Engine, MySQL.


<h2> Project Architecture </h2>

![final_diagram](https://user-images.githubusercontent.com/114337279/230586242-e3f3ad5f-7cc6-4a00-bf53-640ecc2d1aab.png)

<h2> Datasets </h2>

This project features three main datasets that were instrumental in analyzing the three core dimensions of the company: Sales, Marketing, and Customer Preferences. The datasets consist of data related with Customers, Transactions, and Articles, each with their own unique set of columns that were carefully selected for analysis purposes.

- Customers Dataset: The Customers dataset features columns such as customer_id, FN, Active, club_member_status, fashion_news_frequency, age, and postal_code. These columns provide insights into customer demographics, preferences, and behavior. By analyzing this dataset, the business can better understand their customer base and tailor the company efforts to their specific needs.

- Transactions Dataset: The Transactions dataset features columns such as t_dat, customer_id, article_id, price, and sales_channel_id. These columns provide insights into the company's sales performance, customer purchasing behavior, and sales channel effectiveness. By analyzing this dataset, the business can identify areas for improvement in their sales strategy and make data-driven decisions to optimize their revenue.

- Articles Dataset: The Articles dataset features columns such as article_id, product_code, prod_name, product_type_name, colour_group_name, department_name, index_group_name, and section_name. These columns provide insights into the company's product offering, product popularity, and customer preferences. By analyzing this dataset, the business can better understand which products are most popular among customers, which product categories have the highest demand, and which colors or styles are trending.

While the original datasets contained irrelevant or unnecessary columns, the data was aggregated into a final dataframe named "final_data," which was used for the analysis. This dataframe aggregates the relevant columns from the three original datasets. The columns included in the final dataframe are t_dat, customer_id, age, club_member_status, fashion_news_frequency, article_id, product_type_name, colour_group_name, and sales_channel_id.



