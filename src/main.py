from google_api import read_file
from scout import scout
from dotenv import load_dotenv
import os

load_dotenv()
teams_name = ["xFPS", "1RPC", "SDEM", "BWAE", "DTAC", "BACU", "BHSA", "HBG", "GOBS", "BYZZ", "TRY"]
teams_url = os.environ.get("URL")

googleSheets = read_file.GoogleSheets()
df_teams = googleSheets.get_teams(teams_url)
scouting = scout.Scouting(df_teams)

scouting.show_visualization_teams(["1RPC", "GOBS"])
scouting.simulation_group_stage("1RPC", "GOBS")
scouting.simulation_playin("1RPC", "GOBS")

