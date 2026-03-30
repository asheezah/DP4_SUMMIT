import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
