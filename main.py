import json
from enum import Enum

# TODO:
# - read JSON into a data structure / build map
# - make game components (logic)
# - implement turns
# - interface with AI

class RegionType(Enum):
    LAND = 'l'
    SEA = 's'

class EdgeType(Enum):
    LAND = 1
    SEA = 2
    COAST = 3

class Region:
    def __init__(self, name, region_type, supply_centre):
        self.name = name
        self.type = region_type
        self.supply_centre = supply_centre
        self.owner = None
        self.neighbours = []

    # coast means that this edge is only accessible from a particular coast of self
    def add_neighbour(self, region, edge_type=None, coast=None):
        if edge_type is None:
            if region.type is RegionType.SEA:
                edge_type = EdgeType.SEA
            if region.type is RegionType.LAND and self.type is RegionType.LAND:
                edge_type = EdgeType.LAND
        self.neighbours.append({"type": edge_type, "region": region, "coast": coast})

    def assign_owner(self, country):
        self.owner = country
  
## Create logic for turns
class turnLogic:
    def __init__(self,turn_flavor, origin, destination, combatent):
        self.turn_type = turn_flavor
        self.origin = origin
        self.destination = destination
class MOVE:
    def __init__(self, origin, destination, combatent_type):
        
        self.origin = origin
class SUPPORT:
    def __init__(self, origin, destination, ally, ally_type):
        
        self.origin = origin
class ATTACK:
    def __init__(self, origin, destination, combatent_type):
        
        self.origin = origin
class HOLD:
    def __init__(self, origin, destination):
        self.origin = origin

# Load Map
regions = {}
with open('data.json', 'r') as f:
  data = json.load(f)
  # initialize regions
  for object in data:
      regions[object['id']] = Region(object['name'], object['type'], 'supply_centre' in object and object['supply_centre'])
  # add adjacencies
  for object in data:
      region = regions[object['id']]
      for string in object['adjacencies']:
          parts = string.split('_')
          # if it is coastal edge
          if len(parts) > 1:
              region.add_neighbour(region[parts[0]], )