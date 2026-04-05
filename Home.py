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
from functions import sidebar, help_button

st.set_page_config(initial_sidebar_state="expanded", page_title="Summit")

def home():
    #Remove the extra page things at the top that are unnecessary and
    #unfortunately don't have emojis
    ##Display the sidebar
    sidebar()

    #Display the logo
    st.image("pages/summit!.png")

    st.markdown("""
            <h5 style = "text-align: center; color: orange">**Currently only available at McMaster University**</h5>
        """, unsafe_allow_html=True)

    #Button that takes user to the map
    to_map = st.button("Go to the Map!", use_container_width=True)
    if to_map:
        st.switch_page("pages/Map.py")
    
    ##Displays the help button (Bottom right of screen)
    help_button()

home()