import json
from urllib import parse, request


class connection:
    def __init__(self, api_key, userid):
        self.userid = userid
        self.api_key = api_key
        self.base_url = "http://www.notexponential.com/aip2pgaming/api/index.php"

    def get_team_member(self, teamid):
        textmod = {'type': "team", 'teamId': str(teamid)}
        textmod = parse.urlencode(textmod)
        header_dict = {'x-api-key': self.api_key, 'userid': self.userid}
        final_url = self.base_url + '?' + textmod

        req = request.Request(url=final_url, headers=header_dict)
        try:  # try to connect api
            response = request.urlopen(req)
            json_text = response.read().decode(encoding='utf-8')
            response.close()
            return (json.loads(json_text))  # change json text to dict
        except:  # if connection failed
            print("connection failed, return -1")
            response.close()
            return -1

    def create_game(self, teamid1, teamid2, boardsize=12, target=6):
        if (target > boardsize):
            print("Can't create the game,target should <= boardsize")
            return -1
        textmod = {"teamId1": str(teamid1), "teamId2": str(teamid2), "type": "game", "gameType": "TTT",
                   "boardSize": str(boardsize), "target": str(target)}
        textmod = parse.urlencode(textmod).encode(encoding='UTF8')  # change dict to url text
        header_dict = {'x-api-key': self.api_key, 'userid': self.userid}
        final_url = self.base_url
        req = request.Request(url=final_url, data=textmod, headers=header_dict)
        try:
            response = request.urlopen(req)
            json_text = response.read().decode(encoding='utf-8')
            response.close()
            return (json.loads(json_text))
        except:
            print("connection failed, return -1")
            response.close()
            return -1

    def make_move(self, teamid, move_x, move_y, gameid):
        textmod = {"teamId": str(teamid), "move": str(move_x) + "," + str(move_y), "type": "move",
                   "gameId": str(gameid)}
        textmod = parse.urlencode(textmod).encode(encoding='UTF8')
        header_dict = {'x-api-key': self.api_key, 'userid': self.userid}
        final_url = self.base_url
        req = request.Request(url=final_url, data=textmod, headers=header_dict)
        try:
            response = request.urlopen(req)
            json_text = response.read().decode(encoding='utf-8')
            response.close()
            return (json.loads(json_text))
        except:
            print("connection failed, return -1")
            response.close()
            return -1

    def get_move_list(self, gameid, count):
        textmod = {'type': "moves", 'gameId': str(gameid), "count": str(count)}
        textmod = parse.urlencode(textmod)
        header_dict = {'x-api-key': self.api_key, 'userid': self.userid}
        final_url = self.base_url + '?' + textmod

        req = request.Request(url=final_url, headers=header_dict)
        try:  # try to connect api
            response = request.urlopen(req)
            json_text = response.read().decode(encoding='utf-8')
            response.close()
            return (json.loads(json_text))  # change json text to dict
        except:  # if connection failed
            print("connection failed, return -1")
            response.close()
            return -1

    def get_board_string(self, gameid):
        textmod = {'type': "boardString", 'gameId': str(gameid)}
        textmod = parse.urlencode(textmod)
        header_dict = {'x-api-key': self.api_key, 'userid': self.userid}
        final_url = self.base_url + '?' + textmod

        req = request.Request(url=final_url, headers=header_dict)
        try:  # try to connect api
            response = request.urlopen(req)
            json_text = response.read().decode(encoding='utf-8')
            response.close()
            return (json.loads(json_text))  # change json text to dict
        except:  # if connection failed
            print("connection failed, return -1")
            response.close()
            return -1

    def get_board_map(self, gameid):
        textmod = {'type': "boardMap", 'gameId': str(gameid)}
        textmod = parse.urlencode(textmod)
        header_dict = {'x-api-key': self.api_key, 'userid': self.userid}
        final_url = self.base_url + '?' + textmod

        req = request.Request(url=final_url, headers=header_dict)
        try:  # try to connect api
            response = request.urlopen(req)
            json_text = response.read().decode(encoding='utf-8')
            response.close()
            return (json.loads(json_text))  # change json text to dict
        except:  # if connection failed
            print("connection failed, return -1")
            response.close()
            return -1


if __name__ == "__main__":
    game_connect = connection("41b0f3e5ced829a0d14d", '765')
    result = game_connect.get_board_string(1391)
    print(result)
    print(game_connect.get_board_map(1391))