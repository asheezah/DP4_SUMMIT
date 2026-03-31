import streamlit as st

st.title("Meet the Team")
sep = st.col([3,1])
sep[0] = st.markdown("""It's a :fire: team.
                     We're in first year iBioMed @ Mac, and Maccesisble is our DP4 project that we built for Jany, a community member with Multiple Sclerosis, so that she could navigate buildings easier.
                     Ummm I don't know what else to say... Pierce is the GOAT.""")
sep[1] = st.image('AboutUs.jpeg', caption = "From left to right: Emily, Aisha, Erik, and Noah.")

st.markdown("**If you want to contact us, go check out Dr McDonald's email.**")
