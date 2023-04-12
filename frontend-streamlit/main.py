#---------------------------------------------------------------------------------------
# Imports
#---------------------------------------------------------------------------------------

# Importing the necessary libraries and modules.
from sqlalchemy import create_engine, engine, text
from datetime import datetime, timedelta
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import altair as alt
import requests
import streamlit_authenticator as stauth
from concurrent.futures import ThreadPoolExecutor


#---------------------------------------------------------------------------------------
# Login Scenario 1 - Authentication is Successful
#---------------------------------------------------------------------------------------

# Reading the credentials configurations and defining them in the config structure.
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating an authenticator object.
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Rendering the login widget by providing a name for the form and its location.
name, authentication_status, username = authenticator.login('Login', 'main')

# Confirming the name, authentication_status, and username of the authenticated user.

# If the authentication is successful:
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome back, *{name}*!')

    #---------------------------------------------------------------------------------------
    # Load Datasets
    #---------------------------------------------------------------------------------------

    # Loading the Dataframes from the API endpoints.

    api_url = "https://api-dot-capstone-database-test.oa.r.appspot.com"

    def make_request(main_url, service_url):
        headers = {"Authorization": "Bearer DO_NOT_LOSE_THIS_KEY"}
        response = requests.get(f"{main_url}{service_url}", headers = headers)
        response_json = response.json()
        return response_json

    def load_json_to_dataframe(response_json):
        target_json = response_json["result"]
        try:
            df = pd.DataFrame.from_records(target_json)
        except Exception as e:
            print(e)
            df = pd.DataFrame()
        return df
    
    # Using caching and multithreading with ThreadPoolExecutor to increase data loading speed with parallelization.
    # By performing concurrent loading of data from the different API endpoints, the overall loading time is reduced.
    
    @st.cache_data
    def load_data_concurrently(main_url, service_urls):
        with ThreadPoolExecutor() as executor:
            response_jsons = executor.map(lambda url: make_request(main_url, url), service_urls)
            dataframes = {url: load_json_to_dataframe(response_json) for url, response_json in zip(service_urls, response_jsons)}
        return dataframes

    service_urls = ["/api/v2/sales/sales_data", "/api/v2/marketing/marketing_data", "/api/v2/cust_pref/cust_pref_data"]
    dataframes = load_data_concurrently(api_url, service_urls)

    # ------------------------
    # Tab 1 - Sales
    # ------------------------

    # Loading the Sales Tab Dataframe from the API endpoints. 
    sales_df = dataframes["/api/v2/sales/sales_data"]

    # ------------------------
    # Tab 2 - Marketing
    # ------------------------

    # Loading the Marketing Tab Dataframe from the API endpoints. 
    marketing_df = dataframes["/api/v2/marketing/marketing_data"]

    # ------------------------
    # Tab 3 - Cus. Preferences
    # ------------------------

    # Loading the Customer Preferences Tab Dataframe from the API endpoints. 
    cust_pref_df = dataframes["/api/v2/cust_pref/cust_pref_data"]


    #---------------------------------------------------------------------------------------
    # Page Title and Subtitle
    #---------------------------------------------------------------------------------------

    # Creating a title and subheader for the Streamlit Dashboard.
    st.title("J&M Business Dashboard")
    st.subheader("Analyze and manage J&M customer, products, and transactions data.")


    #---------------------------------------------------------------------------------------
    # Filter Sidebar
    #---------------------------------------------------------------------------------------
    # Since all the filter data has to be present on every loaded dataframe and they are ordered in
    # the same way, the sales_df will be used for setting the different filter dates, options and bounds.

    # Adding the J&M logo on top of the sidebar header.
    st.sidebar.image("images/jmd-logo.png", use_column_width=True, output_format='PNG')

    # Creating a sidebar header.
    st.sidebar.header("Filters:")


    # Creating a "Time Period" filter:

    # Adding a Date Range Picker filter for "Time Range".

    # Extracting the dates from "t_dat" column and storing them as a list.
    dates_unique = sales_df["t_dat"].drop_duplicates().to_list()

    #Converting them to datetime.
    dates_as_datetime = pd.to_datetime(dates_unique)

    # Finding the minimum and maximum dates.
    min_date = min(dates_as_datetime).date()
    max_date =max(dates_as_datetime).date()

    # Adding a date range input filter with between the minimum and maximum dates.
    date_range = st.sidebar.date_input(
        label="Time Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Converting the date range tuple to datetime objects.
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])


    # Creating a "Sales Channel" filter:

    # Assigning user friendly options to the Sales Channel options.
    sales_channel_options = {
        1: "Online",
        2: "Offline"
    }

    # Adding a multiselect filter with the Sales Channel options.
    selected_sales_channel = st.sidebar.multiselect("Sales Channel", list(sales_channel_options.values()), default=list(sales_channel_options.values()))

    # Mapping selected the sales channel options to their corresponding keys.
    selected_sales_channel_keys = [k for k, v in sales_channel_options.items() if v in selected_sales_channel]


    # Creating a "Product Price" filter:

    # Finding the minimum and maximum price.
    min_price = float(sales_df['price'].min())
    max_price = float(sales_df['price'].max())

    # Adding slider filter bounded by the minimum and maximum prices.
    price_range = st.sidebar.slider("Product Price", min_value=min_price, max_value=max_price, value=(min_price, max_price), step=0.1)


    # Creating a "Customer Age" filter:

    # Finding the minimum and maximum age.
    min_age = int(sales_df['age'].min())
    max_age = int(sales_df['age'].max())

    # Adding a slider filter bounded by the minimum and maximum ages.
    age_filtered_lst = st.sidebar.slider('Customers Age Range',min_age, max_age, value=(min_age, max_age), step=10)


    # Creating a "Club Member Status" filter:

    # Selecting all different club_member_status in the data.
    club_member_options = list(sales_df['club_member_status'].unique())

    # Adding a multiselect filter with the Club Member Status options.
    selected_club_member = st.sidebar.multiselect("Club Member Status", club_member_options, default=club_member_options)

    #---------------------------------------------------------------------------------------
    # Option Menu for Application Tabs
    #---------------------------------------------------------------------------------------

    # Creating an option menu to display the 4 different tab categories.
    selected = option_menu(None, options = ["Home", "Sales", "Marketing", "Customers"], icons = ["house-door-fill", "bag-check-fill", "megaphone-fill", "person-badge-fill"], 
    default_index = 0, orientation = "horizontal",  styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin":"4px", "--hover-color": "#4F86A8"},
        "nav-link-selected": {"background-color": "#00083A"}})


    #---------------------------------------------------------------------------------------
    # Main KPIs Section
    #---------------------------------------------------------------------------------------

    # Filtering the dataframes based on the user input from the filters.
    def apply_filters(tab_dataframe):

        # Applying datetime_conversion to the "t_dat" column.
        tab_dataframe['t_dat'] = pd.to_datetime(tab_dataframe['t_dat'])

        filtered_df = tab_dataframe.loc[
            (tab_dataframe['t_dat'] >= start_date) & 
            (tab_dataframe['t_dat'] <= end_date) & 
            (tab_dataframe['sales_channel_id'].isin(selected_sales_channel_keys)) & 
            (tab_dataframe['price'] >= price_range[0]) & 
            (tab_dataframe['price'] <= price_range[1]) &
            (tab_dataframe['age'].between(age_filtered_lst[0], age_filtered_lst[1])) &
            (tab_dataframe['club_member_status'].isin(selected_club_member))
        ]
        return filtered_df

    # Generating the filtered dataframes.
    sales_filtered_df = apply_filters(sales_df)
    marketing_filtered_df = apply_filters(marketing_df)
    cust_pref_filtered_df = apply_filters(cust_pref_df)

    # ------------------------
    # Tab 1 - Sales
    # ------------------------

    # Computing Total Revenue Generated:
    total_revenue_generated = sales_filtered_df['price'].sum()

    # Computing Total Number of Individual Sales (minus the header):
    num_individual_sales = len(sales_filtered_df) -1 

    # Computing Average Order Value:
    average_order_value = sales_filtered_df['price'].mean()

    # ------------------------
    # Tab 2 - Marketing
    # ------------------------

    # Computing the the Repeat Customer Rate (RPR):
    repeat_customer_rate = (marketing_filtered_df.groupby('customer_id')['t_dat'].count() > 1).mean() * 100
    repeat_customer_rate = repeat_customer_rate.round(2)

    # ------------------------
    # Tab 3 - Cus. Preferences
    # ------------------------

    # Finding the Best Selling Product Type:

    # Groupping transactions by product type and sum the prices.
    product_sales = cust_pref_filtered_df.groupby('product_type_name')['price'].sum().reset_index()

    # Sorting by Total Revenue.
    product_sales_sorted = product_sales.sort_values(by='price', ascending=False)

    # Getting the Best Selling Product Type.
    best_selling_product_type = product_sales_sorted.iloc[0]['product_type_name']


    # Finding the Best Selling Product Color:

    # Groupping by product color and sum the price.
    color_sales = cust_pref_filtered_df.groupby('colour_group_name')['price'].sum()

    # Getting the color with the highest total revenue.
    best_selling_color = color_sales.idxmax()

    #---------------------------------------------------------------------------------------
    # Data Visualization Section
    #---------------------------------------------------------------------------------------

    # ------------------------
    # Tab 1 - Sales
    # ------------------------

    # Creating a Total Revenues by Sales Channel Chart:

    # Grouping by year-month and sales channel, and sum the revenue.
    sales_by_month = sales_filtered_df.groupby([pd.Grouper(key='t_dat', freq='M'), 'sales_channel_id']).agg({'price': 'sum'}).reset_index()
    sales_by_month.rename(columns={'t_dat': 'Date', 'sales_channel_id': 'Sales Channel', 'price': 'Revenue'}, inplace=True)

    # Mapping the sales_channel_id to the corresponding option.
    sales_by_month['Sales Channel'] = sales_by_month['Sales Channel'].map({1: 'Online', 2: 'Offline'})

    # Building the chart.
    chart_sales = alt.Chart(sales_by_month).mark_bar().encode(
        x=alt.X('yearmonth(Date):T', title='Date'),
        y=alt.Y('Revenue:Q', title='Revenues', axis=alt.Axis(format=',.2s')),
        color=alt.Color('Sales Channel:N', scale=alt.Scale(domain=['Online', 'Offline'], range=['#4F86A8','#01033A'])),
    ).properties(
        title='Total Revenues by Sales Channel',
        height=470
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    ).configure_legend(
        orient='bottom',
        padding=10
    )

    # Creating a Total Revenues by Customers Age Group Chart:

    # Computing total revenue per age group.
    age_groups_revenue = sales_filtered_df.groupby(pd.cut(sales_filtered_df['age'], bins=range(0, 121, 10)))['price'].sum().reset_index()
    age_groups_revenue['age_range'] = age_groups_revenue['age'].astype(str).str.replace(', ', '-').str.strip('()')

    # Building the chart.
    chart_age_groups = alt.Chart(age_groups_revenue).mark_bar().encode(
        y=alt.Y('price:Q', title='Revenues', axis=alt.Axis(format=',.2s')),
        x=alt.X('age_range:O', title='Age Range', axis=alt.Axis(labelAngle=-45)),
        color=alt.Color('age_range:O', title='Age Range', scale=alt.Scale(scheme='blues'), legend=alt.Legend(columns=4))
    ).properties(
        title='Total Revenues by Age Group',
        height=527
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    ).configure_legend(
        orient='bottom',
        padding=10, 
    )

    # ------------------------
    # Tab 2 - Marketing
    # ------------------------

    # Creating a Fashion News Effectiveness Chart:

    # Generating a new column 'fashion_news' based on the values in the 'fashion_news_frequency' column.
    marketing_filtered_df['fashion_news'] = marketing_filtered_df['fashion_news_frequency'].apply(lambda x: 'Yes' if x in ['Regularly', 'Monthly'] else 'No')

    # Aggregating revenue by month and fashion news status.
    revenue_by_month_fn = marketing_filtered_df.groupby([pd.Grouper(key='t_dat', freq='M'), 'fashion_news']).agg({'price': 'sum'}).reset_index()
    revenue_by_month_fn['revenue_normalized'] = revenue_by_month_fn.groupby('t_dat')['price'].apply(lambda x: 100 * x / x.sum())

    # Building the chart.
    chart_news_effectiveness = alt.Chart(revenue_by_month_fn).mark_bar().encode(
        x=alt.X('yearmonth(t_dat):T', title='Date'),
        y=alt.Y('revenue_normalized:Q', title='% of Revenues'),
        color=alt.Color('fashion_news:N', title='Fashion News', 
                        scale=alt.Scale(domain=["No","Yes"], range=['#4F86A8','#01033A'])),
    ).properties(
        title="Fashion News Effectiveness",
        height=368
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    ).configure_legend(
        orient='bottom',
        padding=10
    ).configure_view(
        step = 10
    )


    # Creating a Customers Distribution per Fashion News Subscription Frequency Chart:

    # Counting the number of customers in each frequency category.
    freq_counts = marketing_filtered_df['fashion_news_frequency'].value_counts().reset_index()
    freq_counts.columns = ['Frequency', 'Count']

    # Building the chart.
    chart_news_freq = alt.Chart(freq_counts).mark_bar(size=60).encode(
    y=alt.Y('Frequency:N', axis=alt.Axis(title='Frequency')),
    x=alt.X('Count:Q', axis=alt.Axis(title='Number of Customers')),
    tooltip=[alt.Tooltip('Frequency:N', title='Frequency'), alt.Tooltip('Count:Q', title='Number of Customers')],
    color=alt.Color('Frequency:N', scale=alt.Scale(scheme='blues'))
    ).properties(
        title="Fashion News Subscribers",
        height=368
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    ).configure_legend(
    orient='bottom',
    padding=10
    ).configure_view(
        step=10
    )

    # ------------------------
    # Tab 3 - Cus. Preferences
    # ------------------------

    # Creating a Sales Channel Distribution Pie Chart:

    # Computing the revenues per sales channel.
    revenue_by_channel = cust_pref_filtered_df.groupby('sales_channel_id')['price'].sum()

    # Computing the % of Total Revenues among Sales Channels (Online and Offline).
    percent_by_channel = (revenue_by_channel / total_revenue_generated) * 100
    percent_by_channel = percent_by_channel.round(2)

    # Retrieving the labels for the sales channels from sales_channel_options based on the index values of revenue_by_channel. 
    labels = [sales_channel_options[k] for k in revenue_by_channel.index]

    # Building the chart.
    chart_sales_dist = alt.Chart(pd.DataFrame({'Sales Channel': labels, 'Revenue': revenue_by_channel.values, '% of Total Revenues': percent_by_channel.values})).mark_arc().encode(
        color=alt.Color('Sales Channel:N', scale=alt.Scale(domain=['Online', 'Offline'], range=['#4F86A8','#01033A'])),
        theta='Revenue:Q',
        tooltip=['Sales Channel:N', alt.Tooltip('% of Total Revenues:Q', format='.2f')]
    ).transform_aggregate(
        Revenue='sum(Revenue)',
        groupby=['Sales Channel']
    ).transform_calculate(
        '% of Total Revenues', alt.datum.Revenue / total_revenue_generated * 100
    ).properties(
        title={
        "text": ["Preference for Online and Offline Channels"],
        "subtitle": ["(% of Total Revenues)"],
        "fontSize": 16,
        "fontWeight": "bold",
        "subtitleFontSize": 13
        }
    ).configure_legend(
        orient='bottom',
        padding=10,
        title=None,
        labelFontSize=12,
        labelColor='black',
        labelFontWeight='bold',
        labelLimit=0,
        symbolLimit=0,
        symbolType='square'
    )


    # Creating a Top 10 Cumulative Revenue by Product Type Heatmap Chart:

    # Building a pivot table with revenue by product type and month.
    pivot_df = cust_pref_filtered_df.pivot_table(index='product_type_name', columns=pd.Grouper(key='t_dat', freq='M'), values='price', aggfunc='sum')

    # Resetting the index and rename the columns.
    pivot_df = pivot_df.reset_index().rename(columns={'product_type_name': 'Product Type'})

    # Sorting by total revenue across all months and keep the top 10 product types.
    sorted_df = pivot_df.melt(id_vars=['Product Type'], var_name='Month', value_name='Revenue').groupby('Product Type')['Revenue'].sum().sort_values(ascending=False).head(10).index.tolist()
    pivot_df = pivot_df[pivot_df['Product Type'].isin(sorted_df)]

    # Melting the data to create a long-form dataframe.
    melt_df = pivot_df.melt(id_vars=['Product Type'], var_name='Month', value_name='Revenue')

    # Computing the cumulative sum of revenue for each product type.
    melt_df['Cumulative Revenue'] = melt_df.groupby('Product Type')['Revenue'].cumsum()

    # Building the chart.
    chart_heatmap = alt.Chart(melt_df).mark_rect().encode(
        x=alt.X('Month:T', title='Date'),
        y=alt.Y('Product Type:O', title='Product Type', sort=alt.EncodingSortField(field='Revenue', op='sum', order='descending')),
        color=alt.Color('Cumulative Revenue:Q', title='Cumulative Revenue (€)', scale=alt.Scale(scheme='blues', domain=[melt_df['Cumulative Revenue'].min(), melt_df['Cumulative Revenue'].max()], zero=False)),
        tooltip=[alt.Tooltip('Product Type:O', title='Product Type'),
                alt.Tooltip('Month:T', title='Date', format='%Y-%m-%d'),
                alt.Tooltip('Cumulative Revenue:Q', title='Cumulative Revenue (€)', format='$.0f')] # Format as € full units
    ).properties(
        title={
        "text": ["Revenue by Product Type (Top 10)"],
        "fontSize": 16,
        "fontWeight": "bold",
        "subtitleFontSize": 13
        },
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16,
        font='Arial',
        anchor='middle'
    ).configure_legend(
        orient='bottom',
        padding=10,
    )

    #---------------------------------------------------------------------------------------
    # Page Rendering
    #---------------------------------------------------------------------------------------

    # ------------------------
    # Tab 0 - Home
    # ------------------------

    if selected == "Home":

        # Showing the other tabs descriptions and purposes.
        st.write("""
        The J&M Business Dashboard was designed to empower the J&M's Management Team to make informed decisions based on different KPIs and Charts.
        
        This one is divided into three sections:""")

        st.subheader("💳 Sales")
        st.write("""The Sales tab presents the performance of sales for the company, including metrics such as total revenue generated, average order value, and sales by channel and age group. 
        This information provides valuable insights into the performance of the company's sales efforts and helps the company make informed decisions to improve sales revenue and customer experience.
        """)

        st.subheader("📣 Marketing")
        st.write("""The Marketing tab provides information into the effectiveness of the company's marketing efforts, including metrics such as the repeat customer rate and the impact of fashion news on revenues. 
        This information provides valuable insights into the effectiveness of the company's marketing efforts and enables the company to optimize its marketing strategy and maximize its return on investment.
        """)

        st.subheader("👩🏾🧑🏻 Customer Preferences")
        st.write("""The Customer Preferences tab details the company's best-selling products and how customers prefer to purchase them, including metrics such as the best-selling product type and 
        color, the sales channel distribution, and revenue by product type over time. This information provides valuable insights regarding product offerings, enabling the company to understand its customers' 
        preferences and optimize its next pieces, color selection and sales channels distribution accordingly.""")

        # Creating an horizontal line break.
        st.markdown("---")

        # Displaying support and contact information.
        st.write("""For any question or additional support, please don't hesitate to contact: joaoapinho@student.ie.edu .""")

    # ------------------------
    # Tab 1 - Sales 
    # ------------------------

    # If the selected tab is the sales tab:
    if selected == "Sales":

        # Creating a subheader for the KPIs Section.
        st.subheader("Main KPIs:")
        
        # Rendering Total Revenue Generated, Number of Individual Sales, Average Order Value (AOV) and Repeat Customer Rate (RPR) side by side.
        col1, col2, col3 = st.columns(3, gap="small")
        col1.metric("**Total Revenue Generated**", f"€{total_revenue_generated:,.2f}")
        col2.metric("**# of Individual Sales**", f"{num_individual_sales:,}")
        col3.metric("**Average Order Value**", f"€{average_order_value:,.2f}")

        # Creating a subheader for the Charts Section.
        st.subheader("Data Visualization:")

        # Showing the charts.
        col1, col2 = st.columns(2, gap="small")
        col1.altair_chart(chart_sales, use_container_width=True)
        col2.altair_chart(chart_age_groups, use_container_width=True)

    # ------------------------
    # Tab 2 - Marketing
    # ------------------------

    # If the selected tab is the marketing tab:
    if selected == "Marketing":

        # Creating a subheader for Key Information Section.
        st.subheader("Main KPIs:")
        # Rendering Repeat Customer Rate (RPR).
        st.metric("**Repeat Customer Rate**", f"{repeat_customer_rate:,}%")

        # Creating a subheader for the Charts Section
        st.subheader("Data Visualization:")

        # Showing the charts.
        col1, col2 = st.columns(2, gap="small")
        col1.altair_chart(chart_news_effectiveness, use_container_width=True)
        col2.altair_chart(chart_news_freq, use_container_width=True)


    # ------------------------
    # Tab 3 - Cus. Preferences
    # ------------------------

    # If the selected tab is the customer preferences tab:
    if selected == "Customers": 
        
        # Creating a subheader for Key Information Section.
        st.subheader("Key Information:")
        
        # Rendering Best Selling Product Type, Favourite Purchased Color side by side.
        col1, col2 = st.columns(2, gap="large")
        col1.metric("**Best Selling Product Type**", f"{best_selling_product_type}")
        col2.metric("**Best Selling Product Color**", f"{best_selling_color}")
        
        # Creating a subheader for the Charts Section
        st.subheader("Data Visualization:")

        # Showing the charts.
        col1, col2 = st.columns(2, gap="small")
        col1.altair_chart(chart_sales_dist, use_container_width=True)
        col2.altair_chart(chart_heatmap, use_container_width=True)


    #-------------------------
    # Summary Table Section
    #-------------------------

    # If the selected tab is any of the tabs besides home:
    if selected != "Home":

        # Groupping the data by sales channel and product type, and calculating the key metrics.
        summary_df = cust_pref_filtered_df.groupby(['sales_channel_id', 'product_type_name']).agg(
            total_sales=('article_id', 'count'),
            total_revenue=('price', 'sum'),
            average_price=('price', 'mean'),
            average_age_of_customers=('age', lambda x: round(x.mean()))
        ).reset_index()

        # Mapping the sales_channel_id to the corresponding option.
        summary_df['sales_channel_id'] = summary_df['sales_channel_id'].map({1: 'Online', 2: 'Offline'})

        # Renaming the columns for user reading clarity.
        summary_df.rename(columns={'sales_channel_id': 'Sales Channel', 'product_type_name': 'Product Type', 'total_sales': 'Total Sales', 'total_revenue': 'Total Revenue', 'average_price': 'Average Price', 'average_age_of_customers': 'Avg. Customers Age'}, inplace=True)

        # Creating an expander for the Summary dataframe.
        with st.expander("Sales Channel and Product Type Summary Table"):
            # Showing the summary table.
            st.dataframe(summary_df.style.format({'Total Revenue': '{:,.2f}', 'Average Price': '{:,.2f}', 'Avg. Age of Customers': '{:,.0f}'}))


#---------------------------------------------------------------------------------------
# Login Scenario 2 - Authentication Failed
#---------------------------------------------------------------------------------------

# Confirming the name, authentication_status, and username of the authenticated user.
# If authentication fails:
elif authentication_status == False:
    st.error('Username/password is incorrect')

#---------------------------------------------------------------------------------------
# Login Scenario 3 - No Details Entered 
#---------------------------------------------------------------------------------------

# If there is neither a username nor a password, or both:
elif authentication_status == None:
    st.warning('Please enter your username and password')
