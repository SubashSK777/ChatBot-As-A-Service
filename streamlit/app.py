import streamlit as st
import requests

st.title("CRM AI Chatbot")

prompt = st.text_input("Ask CRM:")

if st.button("Ask"):
    try:
        res = requests.post("http://backend:8000/ask", json={"prompt": prompt})

        try:
            data = res.json()
            st.write("Answer:", data.get("response") or data.get("error"))
        except:
            st.error("❌ Backend did not return valid JSON")
            st.text(res.text)

    except Exception as e:
        st.error("❌ Error contacting backend")
        st.text(str(e))
