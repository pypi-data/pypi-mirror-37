import os
from logging import Logger
import logging
import configparser

from playoff import Playoff
from dotenv import load_dotenv


class ParameterException(Exception):
    """Class that define an exception for parameters methods"""
    pass


class Constant(object):
    """Class that define some useful costant"""
    config = configparser.ConfigParser()
    file_name = "settings.ini"
    config.read(file_name)

    VERSION = config.get("constant", "Version")
    PLAYER_ID = config.get("constant", "Player_id")
    CYCLE = config.get("constant", "Cycle")

    BIG_NUMBER = 10 ** 10
    TOTAL = "total"

    SCORES = "/scores/"

    ADMIN_ROOT = "/admin/"
    ADMIN_PLAYERS = "/admin/players/"
    ADMIN_TEAMS = "/admin/teams/"

    DESIGN_TEAMS = "/design/versions/" + VERSION + "/teams/"
    DESIGN_ACTIONS = "/design/versions/" + VERSION + "/actions/"
    DESIGN_METRICS = "/design/versions/" + VERSION + "/metrics/"
    DESIGN_LEADERBOARDS = "/design/versions/" + VERSION + "/leaderboards/"
    DESIGN_RULES = "/design/versions/" + VERSION + "/rules/"
    DESIGN_DEPLOY = "/design/versions/" + VERSION + "/deploy/"

    RUNTIME_ACTION = "/runtime/actions/"
    RUNTIME_LEADERBOARDS = "/runtime/leaderboards/"


class MigrationLogger:
    __instance: Logger = None

    @staticmethod
    def get_instance():
        if MigrationLogger.__instance is None:
            MigrationLogger()
        return MigrationLogger.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MigrationLogger.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            config = configparser.ConfigParser()
            file_name = "settings.ini"
            config.read(file_name)

            logger_level = config.get("logger", "Level").upper()

            MigrationLogger.__instance = logging.getLogger("migration_logger")
            MigrationLogger.__instance.setLevel(logging.DEBUG)
            ch = logging.FileHandler(filename="migration.log", mode="w")
            ch.setLevel(logger_level)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s",
                "%m/%d/%Y %I:%M:%S %p")
            ch.setFormatter(formatter)
            MigrationLogger.__instance.addHandler(ch)


class Utility(object):
    """Class that define some useful methods"""

    @staticmethod
    def get_number_pages(number):
        """Return number of pages

        :param number: number of items to paginate
        :raise ParameterException: if parameter is negative

        Pages refers to pagination
        Every page has 100 item, so:
        number = 100 -> return 1
        number = 101 -> return 2
        """
        logger = MigrationLogger.get_instance()
        logger.debug("get_number_pages called")

        if number < 0:
            raise ParameterException("Parameter can't be negative")

        division_res = int(number / 100)

        return division_res if number % 100 == 0 else division_res + 1

    @staticmethod
    def raise_empty_parameter_exception(parameters):
        """Raise an exception if one parameter is empty

        :param list parameters: list of parameters to check
        :raise ParameterException
        """
        logger = MigrationLogger.get_instance()

        for par in parameters:
            if not isinstance(par, int):
                if not par:
                    logger.warning("parameters: " + str(parameters))

                    raise ParameterException("Parameter can't be empty")

    @staticmethod
    def get_playoff_client(client_id, client_secret, hostname):
        """Return Playoff game instance given his client id , client secret and
        hostname

        :param client_id: Playoff game client id
        :param client_secret: Playoff game client secret
        :param hostname: hostname
        :return: Playoff game instance
        """
        Utility.raise_empty_parameter_exception([client_id, client_secret,
                                                 hostname])

        logger = MigrationLogger.get_instance()
        logger.info("A new playoff client will be created...")

        from pathlib import Path
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)

        return Playoff(
            client_id=os.environ[client_id],
            client_secret=os.environ[client_secret],
            type='client',
            allow_unsecure=True,
            hostname=os.environ[hostname]
        )
