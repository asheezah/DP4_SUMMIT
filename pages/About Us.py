import streamlit as st
from PIL import Image
from streamlit_extras.floating_button import *
from functions import sidebar, help_button

def about_us():
    ##Create description of the team
    st.title("Meet The Team")
    st.divider()
    st.image('pages/AboutUs!.png')

sidebar()
help_button()
##Displays the about us section previously defined.
about_us()

