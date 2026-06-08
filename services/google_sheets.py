import streamlit as st
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
import time


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_NAME = "Quiniela Mundial 2026"


@st.cache_resource
def get_gspread_client():

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    return gspread.authorize(creds)

# @st.cache_resource
def get_spreadsheet():
    
    client = get_gspread_client()

    return client.open(SPREADSHEET_NAME)
    
    # for _ in range(3):
    #     try: 
    #         return client.open(SPREADSHEET_NAME)
    #     except Exception:
    #         time.sleep(15)
            
    
    # raise Exception("Repetir acceso con Google Sheets")


    

@st.cache_data(ttl=300)
def get_matches():
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet("partidos")
    return worksheet.get_all_records()

def get_user_info(user_id):
    # spreadsheet = get_spreadsheet()
    # worksheet = spreadsheet.worksheet(
    #     "user_info"
    # )
    # records = worksheet.get_all_records()
    # for row in records:
    #     if str(row["user_id"]) == str(user_id):
    #         return row

    # return None
    users = get_all_users()
    return users.get(str(user_id))

@st.cache_data(ttl=300)
def get_all_users():

    spreadsheet = get_spreadsheet()

    worksheet = spreadsheet.worksheet(
        "user_info"
    )

    records = worksheet.get_all_records()

    return {
        str(row["user_id"]): row
        for row in records
    }

def save_user_info(user_id, user_name):
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet("user_info")
    rows = [] 
    rows.append(
        [
            user_id,
            user_name
        ]
    )
    worksheet.append_rows(rows)
    get_all_users.clear()

def save_predictions(predictions):
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet("predicciones")
    rows = []
    timestamp = datetime.now().isoformat()
    for prediction in predictions:
        rows.append(
            [
                timestamp,
                prediction['usuario_id'],
                prediction['etapa'],
                prediction['match_id'],
                prediction['prediccion']
            ]
        )
    # st.write(rows)
    worksheet.append_rows(rows)
    get_all_predictions.clear()
    get_predictions.clear()

@st.cache_data(ttl=600)
def get_predictions(user_id, etapa):
    # spreadsheet = get_spreadsheet()
    # worksheet = spreadsheet.worksheet("predicciones")
    # records = worksheet.get_all_records()
    records = get_all_predictions()
    return [
        row
        for row in records
        if str(row['usuario_id']) == user_id
        and row["etapa"] == etapa
    ]

@st.cache_data(ttl=60)
def get_all_predictions():
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(
        "predicciones"
    )
    return worksheet.get_all_records()

@st.cache_data(ttl=300)
def get_results():
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet("resultados")
    records = worksheet.get_all_records()
    return {
        row['match_id']: row['resultado']
        for row in records
    }

def save_results():

    pass