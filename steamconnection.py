from steam import steamid, WebAPI


class SteamConnection:
    """Connects to the Steam Community API servers to get information
    about friends.
    """

    def __init__(self, key):
        self.api = WebAPI(key=key, format="json")

    def steam64_from_url(self, url):
        return steamid.steam64_from_url(url)

    def friends_list(self, steamid):
        return self.api.ISteamUser.GetFriendList(
                relationship="friend", steamid=steamid)
