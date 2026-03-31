import streamlit as st
from PIL import Image

img = Image.open("pages/AboutUs.jpeg")
rotate = img.rotate(180)
rotate.save("pages/rotate.png")

st.title("Meet the Team")
#sep = st.columns([3,2.7])
st.markdown("""It's a :fire: team.
                     We're in first year iBioMed @ Mac, and Maccesisble is our DP4 project that we built for Jany, a community member with Multiple Sclerosis, so that she could navigate buildings easier.
                     Ummm I don't know what else to say... Pierce is the GOAT.""")
st.image('pages/rotate.png', caption = "From right to left: Noah, Erik, Aisha, and Emily.")

st.markdown("**If you want to contact us, go check out Dr McDonald's contact info.**")
