import os
from json import dump, load

from .design_handler import GetPlayoffDesign, PostPlayoffDesign
from .data_handler import GetPlayoffData, PostPlayoffData
from .utility import MigrationLogger

from playoff import Playoff


class Export(object):
    """Base class that create a base dir and some parameters for exports
    classes
    """

    def __init__(self, game: Playoff):
        self.base_dir = "playoff-data"
        self.proj_path = os.getcwd() + "\\" + self.base_dir + "\\"

        if not os.path.isdir(self.proj_path):
            os.mkdir(self.base_dir)

        self.design_getter = GetPlayoffDesign(game)
        self.data_getter = GetPlayoffData(game)
        self.logger = MigrationLogger.get_instance()


class ExportRawDesign(Export):
    """Class that export raw design information from a game to a file .json"""

    def __init__(self, game: Playoff):
        super().__init__(game)

        self.dir_name = "design-raw"
        self.path = self.proj_path + self.dir_name + "\\"

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def export_teams(self):
        """Saves raw teams design data from the original game in a .json
        file
        """
        self.logger.info("exporting raw teams design")

        with open(self.path + "teams_raw_design.json", "w+") as file:
            cloned_teams_design = []
            teams_design = self.design_getter.get_teams_design()

            for team in teams_design:
                self.logger.debug("exporting " + team['id'] + " design")

                single_team_design = self.design_getter\
                    .get_single_team_design(team['id'])

                cloned_teams_design.append(single_team_design)

            dump(cloned_teams_design, file, sort_keys=True, indent=4)

        self.logger.info("raw teams design exported")

    def export_metrics(self):
        """Saves raw metrics design data from the original game in a .json
        file
        """
        self.logger.info("exporting raw metrics design")

        with open(self.path + "metrics_raw_design.json", "w+") as file:
            cloned_metrics_design = []
            metrics_design_id = self.design_getter.get_metrics_design()

            for metric in metrics_design_id:
                self.logger.debug("exporting " + metric['id'] + " design")

                single_metric_design = self.design_getter\
                    .get_single_metric_design(metric['id'])

                cloned_metrics_design.append(single_metric_design)

            dump(cloned_metrics_design, file, sort_keys=True, indent=4)

        self.logger.info("raw metrics design exported")

    def export_actions(self):
        """Saves raw actions design data from the original game in a .json
        file
        """
        self.logger.info("exporting raw actions design")

        with open(self.path + "actions_raw_design.json", "w+") as file:
            cloned_actions_design = []
            actions_design = self.design_getter.get_actions_design()

            for action in actions_design:
                self.logger.debug("exporting " + action['id'] + " design")

                single_action_design = self.design_getter\
                    .get_single_action_design(action['id'])

                cloned_actions_design.append(single_action_design)

            dump(cloned_actions_design, file, sort_keys=True, indent=4)

        self.logger.info("raw actions design exported")

    def export_leaderboards(self):
        """Saves raw leaderboards design data from the original game in a .json
        file
        """
        self.logger.info("exporting raw leaderboards design")

        with open(self.path + "leaderboards_raw_design.json", "w+") as file:
            cloned_leaderboards_design = []
            leaderboards_id = self.design_getter.get_leaderboards_design()

            for board in leaderboards_id:
                self.logger.debug("exporting " + board['id'] + " design")

                single_design = self.design_getter\
                    .get_single_leaderboard_design(board['id'])

                cloned_leaderboards_design.append(single_design)

            dump(cloned_leaderboards_design, file, sort_keys=True, indent=4)

        self.logger.info("raw leaderboards design exported")

    def export_all_design(self):
        self.logger.info("exporting raw design")

        self.export_teams()
        self.export_metrics()
        self.export_actions()
        self.export_leaderboards()

        self.logger.info("raw design exported")


class ExportRawData(Export):
    """Class that export raw data information from a game to a file .json"""

    def __init__(self, game: Playoff):
        super().__init__(game)

        self.dir_name = "data-raw"
        self.path = self.proj_path + self.dir_name + "\\"

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def export_teams(self):
        """Saves raw instances of all teams from the original game in a .json
        format
        """
        self.logger.info("exporting raw teams data")

        with open(self.path + "teams_raw.json", "w+") as file:
            cloned_teams_instances = []
            teams_by_id = self.data_getter.get_teams_by_id()

            for team in teams_by_id:
                self.logger.debug("exporting " + team + " data")

                team_instance_info = self.data_getter.get_team_info(team)

                cloned_teams_instances.append(team_instance_info)

            dump(cloned_teams_instances, file, sort_keys=True, indent=4)

        self.logger.info("raw teams data exported")

    def export_players(self):
        """Saves raw profile data of all players from the original game in a
        .json format
        """
        self.logger.info("exporting raw players data")

        with open(self.path + "players_raw.json", "w+") as file:
            cloned_players = []
            players_by_id = self.data_getter.get_players_by_id()

            for player in players_by_id:
                self.logger.debug("exporting " + player + " data")

                player_instance_info = self.data_getter\
                    .get_player_profile(player)

                cloned_players.append(player_instance_info)

            dump(cloned_players, file, sort_keys=True, indent=4)

        self.logger.info("raw players data exported")

    def export_players_feed(self):
        """Saves raw feed data of all players from the original game in a
        .json format
        """
        self.logger.info("exporting raw players feed data")

        with open(self.path + "players_feed_raw.json", "w+") as file:
            cloned_feed = {}
            players_id = self.data_getter.get_players_by_id()

            for player in players_id:
                self.logger.debug("exporting " + player + " feed data")

                player_feed = self.data_getter.get_player_feed(player)

                cloned_feed.update({player: player_feed})

            dump(cloned_feed, file, sort_keys=True, indent=4)

        self.logger.info("raw players feed data exported")

    def export_all_data(self):
        self.logger.info("exporting raw data")

        self.export_teams()
        self.export_players()
        self.export_players_feed()

        self.logger.info("raw data exported")


class ExportDesign(Export):

    def __init__(self, game: Playoff):
        super().__init__(game)

        self.dir_name = "design"
        self.path = self.proj_path + self.dir_name + "\\"

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def export_teams(self):
        """ Create json file containing each team design of the original
        game
        """
        self.logger.info("exporting teams design")

        with open(self.path + "teams_design.json", "w+") as file:
            teams_design_clone = []
            teams_design = self.design_getter.get_teams_design()

            for team in teams_design:
                self.logger.debug("exporting " + team['id'] + " design")

                single_team_design = self.design_getter.get_single_team_design(
                    team['id'])

                team_design_data = {
                    'name': single_team_design['name'],
                    'id': single_team_design['id'],
                    'permissions': single_team_design['permissions'],
                    'creator_roles': single_team_design['creator_roles'],
                    'settings': single_team_design['settings'],
                    '_hues': single_team_design['_hues']
                }

                if 'description' in single_team_design.keys():
                    team_design_data.update(
                        {'description': single_team_design['description']})

                teams_design_clone.append(team_design_data)

            dump(teams_design_clone, file, sort_keys=True, indent=4)

        self.logger.info("teams design exported")

    def export_metrics(self):
        """ Create json file containing each metric design of the original
        game
        """
        self.logger.info("exporting metrics design")

        with open(self.path + "metric_design.json", "w+") as file:
            cloned_metrics = []
            metrics_design = self.design_getter.get_metrics_design()

            for metric in metrics_design:
                self.logger.debug("exporting " + metric['id'] + " design")

                single_metric_design = self.design_getter\
                    .get_single_metric_design(metric['id'])

                metric_design_data = {
                    "id": single_metric_design['id'],
                    "name": single_metric_design['name'],
                    "type": single_metric_design['type'],
                    "constraints": single_metric_design['constraints']
                }

                if "description" in single_metric_design.keys():
                    metric_design_data.update(
                        {"description": single_metric_design["description"]})

                cloned_metrics.append(metric_design_data)

            dump(cloned_metrics, file, sort_keys=True, indent=4)

        self.logger.info("metrics design exported")

    def export_actions(self):
        """ Create json file containing each action design of the original
        game
        """
        self.logger.info("exporting actions design")

        with open(self.path + "actions_design.json", "w+") as file:
            cloned_actions = []
            actions_design = self.design_getter.get_actions_design()

            for action in actions_design:
                self.logger.debug("exporting " + action['id'] + " design")

                single_action_design = self.design_getter\
                    .get_single_action_design(action['id'])

                cloned_actions.append(single_action_design)

            dump(cloned_actions, file, sort_keys=True, indent=4)

        self.logger.info("actions design exported")

    def export_leaderboards(self):
        """ Create json file containing each leaderboard design of the original
        game
        """
        self.logger.info("exporting leaderboards design")

        with open(self.path + "leaderboards_design.json", "w+") as file:
            cloned_leaderboards = []
            leaderboards = self.design_getter.get_leaderboards_design()

            for board in leaderboards:
                self.logger.debug("exporting " + board['id'] + " design")

                single_board = self.design_getter\
                    .get_single_leaderboard_design(board['id'])

                board_data = {
                    "id": single_board['id'],
                    "name": single_board['name'],
                    "entity_type": single_board['entity_type'],
                    "scope": single_board['scope'],
                    "metric": single_board['metric'],
                    "cycles": single_board['cycles']
                }

                if "description" in single_board.keys():
                    board_data.update(
                        {"description": single_board["description"]})

                cloned_leaderboards.append(board_data)

            dump(cloned_leaderboards, file, sort_keys=True, indent=4)

        self.logger.info("leaderboards design exported")

    def export_all_design(self):
        self.logger.info("exporting design")

        self.export_teams()
        self.export_metrics()
        self.export_actions()
        self.export_leaderboards()

        self.logger.info("design exported")


class ExportData(Export):

    def __init__(self, game: Playoff):
        super().__init__(game)

        self.dir_name = "data"
        self.path = self.proj_path + self.dir_name + "\\"

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def export_teams(self):
        """ Create json file containing each team instance of the original
        game
        """
        self.logger.info("exporting teams data")

        with open(self.path + "teams.json", "w+") as file:
            cloned_teams_instances = []
            teams_by_id = self.data_getter.get_teams_by_id()

            for team in teams_by_id:
                self.logger.debug("exporting " + team + " data")

                team_data = self.data_getter.get_team_info(team)

                cloned_team_data = {
                    'id': team_data['id'],
                    'name': team_data['name'],
                    'access': team_data['access'],
                    'definition': team_data['definition']['id']
                }

                cloned_teams_instances.append(cloned_team_data)

            dump(cloned_teams_instances, file, sort_keys=True, indent=4)

        self.logger.info("teams data exported")

    def export_players(self):
        """ Create json file containing id and alias of each player of the
        original game
        """
        self.logger.info("exporting players data")

        with open(self.path + "players.json", "w+") as file:
            cloned_players = []
            players_by_id = self.data_getter.get_players_by_id()

            for player in players_by_id:
                self.logger.debug("exporting " + player + " data")

                player_data = self.data_getter.get_player_profile(player)

                cloned_player_data = {
                    'id': player_data['id'],
                    'alias': player_data['alias']
                }

                cloned_players.append(cloned_player_data)

            dump(cloned_players, file, sort_keys=True, indent=4)

        self.logger.info("raw players data exported")

    def export_players_in_team(self):
        """ Create json file containing the team of each player of the
        original game
        """
        self.logger.info("exporting players in team")

        with open(self.path + "players_in_team.json", "w+") as file:
            cloned_players_in_team = {}
            players_by_id = self.data_getter.get_players_by_id()

            for player in players_by_id:
                self.logger.debug("exporting teams of player " + player)

                player_profile = self.data_getter.get_player_profile(player)

                for team in player_profile['teams']:

                    cloned_team_player = {
                        "requested_roles": {
                            team['roles'][0]: True
                        },
                        "player_id": player
                    }

                    team_id = team['id']

                    if not (team_id in cloned_players_in_team.keys()):
                        cloned_players_in_team.update({team_id: []})
                        cloned_players_in_team[team_id]\
                            .append(cloned_team_player)
                    else:
                        cloned_players_in_team[team_id]\
                            .append(cloned_team_player)

            dump(cloned_players_in_team, file, sort_keys=True, indent=4)

        self.logger.info("players in team exported")

    def export_players_feed(self):
        """ Create json file containing the activity feed of each player of the
        original game
        """
        self.logger.info("exporting players feed data")

        with open(self.path + "players_feed.json", "w+") as file:
            cloned_players_feed = {}
            players_id = self.data_getter.get_players_by_id()

            for player in players_id:
                self.logger.debug("exporting " + player + " feed data")

                player_feed = self.data_getter.get_player_feed(player)

                feed_count = str(len(player_feed))
                index = 0

                for feed in player_feed:
                    player_single_feed = {}

                    if feed['event'] == 'action':
                        player_single_feed.update({"id": feed['action']['id']})
                        player_single_feed.update(
                            {"variables": feed['action']['vars']})
                        player_single_feed.update({"scopes": feed['scopes']})

                        if not (player in cloned_players_feed.keys()):
                            cloned_players_feed.update({player: []})
                            cloned_players_feed[player]\
                                .append(player_single_feed)
                        else:
                            cloned_players_feed[player]\
                                .append(player_single_feed)

                    index += 1
                    self.logger.debug("feed " + str(index) + " of " +
                                      feed_count + " exported")

            dump(cloned_players_feed, file, sort_keys=True, indent=4)

        self.logger.info("players feed data exported")

    def export_all_data(self):
        self.logger.info("exporting data")

        self.export_teams()
        self.export_players()
        self.export_players_in_team()
        self.export_players_feed()

        self.logger.info("data exported")


class Import(object):
    """Base class that saves base path and create an instance of a game for
    imports classes"""

    def __init__(self, game: Playoff):
        self.base_dir = "playoff-data"
        self.proj_path = os.getcwd() + "\\" + self.base_dir + "\\"

        if not os.path.isdir(self.proj_path):
            raise Exception("Directory doesn't exists")

        self.design_poster = PostPlayoffDesign(game)
        self.data_poster = PostPlayoffData(game)
        self.logger = MigrationLogger.get_instance()


class ImportDesign(Import):
    """Class that import design in a playoff game from a .json file"""

    def __init__(self, game: Playoff):
        super().__init__(game)

        self.dir_name = "design"
        self.path = self.proj_path + self.dir_name + "\\"

        if not os.path.isdir(self.path):
            raise Exception("Directory doesn't exists")

    def import_teams(self):
        """Import teams from .json file"""
        self.logger.info("importing teams design")

        with open(self.path + "teams_design.json", "r") as file:
            teams_design = load(file)

        for team in teams_design:
            self.logger.debug("importing " + team)

            self.design_poster.create_team_design(team)

        self.logger.info("teams design imported")

    def import_metrics(self):
        """Import metrics from .json file"""
        self.logger.info("importing metrics")

        with open(self.path + "metric_design.json", "r") as file:
            metrics_design = load(file)

        for metric in metrics_design:
            self.logger.debug("importing " + metric)

            self.design_poster.create_metric_design(metric)

        self.logger.info("teams imported")

    def import_actions(self):
        """Import actions from .json file"""
        self.logger.info("importing actions design")

        with open(self.path + "actions_design.json", "r") as file:
            actions_design = load(file)

        for action in actions_design:
            self.logger.debug("importing " + action)

            self.design_poster.create_action_design(action)

        self.logger.info("actions design imported")

    def import_leaderboards(self):
        """Import leaderboards from .json file"""
        self.logger.info("importing leaderboards design")

        with open(self.path + "leaderboards_design.json", "r") as file:
            leaderboards_design = load(file)

        for leaderboard in leaderboards_design:
            self.logger.debug("importing " + leaderboard)

            self.design_poster \
                .create_leaderboard_design(leaderboard)

        self.logger.info("leaderboards design imported")

    def import_all_design(self):
        self.logger.info("importing design")

        self.import_teams()
        self.import_metrics()
        self.import_actions()
        self.import_leaderboards()

        self.logger.info("design imported")


class ImportData(Import):
    """Class that import data in a playoff game from a .json file"""

    def __init__(self, game: Playoff):
        super().__init__(game)

        self.dir_name = "data"
        self.path = self.proj_path + self.dir_name + "\\"

        if not os.path.isdir(self.path):
            raise Exception("Directory doesn't exists")

    def import_teams(self):
        """Import teams from .json file"""
        self.logger.info("importing teams data")

        with open(self.path + "teams.json", "r") as file:
            teams = load(file)

        for team in teams:
            self.logger.debug("importing " + team)

            self.data_poster.create_team(team)

        self.logger.info("teams data imported")

    def import_players(self):
        """Import players from .json file"""
        self.logger.info("importing players data")

        with open(self.path + "players.json", "r") as file:
            players = load(file)

        for player in players:
            self.logger.debug("importing " + player)

            self.data_poster.create_player(player)

        self.logger.info("players data imported")

    def import_players_in_team(self):
        """Import players in team from .json file"""
        self.logger.info("importing players in team")

        with open(self.path + "players_in_team.json", "r") as file:
            players_in_team = load(file)

        for key, value in players_in_team.items():
            for player in value:
                self.logger.debug("importing " + player + " in " + key)

                self.data_poster.join_team(key, player)

        self.logger.info("players in team imported")

    def import_players_feed(self):
        """Import players feed from .json file"""
        self.logger.info("importing players feed")

        with open(self.path + "players_feed.json", "r") as file:
            players_feed = load(file)

        for key, value in players_feed.items():
            self.logger.debug("importing action for " + key)

            feed_count = str(len(value))
            index = 0

            for feed in value:
                data = {
                    "scopes": feed["scopes"],
                    "variables": feed["variables"]
                }
                self.data_poster.take_action(feed['id'], {"player_id": key},
                                             data)

                index += 1
                self.logger.debug("imported action " + str(index) + " of " +
                                  feed_count + " feed")

    def import_all_data(self):
        self.logger.info("importing data")

        self.import_teams()
        self.import_players()
        self.import_players_in_team()
        self.import_players_feed()

        self.logger.info("data imported")
