import streamlit as st
#testing

#import statements
import folium
import webbrowser
import numpy
from folium.raster_layers import ImageOverlay
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation, get_page_location

def get_geocoords():
    user_location = get_geolocation()
    if user_location and 'error' in user_location:
        if user_location['error']['code'] == 1:
            st.error("Couldn't get location, sorry")
        else: st.warning(f"Geolocation error: {user_location['error']['message']}")
    elif user_location:
        user_latitude = user_location['coords']['latitude']
        user_longitude = user_location['coords']['longitude']    
    user_location_json = get_page_location()
    st.write(user_latitude, user_longitude)
    return user_latitude, user_longitude

user_latitude, user_longitude = get_geocoords()

#dictionary of places
places = [{"name": "lot B1", "long":43.263110,"lat": -79.916789, "type": "parking"},
          {"name": "lot B2", "long": 43.263243, "lat": -79.916671, "type": "parking"},
          {"name": "lot C", "long": 43.264228, "lat": -79.916091, "type": "parking"},
          {"name":"elevator1", "long": 43.263744, "lat": -79.917353, "type": "elevator"},
          {"name":"elevator2", "long": 43.263735, "lat":-79.917796, "type": "elevator"},
          {"name": "elevator3", "long":43.263194, "lat": -79.917619, "type": "elevator"},
          {"name": "centre", "long": 43.263407, "lat": -79.917609, "type": "centre"},
          {"name": "current location", "long": float(user_latitude), "lat": float(user_longitude), "type": "current"}]



def backend_main():
    st.title(":fast_forward: Welcome to the Map! :rewind:", text_alignment='center')
    st.divider()
    outMUSC = make_map()
    select = []
    parking_image = 'pages/PARKING.png'
    elevator_image = 'pages/Elevator 2.png'
    map_ready1 = False
    map_ready2 = False
    marker_data = []

    #Intialize a session state
    if 'selected_marker' not in st.session_state:
        st.session_state['selected_marker'] = {"name": 'lot B1', "long":43.263110,"lat": -79.916789, "type": "parking"}
    
    parking_icon, centre_icon, elevator_icon = customize_icon(parking_image,elevator_image)
    custom_map = {"parking":{"icon": parking_icon},
              "elevator":{"icon": elevator_icon}, "centre":{"icon":centre_icon}}


    for i in range(len(places)):
        select.append(places[i]["name"])
    location = st.selectbox("Select your **current** location:", select)
    destination = st.selectbox("Select your **desired** destination:", select)

    if location == destination:
        st.write("Invalid, try again...")
    else:
        #Put Markers for the current location
        for place in places:
            if place["name"] == location:
                long1 = place.get("long")
                lat1 = place.get("lat")
                loc = [long1,lat1]
                folium.Marker(location = loc,
                              tooltip="Click me!",
                              popup = f"This is your location: {location}",
                              icon = folium.Icon(colour = "green")
                              ).add_to(outMUSC)
                map_ready1 = True
            elif place["name"] == destination:
                long2 = place.get("long")
                lat2 = place.get("lat")
                des = [long2,lat2]
                info = custom_map[place["type"]]
                icon = info["icon"]
                folium.Marker(location = des,
                              tooltip="Click me!",
                              popup = f"This is your destination: {destination}",
                              icon = icon).add_to(outMUSC)
                map_ready2 = True
        if map_ready1 and map_ready2:
            st.write("Check the map!")
            map_overlay(outMUSC) #adds map overlay picture
            st_data = st_folium(outMUSC)
            st.write(st_data)

##    map_overlay(outMUSC) #adds map overlay picture
##    #create_line(loc,des,outMUSC) #visually draws a path
##
##    outMUSC.save("test_map.html")
##    #webbrowser.open_new("test_map.html") #opens the map file in your default browser

def make_map():
    outMUSC = folium.Map(location = (43.263407,-79.917609), zoom_start=19)
    return outMUSC

def customize_icon(parking_image,elevator_image):
    #Parking
    parking_icon = folium.CustomIcon(
        parking_image,
        icon_size = (31,31),
        icon_anchor = (15.5,15.5),
        popup_anchor = (-3,20))
    #Centre
    centre_icon = folium.Icon(icon = "star",
            color = "orange")
    #Elevator
    elevator_icon = folium.CustomIcon(
        elevator_image,
        icon_size = (31,31),
        icon_anchor = (15.5,15.5),
        popup_anchor = (-3,20))
    return parking_icon, centre_icon, elevator_icon

def map_overlay(outMUSC):
    #plants a picture overlay
    musc1 = 'pages/MUSC 3.png'
    bounds = [[43.263106,-79.918454],[43.263827,-79.917165]]
    name = 'Floor Plan 1',

    # bounds = [[sw_lat, sw_lon], [ne_lat, nw_lon]
    folium.raster_layers.ImageOverlay(image = musc1,
                                  bounds = bounds,
                                  name = name
                                  ).add_to(outMUSC)

#creates a straight line connecting location and destination
##def create_line(loc,des,outMUSC):
##    folium.PolyLine([loc, des], tooltip = "Coast").add_to(outMUSC)

backend_main()