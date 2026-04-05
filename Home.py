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
    sidebar()

    st.image('pages/Summit_Logo.png')
    st.divider()
    st.markdown("""
            <h2 style = "text-align: center; color: maroon;">The future of accessible navigation, <br> at the click of a button.</h2>
            <h5 style = "text-align: center; color: orange">*Currently only available at McMaster University*</h5>
        """, unsafe_allow_html=True)
    st.divider()
    st.button("Click me and Watch the Magic Happen", use_container_width=True, type='primary')

    help_button()

home()