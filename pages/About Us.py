import streamlit as st
from PIL import Image

st.title("Meet the Team")
st.divider()
sep = st.columns([3,2.7])
sep[0].markdown("""**It's a :fire: team.**  
                     We're in first year iBioMed @ Mac, and Maccessible is our DP4 project that we built for Jany, 
                     a community member with Multiple Sclerosis, so that she could navigate buildings easier.    
                     Pierce is the GOAT.  
                     **If you want to contact us, go check out Dr McDonald's contact info.**""")
sep[1].image('pages/rotate.png', caption = "From left to right: Emily, Aisha, Erik, and Noah.")

