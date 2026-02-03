import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Blood Donor App", page_icon="🩸")
st.markdown("## ✅ App loaded successfully")

db_path = os.path.join(os.getcwd(), "donors.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS donors (
    name TEXT,
    blood TEXT,
    city TEXT,
    phone TEXT,
    last_donation TEXT
)
""")
conn.commit()

st.title("🩸 Blood Donation App")
st.caption("Donate blood. Save lives.")

page = st.radio("Choose an option", ["Register Donor", "Request Blood"])

if page == "Register Donor":
    name = st.text_input("Name")
    blood = st.selectbox(
        "Blood Group",
        ["A+","A-","B+","B-","O+","O-","AB+","AB-"]
    )
    city = st.text_input("City")
    phone = st.text_input("Phone Number")
    last = st.date_input("Last Donation Date", value=date.today())

    if st.button("Register"):
        if name and city and phone:
            c.execute(
                "INSERT INTO donors VALUES (?,?,?,?,?)",
                (name, blood, city, phone, str(last))
            )
            conn.commit()
            st.success("✅ Donor registered successfully!")
        else:
            st.error("❌ Please fill all fields")

elif page == "Request Blood":
    blood = st.selectbox(
        "Required Blood Group",
        ["A+","A-","B+","B-","O+","O-","AB+","AB-"]
    )
    city = st.text_input("City")

    if st.button("Find Donors"):
        df = pd.read_sql(
            "SELECT * FROM donors WHERE blood=? AND city=?",
            conn,
            params=(blood, city)
        )

        if df.empty:
            st.warning("❌ No donors found")
        else:
            st.dataframe(df)
