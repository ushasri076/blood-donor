import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# ---------------- DB SETUP ----------------
conn = sqlite3.connect("donors.db", check_same_thread=False)
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

# ---------------- UI ----------------
st.set_page_config(page_title="Blood Donation App", page_icon="🩸")

st.title("🩸 Blood Donation App")
st.caption("Donate blood. Save lives.")

menu = st.sidebar.selectbox(
    "Menu",
    ["Register Donor", "Request Blood", "All Donors"]
)

# ---------------- REGISTER DONOR ----------------
if menu == "Register Donor":
    st.header("Register as Donor")

    name = st.text_input("Name")
    blood = st.selectbox(
        "Blood Group",
        ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )
    city = st.text_input("City")
    phone = st.text_input("Phone Number")
    last_donation = st.date_input("Last Donation Date", value=date.today())

    if st.button("Register"):
        if name and city and phone:
            c.execute(
                "INSERT INTO donors VALUES (?,?,?,?,?)",
                (name, blood, city, phone, str(last_donation))
            )
            conn.commit()
            st.success("✅ Donor registered successfully!")
        else:
            st.error("❌ Please fill all fields")

# ---------------- REQUEST BLOOD ----------------
elif menu == "Request Blood":
    st.header("Request Blood")

    req_blood = st.selectbox(
        "Required Blood Group",
        ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )
    req_city = st.text_input("City")

    emergency = st.checkbox("🚨 Emergency Case")

    if st.button("Find Donors"):
        df = pd.read_sql_query(
            "SELECT * FROM donors WHERE blood=? AND city=?",
            conn,
            params=(req_blood, req_city)
        )

        if not df.empty:
            if emergency:
                st.error("🚨 Emergency! Contact donors immediately")

            for _, row in df.iterrows():
                st.markdown(f"""
                **👤 {row['name']}**  
                🩸 Blood: {row['blood']}  
                📍 City: {row['city']}  
                📞 Phone: {row['phone']}  
                💬 [WhatsApp](https://wa.me/91{row['phone']})
                ---
                """)
        else:
            st.warning("❌ No donors found")

# ---------------- VIEW ALL DONORS ----------------
else:
    st.header("All Registered Donors")
    df = pd.read_sql("SELECT * FROM donors", conn)
    st.dataframe(df)
