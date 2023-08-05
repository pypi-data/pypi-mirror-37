from .utility import MigrationLogger, Constant, Utility

from playoff import Playoff


class GetPlayoffDesign(object):
    """Class that make GET call via Playoff client to retrieve design from
    the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game
        self.logger = MigrationLogger.get_instance()

    def get_teams_design(self):
        """Return a list containing all teams design"""
        self.logger.debug("calling playoff for teams design")

        return self.game.get(Constant.DESIGN_TEAMS, {})

    def get_single_team_design(self, team_id):
        """Return design of the chosen team

        :param str team_id: id of the team
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.logger.debug("returning " + team_id + " design")

        return self.game.get(Constant.DESIGN_TEAMS + team_id, {})

    def get_metrics_design(self):
        """Return a list containing all metrics design"""
        self.logger.debug("calling playoff for metrics design")

        return self.game.get(Constant.DESIGN_METRICS, {})

    def get_single_metric_design(self, metric_id):
        """Return design of the chosen metric

        :param str metric_id: id of metric
        """
        Utility.raise_empty_parameter_exception([metric_id])

        self.logger.debug("returning " + metric_id + " design")

        return self.game.get(Constant.DESIGN_METRICS + metric_id, {})

    def get_actions_design(self):
        """Return a list containing all actions design"""
        self.logger.debug("calling playoff for actions design")

        return self.game.get(Constant.DESIGN_ACTIONS, {})

    def get_single_action_design(self, action_id):
        """Return design of the chosen action

        :param str action_id: id of action
        """
        Utility.raise_empty_parameter_exception([action_id])

        self.logger.debug("returning " + action_id + " design")

        return self.game.get(Constant.DESIGN_ACTIONS + action_id, {})

    def get_leaderboards_design(self):
        """Return a list of dict containing leaderboards design id and name"""
        self.logger.debug("calling playoff for leaderboards design")

        return self.game.get(Constant.DESIGN_LEADERBOARDS, {})

    def get_single_leaderboard_design(self, leaderboard_id):
        """Return design of the chosen leaderboard

        :param str leaderboard_id: id of leaderboard
        """
        Utility.raise_empty_parameter_exception([leaderboard_id])

        self.logger.debug("returning " + leaderboard_id + " design")

        return self.game.get(Constant.DESIGN_LEADERBOARDS + leaderboard_id, {})

    def get_rules_design(self):
        """Return a list of dict containing rules design id and name"""
        self.logger.debug("calling playoff for rules design")

        return self.game.get(Constant.DESIGN_RULES, {})

    def get_single_rule_design(self, rule_id):
        """Return design of the chosen rule

        :param str rule_id: id of rule
        """
        Utility.raise_empty_parameter_exception([rule_id])

        self.logger.debug("returning " + rule_id + " design")

        return self.game.get(Constant.DESIGN_RULES + rule_id, {})


class PostPlayoffDesign(object):
    """Class that make POST call via Playoff client to create design
    in the Playoff game
    """
    def __init__(self, game: Playoff):
        self.game = game
        self.logger = MigrationLogger.get_instance()

    def create_team_design(self, design_data):
        """Create a team design

        :param dict design_data: info necessary to create a team design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.logger.debug("creating team design")

        self.game.post(Constant.DESIGN_TEAMS, {}, design_data)

        self.logger.debug("team design created")

    def create_metric_design(self, design_data):
        """Create a metric design

        :param dict design_data: info necessary to create a metric design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.logger.debug("creating metric design")

        self.game.post(Constant.DESIGN_METRICS, {}, design_data)

        self.logger.debug("team design created")

    def create_action_design(self, design_data):
        """Create a action design

        :param dict design_data: info necessary to create an action design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.logger.debug("creating action design")

        self.game.post(Constant.DESIGN_ACTIONS, {}, design_data)

        self.logger.debug("action design created")

    def create_leaderboard_design(self, design_data):
        """Create a leaderboard design

        :param dict design_data: info necessary to create an leaderboard design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.logger.debug("creating leaderboard design")

        self.game.post(Constant.DESIGN_LEADERBOARDS, {}, design_data)

        self.logger.debug("leaderboard design created")

    def create_rule_design(self, design_data):
        """Create a rule design

        :param dict design_data: info necessary to create an rule design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.logger.debug("creating rule design")

        self.game.post(Constant.DESIGN_RULES, {}, design_data)

        self.logger.debug("rule design created")


class DeletePlayoffDesign(object):
    """Class that make DELETE call via Playoff client to erase design
    from the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game
        self.design_getter = GetPlayoffDesign(game)
        self.logger = MigrationLogger.get_instance()

    def delete_single_team_design(self, team_id):
        """Delete chosen team_id from the game

        :param str team_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.logger.debug("deleting " + team_id + " design")

        self.game.delete(Constant.DESIGN_TEAMS + team_id, {})

    def delete_single_metric_design(self, metric_id):
        """Delete chosen team_id from the game

        :param str metric_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([metric_id])

        self.logger.debug("deleting " + metric_id + " design")

        self.game.delete(Constant.DESIGN_METRICS + metric_id, {})

    def delete_single_action_design(self, action_id):
        """Delete chosen team_id from the game

        :param str action_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([action_id])

        self.logger.debug("deleting " + action_id + " design")

        self.game.delete(Constant.DESIGN_ACTIONS + action_id, {})

    def delete_single_leaderboard_design(self, leaderboard_id):
        """Delete chosen team_id from the game

        :param str leaderboard_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([leaderboard_id])

        self.logger.debug("deleting " + leaderboard_id + " design")

        self.game.delete(Constant.DESIGN_LEADERBOARDS + leaderboard_id, {})

    def delete_single_rule_design(self, rule_id):
        """Delete chosen rule_id from the game

        :param str rule_id: rule id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([rule_id])

        self.logger.debug("deleting " + rule_id + " design")

        self.game.delete(Constant.DESIGN_RULES + rule_id, {})

    def delete_teams_design(self):
        """Delete teams design"""
        teams_design = self.design_getter.get_teams_design()
        teams_count = str(len(teams_design))

        self.logger.info(teams_count + " teams design will be deleted")
        index = 0

        for team in teams_design:
            self.delete_single_team_design(team['id'])

            index += 1
            self.logger.debug("team " + str(index) + " of " + teams_count +
                              " deleted")

        self.logger.info("teams deleted")

    def delete_metrics_design(self):
        """Delete metrics design"""
        metrics_design = self.design_getter.get_metrics_design()
        metrics_count = str(len(metrics_design))

        self.logger.info(metrics_count + " metrics design will be deleted")
        index = 0

        for metric in metrics_design:
            self.delete_single_metric_design(metric['id'])

            index += 1
            self.logger.debug("metric " + str(index) + " of " + metrics_count +
                              " deleted")

        self.logger.info("metrics deleted")

    def delete_actions_design(self):
        """Delete actions design"""
        actions_design = self.design_getter.get_actions_design()
        actions_count = str(len(actions_design))

        self.logger.info(actions_count + " actions design will be deleted")
        index = 0

        for action in actions_design:
            self.delete_single_action_design(action['id'])

            index += 1
            self.logger.debug("action " + str(index) + " of " + actions_count +
                              " deleted")

        self.logger.info("actions deleted")

    def delete_leaderboards_design(self):
        """Delete leaderboards design"""
        leaderboards_design = self.design_getter.get_leaderboards_design()
        leaderboards_count = str(len(leaderboards_design))

        self.logger.info(leaderboards_count + " leaderboards design will be "
                                              "deleted")
        index = 0

        for leaderboard in leaderboards_design:
            self.delete_single_leaderboard_design(leaderboard['id'])

            index += 1
            self.logger.debug("leaderboard " + str(index) + " of " +
                              leaderboards_count + " deleted")

        self.logger.info("leaderboards deleted")

    def delete_rules_design(self):
        """Delete rules design"""
        rules_design = self.design_getter.get_rules_design()
        rules_count = str(len(rules_design))

        self.logger.info(rules_count + " rules design will be "
                                       "deleted")
        index = 0

        for rule in rules_design:
            self.delete_single_rule_design(rule['id'])

            index += 1
            self.logger.debug("rule " + str(index) + " of " +
                              rules_count + " deleted")

        self.logger.info("rules deleted")

    def delete_all_design(self):
        """Delete all design from the game"""
        self.logger.info("deleting all design")

        self.delete_leaderboards_design()
        self.delete_actions_design()
        self.delete_metrics_design()
        self.delete_teams_design()
        self.delete_rules_design()

        self.logger.info("all design deleted")
