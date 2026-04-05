import streamlit as st
from PIL import Image
from streamlit_extras.floating_button import *
from functions import sidebar, help_button

def about_us():
    ##Create descriptions of the team
    st.title("Meet the Team")
    st.divider()
    st.image('pages/rotate.png', caption = "From left to right: Emily, Aisha, Erik, and Noah.")
    st.markdown("""**It's a :fire: team.**  
                        We're in first year iBioMed @ Mac, and Maccessible is our DP4 project that we built for Jany, 
                        a community member with Multiple Sclerosis, so that she could navigate buildings easier.    
                        Pierce is the GOAT.  
                        Erik: going into Level II iBioMed, specialization: not software (probably), fun fact: He has a banjo.  
                        Noah: going into Level II iBioMed, specialization: not software, fun fact: He doesn't want to do software.  
                        Emily: going into Level II iBioMed, specialization: not software, fun fact: She likes green trees.  
                        Aisha: going into Level II iBioMed, specialization: not software, fun fact: She also likes green trees, but she's allergic to them.  
                        **If you want to contact us, go check out Dr McDonald's contact info.**""")
##Display sidebar and help button   
sidebar()
help_button()
##Displays the about us section previously defined.
about_us()

