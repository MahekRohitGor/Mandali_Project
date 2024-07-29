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
    # st.write(user_id)
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
st.title("સભ્ય ડેટા ડિસ્પ્લે")
st.subheader("શ્રી કચ્છ કેળિણી ખાતાના કર્મચારીઓની શરાફી સહકારી મંડળી લી.")

# Check if the user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("કૃપા કરીને પહેલા લોગ ઇન કરો.")
    st.stop()

# User is logged in, display data
st.subheader("મહિનો અને વર્ષ પસંદ કરો")
month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
year = st.selectbox("Year", [2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2024, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050])

if st.button("ડિસ્પ્લે ડેટા"):
    user_id = st.session_state['user_id']
    data = get_data(month, year, user_id)
    if not data.empty:
        for index, row in data.iterrows():
            st.markdown(
            f"""
            <table style="border: 1px solid black; width: 100%;">
                <tr>
                    <td style="border: 1px solid black;"><strong>સભાસદ નં.:</strong></td>
                    <td style="border: 1px solid black;">{row['Sabhasad No.']}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black;"><strong>નામ:</strong></td>
                    <td style="border: 1px solid black;">{row['Name']}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black;"><strong>શાળાનું નામ:</strong></td>
                    <td style="border: 1px solid black;">{row['School Name']}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black;"><strong>ગ્રુપ નામ:</strong></td>
                    <td style="border: 1px solid black;">{row['Group name']}</td>
                </tr>
            </table>
            """, unsafe_allow_html=True)

            st.write(f"આપની માસ : **{row['Month']}** - **{row['Year']}** સુધી જમા થયેલ શેરભંડોળ , ફરજીયાત બચતની રકમ તથા મંડળીમાંથી લીધેલ લોનની બાકી રહેલ રકમ, આ **{row['Month']}** - **{row['Year']}** મહિનામાં જે કપાત કરિાની થાય છે તે મુદ્દલ,વ્યાજ અને ફરજીયાત બચત રકમનિ કપાત વિગત નીચે મુજબ છે.")
        
            # col1, col2 = st.columns(2)
        
            # with col1:
            st.write("મંડળીમા આપની જમા થયેલ રકમનિ વિગત")
            st.markdown(
                f"""
                <table style="border: 1px solid black; width: 100%;">
                    <tr>
                        <td style="border: 1px solid black;"><strong>શેરની રકમ:</strong></td>
                        <td style="border: 1px solid black;">₹{row['Share Amount']}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid black;"><strong>બચત:</strong></td>
                        <td style="border: 1px solid black;">₹{row['Savings']}</td>
                    </tr>
                </table>
                """, unsafe_allow_html=True)
        
            # with col2:
            st.write(f"**{row['Month']}** - **{row['Year']}** મહિનામાં થનાર કપાતની વિગત")
            st.markdown(
                    f"""
                    <table style="border: 1px solid black; width: 100%;">
                        <tr>
                        <td style="border: 1px solid black;"><strong>લોનની રકમ:</strong></td>
                        <td style="border: 1px solid black;">₹{row['Loan Amount']}</td>
                        </tr>
                        <tr>
                        <td style="border: 1px solid black;"><strong>હપ્તો:</strong></td>
                        <td style="border: 1px solid black;">₹{row['Installment']}</td>
                        </tr>
                    <tr>
                        <td style="border: 1px solid black;"><strong>વ્યાજ:</strong></td>
                        <td style="border: 1px solid black;">₹{row['Intrest']}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid black;"><strong>ફરજિયાત બચત:</strong></td>
                        <td style="border: 1px solid black;">₹{row['Compulsory Saving']}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid black;"><strong>કુલ:</strong></td>
                        <td style="border: 1px solid black;">₹{row['Total']}</td>
                    </tr>
                </table>
                """, unsafe_allow_html=True)
        
            st.write(f"**વર્ષ:** {row['Year']}")
            st.write(f"**માસ:** {row['Month']}")
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
            "Category": ["લોનની રકમ", "હપ્તો", "વ્યાજ", "ફરજિયાત બચત"],
            "Amount": [loan_amount, installment, interest, compulsory_saving]
        })

        # Pie chart to visualize breakdown
        fig = px.pie(pie_chart_data, values='Amount', names='Category', title="Breakdown of Total Amount")
        st.plotly_chart(fig)

        # Display total amount
        st.write(f"**Total Amount:** {total_amount}")
    else:
        st.warning("પસંદ કરેલ મહિના અને વર્ષ માટે કોઈ ડેટા મળ્યો નથી")
logout_button = st.button("લૉગ આઉટ")
if logout_button:
    del st.session_state['logged_in']
    st.success("તમે લૉગ આઉટ થઈ ગયા છો.")
    st.stop()