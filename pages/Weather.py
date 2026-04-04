import requests
import streamlit as st
import time
from streamlit_extras.floating_button import *
from streamlit_js_eval import get_geolocation, get_page_location
from geopy.geocoders import Nominatim

from functions import sidebar, help_button, get_geocoords_func

def weather():

    ##Gets current time of users device
    def get_current_hour():
        current_time = time.localtime()
        current_hour = current_time[3]
        return current_hour

    ##Convert latitude and longitude to city
    def get_city(latitude, longitude):
        geolocate = Nominatim(user_agent="DP4_student_project")
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
        change_in_celcius = round(next_hour_celcius - celcius,2)
        if change_in_celcius == 0:
            rise_or_drop = "Null"
        elif change_in_celcius > 0:
            rise_or_drop = "rise"
        elif change_in_celcius < 0:
            rise_or_drop = "drop"
            change_in_celcius = abs(change_in_celcius)
        
        ##Check if the conditions change
        if conditions == next_hour_conditons:
            change_in_conditions = "No Change in Conditions"
        else: 
            change_in_conditions = "Conditions Expected to Shift to " + str(next_hour_conditons)

        return celcius, conditions, next_hour_celcius, next_hour_conditons, change_in_celcius, change_in_conditions, rise_or_drop, city

    ##Determine the risk levels of the temperatures and conditions
    def risk_evaluation(celcius, conditions):
        adjusted_conditions = str(conditions).split()
        adjusted_next_hour_conditions = str(next_hour_conditions).split()

        ##Temperature Risks: 4: Highest, 0: No Risk
        trisk = 0
        if celcius >= 30 or celcius <=-20:
            trisk = 4
        elif celcius >= 25 or celcius <= -7:
            trisk = 3
        elif celcius >=20 or celcius <= 0:
            trisk = 2
        elif celcius <= 5:
            trisk = 1
        
        ##Assign a returned statement to each risk level
        if trisk == 4:
            temp_risk = "⚠️⚠️⚠️ Very Extreme Temperature Risks! Please Stay Indoors!"
        elif trisk == 3:
            temp_risk = "⚠️ High Temperature Risks! Advisory to Stay Indoors!"
        elif trisk == 2:
            temp_risk = "🟠 Moderate Temperature Risks! Please be Careful Outside"
        elif trisk == 1:
            temp_risk = "🟡 Mild Temperature Risks! Please be Careful Outside!"
        else:
            temp_risk = "🟢 Temperatures Looking Good!"
        
        ##Condition Risk
        crisk = "None"
        high_risk_conditions = ["Thunderstorm", "thunderstorm", "Squall", "squal", "Freezing", "freezing"]
        mod_risk_conditions = ["Rain", "rain", "Snow", "snow", "Fog", "fog"]
        low_risk_conditions = ["Drizzle", "drizzle"]
        for i in adjusted_conditions:
            for x in high_risk_conditions:
                if i == x:
                    crisk = "High"
                    break
            for y in mod_risk_conditions:
                if i == y:
                    crisk = "Mod"
                    break
            for z in low_risk_conditions:
                if i == z:
                    crisk = "Low"
                    break

        ##Assign conditions risk to output statements
        if crisk == "High":
            cond_risk = "⚠️ Current Weather Condtions Pose HIGH Risk! Please Stay Indoors!"
        elif crisk == "Mod":
            cond_risk = "🟠 Current Weather Condtions Pose MODERATE Risk! Advisory to Stay Indoors!"
        elif crisk == "Low":
            cond_risk = "🟡 Current Weather Condtions Pose MILD Risk! Advisory to Stay Indoors!"
        else:
            cond_risk = "🟢 Current Conditions Looking Good!"

        ##Will Be used later, but if conditions improve, a different statement is output
        next_hour_dangerous_conditions = ["Thunderstorm", "thunderstorm", "Squall", "squal", "Freezing", "freezing", "Rain", "rain", "Snow", "snow", "Fog", "fog", "Drizzle", "drizzle"]
        next_hour_crisk = False        
        for i in adjusted_next_hour_conditions:
            for j in next_hour_dangerous_conditions:
                if i == j:
                    next_hour_crisk = True
                    break
        

        
        return trisk, crisk, temp_risk, cond_risk, next_hour_crisk

    ##Displays the Temperature
    def display_temp():
            st.markdown("Temperature") 
            st.header(str(celcius)+" °C")
            ##If temp is rise or drop, check if its entering a dangerous range, if so, warn the user
            if rise_or_drop == "rise" or rise_or_drop == "drop":
                if next_hour_celcius >=20 or next_hour_celcius <=5:
                    if celcius >= 20 or celcius <= 5:
                        st.markdown(f":red[Expected to {rise_or_drop} {str(change_in_celcius)} °C in the next hour (Warning Persists)]")
                    else:
                        st.markdown(f":red[Expected to {rise_or_drop} {str(change_in_celcius)} °C in the next hour (Entering Dangerous Range)]")
                else:
                    st.markdown(f":green[Expected to {rise_or_drop} {str(change_in_celcius)} °C in the next hour]")
            elif rise_or_drop == "Null":
                st.write("No expected change in temperature in the next hour")
            ##Output the string output for the temperature risks
            if trisk > 0:
                st.error(temp_risk)
            else:
                st.success(temp_risk)

    ##Displays the Conditions
    def display_cond():
            ##Display the conditions
            st.markdown("Conditions")
            st.header(str(conditions))
            ##If conditions are harsh, display the change as red
            if next_hour_crisk == True:
                st.markdown(f":red[{str(change_in_conditions)} in the next hour]")
            else:
                st.markdown(f":green[{str(change_in_conditions)} in the next hour]")
            if crisk == "High" or crisk == "Mod" or crisk == "Low":
                st.error(cond_risk)
            else:
                st.success(cond_risk)

    def display():

        with st.container(border=True):
                st.header("Displaying weather for " + str(city))
                col1, col2 = st.columns(2)
                with col1:
                    with st.container(border=True):
                        display_temp()
                with col2:
                    with st.container(border=True):
                        display_cond()

    ##Call functions and assign the multitude of variables
    st.title("Weather")
    with st.spinner("Working on it..."): 
        time.sleep(0.5)
        user_latitude, user_longitude, error = get_geocoords_func()     
        if error == False:
            
            if user_latitude and user_longitude != 0:
                celcius, conditions, next_hour_celcius, next_hour_conditions, change_in_celcius, change_in_conditions, rise_or_drop, city = setup_weather(str(user_latitude), str(user_longitude))
                trisk, crisk, temp_risk, cond_risk, next_hour_crisk  = risk_evaluation(celcius, conditions)
                display()
                st.toast("Done!", icon="✅")
            
        else:
            st.error("Could Not Get Access to Geolocation, Weather Unavailable")
            
sidebar()
help_button()
weather()

