from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def check_base(bases, base):
    if base is not None and base != "x":
        bases.append(base)
    return bases


def bases(base1, base2, base3, base4):
    bases = []
    bases = check_base(bases, base1)
    bases = check_base(bases, base2)
    bases = check_base(bases, base3)
    bases = check_base(bases, base4)
    return bases


def join_bases(base1, base2, base3, base4):
    bases_list = []
    for i in range(0, len(base1)):
        bases_list.append(str(bases(base1[i], base2[i], base3[i], base4[i])))
    return bases_list


class GoogleSheets:
    def __init__(self):
        self.sheet = None
        self.connect()
        self.SAMPLE_SPREADSHEET_ID = None
        self.SAMPLE_RANGE_NAME = 'A1:AA1000'

    def get_sheet_ID(self, url):
        url = url.replace("https://docs.google.com/spreadsheets/d/", "")
        self.SAMPLE_SPREADSHEET_ID = url.split("/")[0]

    def connect(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)
        self.sheet = service.spreadsheets()

    def create_dataset(self, values):
        teams = {"team_name": values[1], "bases_name": join_bases(values[3], values[4], values[5], values[6]), "type": values[8], "date": values[7]}
        df_teams = pd.DataFrame(teams, columns=['team_name', 'bases_name', 'type', 'date'])
        return df_teams

    def get_teams(self, link):
        self.get_sheet_ID(link)
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                                         range=self.SAMPLE_RANGE_NAME, majorDimension='COLUMNS').execute()
        values = result.get('values', [])
        df_teams = self.create_dataset(values)
        return df_teams
