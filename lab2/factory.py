from player import Player
import xml.etree.ElementTree as ET
import json
from datetime import datetime


import player_pb2

class PlayerFactory:
    def to_json(self, players):
        list = []
        
        for player in players:
            list2 = {}
            list2["nickname"] = player.nickname
            list2['email'] = player.email
            list2['date_of_birth'] = datetime.strftime(player.date_of_birth,  "%Y-%m-%d")
            list2['xp'] = player.xp
            list2['class'] = player.cls
            
            list.append(list2)
        
        '''
            This function should transform a list of Player objects into a list with dictionaries.
        '''
        return list
    

    def from_json(self, list_of_dict):

        list = []
        
        for player in list_of_dict:
            list.append(Player(player["nickname"], player["email"], player["date_of_birth"], player["xp"], player["class"]))

        '''
            This function should transform a list of dictionaries into a list with Player objects.
        '''
        return list

    def from_xml(self, xml_string):
        players = []
        root = ET.fromstring(xml_string)
        
        for player in root.findall('player'):
            nickname = player.find('nickname')
            email = player.find('email')
            dob = player.find('date_of_birth')
            xp = player.find('xp')
            cls = player.find('class')
            
            nickname = nickname.text
            email = email.text
            date_of_birth = dob.text
            xp = int(xp.text)
            cls = cls.text
            player = Player(nickname, email, date_of_birth, xp, cls)

            players.append(player)
        
        '''
            This function should transform a XML string into a list with Player objects.
        '''
        return players

    def to_xml(self, list_of_players):
        root = ET.Element("data")
        
        for player in list_of_players:
            rez = ET.SubElement(root, "player")
            
            nickname = ET.SubElement(rez, "nickname")
            nickname.text = player.nickname
            
            email = ET.SubElement(rez, "email")
            email.text = player.email
            
            dob = ET.SubElement(rez, "date_of_birth")
            dob.text = datetime.strftime(player.date_of_birth,  "%Y-%m-%d")
            
            xp = ET.SubElement(rez, "xp")
            xp.text = str(player.xp)
            
            cls = ET.SubElement(rez, "class")
            cls.text = player.cls
        
        '''
            This function should transform a list with Player objects into a XML string.
        '''
        return ET.tostring(root, encoding="utf-8").decode()

    def from_protobuf(self, binary):
        players = []
        player_message = player_pb2.PlayersList()  # Create an instance of the Player protobuf message
        player_message.ParseFromString(binary)

        for item in player_message.player:
            cls_name = player_pb2.Class.Name(item.cls)
            players.append(Player(
                item.nickname,
                item.email,
                item.date_of_birth,
                item.xp,
                cls_name
            ))

        return players
    
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''

    def to_protobuf(self, list_of_players):
        players_list = player_pb2.PlayersList()

        for item in list_of_players:
            proto_player = players_list.player.add()

            setattr(proto_player, 'nickname', item.nickname)
            setattr(proto_player, 'email', item.email)
            setattr(proto_player, 'date_of_birth', item.date_of_birth.strftime("%Y-%m-%d"))
            setattr(proto_player, 'xp', item.xp)
            setattr(proto_player, 'cls', getattr(player_pb2.Class, item.cls))

        players_list = players_list.SerializeToString()
        
        return players_list
        '''
            This function should transform a list with Player objects intoa binary protobuf string.
        '''
