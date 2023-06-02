import json
from enum import Enum

# TODO:
# - read JSON into a data structure / build map
# - make game components (logic)
# - implement turns
# - interface with AI

class RegionType(Enum):
    LAND = 1
    SEA = 2

class EdgeType(Enum):
    LAND = 1
    SEA = 2
    COAST = 3

class Region:
    def __init__(self, name, id, region_type=RegionType.LAND, supply_centre=False):
        self.name = name
        self.id = id
        self.type = region_type
        self.supply_centre = supply_centre
        self.owner = None
        self.neighbours = []

    def add_neighbour(self, region, edge_type=None):
        if edge_type is None:
            if region.type is RegionType.
        self.neighbours.append({"by": edge_type})

    def assign_owner(self, country):
        self.owner = country


