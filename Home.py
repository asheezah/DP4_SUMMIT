import streamlit as st

st.set_page_config(initial_sidebar_state="expanded", page_title="Maccessible")
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)



st.title("**MACCESSIBLE**  :sunglasses:!", width = "stretch", text_alignment = "center")
st.markdown("Your all-in-one place for accessibility mapping, currently available only at McMaster University.")

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

data_from = st.text_input("Enter current location:")
data = st.columns(2)
#data_to, to_map = st.columns(2)
data_to = data[0].text_input("To where?")
data[1].space("small")
to_map = data[1].button("Take me to Map!", icon = '➡️', icon_position = 'left')
if to_map:
    st.switch_page("pages/Map.py")
elif to_map and data_to != None and data_from != None:
    st.switch_page("pages/Map.py")


#OR USE PAGE NAVIGATION!!!

##pages = {"Menu": [st.Page("Home.py", title = "🏠 Home"),
##                  st.Page("pages/Map.py", title = "🚗 Map"),
##                  st.Page("pages/Help.py", title = "⁉️ Help!")]}
##pg = st.navigation(pages, position="sidebar")
###pg.run()

#So this is switch page, with buttons
##with st.sidebar:
##    home = st.button(":house: Home")
##    Map = st.button(":red_car: Map")
##    HELP = st.button(":question: Help!")
##
##    if home:
##        st.switch_page("Home.py")
##    if Map:
##        st.switch_page("pages/Map.py")
##    if HELP:
##        st.switch_page("pages/Help.py")
