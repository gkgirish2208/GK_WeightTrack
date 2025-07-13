import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# Set page config
st.set_page_config(page_title="My Weight Tracker", layout="centered")

st.title("🏋️‍♂️ My Weight Tracker")

# File path
file_path = "weight_data.csv"

# Load or create CSV
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=['Date', 'Weight'])
    df.to_csv(file_path, index=False)

# Add serial numbers
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

# Graph type selection
st.write("### 📊 Select Graph Type")
graph_type = st.selectbox("Choose Graph Type", ['Bar', 'Line', 'Scatter'])

# Define multicolour palette
colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1',
          '#955251', '#B565A7', '#009B77', '#DD4124', '#45B8AC']
if len(df) > len(colors):
    colors = colors * (len(df)//len(colors) + 1)

# Graph plotting
if not df.empty:

    if graph_type == 'Bar':
        # Multicolour bar graph with date + weight inside bars

        # Combine Date + Weight text
        combined_text = df['Date'] + " | " + df['Weight'].astype(str) + " kg"

        # Dynamically adjust graph height based on number of entries
        graph_height = max(500, len(df)*80)  # 80px per bar, minimum 500px

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df['S.No'].astype(str),  # serial number as x-axis
            y=df['Weight'],
            text=combined_text,  # date + weight inside bar
            textposition='inside',
            insidetextanchor='middle',
            marker_color=colors[:len(df)],
            textfont=dict(color="white", size=12, family="Arial Black"),
            hovertemplate='S.No: %{x}<br>Date: %{text}<br>Weight: %{y} kg<extra></extra>',
            width=0.5,  # fixed bar thickness
        ))

        fig.update_layout(
            title="Weight Records Progression (S.No vs Weight)",
            xaxis_title="Serial Number",
            yaxis_title="Weight (kg)",
            yaxis=dict(range=[0,120]),
            plot_bgcolor='white',
            bargap=0.05,
            uniformtext_minsize=8,
            uniformtext_mode='show',
            showlegend=False,
            width=400,  # optimal for mobile view
            height=graph_height
        )

        # Use st.container with scrollable style
        with st.container():
            st.markdown(
                f"""
                <div style="overflow-y: scroll; height:{min(graph_height, 600)}px;">
                """,
                unsafe_allow_html=True
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif graph_type == 'Line':
        fig = px.line(
            df,
            x='S.No',
            y='Weight',
            markers=True,
            text='Date',
            title="Weight Progression (Line Graph)",
            labels={"S.No": "Serial Number", "Weight": "Weight (kg)"}
        )
        fig.update_traces(textposition="top center")
        fig.update_yaxes(range=[0,120])
        fig.update_layout(
            plot_bgcolor='white',
            width=800,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    elif graph_type == 'Scatter':
        fig = px.scatter(
            df,
            x='S.No',
            y='Weight',
            color='Weight',
            size='Weight',
            text='Date',
            title="Weight Progression (Scatter Plot)",
            labels={"S.No": "Serial Number", "Weight": "Weight (kg)"}
        )
        fig.update_traces(textposition='top center')
        fig.update_yaxes(range=[0,120])
        fig.update_layout(
            plot_bgcolor='white',
            width=800,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Add data to view graph.")
