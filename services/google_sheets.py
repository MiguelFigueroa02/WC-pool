import streamlit as st
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_NAME = "Quiniela Mundial 2026"


def get_gspread_client():

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    return gspread.authorize(creds)


def get_spreadsheet():

    client = get_gspread_client()

    return client.open(SPREADSHEET_NAME)


def get_matches():
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet("partidos")
    return worksheet.get_all_records()



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
    st.write(rows)
    worksheet.append_rows(rows)

def get_predictions():

    pass


def save_results():

    pass