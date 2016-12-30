from neo4jrestclient import client
from neo4jrestclient.client import GraphDatabase


class DatabaseConnection:
    """Connects to a Neo4j database."""
    def __init__(self, port, username, password):
        self.db = GraphDatabase("http://localhost:"+port,
                                username=username,
                                password=password)

    def initialize(self):
        """Initializes the Neo4j database for use by the crawler."""
        self.users = self.db.labels.create("SteamUser")
        
    def retrieveUser(self, steamid):
        if not type(steamid) is int:
            throw ArgumentError("steamid must be an integer")

        query = "match (u:SteamUser) where u.steamid=\""+steamid+"\" return u"
        return elf.db.query(q=query, returns=(client.Node))[0]

    def addUser(self, user):
#        self.users.add(db.nodes.create(
        pass

    def shutdown(self):
        self.db.shutdown()
