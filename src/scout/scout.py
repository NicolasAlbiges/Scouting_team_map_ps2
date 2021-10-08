from __future__ import print_function
from . import teams
import sys
from utils import utils

sys.path.append("..")


class Scouting:
    def __init__(self, df_teams):
        self.df_teams = df_teams
        self.bases_name = ["Waterson", "Pale", "Peris", "Fort liberty", "Acan", "Kessel", "Bridgewater"]
        self.teams_name = ["1RPC", "GOBS", "BYZZ", "xFPS", "GENX", "SDEM", "BWAE", "DTAC", "BACU", "HBG", "TRY"]
        self.bases_count = {}
        self.teams = []
        self.teams_computing()
        self.current_meta_map()

    def teams_computing(self):
        for team in self.teams_name:
            team_obj = teams.Teams(self.df_teams, team)
            # print(self.df_teams)
            self.teams.append(team_obj)

    def show_visualization_teams(self, teams_name):
        for team_obj in self.teams:
            if team_obj.team_name in teams_name:
                team_obj.visualization_bar_bases()

    def current_meta_map(self):
        print("\n----------- CURRENT META WITH MAP PLAYED BY EVERYONE (expect 1RPC) ------------------")
        df_teams = self.df_teams[self.df_teams.team_name != "1RPC"]
        df_teams_scrim = df_teams[df_teams.type == "Scrim"]

        bases_played = utils.split_bases(list(df_teams.bases_name.values))
        bases_played_scrim = utils.split_bases(list(df_teams_scrim.bases_name.values))

        print("\nStats with Scrim + Internal : \n")
        for base in self.bases_name:
            nbr = bases_played.count(base)
            print(base + " has been played : " + str(nbr) + " times")

        print("\nStats with Scrim : \n")
        for base in self.bases_name:
            nbr = bases_played_scrim.count(base)
            print(base + " has been played : " + str(nbr) + " times")

    def find_team_obj(self, team_name):
        team_index = self.teams_name.index(team_name)
        return self.teams[team_index]

    # TODO Smart ban, ban enney best map but also trying to ban a map you dont want to play
    #  not banning your best map as well
    def smart_ban(self, bases, team_bases_name, enemy_team_base, i, ct):
        enemy_best_map = enemy_team_base[i]
        return enemy_best_map

    def simulation_group_stage_remove_bases(self, bases, team_bases_name, team_name):
        for base in team_bases_name:
            worst_map = base
            if base in bases:
                break
        base_index = bases.index(worst_map)
        bases.pop(base_index)
        print(team_name + " BAN this map " + worst_map + "\n")
        return bases

    def smart_pick(self, bases, team_bases_name, enemy_team_base, i, ct):
        best_map = team_bases_name[i]
        if best_map in bases and best_map != enemy_team_base[ct]:
            return best_map
        elif i > len(team_bases_name):
            return self.smart_pick(bases, team_bases_name, enemy_team_base, len(team_bases_name) - 1, ct - 1)
        return self.smart_pick(bases, team_bases_name, enemy_team_base, i - 1, ct)

    def simulation_group_stage_pick_bases(self, bases, team_bases_name, enemy_team_base, team_name):
        best_map = self.smart_pick(bases, team_bases_name, enemy_team_base, len(team_bases_name) - 1, len(enemy_team_base) - 1)
        base_index = bases.index(best_map)
        bases.pop(base_index)
        print(team_name + " PICK this map " + best_map + "\n")
        return bases

    def simulation_group_stage(self, team_name_winner_name, team_name_loser_name):
        print("\n----------- SIMULATION GROUP STAGE STARTS ------------------\n")
        team_winner = self.find_team_obj(team_name_winner_name)
        team_loser = self.find_team_obj(team_name_loser_name)

        bases = self.bases_name.copy()

        bases = self.simulation_group_stage_remove_bases(bases, team_winner.sorted_base_name, team_name_winner_name)

        bases = self.simulation_group_stage_remove_bases(bases, team_loser.sorted_base_name, team_name_loser_name)

        bases = self.simulation_group_stage_remove_bases(bases, team_winner.sorted_base_name, team_name_winner_name)

        bases = self.simulation_group_stage_remove_bases(bases, team_loser.sorted_base_name, team_name_loser_name)

        print("\nThe remaining bases are :", bases)

    def simulation_playin(self, team_name_winner_name, team_name_loser_name):
        print("\n----------- SIMULATION PLAYINS STARTS ------------------\n")
        team_winner = self.find_team_obj(team_name_winner_name)
        team_loser = self.find_team_obj(team_name_loser_name)

        bases = self.bases_name.copy()

        bases = self.simulation_group_stage_remove_bases(bases, team_winner.sorted_base_name, team_name_winner_name)
        bases = self.simulation_group_stage_remove_bases(bases, team_loser.sorted_base_name, team_name_loser_name)

        bases = self.simulation_group_stage_pick_bases(bases, team_winner.sorted_base_name, team_loser.sorted_base_name, team_name_winner_name)
        bases = self.simulation_group_stage_pick_bases(bases, team_loser.sorted_base_name, team_winner.sorted_base_name, team_name_loser_name)

        bases = self.simulation_group_stage_remove_bases(bases, team_winner.sorted_base_name, team_name_winner_name)
        bases = self.simulation_group_stage_remove_bases(bases, team_loser.sorted_base_name, team_name_loser_name)

        print("The last base is :", bases)


