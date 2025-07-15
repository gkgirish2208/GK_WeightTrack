import streamlit as st
import pandas as pd
import os
import random

# Set page config
st.set_page_config(page_title="My Weight Tracker", layout="wide")

# 🔑 Initialize session state keys safely
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ----- LOGIN PAGE -----
if not st.session_state['logged_in']:
    st.title("🔐 Login Required")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    if login_button:
        if username == "gkgirish" and password == "gkgirish2208":
            st.session_state['logged_in'] = True
            st.success("Login successful! Please wait...")
        else:
            st.error("Invalid username or password. Please try again.")

# ----- MAIN APP -----
if st.session_state['logged_in']:
    st.title("🏋️‍♂️ My Weight Tracker - Progress View")

    # File path
    file_path = "weight_data.csv"

    # Load or create CSV
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=['Date', 'Weight'])
        df.to_csv(file_path, index=False)

    # Add serial numbers without skipping (1,2,3,...)
    df['S.No'] = range(1, len(df) + 1)

    # Display existing data
    st.write("### Your Weight Records")
    st.dataframe(df[['S.No', 'Date', 'Weight']], use_container_width=True)

    # Add new entry
    st.write("### ➕ Add New Entry")
    if 'add_clicked' not in st.session_state:
        st.session_state['add_clicked'] = False

    date = st.date_input("Select Date")
    weight = st.number_input("Enter Weight (kg)", min_value=0.0, max_value=120.0, step=0.1)
    add_button = st.button("Add")

    if add_button:
        new_data = pd.DataFrame({'Date': [str(date)], 'Weight': [weight]})
        df = pd.concat([df.drop('S.No', axis=1), new_data], ignore_index=True)
        df['S.No'] = range(1, len(df) + 1)
        df.to_csv(file_path, index=False)
        st.session_state['add_clicked'] = True
        st.success(f"Added: {date}, {weight} kg")

    if st.session_state['add_clicked']:
        df = pd.read_csv(file_path)
        df['S.No'] = range(1, len(df) + 1)
        st.session_state['add_clicked'] = False

    # Delete entry
    st.write("### ❌ Delete Entry")
    if not df.empty:
        delete_index = st.selectbox("Select entry to delete (by S.No)", df['S.No'])
        delete_button = st.button("Delete")
        if delete_button:
            df = df[df['S.No'] != delete_index].reset_index(drop=True)
            df['S.No'] = range(1, len(df) + 1)
            df.to_csv(file_path, index=False)
            st.success("Deleted entry successfully")
            # Reload data
            df = pd.read_csv(file_path)
            df['S.No'] = range(1, len(df) + 1)
    else:
        st.info("No data available to delete.")

    # ----- Progress bar visualization -----
    st.write("### 📊 Weight Progress Bars")

    if not df.empty:
        # Define multi colours randomly for bars
        colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1',
                  '#955251', '#B565A7', '#009B77', '#DD4124', '#45B8AC']

        for index, row in df.iterrows():
            s_no = row['S.No']
            date = row['Date']
            weight = row['Weight']
            percent = (weight / 120)  # Normalize to 0-1 scale

            # Random colour selection for fun
            bar_color = random.choice(colors)

            # Custom HTML progress bar with label
            st.markdown(f"""
                <div style="margin-bottom:15px;">
                    <b>S.No {s_no}</b>: {date} | {weight} kg
                    <div style="background-color:lightgrey; border-radius:5px; width:100%; height:20px;">
                        <div style="width:{percent*100}%; background-color:{bar_color}; height:20px; border-radius:5px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Add data to view progress bars.")
