import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

    st.space("small")
    st.balloons()
    to_map = st.button("Take me to Map!", icon = '➡️', width="stretch")
    if to_map:
        st.switch_page("pages/Map.py")
    #Feedback Form
    st.space("xsmall")    
    feedback = st.button(":bar_chart: Looking to give feedback?", width = "stretch")
    if feedback:
        give_feedback()
            
home_page()
