from __future__ import print_function
import pickle
import os.path
import pandas as pd
import matplotlib.pyplot as plt
import ast
import numpy as np


def split_bases(bases):
    clean_bases = []
    for base in bases:
        base = ast.literal_eval(base)
        print(base)
        clean_bases = clean_bases + base
    return clean_bases


class Scouting:
    def __init__(self, df_teams):
        self.df_teams = df_teams
        self.bases = ["Waterson", "Pale", "Peris", "Fort liberty", "Acan", "Kessel", "Bridgewater"]
        self.teams_name = []

    def team_scrim_stats(self, team_name):
        self.df_teams = self.df_teams[self.df_teams.team_name == team_name]
        df_teams_scrim = self.df_teams[self.df_teams.type == "Scrim"]
        print(self.df_teams)
        bases_played = split_bases(list(self.df_teams.bases_name.values))
        bases_played_scrim = split_bases(list(df_teams_scrim.bases_name.values))

        self.visualization_bar_bases(bases_played, bases_played_scrim, team_name)

    def visualization_bar_bases(self, bases, bases_played_scrim, team_name):
        print("Bases played by " + team_name)
        bases_nbr = []
        for base in self.bases:
            nbr = bases.count(base)
            bases_nbr.append(nbr)
        bases_scrim_nbr = []
        for base in self.bases:
            nbr = bases_played_scrim.count(base)
            bases_scrim_nbr.append(nbr)

        print(bases_nbr)
        print(bases_scrim_nbr)

        x = np.arange(len(self.bases))

        fig, ax = plt.subplots()

        bar1 = ax.bar(x=(x - 0.3/2), height=bases_nbr, width=0.3, color='b', label="Internal + Scrim", align='edge', edgecolor='black')
        bar2 = ax.bar(x=(x + 0.3/2), height=bases_scrim_nbr, width=0.3, color='r', label="Scrim", align='edge', edgecolor='black')

        plt.xlabel("Bases")
        plt.ylabel("Number of Scrims and Internals")
        plt.title("Number of Scrim and Internal of " + team_name)
        ax.set_xticks(x)
        ax.set_xticklabels(self.bases)
        ax.legend()

        ax.bar_label(bar1, padding=3)
        ax.bar_label(bar2, padding=3)

        fig.tight_layout()
        plt.show()
