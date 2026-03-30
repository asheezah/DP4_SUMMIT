import streamlit as st
import smtplib
import time
import requests
from streamlit_js_eval import get_geolocation, get_page_location
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from geopy.geocoders import Nominatim

#Feedback Dialog
@st.dialog("Send Feedback", width = "medium", dismissible = True, icon = '📃')
def give_feedback():
    email = str(st.secrets['gmail'])
    pswd = str(st.secrets['password'])
    sender_email = email
    sender_password = pswd
    receiver_email = email

    st.title("Feedback")

    def send_an_email(subject, body, user_rating):
        index = 0

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject 

        if user_rating == "No Rating":
            msg.attach(MIMEText(body + "\n\nUser Did Not Leave a Review", 'plain'))
        else:
            msg.attach(MIMEText(body + "\n\nUser Rating: " + str(user_rating) + "/5", 'plain'))

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



    subject = st.text_input("Subject", max_chars=100, placeholder="Begin Typing")
    body = st.text_area("Body", max_chars=500, placeholder="Begin Typing")
    ratings = [1,2,3,4,5]
    selected = st.feedback("stars")

    if subject == "" or body == "":
        if st.button("Send Email"):
            st.session_state.button = False
            if subject == "" and body == "":
                st.toast("Please Enter a Subject and Body to Send")
            elif subject == "":
                st.toast("Please Enter a Subject to Send")
            elif body == "":
                st.toast("Please Enter a Body to Send")
    else:
        if st.button("Send Email"):
            st.session_state.button = True
            if selected != None:
                user_rating = ratings[selected]
            else:
                user_rating = "No Rating"
            
            test = send_an_email(subject, body, user_rating)
            if test ==1:
                st.toast("Email Recieved!", icon="✅")
            else:
                st.toast("Email Couldn't Send...")

def weather_widget():
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
            change_in_conditons = "No Change in Conditions"
        else: 
            change_in_conditons = "Conditions Expected to Shift to " + str(next_hour_conditons)

        return celcius, conditions, next_hour_celcius, next_hour_conditons, change_in_celcius, change_in_conditons, rise_or_drop, city

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
            temp_risk = "⚠️⚠️⚠️ Very Extreme Temperature Risks! Advisory to Stay Indoors!"
        elif trisk == 3:
            temp_risk = "⚠️ High Temperature Risks! Advisory to Stay Indoors!"
        elif trisk == 2:
            temp_risk = "🟠 Moderate Temperature Risks! Please be Careful Outside"
        elif trisk == 1:
            temp_risk = "🟡 Mild Temperature Risks! Please be Careful Outside!"
        else:
            temp_risk = "🟢 Temperatures Looking Good!"
        
        ##Condition Risk
        crisk = False
        for i in adjusted_conditions:
            if i == "Thunderstorm" or i == "thunderstorm":
                crisk = True
            elif i == "Rain" or i == "rain":
                crisk = True
            elif i == "Squall" or i == "squall":
                crisk = True
            elif i == "Snow" or i == "snow":
                crisk = True

        ##Will Be used later, but if conditions improve, a different statement is output
        next_hour_crisk = False        
        for i in adjusted_next_hour_conditions:
            if i == "Thunderstorm" or i == "thunderstorm":
                next_hour_crisk = True
            elif i == "Rain" or i == "rain":
                next_hour_crisk = True
            elif i == "Squall" or i == "squall":
                next_hour_crisk = True
            elif i == "Snow" or i == "snow":
                next_hour_crisk = True
        
        ##Assign conditions risk to output statements
        if crisk == True:
            cond_risk = "⚠️ Weather Condtions Pose Risk! Advisory to Stay Indoors!"
        else:
            cond_risk = "🟢 Conditions Looking Good!"
        
        return trisk, crisk, temp_risk, cond_risk, next_hour_crisk

    ##Displays the Temperature
    def display_temp():
            st.metric("Temperature", str(celcius)+" °C")
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
                st.write("No expected change in weather in the next hour")
            ##Output the string output for the temperature risks
            if trisk > 0:
                st.error(temp_risk)
            else:
                st.success(temp_risk)

    ##Displays the Conditions
    def display_cond():
            ##Display the conditions
            st.metric("Conditions", str(conditions))
            ##If conditions are harsh, display the change as red
            if next_hour_crisk == True:
                st.markdown(f":red[{str(change_in_conditons)} in the next hour ]")
            else:
                st.markdown(f":green[{str(change_in_conditons)} in the next hour]")
            if crisk == True:
                st.error(cond_risk)
            else:
                st.success(cond_risk)

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
        return user_latitude, user_longitude

    ##Call functions and assign the multitude of variables    
    user_latitude, user_longitude = get_geocoords()
    celcius, conditions, next_hour_celcius, next_hour_conditions, change_in_celcius, change_in_conditons, rise_or_drop, city = setup_weather(str(user_latitude), str(user_longitude))
    trisk, crisk, temp_risk, cond_risk, next_hour_crisk  = risk_evaluation(celcius, conditions)

    with st.container(border=True):
        st.header("Displaying weather for " + str(city))
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                display_temp()
        with col2:
            with st.container(border=True):
                display_cond()

def home_page():
    
    st.set_page_config(initial_sidebar_state="expanded", page_title="Maccessible")

    #Remove the extra page things at the top that are unnecessary and
    #unfortunately don't have emojis
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    st.title("**MACCESSIBLE**  :sunglasses:!", width = "stretch", text_alignment = "center")
    st.space("xsmall")
    st.markdown("Your all-in-one place for accessibility mapping, currently available only at McMaster University.",
                text_alignment = "center")

    #Setting Sidebar to have linked pages (i.e. like a menu) (not buttons)
    ##
    st.sidebar.subheader("Menu")
    st.sidebar.page_link("Home.py", label = "Home", icon = '🏠')
    st.sidebar.page_link("pages/Map.py", label = "Map", icon = '🚗')
    st.sidebar.page_link("pages/Help.py", label = "Help!", icon = '⁉️')
    st.sidebar.page_link("pages/About Us.py", label = "About Us...", icon = '✨')
    st.sidebar.page_link("pages/FAQs.py", label = "FAQs", icon = '❓')
    st.sidebar.page_link("pages/Dr McDonald's Contact Info.py", label =
                         "Dr McDonald's Contact Info", icon = '💯')

    weather_widget()
    st.space("small")
    #st.balloons()
    to_map = st.button("Take me to Map!", icon = '➡️', width="stretch")
    if to_map:
        st.switch_page("pages/Map.py")
    #Feedback Form
    st.space("xsmall")    
    feedback = st.button(":bar_chart: Looking to give feedback?", width = "stretch")
    if feedback:
        give_feedback()
            

home_page()