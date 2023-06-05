import json
from enum import Enum
from typing import Type
from typing_extensions import Self

# TODO:
# - read JSON into a data structure / build map
# - make game components (logic)
# - implement turns
# - interface with AI

class TroopType(Enum):
    FLEET = 'f'
    ARMY = 'a'

class Troop:
    def __init__(self, region, type, coast=None):
        self.location = {'region': region, 'coast': coast}
        region.move_troop(self, coast)
        self.type = type

class RegionType(Enum):
    LAND = 'l'
    SEA = 's'

class EdgeType(Enum):
    LAND = 1
    SEA = 2
    COAST = 3

class Region:
    def __init__(self, name, region_type, supply_centre, coasts=None):
        self.name = name
        self.type = region_type
        self.supply_centre = supply_centre
        self.coasts = coasts
        self.owner = None
        self.occupied = {'troop': None, 'coast': None}
        self.edges : list[Self] = []

    # self_coast means that edge is accessible if troop is in this particular coast
    # dest_coast means that edge leads to this particular coast of dest
    def add_edge(self, dest : Self, edge_type=None, self_coast=None, dest_coast=None):
        if edge_type is None:
            if dest.type is RegionType.SEA:
                edge_type = EdgeType.SEA
            if dest.type is RegionType.LAND and self.type is RegionType.LAND:
                edge_type = EdgeType.LAND
        self.edges.append({'type': edge_type, 'region': dest, 'self_coast': self_coast, 'dest_coast': dest_coast})

    # get edges on coasts
    def get_edges(self, self_coast):
        edge_list = []
        for edge in self.edges:
            if edge['self_coast'] == self_coast:
                edge_list.append(edge)
        return edge_list
    
    # get edge (if it exists) between coasts
    def get_edge(self, self_coast, region, dest_coast):
        for edge in self.edges:
            if edge['self_coast'] == self_coast and edge['region'] == region and edge['dest_coast'] == dest_coast:
                return edge
        return None

    def assign_owner(self, country):
        self.owner = country

    def move_troop(self, troop, coast=None):
        self.occupied['troop'] = troop
        self.occupied['coast'] = coast

  
## Create logic for turns
class turnLogic:
    def __init__(self,turn_flavor, origin, destination, combatent):
        self.turn_type = turn_flavor
        self.origin = origin
        self.destination = destination


class Action:
    def verify(self) -> bool:
        pass

    def is_executable(self, other_actions : list[Self]) -> bool:
        pass

    def execute(self):
        pass

    def do(self):
        if self.is_executable():
            self.execute()


class Move(Action):
    def __init__(self, troop : Troop, dest : Region, dest_coast=None):
        self.dest = dest
        self.dest_coast = dest_coast
        self.troop = troop
    
    def verify(self) -> bool:
        coast = self.troop.location['coast']
        region : Region = self.troop.location['region']
        edge = region.get_edge(coast, self.dest, self.dest_coast)
        # Check that destination is adjacent, A isn't going along SEA edge, and F isn't going along LAND edge
        if edge is not None and ((self.troop.type is TroopType.ARMY and edge['type'] is not EdgeType.SEA) or 
                                 (self.troop.type is TroopType.FLEET and edge['type'] is not EdgeType.LAND)):
            return True
        return False

    def is_executable(self, other_actions : list[Self]) -> bool:
        pass

    def execute(self):
        pass

class SUPPORT:
    def __init__(self, origin, destination, ally, ally_type):
        
        self.origin = origin

class ATTACK:
    def __init__(self, origin, destination, combatent_type):
        
        self.origin = origin

class HOLD:
    def __init__(self, origin, destination):
        self.origin = origin


def add_adjacencies(region : Region, adjacencies : list[str], region_coast=None):
    for string in adjacencies:
        # parse string
        parts = string.split('_')
        id_parts = parts[0].split('-')
        # get dest
        dest = regions[region[id_parts[0]]]
        # if dest is a particular coast
        dest_coast = None
        if len(id_parts) > 1:
            dest_coast = id_parts[1]
        # if it is coastal edge
        if len(parts) > 1: # NOTE: > 1 implies there is a second part to string which must be "c", which denotes a coastal edge
            region.add_edge(dest, edge_type=EdgeType.COAST, self_coast=region_coast, dest_coast=dest_coast)
        else:
            region.add_edge(region[parts[0]], self_coast=region_coast, dest_coast=dest_coast)


# Load Map
regions = {}
with open('data.json', 'r') as f:
  data = json.load(f)
  # initialize regions
  for json_object in data:
    regions[json_object['id']] = Region(json_object['name'], json_object['type'], 
                                        'supply_centre' in json_object and json_object['supply_centre'],
                                        None if 'coasts' not in json_object else json_object['coasts'])
  # add adjacencies
  for json_object in data:
    region = regions[json_object['id']]
    # if region has many coasts
    if 'coasts' in json_object:
        for i in range(len(region['coasts'])):
            add_adjacencies(region, json_object['adjacencies'][i], json_object['coasts'][i])
