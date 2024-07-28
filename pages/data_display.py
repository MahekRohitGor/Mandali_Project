import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/credentials.json", scope)
client = gspread.authorize(creds)

# Load the Google Sheets
data_sheet = client.open("Mandali").worksheet("Data")

def get_data(month, year, user_id):
    data = data_sheet.get_all_records()
    df = pd.DataFrame(data)
    st.write(user_id)
    # print(df)

    df['Month'] = df['Month'].astype(str)
    df['Year'] = df['Year'].astype(int)
    df['Sabhasad No.'] = df['Sabhasad No.'].astype(str)

    filtered_data = df[(df['Month'] == month) & (df['Year'] == year) & (df['Sabhasad No.'] == str(user_id))]
    # print(filtered_data)
    if filtered_data.empty:
        return pd.DataFrame()
    else:
        return filtered_data

# Streamlit app
st.title("Member Data Display")

# Check if the user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in first.")
    st.stop()

# User is logged in, display data
st.subheader("Select Month and Year")
month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
year = st.selectbox("Year", [2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2024, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050])

if st.button("Display Data"):
    user_id = st.session_state['user_id']
    data = get_data(month, year, user_id)
    if not data.empty:
        for index, row in data.iterrows():
            st.write(f"**Sabhasad No.:** {row['Sabhasad No.']}")
            st.write(f"**Name:** {row['Name']}")
            st.write(f"**School Name:** {row['School Name']}")
            st.write(f"**Group Name:** {row['Group name']}")
            st.write(f"**Share Amount:** {row['Share Amount']}")
            st.write(f"**Savings:** {row['Savings']}")
            st.write(f"**Loan Amount:** {row['Loan Amount']}")
            st.write(f"**Installment:** {row['Installment']}")
            st.write(f"**Interest:** {row['Intrest']}")
            st.write(f"**Compulsory Saving:** {row['Compulsory Saving']}")
            st.write(f"**Total:** {row['Total']}")
            st.write(f"**Year:** {row['Year']}")
            st.write(f"**Month:** {row['Month']}")
            st.write("---")
        
        # Visualization example
        # fig = px.bar(data, x='Name', y='Total', title="Total Amount by Member")
        # st.plotly_chart(fig)
        loan_amount = data["Loan Amount"].sum()
        installment = data["Installment"].sum()
        interest = data["Intrest"].sum()
        compulsory_saving = data["Compulsory Saving"].sum()
        total_amount = data["Total"].sum()

        pie_chart_data = pd.DataFrame({
            "Category": ["Loan Amount", "Installment", "Interest", "Compulsory Saving"],
            "Amount": [loan_amount, installment, interest, compulsory_saving]
        })

        # Pie chart to visualize breakdown
        fig = px.pie(pie_chart_data, values='Amount', names='Category', title="Breakdown of Total Amount")
        st.plotly_chart(fig)

        # Display total amount
        st.write(f"**Total Amount:** {total_amount}")
    else:
        st.warning("No data found for the selected month and year")
logout_button = st.button("Logout")
if logout_button:
    del st.session_state['logged_in']
    st.success("You have been logged out.")
    st.stop()