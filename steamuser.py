

class SteamUser:
    def __init__(self, steamid):
        self.steamid = steamid

    def get_friends(self, webapi):
       friends_raw = webapi.ISteamUser.GetFriendList(relationship="friend", steamid=self.steamid)

        
