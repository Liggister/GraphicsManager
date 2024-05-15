""" Copyright (cc) 2024, developer@liggist.se. Read the licence.txt file for details."""
# GM_Plugin Version 1,0,0,0
from collections import namedtuple

BoundingBox = namedtuple('BoundingBox', ['left', 'right', 'top', 'bottom'])

class GM_Plugin:
    def __init__(self, graphics_manager,position,size):
        self.graphics_manager = graphics_manager
        self.version = None
        self.value = None
        self.new_value = False
        self.bounding_box = BoundingBox(left=position[0], right=position[0]+size[0], top=position[1], bottom=position[1]+size[1])
        
    def print_version(self):
        if self.version != None:
            print("GM_Plugin {} version {}.{}.{}.{} loaded".format(self.__class__.__name__,*self.version))
        else:
            print("{} version None".format(self.__class__.__name__))
    
    def update(self, value):
        # Update the stored value
        self.value = value
        self.new_value = True
        # print("{} got new value: {}.".format(type(self).__name__,self.value)) # debugging print-string

    def render(self):
        # Abstract method for rendering, to be implemented by subclasses
        raise NotImplementedError("Subclasses must implement the render method")

    def get_bounding_box(self):
        # Return the bounding box dimensions as a named tuple
        return self.bounding_box
