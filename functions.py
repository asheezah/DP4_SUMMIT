import streamlit as st
import smtplib
import time
import requests
from streamlit_js_eval import get_geolocation, get_page_location
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from geopy.geocoders import Nominatim
from streamlit_extras.floating_button import *
from streamlit_extras.stoggle import *

##Define the sidebar function thaat will be called in every page
def sidebar():
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
                
        </style>
    """, unsafe_allow_html=True)

    st.logo("pages/summit!.png", size="large", icon_image="pages/summit!.png")
    st.sidebar.page_link("Home.py", label = "Home")
    st.sidebar.page_link("pages/Map.py", label = "Map")
    st.sidebar.page_link("pages/About Us.py", label = "About Us")
    st.sidebar.page_link("pages/Weather.py", label = "Weather")
    st.sidebar.page_link("pages/Dr McDonald's Contact Info.py", label = "Get In Touch!")
    st.sidebar.divider()
    st.sidebar.page_link("pages/Feedback.py", label = "Give us Feedback")

##Define the help button function that will also be called in every page
def help_button():
    @st.dialog("Support", width="large")
    def button_dialog() -> None:
        st.subheader("Map")
        with st.expander("How do I view the map?"):
            st.write("To view the map, click on the arrow (>) on the top left of your screen. Then select (Map)")
            q1col1, q1col2 = st.columns([1,3])
            with q1col1:
                st.write('Or just click here: ')
            with q1col2:
                st.page_link("pages/Map.py",label=":blue[Map]")
        with st.expander("I found a discrepancy on the map, can I report this?"):
            st.write("Yes (and please do)! To do this, pleae visit the (Map) page and select (Report Discrepancy).")
        st.subheader("Weather")
        with st.expander("What does the \"Expected\" text mean?"):
            st.write("The \"Expected\" text denotes the transition to the next hours weather!")
            st.markdown(":green[Green text indicates that temperature or weather is entering or remaining in a safe range.]")
            st.markdown(":red[Red text indicates that temperature or weather is entering or remaining in a dangerous range.]")
        st.subheader("Feedback")
        with st.expander("I want to provide feedback for Maccessible, how should I do this?"):
            st.write("We gratefully appreciate all feedback! To tell us how were doing, click on the arrow (>) on the top left of your screen, then select (Feedback)")
            q2col1, q2col2 = st.columns([1,3])
            with q2col1:
                st.write('Or just click here: ')
            with q2col2:
                st.page_link("pages/Feedback.py",label=":blue[Feedback Form]")
        st.subheader("About Maccessible")
        with st.expander("Who made this epic app?"):
            st.write("Maccessible was made by 4 ambitious first-year iBioMed students for a class project!")
            q3col1, q3col2 = st.columns([1,3])
            with q3col1:
                st.write('Read more here: ')
            with q3col2:
                st.page_link("pages/About Us.py",label=":blue[About Us]")
    
    ##Uses streamlit extras to make a button that permanents sits at the bottom right of screen
    if floating_button(":question:"):
        button_dialog()

##Gets user coordinates (Can be called on pages that need it)
def get_geocoords_func():
        ##Gets location
        user_location = get_geolocation()
        ##The library being used to get geolocation completes before actually getting coords
        ##Variable error will ensure that future functions are not called out of turn.
        error = False
        ##To ensure there are no errors, define lat and long as 0 (placeholder)
        user_latitude_get = 0
        user_longitude_get = 0
        if user_location and 'error' in user_location:
            error = True
        ##If user location is found get lat and long and assign them
        elif user_location:
            user_latitude_get = user_location['coords']['latitude']
            user_longitude_get = user_location['coords']['longitude']
            error = False
        ##Browser location
        user_location_json = get_page_location()
        return user_latitude_get, user_longitude_get, error