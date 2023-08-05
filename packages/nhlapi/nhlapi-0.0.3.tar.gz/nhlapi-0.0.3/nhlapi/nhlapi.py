#!/usr/bin/env python

from services.team_service import TeamService
from services.game_service import GameService
from data_source import api
from data_source import json_api

class NhlApi(object):
    def __init__(self):
        dataSource = api.Api()
        self.dataSource = dataSource
        self.teamService = TeamService(self.dataSource)
        self.gameService = GameService(self.dataSource)

    def getTeamsList(self):
        return self.teamService.getTeamsList()

    def getNextGameForTeam(self, abbrev):
        team = self.teamService.getTeamByAbbreviation(abbrev)
        return self.gameService.getNextGameForTeam(team)

    def getUpdatedGame(self, game):
        return self.gameService.updateGame(game)

    def getTodaysGames(self):
        return self.gameService.getTodaysGames()