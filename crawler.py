from database import DatabaseConnection
from steamuser import SteamUser
from steamconnection import SteamConnection


class Crawler:
    """The main crawler class."""

    def __init__(self):
        self._init_steam_api()
        self._init_db()

        root_user = self.steam_api.steam64_from_url(
                "http://steamcommunity.com/id/longbyte1")

    def _load_steam_key(self):
        try:
            with open("steamapi-key.txt", "r") as key:
                return key.read()
        except OSError:
            OSError("Couldn't open steamapi-key.txt. Abort.")

    def _init_steam_api(self):
        self.steam_api = SteamConnection(self._load_steam_key())

    def _init_db(self):
        db = DatabaseConnection(7474, "neo4j", "neo4j")
        db.initialize()
