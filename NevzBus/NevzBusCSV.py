import streamlit as st
import pandas as pd

# Load data from CSV
@st.cache_data
def data_load():
    # Read the CSV file into a DataFrame
    bus_data = pd.read_csv("aa_rb_data.csv")
    return bus_data

bus_data = data_load()

# Initialize session state for filters
if 'select_bus_type' not in st.session_state:
    st.session_state.select_bus_type = "All"
if 'select_boarding' not in st.session_state:
    st.session_state.select_boarding = "All"
if 'select_destination' not in st.session_state:
    st.session_state.select_destination = "All"
if 'select_star_rating' not in st.session_state:
    st.session_state.select_star_rating = "All"
if 'select_route' not in st.session_state:
    st.session_state.select_route = "All"
if 'select_seat_availability' not in st.session_state:
    st.session_state.select_seat_availability = "All"
if 'select_price_min' not in st.session_state:
    st.session_state.select_price_min = int(bus_data["Price"].min())
if 'select_price_max' not in st.session_state:
    st.session_state.select_price_max = int(bus_data["Price"].max())



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
   - **Filter by Boarding Point:** Choose the specific boarding point.
   - **Filter by Destination:** Choose the specific Destination.
   - **Filter by Bus Type:** Select the type of bus you are interested in (e.g., luxury, semi-luxury).
   - **Filter by Star Rating:** Specify the minimum star rating for the bus service.
   - **Filter by Price Range:** Set the price range for the bus tickets.
   - After applying the filters, a table displays the filtered bus data, showing options that meet your criteria.

3. **Bus Table:**
   - View the entire bus dataset in a table, only 10 rows will be visible at once.
   - Navigate through pages to see whole bus data.
             

**How to Use**

1. **Navigate to the 'Find Buses' Page:**
   - Use the filters on the sidebar to select your preferences.
   - Click "Clear Filters" to reset the filter settings.
   - View the filtered results in the main content area.

2. **Navigate to the 'Bus Table' Page:**
   - Select the page number to view a specific subset of the data.
   - Browse through the paginated results to see different entries.


**Contact**

For any questions or issues, please contact **NEVZ-K** in github.

Thank you for using the Streamlit Bus Data Application!
""")
    
# Code for Find Buses Radio Button
if nav_sbar == "Find Buses":

    # Clear Filters button
    if st.button("Clear Filters"):
        st.session_state.select_bus_type = "All"
        st.session_state.select_boarding = "All"
        st.session_state.select_destination = "All"
        st.session_state.select_star_rating = "All"
        st.session_state.select_route = "All"
        st.session_state.select_seat_availability = "All"
        st.session_state.select_price_min = int(bus_data["Price"].min())
        st.session_state.select_price_max = int(bus_data["Price"].max())

    # Dynamically update select boxes based on current selections
    def update_options():
        filtered_data = bus_data.copy()

        if st.session_state.select_boarding != "All":
            filtered_data = filtered_data[filtered_data["Boarding"] == st.session_state.select_boarding]

        if st.session_state.select_destination != "All":
            filtered_data = filtered_data[filtered_data["Destination"] == st.session_state.select_destination]

        if st.session_state.select_bus_type != "All":
            filtered_data = filtered_data[filtered_data["Bus_Type"] == st.session_state.select_bus_type]

        if st.session_state.select_star_rating != "All":
            filtered_data = filtered_data[filtered_data["Star_Rating"] >= int(st.session_state.select_star_rating)]

        if st.session_state.select_route != "All":
            filtered_data = filtered_data[filtered_data["Route_Name"] == st.session_state.select_route]

        if st.session_state.select_seat_availability != "All":
            filtered_data = filtered_data[filtered_data["Seats_Available"] == st.session_state.select_seat_availability]

        bus_type_list = ["All"] + sorted(filtered_data["Bus_Type"].unique())
        star_rating_list = ["All"] + sorted(filtered_data["Star_Rating"].unique())
        boarding_list = ["All"] + sorted(filtered_data["Boarding"].unique())
        destination_list = ["All"] + sorted(filtered_data["Destination"].unique())
        route_list = ["All"] + sorted(filtered_data["Route_Name"].unique())
        seat_availability_list = ["All"] + sorted(filtered_data["Seats_Available"].unique())

        return bus_type_list, star_rating_list, boarding_list, destination_list, route_list, seat_availability_list

    bus_type_list, star_rating_list, boarding_list, destination_list, route_list, seat_availability_list = update_options()

    # Creating columns to add select boxes in one row
    sb, sd = st.columns(2)
    bt, sr = st.columns(2)
    rt, sa = st.columns(2)

    # Select Boarding point and update destination list
    select_boarding = sb.selectbox(
        "Select Boarding Point",
        boarding_list,
        index=boarding_list.index(st.session_state.select_boarding)
        if st.session_state.select_boarding in boarding_list
        else 0,
        on_change=lambda: st.session_state.update({'select_destination': 'All'})
    )

    # Update the destination select box based on the selected boarding point
    select_destination = sd.selectbox(
        "Select Destination Point",
        destination_list,
        index=destination_list.index(st.session_state.select_destination)
        if st.session_state.select_destination in destination_list
        else 0
    )

    # Handle the index for default selections
    select_bus_type = bt.selectbox(
        "Select Bus Type",
        bus_type_list,
        index=bus_type_list.index(st.session_state.select_bus_type)
        if st.session_state.select_bus_type in bus_type_list
        else 0
    )

    select_star_rating = sr.selectbox(
        "Select Star Rating",
        star_rating_list,
        index=star_rating_list.index(st.session_state.select_star_rating)
        if st.session_state.select_star_rating in star_rating_list
        else 0
    )

    # Select Route
    select_route = rt.selectbox(
        "Select Route",
        route_list,
        index=route_list.index(st.session_state.select_route)
        if st.session_state.select_route in route_list
        else 0
    )

    # Select Seat Availability
    select_seat_availability = sa.selectbox(
        "Select Seat Availability",
        seat_availability_list,
        index=seat_availability_list.index(st.session_state.select_seat_availability)
        if st.session_state.select_seat_availability in seat_availability_list
        else 0
    )

    # Full-width price range slider
    select_price_min, select_price_max = st.slider(
        "Select Price Range",
        min_value=int(bus_data["Price"].min()),
        max_value=int(bus_data["Price"].max()),
        value=(st.session_state.select_price_min, st.session_state.select_price_max)
    )

    # Update session state
    st.session_state.select_boarding = select_boarding
    st.session_state.select_destination = select_destination
    st.session_state.select_bus_type = select_bus_type
    st.session_state.select_star_rating = select_star_rating
    st.session_state.select_route = select_route
    st.session_state.select_seat_availability = select_seat_availability
    st.session_state.select_price_min = select_price_min
    st.session_state.select_price_max = select_price_max

    # Re-filter the data based on final selections
    filtered_data = bus_data.copy()

    if select_boarding != "All":
        filtered_data = filtered_data[filtered_data["Boarding"] == select_boarding]
    if select_destination != "All":
        filtered_data = filtered_data[filtered_data["Destination"] == select_destination]
    if select_bus_type != "All":
        filtered_data = filtered_data[filtered_data["Bus_Type"] == select_bus_type]
    if select_star_rating != "All":
        filtered_data = filtered_data[filtered_data["Star_Rating"] >= int(select_star_rating)]
    if select_route != "All":
        filtered_data = filtered_data[filtered_data["Route_Name"] == select_route]
    if select_seat_availability != "All":
        filtered_data = filtered_data[filtered_data["Seats_Available"] == select_seat_availability]
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
