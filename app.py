import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/credentials.json", scope)
client = gspread.authorize(creds)

# Load the Google Sheets
login_sheet = client.open("Mandali").worksheet("Login")

def check_credentials(username, password):
    credentials = login_sheet.get_all_records()
    st.session_state.logged_in = True
    st.session_state['user_id'] = username
    for cred in credentials:
        if str(cred['Username']) == str(username) and cred['Password'] == password:
            return True
    return False

# Streamlit app
st.header("લોગ ઇન")
st.subheader("શ્રી કચ્છ કેળિણી ખાતાના કર્મચારીઓની શરાફી સહકારી મંડળી લી.")

# Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("લોગ ઇન")
    username = st.text_input("સભાસદ નંબર")
    password = st.text_input("પાસવર્ડ", type='password')
    if st.button("લોગ ઇન"):
        if check_credentials(username, password):
            st.session_state.logged_in = True
            st.query_params["page"] = "data_display"
            st.success("લૉગિન સફળ! કૃપા કરીને પૃષ્ઠ પ્રદર્શન પર નેવિગેટ કરો")
        else:
            st.error("અમાન્ય સભાસદ નંબર અથવા પાસવર્ડ")

query_params = st.query_params
if st.session_state.logged_in or query_params.get("page") == ["data_display"]:
    st.query_params["page"] = "data_display"
    st.stop()