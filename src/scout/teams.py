from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import sys
from utils import utils

sys.path.append("..")


class Teams:
    def __init__(self, df_teams, team_name):
        self.df_teams = df_teams
        self.df_teams_scrim = {}
        self.bases_name = ["Waterson", "Pale", "Peris", "Fort liberty", "Acan", "Kessel", "Bridgewater"]
        self.team_name = team_name
        self.bases_count = {}
        self.bases_played = []
        self.bases_played_scrim = []
        self.bases_scrim_nbr = []
        self.bases_nbr = []
        self.sorted_base_nbr = []
        self.sorted_base_name = []
        self.compute_team_scrim_stats(team_name)

    def compute_team_scrim_stats(self, team_name):
        self.df_teams = self.df_teams[self.df_teams.team_name == team_name]
        self.df_teams_scrim = self.df_teams[self.df_teams.type == "Scrim"]
        self.bases_played = utils.split_bases(list(self.df_teams.bases_name.values))
        self.sorted_base = []
        self.bases_played_scrim = utils.split_bases(list(self.df_teams_scrim.bases_name.values))

        for base in self.bases_name:
            nbr = self.bases_played.count(base)
            self.bases_nbr.append(nbr)

        for base in self.bases_name:
            nbr = self.bases_played_scrim.count(base)
            self.bases_scrim_nbr.append(nbr)
            self.bases_count[base] = nbr

        self.sorted_base_nbr, self.sorted_base_name = utils.my_sort(self.bases_count, [], [])
        #print("Sorted list : ", self.sorted_base_nbr, self.sorted_base_name)

    def visualization_bar_bases(self):
        print("Bases played by " + self.team_name)

        x = np.arange(len(self.bases_name))

        fig, ax = plt.subplots()
        bar1 = ax.bar(x=(x - 0.3/2), height=self.bases_nbr, width=0.3, color='b', label="Internal + Scrim", align='edge', edgecolor='black')
        bar2 = ax.bar(x=(x + 0.3/2), height=self.bases_scrim_nbr, width=0.3, color='r', label="Scrim", align='edge', edgecolor='black')

        plt.xlabel("Bases")
        plt.ylabel("Number of Scrims and Internals")
        plt.title("Number of Scrim and Internal of " + self.team_name)
        ax.set_xticks(x)
        ax.set_xticklabels(self.bases_name)
        ax.legend()

        ax.bar_label(bar1, padding=3)
        ax.bar_label(bar2, padding=3)

        fig.tight_layout()
        plt.show()
