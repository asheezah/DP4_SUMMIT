import streamlit as st

#import statements
import time
import requests
import smtplib
import folium
import webbrowser
from geopy.geocoders import Nominatim
from streamlit_extras.floating_button import *
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation, get_page_location, streamlit_js_eval
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import networkx as nx

from functions import sidebar, help_button, get_geocoords_func

##Will display visual warning if current hour or next hour has any dangerous weather
def weather_warning(user_latitude, user_longitude, error):

    ##Gets current time of users device
    def get_current_hour():
        current_time = time.localtime()
        current_hour = current_time[3]
        return current_hour

    ##Convert latitude and longitude to city
    def get_city(latitude, longitude):
        geolocate = Nominatim(user_agent="student_project")
        coords = [latitude, longitude]
        location = geolocate.reverse(coords)
        full_geocode = location.raw['address']
        ##Normally full_geocode teturns a VERY long string of location data
        ##Needs to get just the city, town or county
        for i in full_geocode:
            if i == "city" or i == "town" or i == "county":
                city_name = full_geocode[i]
                for j in full_geocode:        
                    if j == "state":
                        area = full_geocode[j]
                        city = str(city_name + ", " + area)
                        break
                    else:
                        city = city_name
                break      
        return city

    ##Set up Weather API
    def setup_weather(latitude, longitude):
        BASE_URL = "http://api.weatherapi.com/v1/forecast.json?"
        key = str(st.secrets['weather_api'])
        city = get_city(str(latitude), str(longitude))  

        url = BASE_URL + "key=" + key + "&q=" + city + "&days=2"
        query = requests.get(url).json()

        #Get current temp and conditons
        celcius = query['current']['temp_c']
        conditions = str(query['current']['condition']['text']).strip()
    
        ##Get next hour temp and conditions
        hour = get_current_hour()
        if hour != 23:
            next_hour_conditons = str(query['forecast']['forecastday'][0]['hour'][hour+1]['condition']['text']).strip()
            next_hour_celcius = query['forecast']['forecastday'][0]['hour'][hour+1]['temp_c']
            
        else:
            next_hour_conditons = str(query['forecast']['forecastday'][1]['hour'][1]['condition']['text']).strip()
            next_hour_celcius = query['forecast']['forecastday'][1]['hour'][1]['temp_c']

        ##Compute the difference in temperatues to see if there was a change

        return celcius, conditions, next_hour_celcius, next_hour_conditons

    ##Determine the risk levels of the temperatures and conditions
    def risk_evaluation():
        adjusted_conditions = str(conditions).split()
        adjusted_next_hour_conditions = str(next_hour_conditions).split()

        ##Temperature Risks: 4: Highest, 0: No Risk
        trisk = 0
        if celcius >= 30 or celcius <=-20 or next_hour_celcius >= 30 or next_hour_celcius <= -20:
            trisk = 4
        elif celcius >= 25 or celcius <= -7 or next_hour_celcius >= 25 or next_hour_celcius <= -7:
            trisk = 3
        elif celcius >=20 or celcius <= 0 or next_hour_celcius >= 20 or next_hour_celcius <= 0:
            trisk = 2
        elif celcius <= 5 or next_hour_celcius <= 5:
            trisk = 1
        
        ##Condition Risk
        crisk = False
        dangerous_conditions = ["Thunderstorm", "thunderstorm", "Squall", "squall", "Freezing", "freezing", "Rain", "rain", "Snow", "snow", "Fog", "fog", "Drizzle", "drizzle"]
        next_hour_crisk = False        
        for i in adjusted_next_hour_conditions:
            for j in dangerous_conditions:
                if i == j:
                    crisk = True
                    break
        for i in adjusted_conditions:
            for j in dangerous_conditions:
                if i == j:
                    crisk = True
                    break
        return trisk, crisk

    
    ##If a dangerous temp or condition is present, warning will display
    def display_warning():
        if trisk > 0 or crisk == True:
            with st.container(border=True):
                st.header("⚠️")
                st.error("Temperature and conditions outside are not ideal, outdoor naviagation may be unsafe")
                ##Give user option to swap to weather page to see whats wrong
                if st.button("Click to see why", use_container_width=True, type='primary'):
                    st.switch_page("pages/Weather.py")


    ##Call functions and assign the multitude of variables
    with st.spinner("Getting Weather Data"): 
        time.sleep(0.5)
        #user_latitude, user_longitude, error = get_geocoords_func()     
        if error == False:
            if user_latitude and user_longitude != 0:
                celcius, conditions, next_hour_celcius, next_hour_conditions = setup_weather(str(user_latitude), str(user_longitude))
                trisk, crisk = risk_evaluation()
                display_warning()
        else:
            st.error("Could Not Get Access to Geolocation, Weather Unavailable")

##Provide user the opportunity to report discrepencies on the map
def report(user_latitude, user_longitude, error):
    ##Streamlit secrets to hide valuable information
    email = str(st.secrets['gmail'])
    pswd = str(st.secrets['password'])
    sender_email = email
    sender_password = pswd
    receiver_email = email

    st.title("Report")
    ##Call very similar function to feedback email function
    def send_an_email(problem, affected, prob_body, affect_body, user_location):
        index = 0

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "REPORT: Problem: " + problem + ", Affected: " + affected 

        msg.attach(MIMEText("Problem: " + problem + "\n" + prob_body + "\n" + "Affected: " + affected + "\n" + affect_body + "\nLocation Reported: " + user_location, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                text = msg.as_string()

                server.sendmail(sender_email, receiver_email, text)
                index = 1
        except:
            index = 2
        
        return index

    #user_latitude, user_longitude, error = get_geocoords_func()  
    prob_body = ""
    affect_body = ""
    ##Allow the user to define the problem
    problem = st.selectbox(
        "What is the issue?",
        ("", "Broken/Blocked Location", "Missing Feature", "Other")
    )
    ##If user selects other, provide the option to expand
    if problem == "Other":
        prob_body = st.text_input("Please Expand:", max_chars=100, placeholder="Begin Typing")
    ##Allow the user to define what is affected
    affected = st.selectbox(
        "What is affected?",
        ("", "Elevator", "Stairs", "Ramp", "Food Location", "Other")
    )
    ##If user selects other, provide the option to expand
    if affected == "Other":
        affect_body = st.text_input("Please Expand:", max_chars=150, placeholder="Begin Typing")
    ##If problem and effected have inputs, open the opportunity to attach a location, either current or other, which lets the user type their location
    if problem != "" and affected != "":
        location = st.selectbox(
            "Where is this?",
            ("", "Current location", "Other")
        )
        ##Show loading wheel to express to the user that geolocation is being collected
        if location == "Current location":
            with st.spinner("Working on it..."): 
                time.sleep(3)   
                if error == False:
                    if user_latitude and user_longitude != 0:
                        user_location = "\nLatitude: " + str(user_latitude) + "\nLongitude: " + str(user_longitude)            
                ##If geolocation could not be found, display this to the user
                else:
                    st.markdown(":red[Couldn't get current location]")
                    location = "Other"
        if location == "Other": 
            user_location = st.text_input("Please describe the location:", max_chars=100, placeholder="Begin Typing")

    ##Ensures no empty emails are send
    if problem == "" or affected == "" or location == "" or user_location == "":
        if st.button("Send Email"):
            st.session_state.button = False
            if problem == "" or affected == "":
                st.toast("Please fill out required fields.")
    else:
        if st.button("Send Email"):
            st.session_state.button = True
            
            index = send_an_email(problem, affected, prob_body, affect_body, user_location)
            if index ==1:
                st.toast("Email Recieved!", icon="✅")
                time.sleep(1.5)
                ##Reload the page to reset the report form
                streamlit_js_eval(js_expressions="parent.window.location.reload()")
            else:
                st.toast("Email Couldn't Send...")

#1: GET GEOLOCATION
# def get_geocoords():
#     user_location = get_geolocation()
#     if user_location and 'error' in user_location:
#         if user_location['error']['code'] == 1:
#             st.error("Couldn't get location, sorry")
#         else: st.warning(f"Geolocation error: {user_location['error']['message']}")
#     elif user_location:
#         user_latitude = user_location['coords']['latitude']
#         user_longitude = user_location['coords']['longitude']    
#     user_location_json = get_page_location()
#     return (user_latitude, user_longitude)


#2: MAP
def make_map():
    outMUSC = folium.Map(location = (43.263407,-79.917609), tiles="CartoDB Positron", zoom_start=20) #initalizes map, centred at MUSC
    musc1 = 'pages/MUSC.png'
    name = 'Floor Plan 1'
    bounds = [[43.263106,-79.918454],[43.263827,-79.917165]] #bounds for the floor map overlap
    folium.raster_layers.ImageOverlay(image = musc1, #overlays a floor map png onto the base map
                                  bounds = bounds,
                                  name = name
                                  ).add_to(outMUSC)
    
    #Return map object
    return outMUSC

#3: NODES
def dist(Source, Target): #find the distance between two points/nodes, written in the format: source = (lat, long), target...
    return ((Source[0]-Target[0])**2 + (Source[1]-Target[1])**2)**0.5

def init_graph(node_file, edge_file): #uses networkx to initalize nodes and edges
    G = nx.Graph() #create G, which the graph object for networkx
    node_fields = ['name','lat','long','type'] #column titles in excel file
    nodes = pd.read_csv(node_file,usecols=node_fields) #reads through excel file, using column titles
    places = {
        types:group[['name','lat','long','type']].to_dict(orient='records')
        for types, group in nodes.groupby('type')
        } #creates a dictionary, organizing them based on type
    
    #initalizes node in graph
    for i in range(len(nodes['name'])): #loops through G to add each node, with name, position (lat, long), and type
        G.add_node(nodes['name'][i], 
                   pos = (nodes['lat'][i], nodes['long'][i]), 
                   type = nodes['type'][i])
        
    #adds list of edges
    values = pd.read_csv(edge_file, usecols=['Source', 'Target']) #reads through another excel file, using column titles
    
    lists = {'Source': values['Source'].tolist(), #creates a list of both columns, with each column keyed to the column header
             'Target': values['Target'].tolist()}
    
    for i in range(len(lists['Source'])):
        source = lists['Source'][i] #goes through the list of edges, and retrieves the name of each corresponding source and target
        target = lists['Target'][i]

        source_pos = G.nodes[source]['pos'] #uses the names we just retrieved to get the coordinates associated with those nodes
        target_pos = G.nodes[target]['pos']

        edge_weight = dist(source_pos, target_pos) #calculates the distance between the two nodes, which will be used as weight
        G.add_edge(lists['Source'][i], lists['Target'][i], weight=edge_weight) #loops through list of edges, adding each edge to the graph
    return G, places #returns the graph object and places, which has each node location and type

def init_location(G, user_coords, outMUSC, state): #user_coords needs to be (lat, long)
    state.insert(0,
        folium.Marker(location = user_coords, #creates a marker for the user's location, using geolocation
                              tooltip="Click me!",
                              popup = f"This is your location",
                              icon = folium.Icon(color = "green")
                              ))
    user_node_name = 'Start Node' #all nodes need to have a string name associated with their position coordinates
    G.add_node(user_node_name, pos=user_coords)
    return user_node_name

#4A: DISPLAY
def customize_image(destination): #matches custom folium icons to the key in the dictionary (type of location)
    if destination == 'elevator':
        image = 'pages/ELEVATOR.png'
    elif destination == 'stairs':
        image = 'pages/STAIRS.png'
    elif destination == 'exit':
        image = 'pages/EXIT.png'
    elif destination == 'parking':
        image = 'pages/PARKING.png'
    elif destination == 'washroom':
        image = 'pages/WASHROOM.png'
    elif destination == 'ramp':
        image = 'pages/RAMP.png'
    elif destination == 'food':
        image = 'pages/FOOD.png'
    return image #returns the specific png, so that it can be called inputted later 

def customize_icon(image): #defines custom icon
    icon = folium.CustomIcon(
        image,
        icon_size = (31,31),
        icon_anchor = (15.5,15.5),
        popup_anchor = (-3,20))
    return icon

def display_markers(outMUSC, places, destination, state): #displays all locations of a specific category (ex. all elevators)
    image = customize_image(destination)

    for i in places.get(destination,[]):
        icon = customize_icon(image)

        state.append(
            folium.Marker(
            location=[i['lat'], i['long']],
            tooltip=i['name'],
            icon=icon
        ))

#4B: SHORTEST PATH
def find_closest_node(G, user_node_name): #pulls coordinates from nx graph, then initalizes edge to closest node
    user_pos = G.nodes[user_node_name]['pos']
    best_dis = float('inf')
    closest_node_name = None
    for node in G.nodes: #iterates through every node and finds the closest one
        if node == user_node_name:
            continue
        node_pos = G.nodes[node]['pos']
        distance = dist(user_pos, node_pos)
        if distance < best_dis: 
            best_dis = distance
            closest_node_name = node
    G.add_edge(user_node_name, closest_node_name, weight = best_dis) #initalizes edge, so that the geolocation node can be connected to the graph

def find_shortest_path(G, user_node_name, destination, heuristic, places): #returns shortest path out of specified type (ex. elevator)
    best_path = float('inf')
    for des in places[destination]: #places['destination'] opens list of all ex. elevators, des = elevator1, etc
        target_name = des['name']
        possible_path = nx.astar_path_length(G, user_node_name, target_name, heuristic = heuristic, weight = 'weight')
        if possible_path < best_path:
            best_path = possible_path
            closest_location = target_name #closest_location is the name of the node that leads to the shortest path
    return closest_location

def shortest_path(G, user_node_name, closest_location, heuristic): #returns nodes of shortest path
    return nx.astar_path(G, user_node_name, closest_location, heuristic = heuristic, weight = 'weight')
    
def display_path(G, path, outMUSC, closest_location, image, destination, state, route): #display path and marker at destination
    coords = []
    for i in path: #output of shortest path function
        temp_list = G.nodes[i]['pos']
        coords.append(temp_list)
    route.append(folium.PolyLine(coords, smooth_factor = 50))
    image = customize_image(destination) #matches the image to the type of destination
    icon = customize_icon(image) #creates an icon for that destination
    state.append(
        folium.Marker(location = G.nodes[closest_location]['pos'], #creates marker at destination
                  tooltip="Click me!",
                  popup = f"This is your destination: {closest_location}",
                  icon = icon
                  ))


def backend_main(user_lat, user_long, error):
    st.title(":fast_forward: Welcome to the Map! :rewind:", text_alignment='center')
    st.divider()

    if error == False:
        user_coords = [user_long, user_lat]
    if error == True:
        user_coords = [43.263407, -79.917609]
        st.toast("Could not get geolocation, preset applied", icon = "🚨")

    #Intialize a session state for markers so that they appear on map across reruns
    #initialize a session state for the polyline (pathfinding) route so that it appears across reruns
    if 'route' not in st.session_state:
        st.session_state['route'] = []
    if 'marker' not in st.session_state:
        st.session_state['marker'] = []

    #Create a feature group for markers (so that the map doesn't have to reload as markers are added and removed)
    fg = folium.FeatureGroup(name="markers")

    outMUSC = make_map()
    G, places = init_graph('pages/DP4 Node Locations - Nodes.csv', 'pages/DP4 Node Locations - Edges.csv') #create network of nodes and edges
    user_node_name = init_location(G, user_coords, outMUSC, st.session_state["marker"]) #plots user location on map, and initalizes a node for the user in the graph

    select = []
    map_ready = False

    #Get user locations with dropdown menu, from the node csv file
    for i in list(places.keys()):
        #Hallway is a node, but we don't want the user to select it
        if i != 'hallway':
            select.append(i)
    destination = st.selectbox("Select your **desired** destination:", select)

    #Determine mode
    #MODE: either display all markers of that types (e.g. all elevators)
    #OR find and display  shortest path
    organize = st.columns(2)
    display = organize[0].button("Display All " + destination, key = "display_mode", help = "Show all features of specified category on map", width = "content")
    sp = organize[1].button("Find Shortest Path to " + destination,  key = "sp_mode", help = "Navigate to desired feature", width = "content")

    if sp:
        #clear session states so that every time the user selects something new, the previous option they selected is not present as well
        st.session_state["marker"] = [st.session_state["marker"][0]]
        st.session_state["route"] = []
        find_closest_node(G,user_node_name)
        def heuristic(source,target): #heuristic has to be formatting in a specific way for networkx to function, so it can't have G as an arg.
            x1, y1 = G.nodes[source]['pos'] #therefore, it has to be defined in main()
            x2, y2 = G.nodes[target]['pos']
            return ((x1-x2)**2 + (y1-y2)**2)**0.5
        closest_location = find_shortest_path(G, user_node_name, destination, heuristic, places)
        path = shortest_path(G, user_node_name, closest_location, heuristic)
        image = customize_image(destination) #function is reused from toggle code, for simplicity
        display_path(G, path, outMUSC, closest_location, image, destination, st.session_state["marker"], st.session_state["route"])
        map_ready = True
    if display:
        #clear session states so that every time the user selects something new, the previous option they selected is not present as well
        st.session_state["route"] = []
        #We want to clear the marker session state, but keep the marker that indicates user location still there
        st.session_state["marker"] = [st.session_state["marker"][0]]

        display_markers(outMUSC, places, destination, st.session_state["marker"]) #display mode relies only on the key, ex. elevators not any specific location
        #display_markers is essentially a 'mini main()', which is why the code is shorter here
        map_ready = True
    st.write("Check the map!")

    #Add the markers to the feature group so that they can be displayed together, and added and removed without reloading the entire map
    for m in st.session_state["marker"]:
        m.add_to(fg)
    
    #Add the polyline to the map, if it exists
    for r in st.session_state['route']:
        r.add_to(outMUSC)

    #Using the streamlit-folium library to integrate the folium map into the streamlit website
    st_data = st_folium(outMUSC, feature_group_to_add = fg, width=1200, height=500)
    st.write(st_data)

    #some random json text kept showing up underneath so this html code is to get rid of that, good riddance
    st.markdown("""
                <style>
                [data-testid="stJson"] {display: none;}

                </style>""", unsafe_allow_html = True)
    st.markdown("""
                <style>
                <div class="stElementContainer element-container st-key-LOC st-emotion-cache-1vo6xi6 e1rw0b1u1"  {display: none;}
                </style>""", unsafe_allow_html = True)

def map_page():
    user_latitude, user_longitude, error = get_geocoords_func()
    backend_main(user_latitude, user_longitude, error)
    with st.popover("Report Discrepancy", use_container_width=True):
        report(user_latitude, user_longitude, error)
    weather_warning(user_latitude, user_longitude, error)

sidebar()
help_button()
map_page()