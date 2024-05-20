""" Copyright (cc) 2024, developer@liggist.se. Read the licence.txt file for details."""
# GM_Plugin Version 1,0,0,1
from collections import namedtuple

BoundingBox = namedtuple('BoundingBox', ['left', 'right', 'top', 'bottom'])

class GM_Plugin:
    def __init__(self, graphics_manager,position,size):
        """
        The GM_Plugin class is the base class for all GM_Plugin subclasses.
        :param graphics_manager: The GraphicsManager instance
        :param position: The position of the GM_Plugin on the screen, (x,y).
        :param size: The size of the GM_Plugin on the screen, (length,width).
        """
        self.graphics_manager = graphics_manager
        self.version = None
        self.value = None
        self.new_value = False
        self.bounding_box = BoundingBox(left=position[0], right=position[0]+size[0], top=position[1], bottom=position[1]+size[1])
        
    def print_version(self):
        """Report the current plugin version"""
        if self.version != None:
            print("GM_Plugin {} version {}.{}.{}.{} loaded".format(self.__class__.__name__,*self.version))
        else:
            print("{} version None".format(self.__class__.__name__))
    
    def update(self, value):
        """Updates the plugin self.value.
        :param value: The new value to be stored.
        """
        # Update the stored value
        self.value = value
        self.new_value = True
        # print("{} got new value: {}.".format(type(self).__name__,self.value)) # debugging print-string

    def render(self):
        """Renders the plugin instance."""
        # Abstract method for rendering, to be implemented by subclasses
        raise NotImplementedError("Subclasses must implement the render method")

    def get_bounding_box(self):
        """Returns the bounding box of the plugin instance.
        :return: The bounding box of the plugin instance as a named tuple.
        """
        # Return the bounding box dimensions as a named tuple
        return self.bounding_box
