import streamlit as st
#testing

#import statements
import folium
import webbrowser
import numpy
from folium.raster_layers import ImageOverlay
from streamlit_folium import st_folium

#dictionary of places
places = [{"name": "lot B1", "long":43.263110,"lat": -79.916789, "type": "parking"},
          {"name": "lot B2", "long": 43.263243, "lat": -79.916671, "type": "parking"},
          {"name": "lot C", "long": 43.264228, "lat": -79.916091, "type": "parking"},
          {"name":"elevator1", "long": 43.263744, "lat": -79.917353, "type": "elevator"},
          {"name":"elevator2", "long": 43.263735, "lat":-79.917796, "type": "elevator"},
          {"name": "elevator3", "long":43.263194, "lat": -79.917619, "type": "elevator"},
          {"name": "centre", "long": 43.263407, "lat": -79.917609, "type": "centre"}]

def backend_main():
    outMUSC = make_map()
    st.write("The current locations in the dictionary are: ")
    for place in places:
        st.markdown(f"-{place['name']}")

    #customize icons and markers
    parking_image = 'pages/PARKING.png'
    elevator_image = 'pages/Elevator 2.png'
    
    parking_icon, centre_icon, elevator_icon = customize_icon(parking_image,elevator_image)
    custom_map = {"parking":{"icon": parking_icon},
              "elevator":{"icon": elevator_icon}, "centre":{"icon":centre_icon}}

    org1 = st.columns(2)
    location = org1[0].text_input("What is your current location?", key='location')
    org1[1].space("small")
    enter1 = org1[1].button("Enter", icon = '👍', key='button1')
    found_loc = False
    if enter1:
        #location = input("What is your current location?: ")
        #Check if current location in dictionary
        for place in places:
            if place["name"] == location: #sorts through the dictionary to see if any names match
                long1 = place.get("long")
                lat1 = place.get("lat")
                loc = [long1,lat1]
                folium.Marker(location = loc,
                              tooltip="Click me!",
                              popup = f"This is your location: {location}",
                              icon = folium.Icon(colour = "green")
                              ).add_to(outMUSC)
                found_loc = True
                break
        if not found_loc:
            st.write("Invalid input, reinput a location from the dictionary")
        elif found_loc:
            
            #Now find the destination
            org2 = st.columns(2)
            destination = org2[0].text_input("What is your destination?", key='destination')
            org2[1].space("small")
            enter2 = org2[1].button("Enter", icon = '👍', key = 'button2')
            found_des = False
            if enter2:
            #destination = input("What is your destination?: ")
                for place in places:
                    if place["name"] == destination:
                        long2 = place.get("long")
                        lat2 = place.get("lat")
                        des = [long2,lat2]
                        info = custom_map[place["type"]]
                        icon = info["icon"]
                        folium.Marker(location = des,
                                      tooltip="Click me!",
                                      popup = f"This is your destination: {destination}",
                                      icon = icon).add_to(outMUSC)
                    
                        found_des = True
                        break
                if not found_des:
                    st.write("Invalid input, reinput a location from the dictionary") 
                elif found_des:
                    st.write("Destination Found!")
                    st.write("Check the map!")

    map_overlay(outMUSC) #adds map overlay picture
    #create_line(loc,des,outMUSC) #visually draws a path

    outMUSC.save("test_map.html")
    st_data = st_folium(outMUSC)
    st.write(st_data)
    #webbrowser.open_new("test_map.html") #opens the map file in your default browser

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
