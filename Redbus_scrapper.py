import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import pymysql

route_links_l = []

route_names_l = []

boarding_point_l = []

destination_l = []

state_l = []

print(r"Default Location : D:\GitHub\Capstone Projects\RedBus Data Scrapping and Streamlit Application\RB_All_Govt_Bus_Route_Links.csv ")
loc = input("Select the location and name to save the .CSV file")

host_name = input("Enter your SQL host name (Default: localhost)")
root_name = input("Enter your SQL root name (Default: root)")
sql_password = input("Enter yourr SQL password (Default: 1234)")


# Connect to the MySQL server
mydb = pymysql.connect(
    host=host_name,
    user=root_name,
    password=sql_password
)

# Create a cursor object
cursor = mydb.cursor()

# Initialize the WebDriver (Make sure to specify the path if the WebDriver is not in your PATH)
driver = webdriver.Chrome()

# URL of the webpage
url = "https://www.redbus.in/"   # Replace with your actual URL

# Open the URL
driver.get(url)

# Wait for the carousel to load (GOVT BUSES WHOLE TAB AT THE BOTTOM OF 1ST PAGE)
carousel = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='Carousel']")))

# Find all the direct child divs of the main carousel div (SELECTING EACH GOVT BUS DIV)
sub_divs = carousel.find_elements(By.XPATH, "./div")

# Number of sub divs within the carousel (COUNTING THE NUMBER OF GOVT BUSES DIVS)
num_sub_divs = len(sub_divs)

# Iterate through EACH GOVT BUS DIVS
for i in range(1, num_sub_divs + 1):
    try:
        print(f"Inside Govt bus link number : {i}")
        # THERE ARE TWO DIVs INSIDE EACH BUS DIV AND WE NEED TO CLICK ON THE 2ND DIV TO NAVIGATE
        sub_div_xpath = f"//div[@id='Carousel']/div[{i}]/div[2]"

        # Find the second sub div element - WAITING TO LOAD EVERYTHING IN THE ABOVE DIV
        sub_div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, sub_div_xpath)))

        # Scroll to the element to ensure it's visible - TO CLICK A LINK WE NEED TO BRING IT TO THE FOCUS
        actions = ActionChains(driver)
        actions.move_to_element(sub_div).perform()

# The following code fetches the State Transport Corporation name from the website and adds it to the list
#________________________________________________________________________________________________________________________________
        state_bus = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//div[@id='Carousel']/div[{i}]")))

        state_name = state_bus.find_element(By.CLASS_NAME, "rtcName").text

        #print("The name of the state is : ",state_name)
#________________________________________________________________________________________________________________________________

        # Click on the second sub div - CLICKING ON EACH GOVT BUS PAGE IN PAGE 1
        sub_div.click()
        
        # NAVIGATING TO THE SECOND PAGE WHICH CONTAINS THE ROUTE LINKS FOR ONE STATE
#_________________________________________________________________________________________________________________________
        
        try:

            # The below code is used to get the bottom number list - FOOTER NUMBER LIST TO SEE THE NUMBER OF PAGES
            below_list = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='root']/div/div[4]/div[12]"))
            )

            # Getting all the sub divs in the bottom list - WAITING FOR THE FOOTER TO LOAD
            sub_div_bottoms = below_list.find_elements(By.XPATH, "./div")

            num_sub_div_bottom = len(sub_div_bottoms)

            # Avoiding the 1st number in the bottom list since it is already selected
            for b_ind in range(2, num_sub_div_bottom + 2):
                # Avoiding the 1st value in the 1st sub div
        
                # Main container in each government buses page - WAITING FOR ALL ROUTE LINKS TO LOAD IN THE MAIN DIV
                main_container = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='root']/div/div[4]"))
                )
        
                # Finding all the sub divs in the main container - LOADING ALL ROUTE LINKS IN SUB DIVS
                sub_divs2 = main_container.find_elements(By.XPATH, "./div")
        
                # Getting the number of sub divs inside the main container - COUNTING THE NUMBER OF BUSES IN SELECTED PAGE
                num_sub_divs2 = len(sub_divs2)
                
                # ITERATING THROUGH EACH LINKS FOR SCRAPPING THE ROUTE HYPERLINK
                # aVOIDING THE 1ST DIV BECAUSE IT ALWAYS CONTAINS ADS - SO RANGE STARTS FROM 2
                for ind in range(2, num_sub_divs2):
                    try:
                        # Construct the XPath for each sub div in the second page - EACH ROUTE LINKS
                        sub_div2_Xpath = f"//div[@id='root']/div/div[4]/div[{ind}]"

                        # Accessing sub div 2 into the variable - WAITING TO LOAD
                        sub_div2 = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, sub_div2_Xpath))
                        )

                        # Moving the cursor to the desired div - MOVING THE CURSOR TO GET THE FOCUS
                        actions2 = ActionChains(driver)
                        actions2.move_to_element(sub_div2).perform()

                        # Waiting for the route details to load fully before accessing it - WAITING FOR IT TO LOAD
                        route_element = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, f"//div[@id='root']/div/div[4]/div[{ind}]/div[1]/a"))
                        )

                        # Get the route name of the acnhor tag - GETTING THE ROUTE NAME
                        route_name = route_element.get_attribute('title')
                        
                        route_names_l.append(route_name)
                
                        # Get the href attribute of the anchor tag - GETTING THE ROUTE LINK
                        route_link = route_element.get_attribute('href')
                
                        route_links_l.append(route_link)

                        state_l.append(state_name)

                        # Going back to the original page and waiting to load all the div in the second page - LOADING THE MAIN DIV
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@id='root']/div/div[4]"))
                        )

                        # Re-load the main container and sub_divs2 after going back - REPEATING THE ABOVE STEP
                        main_container = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@id='root']/div/div[4]"))
                        )

                        sub_divs2 = main_container.find_elements(By.XPATH, "./div")
                        num_sub_divs2 = len(sub_divs2)

                    except Exception as e:
                        #print(f"Error interacting with sub div {ind}: {e}")
                        pass
        
                # Construct the XPath for the bottom number list div - ONCE THE ABOVE PAGE IS FINISED GOING TO THE BOTTOM TO GO TO NEXT PAGE
                sub_div_bottom2Xpath = f"//div[@id='root']/div/div[4]/div[12]/div[{b_ind}]"
        

                # Waiting for the bottom index to load - WAITING FOR BOTTOM NUMBERS TO LOAD
                sub_div_bottom = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, sub_div_bottom2Xpath))
                )
        
                # Moving the cursor to the desired div - BRINGING TO FOCUS
                actions2 = ActionChains(driver)
                actions2.move_to_element(sub_div_bottom).perform()

                # Clicking on the bottom index numbers to navigate to the next contents - CLICKING ON NEXT PAGE NUMBER IF AVAILABLE
                sub_div_bottom.click()
        
        except Exception as e:
            #print(f"Error interacting with sub div {b_ind}: {e}")
            pass

        # Add a delay to allow for any loading or transitions (adjust as needed)
        time.sleep(2)

        # Navigate back to the main page - GOING BACK TO THE 1ST PAGE TO CLICK ON THE NEXT GOVT BUS DIV
        driver.back()

        # Wait for the carousel to be ready again (if necessary) - WAITING TO LOAD THE PAGE
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='Carousel']")))

    except Exception as e:
        print(f"Error interacting with sub div {i}: {e}")
        
# THE ABOVE CODES SCRAPPED ALL THE LINKS FROM ALL THE GOVT BUS LINKS 

# THE BELOW CODE IS USED TO SPLIT THE BOARDING POINT AND DESTIANTION FROM THE ROUTE LINK NAME

for route in route_names_l:
    boarding, destination = route.split(" to ")
    boarding_point_l.append(boarding)
    destination_l.append(destination)

# THE BELOW CODE WILL SAVE THE SCRAPPED LINKS INTO A CSV FILE FOR FURTHER USE
try:
    print(f"Creating links list")
    # Create a DataFrame
    link_df = pd.DataFrame({
        'Serial Number': range(1, len(route_links_l) + 1),  # Auto-generated serial numbers
        'State_RTC': state_l, # Data from state_l
        'Route Link': route_links_l,  # Data from route_links_l
        'Route Name': route_names_l,   # Data from route_names_l
        'Boarding_point': boarding_point_l,
        'Destination': destination_l
    })

    link_df.to_csv(loc)
    print(f"Links list created")

except Exception as e:
    pass

# NOW THE LINKS HAVE BEEN SAVED INTO A CSV FILE NOW LET'S START SCRAPPING FROM ALL THE STORED LINKS
# THE FOLLWOING LINKS WILL GO TO EACH SAVED LINK AND WILL SCRAP THE BUS DATA AND STORE IT INTO THE SQL DIRECTLY
#_______________________________________________________________________________________________________________________

try:
    
    print(f"Creating database")
    # Create the REDBUS_DB database
    cursor.execute("CREATE DATABASE IF NOT EXISTS All_RedBus_db")

    # Use the REDBUS_DB database
    cursor.execute("USE All_RedBus_db")

    # Create a table with the specified columns and data types
    create_table_query = """
    CREATE TABLE IF NOT EXISTS All_RB_data (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        Rtc_Name TEXT,
        Route_Name TEXT,
        Route_Link TEXT,
        Boarding_Point TEXT,
        Destination TEXT,
        Bus_Name TEXT,
        Bus_Type TEXT,
        Departing_Time TIME,
        Duration TEXT,
        Reaching_Time TIME,
        Star_Rating FLOAT,
        Price DECIMAL(10, 2),
        Seats_Available INT
    )
    """
    cursor.execute(create_table_query)
    print(f"Database created")
    
except Exception as e:
    print(f"Error creating database {e}")
#----------------------------------------------------------------------------------

# # Path to import the links from the CSV file
# csv_file_path = r"C:\Users\Dell\Desktop\Data Science\GUVI\Pandas files\RB_All_Govt_Bus_Route_Links.csv"

# # Read the CSV file into a DataFrame
# load_df = pd.read_csv(csv_file_path)

# # Extract the Links column by index (index 2 since it is zero-based)
# links_column = load_df.iloc[:, 2]

# # Convert the links column to a list
# links_l = links_column.tolist()

# link_num = len(links_l)

a = 0

#-------------------------------------------------------------------------------------

for li_num, urls in enumerate(route_links_l):
    try:

        a = a + 1

        bus_data = []

        # URL of the website is taken from the list of URLs
        url = urls
        # Boarding point of the present URL
        boarding_point = boarding_point_l[li_num]
        # Destination of the present URL
        destination_point = destination_l[li_num]
        # State RTC name of the present URL
        state_rtc = state_l[li_num]

        print(f"{a} : From : {urls}")

        # Open the URL
        driver.get(url)

        #time.sleep(5)
        
        # Wait for the contents in the EACH GOVT BUSES LINK PAGE to load
        result_section = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='result-section']"))
        )

        gov_bus_div = result_section.find_elements(By.XPATH, "./div")

        # This is used to count the number of DIV with GOVT BUS to PRESS THE VIEW BUSES BUTTON
        num_gov_bus_div = len(gov_bus_div)

        time.sleep(6)

        p_div_len = num_gov_bus_div + 1

        # This FOR LOOP is used to press the number of VIEW BUSES BUTTON in the 3rd page
        for gind in range(1, num_gov_bus_div):
            try:
                #print()
                print(f"Pressing View Buses button")

                # Construct the XPath for the current bus div
                bus_div_xpath = f"//div[@id='result-section']/div[{gind}]"

                # Scroll until the element is visible in the viewport
                bus_div = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, bus_div_xpath))
                )

                # Use JavaScript to scroll to the element to the VIEW BUSES BUTTON
                driver.execute_script("arguments[0].scrollIntoView();", bus_div)

                # Optional: Small delay to ensure the page has scrolled
                time.sleep(1)

                # Move the cursor to the desired div
                actions2 = ActionChains(driver)
                actions2.move_to_element(bus_div).perform()

                # Find and click the "VIEW BUSES" button inside the div
                view_buses_btn = driver.find_element(
                    By.XPATH, f"//div[@id='result-section']/div[{gind}]/div/div[2]/div/div[4]/div[2]"
                ).click()
                #print()
                #print("Button pressed")
            except:
                pass

        try:

            print("Scrapping Data")   

            # Waiting for all the GOVT BUSES to load after pressing the "VIEW BUSES" button
            p_bus_div = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH,f"//div[@id='result-section']/div[{num_gov_bus_div}]/ul/div[1]"))
            )

            # Use JavaScript to scroll to the element to the PRIVATE BUSES button
            driver.execute_script("arguments[0].scrollIntoView();", p_bus_div)
            
            # NEW CODE TO SCROLL DOWN TO THE BOTTOM OF EACH PAGE
            
            while True:
                try:
                    # Get current height of the page
                    last_height = driver.execute_script("return document.body.scrollHeight")

                    # Scroll down to the bottom of the page
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                    # Wait for new bus items to load
                    time.sleep(3)

                    # Get new height of the page after scrolling
                    new_height = driver.execute_script("return document.body.scrollHeight")

                    # Check if new bus items have loaded by comparing heights
                    if new_height == last_height:
                        break
                except:
                    pass
            
            # NEW CODE ENDS HERE

            # NOW I NEED TO SCRAPE THE DATA FROM THE TOP TILL THE LOADED PAGE

            # Wait for the bus items to load
            bus_items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "bus-item")))

            # Wait for the bus items to load
            bus_items = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "bus-item")))

            # Loop through each bus item and extract the desired information
            for bus in bus_items:
                try:
                    # Extract data for each bus item
                    bus_name = bus.find_element(By.CLASS_NAME, "travels").text
                    bus_type = bus.find_element(By.CLASS_NAME, "bus-type").text
                    departing_time = bus.find_element(By.CLASS_NAME, "dp-time").text
                    start_place = bus.find_element(By.CLASS_NAME, "dp-loc").text
                    duration = bus.find_element(By.CLASS_NAME, "dur").text
                    reaching_time = bus.find_element(By.CLASS_NAME, "bp-time").text
                    destination_place = bus.find_element(By.CLASS_NAME, "bp-loc").text
                    try:
                        # Convert star rating to a float
                        star_rating = float(bus.find_element(By.XPATH, ".//div[contains(@class, 'rating-sec')]//span").text)
                    except ValueError:
                        # If conversion fails, assign a default value (e.g., 0.0) or skip the record
                        star_rating = 0.0
                    price_element = bus.find_element(By.CLASS_NAME, "fare")
                    price = price_element.text.split(" ")[-1]  # Extracting just the numeric price
                    seats_available_element = bus.find_element(By.CLASS_NAME, "seat-left")
                    seats_available = seats_available_element.text.split(" ")[0]  # Extracting just the number of seats available

                    # Fixed route link
                    route_link = url
                    
                    # Fixed Boarding Point
                    boarding_name = boarding_point

                    #Fixed Destination
                    destination_name = destination_point

                    #RTC NAME
                    rtc_name = state_rtc

                    # Route name (combining start and destination places)
                    route_name = f"{start_place} to {destination_place}"

                    # Append the extracted data to the list
                    bus_data.append([
                        rtc_name,
                        route_name,
                        route_link,
                        boarding_name,
                        destination_name,
                        bus_name,
                        bus_type,
                        departing_time,
                        duration,
                        reaching_time,
                        star_rating,
                        price,
                        seats_available
                    ])
                except Exception as e:
                    #print(f"Error extracting data for a bus item: {e}")
                    pass

        except:
            pass

        # TILL HERE

        # SQL CODES MUST COME HERE
        #_________________________________________________________________________________________________________________________

        # CODE MUST START AT THIS INDENTATION
        try:

            # Create a DataFrame
            columns = ["Rtc_Name", "Route_Name", "Route_Link", "Boarding_Point", "Destination", "Bus_Name", "Bus_Type", "Departing_Time", "Duration", "Reaching_Time", "Star_Rating", "Price", "Seats_Available"]
            bus_lis_df = pd.DataFrame(bus_data, columns=columns)

            # TILL HERE

            # Here we need to add the code to add the scrapped data into the SQL

            print(f"Inserting data into SQL")

            # Insert DataFrame data into the table
            insert_query = """
            INSERT INTO All_RB_data (Rtc_Name, Route_Name, Route_Link, Boarding_Point, Destination, Bus_Name, Bus_Type, Departing_Time, Duration, Reaching_Time, Star_Rating, Price, Seats_Available)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Convert 'departing_time' and 'reaching_time' to time format for insertion
            bus_lis_df['Departing_Time'] = pd.to_datetime(bus_lis_df['Departing_Time']).dt.time
            bus_lis_df['Reaching_Time'] = pd.to_datetime(bus_lis_df['Reaching_Time']).dt.time

            time.sleep(2)

            # Insert DataFrame data into the SQL table
            for index, row in bus_lis_df.iterrows():
                cursor.execute(insert_query, (
                    row['Rtc_Name'],
                    row['Route_Name'],
                    row['Route_Link'],
                    row['Boarding_Point'],
                    row['Destination'],
                    row['Bus_Name'],
                    row['Bus_Type'],
                    row['Departing_Time'],
                    row['Duration'],
                    row['Reaching_Time'],
                    row['Star_Rating'],
                    row['Price'],
                    row['Seats_Available']
                ))

            # Commit the changes
            mydb.commit() 

            print("------Inserted------")

        except Exception as e:
            print(f"Error inserting data : \n {e}")
    #_________________________________________________________________________________________________________________________
    # SQL CODES TILL HERE

    except Exception as e:
        print(f"Oops no buses found in the link : {urls}")
        pass       

#________________________________________________________________________________________________________________________________

# SQL query to select all data from the table
query = "SELECT * FROM All_RB_data"

# Use pandas to execute the query and load the data into a DataFrame
all_bus_data_df = pd.read_sql(query, mydb)

# Path to save the CSV file
csv_file_path = r"D:\GitHub\Capstone Projects\RedBus Data Scrapping and Streamlit Application\RB_All_Govt_Bus_Data.csv"

# Save the DataFrame to a CSV file
all_bus_data_df.to_csv(csv_file_path, index=False)
#________________________________________________________________________________________________________________________________


# Closign SQL connection
cursor.close()
mydb.close()

print(f"Data successfully exported to {csv_file_path}")
#________________________________________________________________________________________________________________________
# Close the WebDriver
driver.quit()
