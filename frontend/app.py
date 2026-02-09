import streamlit as st
import requests

st.title("🤖 HR Resource Chatbot")

query = st.text_input("Enter your HR query:")

if st.button("Search"):
    if query:
        response = requests.post("http://localhost:8000/chat", params={"query": query})
        st.subheader("🔍 Results:")
        st.text(response.json()['response'])
    else:
        st.warning("Please enter a query.")
