import streamlit as st
import pandas as pd

# Load data from CSV
@st.cache_data
def data_load():
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

# Sidebar with navigation options
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Select Bus"])

if page == "Home":
    st.title("This is home page")
elif page == "Select Bus":

    # LOGO image for the webpage
    st.image("NevzBusLogo.png", width=750)

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
