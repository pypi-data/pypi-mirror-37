from .utility import MigrationLogger, Constant, Utility
from .design_handler import GetPlayoffDesign

from playoff import Playoff


class GetPlayoffData(object):
    """Class that make GET call via Playoff client to retrieve data from
    the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game
        self.logger = MigrationLogger.get_instance()

    # ==============
    # COUNT METHODS
    # ==============

    def get_team_count(self):
        """Return number of teams in the game"""
        self.logger.debug("returning number of teams")

        return self.game.get(Constant.ADMIN_TEAMS, {})[Constant.TOTAL]

    def get_players_count(self):
        """Returns number of players in the game"""
        self.logger.debug("returning number of players")

        return self.game.get(Constant.ADMIN_PLAYERS, {})[Constant.TOTAL]

    def get_players_count_in_team(self, team_id):
        """Return number of players of the chosen team

        :param str team_id: containing id of a team
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.logger.debug("returning number of players in team: " + team_id)

        return self.game.get(Constant.ADMIN_TEAMS + team_id +
                             '/members', {})[Constant.TOTAL]

    # ==============
    # INFO METHODS
    # ==============

    def get_game_id(self):
        """ Returns game id of the chosen game """
        self.logger.debug("returning game_id")

        return self.game.get(Constant.ADMIN_ROOT)["game"]["id"]

    def get_teams_by_id(self):
        """Returns a list of teams id"""
        teams_id = []
        number_teams = self.get_team_count()
        number_pages = Utility.get_number_pages(number_teams)

        self.logger.info("preparing list of teams id")

        for count in range(number_pages):

            teams = self.game.get(Constant.ADMIN_TEAMS,
                                  {"skip": str(count * 100), "limit": "100"})

            for team in teams['data']:
                teams_id.append(team['id'])

                self.logger.debug(team['id'] + " added to list")

        self.logger.info("returning list of teams id")

        return teams_id

    def get_team_info(self, team_id):
        """Return information of the chosen team

        :param str team_id: containing id of a team
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.logger.debug("returning info of team: " + team_id)

        return self.game.get(Constant.ADMIN_TEAMS + team_id, {})

    def get_players_by_id(self):
        """Return a list of players id"""
        players_id = []
        number_players = self.get_players_count()
        number_pages = Utility.get_number_pages(number_players)

        self.logger.info("preparing list of players id")

        for count in range(number_pages):
            players = self.game.get(Constant.ADMIN_PLAYERS,
                                    {"skip": str(count * 100), "limit": "100"})

            for player in players['data']:
                players_id.append(player['id'])

                self.logger.debug(player['id'] + "added to list")

        self.logger.info("returning list of players id")

        return players_id

    def get_player_profile(self, player_id):
        """Return profile data of the chosen player

        :param str player_id: containing id of a player
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_id])

        self.logger.debug("returning info of player: " + player_id)

        return self.game.get(Constant.ADMIN_PLAYERS + player_id, {})

    def get_player_feed(self, player_id):
        """Return a list of feed of the chosen player

        :param str player_id: player id
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_id])

        self.logger.debug("returning feed of player: " + player_id)

        player_feed = self.game.get(Constant.ADMIN_PLAYERS + player_id +
                                    "/activity", {"start": "0"})

        if player_feed is None:
            return []

        return player_feed

    def get_leaderboard(self, leaderboard_id):
        """Return chosen leaderboard

        :param str leaderboard_id: chosen leaderboard
        :raise: ParameterException: when parameter is empty
        """
        Utility.raise_empty_parameter_exception([leaderboard_id])

        self.logger.debug("returning leaderboard: " + leaderboard_id)

        data = {
            "player_id": Constant.PLAYER_ID,
            "cycle": Constant.CYCLE,
            "limit": Constant.BIG_NUMBER
        }

        return self.game.get(Constant.RUNTIME_LEADERBOARDS + leaderboard_id,
                             data)

    def get_metric_scores(self, player_id):
        """
        Return a list of all scores of the chosen player

        :param player_id: player id
        :return: list containing player's scores
        """
        Utility.raise_empty_parameter_exception([player_id])

        player_profile = self.get_player_profile(player_id)

        self.logger.info("returning player " + player_id + " scores")

        return player_profile['scores']

    def get_single_metric_score(self, player_id, metric_id):
        """
        Return score of the chosen player in the chosen metric
        :param player_id: player id
        :param metric_id: metric to get score
        :raise exception: if metric_id doesn't exists in the game
        :return: score of the player in the given metric
        """
        Utility.raise_empty_parameter_exception([player_id, metric_id])

        player_scores = self.get_metric_scores(player_id)

        self.logger.info("returning metric " + metric_id)

        for score in player_scores:
            if score['metric']['id'] == metric_id:
                return score

        self.logger.warning("metric " + metric_id + " wasn't found")
        raise Exception("no metric with given name was found")


class PostPlayoffData(object):
    """Class that make POST call via Playoff client to create instances
    in the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game
        self.logger = MigrationLogger.get_instance()

    def create_team(self, team_data):
        """Create a team

        :param dict team_data: team info necessary to create a team
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_data])

        self.logger.debug("creating team " + team_data['id'])

        self.game.post(Constant.ADMIN_TEAMS, {}, team_data)

        self.logger.debug("team created")

    def create_player(self, player_data):
        """Create a player

        :param dict player_data: player info necessary to create a player
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_data])

        self.logger.debug("creating player " + player_data['id'])

        self.game.post(Constant.ADMIN_PLAYERS, {}, player_data)

        self.logger.debug("player created")

    def join_team(self, team_id, data):
        """Join a team

        :param str team_id: team id to join
        :param dict data: data necessary to join a team
        :raise ParameterException: if a parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id, data])

        self.logger.debug("join team " + team_id)

        self.game.post(Constant.ADMIN_TEAMS + team_id + "/join", {}, data)

        self.logger.debug("team joined")

    def take_action(self, action_id, player_id, data):
        """Take an action

        :param str action_id: action id to take
        :param dict player_id: player id that take action
        :param dict data: data necessary to take action
        :raise ParameterException: if a parameter is empty
        """
        Utility.raise_empty_parameter_exception([action_id, player_id, data])

        self.logger.debug("taking action " + action_id + " by " +
                          player_id['player_id'])

        self.game.post(Constant.RUNTIME_ACTION + action_id + "/play",
                       player_id, data)

        self.logger.debug("action taken")


class DeletePlayoffData(object):
    """Class that make DELETE call via Playoff client to erase data
    from the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game
        self.data_getter = GetPlayoffData(game)
        self.logger = MigrationLogger.get_instance()

    def delete_single_team(self, team_id):
        """Delete chosen team

        :param str team_id: team id to destroy
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.logger.debug("team " + team_id + " will be deleted")

        self.game.delete(Constant.ADMIN_TEAMS + team_id, {})

        self.logger.debug("team deleted")

    def delete_single_player(self, player_id):
        """Delete chosen player

        :param str player_id: player id to destroy
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_id])

        self.logger.debug("player " + player_id + " will be deleted")

        self.game.delete(Constant.ADMIN_PLAYERS + player_id, {})

        self.logger.debug("player deleted")

    def delete_teams(self):
        """Delete all teams"""
        teams_by_id = self.data_getter.get_teams_by_id()
        teams_count = str(len(teams_by_id))

        self.logger.info(teams_count + " teams will be deleted")
        index = 0

        for team in teams_by_id:
            self.delete_single_team(team)

            index += 1
            self.logger.debug("team " + str(index) + " of " + teams_count +
                              " deleted")

        self.logger.info("teams deleted")

    def delete_players(self):
        """Delete all players"""
        players_by_id = self.data_getter.get_players_by_id()
        players_count = str(len(players_by_id))

        self.logger.info(players_count + " players will be deleted")
        index = 0

        for player in players_by_id:
            self.delete_single_player(player)

            index += 1
            self.logger.debug("player " + str(index) + " of " + players_count +
                              " deleted")

        self.logger.info("players deleted")

    def delete_all_data(self):
        """Delete all data from the game"""
        self.logger.info("deleting data")

        self.delete_players()
        self.delete_teams()

        self.logger.info("data deleted")


class PatchPlayoffData(object):
    """
    Class that make PATCH call via Playoff client to modify data in the
    Playoff game
    """
    def __init__(self, game: Playoff):
        self.game = game
        self.design_getter = GetPlayoffDesign(game)
        self.logger = MigrationLogger.get_instance()

    @staticmethod
    def state_metric_parser(metric_constraints):
        """
        Return dict containing item name as a key and id as a value
        :param metric_constraints: constraints to extract name and id
        """
        Utility.raise_empty_parameter_exception([metric_constraints])

        set_metric_dict = {}

        for item in metric_constraints['states']:
            key = item['name']
            value = item['id']

            set_metric_dict.update({key: value})

        return set_metric_dict

    @staticmethod
    def set_metric_parser(metric_constraints):
        """
        Return dict containing item name as a key and id as a value
        :param metric_constraints: constraints to extract name and id
        """
        Utility.raise_empty_parameter_exception([metric_constraints])

        set_metric_dict = {}

        for item in metric_constraints['items']:
            key = item['name']
            value = item['id']

            set_metric_dict.update({key: value})

        return set_metric_dict

    def value_parser(self, metric):
        """
        Return value formatted right to be used in patch method
        :param metric: metric from retrieve information
        """
        Utility.raise_empty_parameter_exception([metric])

        metric_id = metric['metric']['id']
        metric_type = metric['metric']['type']
        value = metric['value']

        metric_design = self.design_getter.get_single_metric_design(metric_id)
        metric_constraints = metric_design['constraints']

        if metric_type == "point":
            return value
        elif metric_type == "set":
            set_parser = self.set_metric_parser(metric_constraints)
            cloned_value = {}

            for score in value:
                key = set_parser[score['name']]
                value = score['count']

                cloned_value.update({key: value})

            return cloned_value
        elif metric_type == "state":
            state_parser = self.state_metric_parser(metric_constraints)

            return state_parser[value['name']]

    def json_metric_parser(self, metric):
        """
        Return json data accepted to json schema for call patch method

        :param metric: metric data to create dict/json
        :return: dict/json to use in patch_player_score
        """
        Utility.raise_empty_parameter_exception([metric])

        metric_id = metric['metric']['id']
        metric_type = metric['metric']['type']
        value = self.value_parser(metric)

        data = {
            "rewards": [{
                "metric": {
                    "id": metric_id,
                    "type": metric_type
                },
                "verb": "set",
                "value": value
            }]
        }

        self.logger.debug("returning json score")
        self.logger.debug(data)

        return data

    def patch_player_score(self, player_id, data):
        """
        Update a player score

        :param player_id: player id to update score
        :param data: data necessary to update a score
        """
        Utility.raise_empty_parameter_exception([player_id, data])

        self.logger.debug("updating score of player " + player_id)
        self.logger.debug("data given")
        self.logger.debug(data)

        self.game.patch(Constant.ADMIN_PLAYERS + player_id + Constant.SCORES,
                        {"player_id": player_id}, data)

        self.logger.debug("scores updated")

    def update_metric(self, player_id, metric_value):
        """
        Update a score of the given player in the given metric

        :param player_id: player id
        :param metric_value: metric data
        """
        Utility.raise_empty_parameter_exception([player_id, metric_value])

        metric_id = metric_value['metric']['id']

        self.logger.info("updating metric " + metric_id + " of player " +
                         player_id)

        # making json data for patch call
        data = self.json_metric_parser(metric_value)
        self.patch_player_score(player_id, data)
