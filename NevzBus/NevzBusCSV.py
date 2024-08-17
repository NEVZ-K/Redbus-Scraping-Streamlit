import streamlit as st
import pandas as pd

# Load data from CSV
@st.cache_data
def data_load():
    # Read the CSV file into a DataFrame
    bus_data = pd.read_csv("aa_rb_data.csv")
    return bus_data

bus_data = data_load()

# Accessing unique values for filtering
bus_type = sorted(bus_data["Bus_Type"].unique())
routes = sorted(bus_data["Route_Name"].unique())
star_rating = sorted(bus_data["Star_Rating"].unique())
price_range = bus_data["Price"].agg(['min', 'max'])
price_min, price_max = price_range['min'], price_range['max']

# Initialize session state for filters
if 'select_bus_type' not in st.session_state:
    st.session_state.select_bus_type = "All"
if 'select_bus_route' not in st.session_state:
    st.session_state.select_bus_route = "All"
if 'select_star_rating' not in st.session_state:
    st.session_state.select_star_rating = "All"
if 'select_price_min' not in st.session_state:
    st.session_state.select_price_min = int(price_min)
if 'select_price_max' not in st.session_state:
    st.session_state.select_price_max = int(price_max)

# LOGO image for the webpage
st.image("NevzBusLogo.png", width=750)

nav_sbar = st.sidebar.radio(" ", ["Home", "Find Buses", "Bus Table"])  # Sidebar

# Code for Home page
if nav_sbar == "Home":
    st.write("""**Streamlit Bus Data Application**

**Overview**

This Streamlit application allows users to view and filter bus data from the RedBus platform, enabling users to search and explore various bus options based on different criteria.

**Features**

1. **Home Page:**
   - A simple introductory page with basic information about the application.

2. **Find Buses:**
   - **Filter by Bus Type:** Select the type of bus you are interested in (e.g., luxury, semi-luxury).
   - **Filter by Route:** Choose the specific route or destination.
   - **Filter by Star Rating:** Specify the minimum star rating for the bus service.
   - **Filter by Price Range:** Set the price range for the bus tickets.
   - After applying the filters, a table displays the filtered bus data, showing options that meet your criteria.

3. **Bus Table:**
   - View the entire bus dataset in a paginated format.
   - Navigate through pages to see different chunks of data.
             

**How to Use**

1. **Navigate to the 'Find Buses' Page:**
   - Use the filters on the sidebar to select your preferences.
   - Click "Clear Filters" to reset the filter settings.
   - View the filtered results in the main content area.

2. **Navigate to the 'Bus Table' Page:**
   - Select the page number to view a specific subset of the data.
   - Browse through the paginated results to see different entries.


**Contact**

For any questions or issues, please contact **Nevil K Joseph**.

Thank you for using the Streamlit Bus Data Application!
""")
    
# Code for Find Buses Radio Button
if nav_sbar == "Find Buses":
    bt, br = st.columns(2)
    sr, pr = st.columns([1, 3])

    # Add a clear button
    if st.sidebar.button("Clear Filters"):
        st.session_state.select_bus_type = "All"
        st.session_state.select_bus_route = "All"
        st.session_state.select_star_rating = "All"
        st.session_state.select_price_min = int(price_min)
        st.session_state.select_price_max = int(price_max)

    # Ensure 'All' is always the first option
    bus_type_list = ["All"] + bus_type

    # Get the list of routes based on selected bus type
    if st.session_state.select_bus_type != "All":
        routes_list = ["All"] + sorted(bus_data[bus_data["Bus_Type"] == st.session_state.select_bus_type]["Route_Name"].unique())
    else:
        routes_list = ["All"] + routes

    star_rating_list = ["All"] + star_rating

    # Handle the index for default selections
    select_bus_type = bt.selectbox(
        "Select Bus Type",
        bus_type_list,
        index=bus_type_list.index(st.session_state.select_bus_type)
        if st.session_state.select_bus_type in bus_type_list
        else 0
    )
    
    select_bus_route = br.selectbox(
        "Select Bus Route",
        routes_list,
        index=routes_list.index(st.session_state.select_bus_route)
        if st.session_state.select_bus_route in routes_list
        else 0
    )
    
    select_star_rating = sr.selectbox(
        "Select Star Rating",
        star_rating_list,
        index=star_rating_list.index(st.session_state.select_star_rating)
        if st.session_state.select_star_rating in star_rating_list
        else 0
    )
    
    select_price_min, select_price_max = pr.slider(
        "Select Price Range",
        min_value=int(price_min),
        max_value=int(price_max),
        value=(st.session_state.select_price_min, st.session_state.select_price_max)
    )

    st.session_state.select_bus_type = select_bus_type
    st.session_state.select_bus_route = select_bus_route
    st.session_state.select_star_rating = select_star_rating
    st.session_state.select_price_min = select_price_min
    st.session_state.select_price_max = select_price_max

    filtered_data = bus_data.copy()

    # Filtering data based on user input
    if select_bus_type != "All":
        filtered_data = filtered_data[filtered_data["Bus_Type"] == select_bus_type]
    if select_bus_route != "All":
        filtered_data = filtered_data[filtered_data["Route_Name"] == select_bus_route]
    if select_star_rating != "All":
        filtered_data = filtered_data[filtered_data["Star_Rating"] >= int(select_star_rating)]
    filtered_data = filtered_data[
        (filtered_data["Price"] >= select_price_min) & 
        (filtered_data["Price"] <= select_price_max)
    ]

    st.dataframe(filtered_data.reset_index(drop=True))

# Code for Bus Table Radio Button
if nav_sbar == "Bus Table":
    page_size = 10
    total_rows = len(bus_data)
    pages = total_rows // page_size + (total_rows % page_size != 0)

    sele, a, b, c, d = st.columns(5)
    page = sele.number_input("Select Page Number", min_value=1, max_value=pages, step=1)

    start_row = (page - 1) * page_size
    end_row = start_row + page_size

    st.dataframe(bus_data.iloc[start_row:end_row].reset_index(drop=True))
