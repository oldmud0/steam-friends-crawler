

class SteamUser:
    """Represents a local, out-of-database copy of a Steam user.
    No guarantees are made on whether or not a SteamUser has already been
    copied to the database or not.
    """

    def __init__(self, steamid, private=False):
        self.steamid = steamid
        self.private = private
        self.friends = set()

    def add_friends(self, friends):
        """Add friends to a SteamUser given
        a valid set of SteamUsers.
        """
        if isinstance(friends, set):
            if len(friends) == 0:
                return
            if isinstance(friends[0], SteamUser):
                self.friends.add(friends)
                return
        TypeError("Friends must be a set of SteamUser objects")
