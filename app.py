import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Blood Rapid Connect",
    page_icon="🩸",
    layout="wide"
)

# ---------- STYLES (Lovable-like) ----------
st.markdown("""
<style>
body {
    background-color: #fffafa;
}
.hero {
    background: linear-gradient(135deg, #b71c1c, #e53935);
    padding: 40px;
    border-radius: 18px;
    color: white;
    margin-bottom: 30px;
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.donor-card {
    border-left: 6px solid #e53935;
    padding: 20px;
    border-radius: 14px;
    background: #ffffff;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.06);
    margin-bottom: 15px;
}
.stButton > button {
    background-color: #e53935;
    color: white;
    border-radius: 12px;
    height: 48px;
    font-size: 16px;
}
label { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ---------- DATABASE ----------
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

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <h1>🩸 Blood Rapid Connect</h1>
    <p>Instantly connect with nearby blood donors.<br>
    Fast • Reliable • Life-saving</p>
</div>
""", unsafe_allow_html=True)

# ---------- NAV ----------
page = st.radio(
    "",
    ["🧑‍⚕️ Register as Donor", "🚑 Find Blood"],
    horizontal=True
)

st.divider()

# ---------- REGISTER ----------
if page == "🧑‍⚕️ Register as Donor":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Become a Blood Donor ❤️")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        blood = st.selectbox(
            "Blood Group",
            ["A+","A-","B+","B-","O+","O-","AB+","AB-"]
        )
        last = st.date_input("Last Donation Date", value=date.today())

    with col2:
        city = st.text_input("City")
        phone = st.text_input("Phone Number")

    if st.button("Register Donor"):
        if name and city and phone:
            c.execute(
                "INSERT INTO donors VALUES (?,?,?,?,?)",
                (name, blood, city, phone, str(last))
            )
            conn.commit()
            st.success("🎉 You are now a registered donor!")
        else:
            st.error("Please complete all fields")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- FIND BLOOD ----------
else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Find Blood Donors 🔍")

    col1, col2 = st.columns(2)
    with col1:
        blood = st.selectbox(
            "Required Blood Group",
            ["A+","A-","B+","B-","O+","O-","AB+","AB-"]
        )
    with col2:
        city = st.text_input("City")

    search = st.button("Search Donors")
    st.markdown('</div>', unsafe_allow_html=True)

    if search:
        df = pd.read_sql(
            "SELECT * FROM donors WHERE blood=? AND city=?",
            conn,
            params=(blood, city)
        )

        if df.empty:
            st.warning("No donors found nearby 😔")
        else:
            st.success(f"{len(df)} donor(s) available")

            for _, row in df.iterrows():
                st.markdown(f"""
                <div class="donor-card">
                    <h4>{row['name']} ({row['blood']})</h4>
                    <p>📍 {row['city']}</p>
                    <p>📞 {row['phone']}</p>
                    <p>🩸 Last Donated: {row['last_donation']}</p>
                </div>
                """, unsafe_allow_html=True)
