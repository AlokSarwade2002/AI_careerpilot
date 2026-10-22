
import streamlit as st

st.set_page_config(page_title="CareerPilot UI Test")

st.title("🎯 AI CareerPilot")
st.success("Streamlit is rendering correctly!")
st.write("If you can see this message, the UI framework works.")

name = st.text_input("Test input")
st.write("You entered:", name)
