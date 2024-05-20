""" Copyright (cc) 2024, developer@liggist.se. Read the licence.txt file for details."""
from graphics_manager.plugins import GM_Plugin, BoundingBox

class LinearGaugePlugin(GM_Plugin):
    def __init__(self, graphics_manager, position, size, **kwargs):
        """Linear gauge plugin constructor.
        :param graphics_manager: The graphics manager instance.
        :param position: The position of the plugin, (x,y).
        :param size: The size of the plugin, (length,width).
        kwargs: optional keyword arguments:
        direction: The direction of the gauge. 0,2 = horizontal, 1,3 = vertical. 2,3 use inverted direction.
        min_value: The value when gauge is empty. Defaults to 0.
        max_value: The value when gauge is full. Defaults to 100.
        """
        super().__init__(graphics_manager, position, size)
        self.version = (1,1,0,8)
        self.position = position
        self.direction = kwargs.get("direction", 0)
        self.min_value = kwargs.get("min_value", 0)
        self.max_value = kwargs.get("max_value", 100)
        self.current_value = self.min_value
        self.gauge_size = () # gauge_size value is always x,y while the incoming size is always length(in direction axis),width
        # Calculate gauge dimensions based on direction
        if self.direction not in (0,1,2,3):
            print("direction unknown! Setting direction = 0.")
            self.direction = 0
        if any([self.direction == 0,self.direction == 2]):
            self.gauge_size = size # size i lengt,width, direction 0 is horizontal so gauge_size is equal to size.
            print("horisontal, gauge_size: {}.".format(self.gauge_size))
        elif self.direction == 1:
            self.gauge_size = size[1],size[0] # gauge direction is now vertical, so length is in the other direction.
            print("vertical, gauge_size: {}.".format(self.gauge_size))
        elif self.direction == 3:
            self.gauge_size = size[1],size[0]
        # size is a tuple of length,width of the gauge, length is always in the direction of direction.
        if self.direction in (0, 2):  # Horizontal
            #self.gauge_size = (size[0], size[1])
            self.bounding_box = BoundingBox(
                left=position[0],
                right=position[0]+self.gauge_size[0],
                top=position[1]-self.gauge_size[1],
                bottom=position[1]
                )
        elif self.direction in(1, 3):  # Vertical
            #self.position = position[0],position[1] - size[0]
            #self.gauge_size = (size[1], size[0])
            self.bounding_box = BoundingBox(
                left=position[0],
                right=position[0]+size[1],
                top=position[1]-size[0],
                bottom=position[1]
                )
        else:
            print("something went very wrong...")
            self.bounding_box = BoundingBox(
                left=position[0],
                right=position[0]+size[0],
                top=position[1]-size[1],
                bottom=position[1]
                )
    
    def render(self):
        """Draw the gauge onto the display."""
        # if self.new_value:
        #    print("Got new value!! {}.".format(self.value))
        def resize(a_tuple,val)->tuple:
            return (a_tuple[0] + val, a_tuple[1] + val)
        # Determine fill size and coordinates based on gauge value
        framewidth = 4
        if type(self.value) != type(1): #if needed, initialize the value variable
            self.value = 0
        value = self.value
        # [name]_size holds the width,length of the rectangle
        # [name]_pos holds the x,y values of the rectangle.
        # frame is eqal to the whole gauge in size and position.
        frame_size = self.gauge_size
        frame_pos = self.bounding_box.left,self.bounding_box.top

        # gauge sits inside frame, with a framewidth frame thickness.
        gauge_size = resize(frame_size,(-framewidth*2))
        gauge_pos = resize(frame_pos,framewidth)
        
        #
        # fill is a "child" of gauge, defines the area to color in relation to value.
        fill_size = 0,0
        fill_pos = 0,0
        if self.direction == 0 or self.direction == 2: # horisontal
            fill_size = int( value / self.max_value * gauge_size[0]),gauge_size[1]
        elif self.direction == 1 or self.direction == 3: # vertical
            fill_size = gauge_size[0],int( value / self.max_value * gauge_size[1])
        
        if self.direction == 0: # 0 to the left.
            fill_pos = gauge_pos[0],gauge_pos[1]
        elif self.direction == 1: # vertical, zero at the bottom,
            fill_pos = gauge_pos[0],gauge_pos[1] + (gauge_size[1] - fill_size[1])
        elif self.direction == 2: # inverted sense of direction
            fill_pos = gauge_pos[0] + (gauge_size[0] - fill_size[0]), gauge_pos[1]
        elif self.direction == 3: # vertical, zero at the top
            fill_pos = gauge_pos[0],gauge_pos[1] + (gauge_size[0] - fill_size[0])
            
       
        # Draw the gauge
        # Draw the Frame first:
        self.graphics_manager.select_color(self.graphics_manager.palette[2])
        self.graphics_manager.draw_rect(*frame_pos, *frame_size)
        # then draw the empty field:
        self.graphics_manager.select_color(self.graphics_manager.palette[1])
        self.graphics_manager.draw_rect(*gauge_pos, *gauge_size)  # draw the info-box background
        # Draw fill colored rectangle on top
        self.graphics_manager.select_color(self.graphics_manager.palette[3])
        self.graphics_manager.draw_rect(*fill_pos, *fill_size)  # draw the info-box background
