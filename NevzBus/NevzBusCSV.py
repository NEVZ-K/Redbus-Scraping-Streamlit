import streamlit as st
import pandas as pd

# Load data from CSV
@st.cache_data
def data_load():
    # Read the CSV file into a DataFrame
    bus_data = pd.read_csv("aa_rb_data.csv")
    return bus_data

bus_data = data_load()

# Initialize session state for filters to remember the widget selections while loading the page
# Check if 'select_bus_type' key exists in session state; if not, initialize it with the value "All"
if 'select_bus_type' not in st.session_state:
    st.session_state.select_bus_type = "All"

# Check if 'select_boarding' key exists in session state; if not, initialize it with the value "All"
if 'select_boarding' not in st.session_state:
    st.session_state.select_boarding = "All"

# Check if 'select_destination' key exists in session state; if not, initialize it with the value "All"
if 'select_destination' not in st.session_state:
    st.session_state.select_destination = "All"

# Check if 'select_star_rating' key exists in session state; if not, initialize it with the value "All"
if 'select_star_rating' not in st.session_state:
    st.session_state.select_star_rating = "All"

# Check if 'select_route' key exists in session state; if not, initialize it with the value "All"
if 'select_route' not in st.session_state:
    st.session_state.select_route = "All"

# Check if 'select_seat_availability' key exists in session state; if not, initialize it with the value "All"
if 'select_seat_availability' not in st.session_state:
    st.session_state.select_seat_availability = "All"

# Check if 'select_price_min' key exists in session state; if not, initialize it with the minimum price from the dataset
if 'select_price_min' not in st.session_state:
    st.session_state.select_price_min = int(bus_data["Price"].min())

# Check if 'select_price_max' key exists in session state; if not, initialize it with the maximum price from the dataset
if 'select_price_max' not in st.session_state:
    st.session_state.select_price_max = int(bus_data["Price"].max())
    
# Check if 'select_state_rtc' key exists in session state; if not, initialize it with the value "Select"
if 'select_state_rtc' not in st.session_state:
    st.session_state.select_state_rtc = "Select"



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

    # Clear Filters button and Select State RTC select box
    clear_col, rtc_col = st.columns([2, 3])
    
    # Code to clear the filters while pressing clear button
    if clear_col.button("Clear Filters"):
        st.session_state.select_bus_type = "All"
        st.session_state.select_boarding = "All"
        st.session_state.select_destination = "All"
        st.session_state.select_star_rating = "All"
        st.session_state.select_route = "All"
        st.session_state.select_seat_availability = "All"
        st.session_state.select_price_min = int(bus_data["Price"].min())
        st.session_state.select_price_max = int(bus_data["Price"].max())
        st.session_state.select_state_rtc = "Select"
    
    # Select State RTC dropdown with added "Select" option
    select_state_rtc = rtc_col.selectbox(
        "Select State RTC",
        ["Select"] + ["All"] + sorted(bus_data["Rtc_Name"].unique()),
        index=["Select", "All"].index(st.session_state.select_state_rtc) 
        if st.session_state.select_state_rtc in ["Select", "All"]
        else sorted(bus_data["Rtc_Name"].unique()).index(st.session_state.select_state_rtc) + 2
    )
    
    st.session_state.select_state_rtc = select_state_rtc

    if select_state_rtc == "Select":
        # Display message when "Select" is chosen and hide filters
        st.write("**Select any State RTC bus to continue**")
    else:
        # Dynamically update select boxes based on current selections
        def update_options():
            # Create a copy of the original data to apply filters
            filtered_data = bus_data.copy()

            # Filter the data based on the selected boarding point
            if st.session_state.select_boarding != "All":
                filtered_data = filtered_data[filtered_data["Boarding"] == st.session_state.select_boarding]

             # Filter the data based on the selected destination
            if st.session_state.select_destination != "All":
                filtered_data = filtered_data[filtered_data["Destination"] == st.session_state.select_destination]

            # Filter the data based on the selected bus type
            if st.session_state.select_bus_type != "All":
                filtered_data = filtered_data[filtered_data["Bus_Type"] == st.session_state.select_bus_type]

            # Filter the data based on the selected star rating
            if st.session_state.select_star_rating != "All":
                filtered_data = filtered_data[filtered_data["Star_Rating"] >= int(st.session_state.select_star_rating)]

             # Filter the data based on the selected route
            if st.session_state.select_route != "All":
                filtered_data = filtered_data[filtered_data["Route_Name"] == st.session_state.select_route]

            # Filter the data based on the selected seat availability
            if st.session_state.select_seat_availability != "All":
                filtered_data = filtered_data[filtered_data["Seats_Available"] >= st.session_state.select_seat_availability]

            # Filter the data based on the selected RTC name
            if st.session_state.select_state_rtc != "All":
                filtered_data = filtered_data[filtered_data["Rtc_Name"] == st.session_state.select_state_rtc]

            # Create a list of unique data from the database, adding "All" as the first option and sorting the remaining values
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

        # Creating select box for boarding point and updating values in the session state based on selection
        select_boarding = sb.selectbox(
            "Select Boarding Point",
            boarding_list,
            index=boarding_list.index(st.session_state.select_boarding)
            if st.session_state.select_boarding in boarding_list
            else 0,
            on_change=lambda: st.session_state.update({'select_destination': 'All'})
        )

        # # Creating select box for destination and updating values in the session state based on selection
        select_destination = sd.selectbox(
            "Select Destination Point",
            destination_list,
            index=destination_list.index(st.session_state.select_destination)
            if st.session_state.select_destination in destination_list
            else 0
        )

        # # Creating select box for bus_type and updating values in the session state based on selection
        select_bus_type = bt.selectbox(
            "Select Bus Type",
            bus_type_list,
            index=bus_type_list.index(st.session_state.select_bus_type)
            if st.session_state.select_bus_type in bus_type_list
            else 0
        )

        # Creating select box for star Rating and updating values in the session state based on selection
        select_star_rating = sr.selectbox(
            "Select Star Rating",
            star_rating_list,
            index=star_rating_list.index(st.session_state.select_star_rating)
            if st.session_state.select_star_rating in star_rating_list
            else 0
        )

        # Creating select box for route and updating values in the session state based on selection
        select_route = rt.selectbox(
            "Select Route",
            route_list,
            index=route_list.index(st.session_state.select_route)
            if st.session_state.select_route in route_list
            else 0
        )

        # Creating select box for seat availablility and updating values in the session state based on selection
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

        # Update session state so that if you navigate to other pages the selected values stay the same
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

        # Filter the data based on the selected boarding point, if it's not set to "All"
        if select_boarding != "All":
            filtered_data = filtered_data[filtered_data["Boarding"] == select_boarding]
        # Filter the data based on the selected destination, if it's not set to "All"
        if select_destination != "All":
            filtered_data = filtered_data[filtered_data["Destination"] == select_destination]
        # Filter the data based on the selected bus type, if it's not set to "All"
        if select_bus_type != "All":
            filtered_data = filtered_data[filtered_data["Bus_Type"] == select_bus_type]
        # Filter the data based on the selected star rating, if it's not set to "All"
        # The rating should be greater than or equal to the selected rating
        if select_star_rating != "All":
            filtered_data = filtered_data[filtered_data["Star_Rating"] >= int(select_star_rating)]
        # Filter the data based on the selected route, if it's not set to "All"
        if select_route != "All":
            filtered_data = filtered_data[filtered_data["Route_Name"] == select_route]
        # Filter the data based on the selected seat availability, if it's not set to "All"
        # The number of available seats should be greater than or equal to the selected availability
        if select_seat_availability != "All":
            filtered_data = filtered_data[filtered_data["Seats_Available"] >= select_seat_availability]
        # Filter the data based on the selected RTC (State RTC) name, if it's not set to "All"
        if select_state_rtc != "All":
            filtered_data = filtered_data[filtered_data["Rtc_Name"] == select_state_rtc]
        # Filter the data based on the selected price range
        # The price should be within the minimum and maximum selected values
        filtered_data = filtered_data[
            (filtered_data["Price"] >= select_price_min) & 
            (filtered_data["Price"] <= select_price_max)
        ]

        # Drop the 'ID' column before displaying the DataFrame
        filtered_data = filtered_data.drop(columns=["ID"])

        st.dataframe(filtered_data.reset_index(drop=True))


# Code for Bus Table Radio Button
if nav_sbar == "Bus Table":
    bus_data = bus_data.drop(columns=["ID"])
    # Setting only 10 rows per page
    page_size = 10
    # Getting the total number of rows
    total_rows = len(bus_data)
    # Dividing the total number of rows with the rows per page to set the page nubers in number input
    pages = total_rows // page_size + (total_rows % page_size != 0)

    # Splitting single column into 5 and using only the 1st one for the number input
    sele, a, b, c, d = st.columns(5)
    page = sele.number_input("Select Page Number", min_value=1, max_value=pages, step=1)

    start_row = (page - 1) * page_size
    end_row = start_row + page_size

    # Showing datas in the dataframe
    st.dataframe(bus_data.iloc[start_row:end_row].reset_index(drop=True))
