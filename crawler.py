import os
from steam import steamid, WebAPI

from database import DatabaseConnection
from steamuser import SteamUser

try:
    with open("steamapi-key.txt", "r") as key:
        apikey = key.read()
except OSError:
    print("Couldn't open steamapi-key.txt. Abort.")
    os.exit(1)

webapi = WebAPI(key=apikey, format="json")

root_user = steamid.steam64_from_url("http://steamcommunity.com/id/longbyte1")

db = DatabaseConnection(7474, "neo4j", "neo4j")
db.initialize()
