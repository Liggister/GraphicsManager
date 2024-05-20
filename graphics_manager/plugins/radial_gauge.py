""" Copyright (cc) 2024, developer@liggist.se. Read the licence.txt file for details."""
from graphics_manager.plugins import GM_Plugin, BoundingBox
import math

class RadialGaugePlugin(GM_Plugin):
    def __init__(self, graphics_manager, position, size, **kwargs):
        """Radial gauge plugin constructor.
        :param graphics_manager: The graphics manager instance.
        :param position: The position of the plugin, (x,y).
        :param size: The size of the plugin, (radius,direction).
        kwargs: optional keyword arguments:
        start_angle: The start angle of the gauge. Defaults to 215.
        stop_angle: The stop angle of the gauge. Defaults to 90.
        full_range: If True, the range will be from -max_value to max_value, with min_value in the middle of the gauge. Defaults to False.
        min_value: The value when gauge is empty. Defaults to 0.
        max_value: The value when gauge is full. Defaults to 100.
        grad_lines: The number of graduation lines between the max/min lines. Defaults to 3.
        
        """
        super().__init__(graphics_manager, position, size)
        self.version = (1, 2, 2, 3)
        self.direction = size[1]  # Direction of the gauge needle movement
        self.center = position  # Center position of the gauge
        self.radius = size[0]  # Radius of the gauge
        self.min_value = kwargs.get("min_value", 0)
        self.max_value = kwargs.get("max_value", 100)
        self.full_range = kwargs.get("full_range", False)
        self.grad_lines = kwargs.get("grad_lines", 3)  # start and stop is always marked, value represents intermediate marks.
        self.start_angle = kwargs.get("start_angle", 215)
        self.stop_angle = kwargs.get("stop_angle", 90)
        self.current_angle = self.start_angle
        self.sweep_span = 0
        if self.start_angle > self.stop_angle:
            self.sweep_span = self.start_angle - self.stop_angle
        else:
            self.sweep_span = self.stop_angle - self.start_angle
        # print("sweep:{}.".format(self.sweep_span))
        self.indicator_ngon = RadialGaugePlugin.create_indicator(*self.center,self.radius)
        self.chevrons = RadialGaugePlugin.create_markers(*self.center,self.radius,self.start_angle,self.stop_angle,self.grad_lines)
        self.indicator = []
        self.draw_indicator()
    def got_new_val(self):
        """Gets called whenever a new value is provided.
        Clamps the value between max/min values and updates the gauge indicator angle accordingly."""
        start_val = self.min_value
        if self.value > self.max_value:
            self.value = self.max_value
        if self.full_range:
            start_val = -self.max_value
        if self.start_angle > self.stop_angle:
            hi_angle = self.start_angle
            lo_angle = self.stop_angle
        else:
            hi_angle = self.stop_angle
            lo_angle = self.start_angle
        val_angle = RadialGaugePlugin.map_value_to_angle(self.value, start_val, self.max_value, 0, self.sweep_span)
        # print("val_angle: {}.".format(val_angle))
        if self.direction == 0:
            if self.start_angle > self.stop_angle: # stop angle is smaller than start angle,
                self.current_angle = self.start_angle - val_angle # start from the start..????
            else: # stop angle is larger..
                self.current_angle = self.start_angle + val_angle # start from the other end
        elif self.direction == 1: #this is working as intended!
            if self.start_angle > self.stop_angle:
                self.current_angle = self.stop_angle + val_angle
            else:
                self.current_angle = self.stop_angle - val_angle
        else:
            print("Direction {} is not implemented!".format(self.direction))
            self.current_angle = self.start_angle - val_angle
        self.new_value = False
        # print("New angle from {}: {}.".format(self.value,self.current_angle))
        self.draw_indicator()
    
    def draw_indicator(self):
        """ Creates a indicator needle from stored values."""
        self.indicator = RadialGaugePlugin.rotate_ngon(self.center,self.indicator_ngon,self.current_angle)
    
    def render(self):
        """ Renders the gauge to teh display."""
        if self.new_value:
            self.got_new_val()
        # Draw the gauge scale and center dot:
        self.graphics_manager.select_color(self.graphics_manager.palette[2])
        self.graphics_manager.draw_circ(*self.center, 4)
        for chevron in self.chevrons:
            self.graphics_manager.draw_ngon(*chevron)
        
        # Draw the needle
        self.graphics_manager.select_color(self.graphics_manager.palette[3])
        self.graphics_manager.draw_ngon(self.indicator)
    
    @classmethod
    def rotate_ngon(cls,origin,ngon,angle):
        """ Rotate a polygon around a origin using a specified angle.
        :param origin: The center of rotation as a tuple:(x,y).
        :param ngon: The polygon to rotate as a list of tuples:[(x,y),].
        :param angle: The angle in degrees to rotate the polygon."""
        def rotate(origin, point, radangle):
            """ Rotate a point around a origin using a specified angle.
            :param origin: The center of rotation as a tuple:(x,y).
            :param point: The point to rotate as a tuple:(x,y).
            :param radangle: The angle in radians to rotate the polygon.
            """
            ox, oy = origin
            px, py = point
            
            qx = ox + math.cos(radangle) * (px - ox) - math.sin(radangle) * (py - oy)
            qy = oy + math.sin(radangle) * (px - ox) + math.cos(radangle) * (py - oy)
            return int(qx), int(qy)
        rotated_ngon = []
        radangle = math.radians(angle%360)
        for point in ngon:
            rotated_ngon.append(rotate(origin,point,radangle))
        return rotated_ngon
    
    @classmethod
    def move_ngon(cls,ngon,x_dist,y_dist):
        """ Moves a polygon.
        :param ngon: The polygon to move as a list of tuples:[(x,y),].
        :param x_dist: The x distance to move the polygon.
        :param y_dist: The y distance to move the polygon.
        """
        moved_ngon = []
        for point in ngon:
            out_x = point[0] + x_dist
            out_y = point[1] + y_dist
            moved_ngon.append((out_x,out_y))
        return moved_ngon
    @classmethod
    def scale_ngon(cls,ngon,radius):
        """Scale the polygon to the gauge radius specified"""
        scale = 1.0
        _scale = radius/100
        do_scale = True
        if _scale > 0.99 and _scale < 1.01:
            do_scale = False
        scaled_ngon = []
        for point in ngon:
            inX = int((point[0]/100) * radius )
            inY = int((point[1]/100) * radius )
            scaled_ngon.append((inX,inY))
        return scaled_ngon
    
    @classmethod
    def create_indicator(cls,x,y,radius):
        """ Creates a indicator needle from provided values."""
        indicator = []
        base_hand = [ (0,-14), (1,-16), (11,-42), (2,-58), (4,-73), (7,-75), (0,-94), (-7,-75), (-3,-73), (0,-58), (4,-42), (-1,-16) ] # Pointing upwards!
        indicator = RadialGaugePlugin.move_ngon(RadialGaugePlugin.scale_ngon(base_hand,radius),x,y)
        return indicator
    
    @classmethod
    def create_markers(cls,x,y,radius,start_angle,stop_angle,num_chevrons):
        """ Creates the clock hour markers.
        :param x: The x coordinate of the center of the gauge.
        :param y: The y coordinate of the center of the gauge.
        :param radius: The radius of the gauge.
        :param start_angle: The start angle of the gauge.
        :param stop_angle: The stop angle of the gauge.
        :param num_chevrons: The number of chevrons to draw.
        """
        r = int(radius)
        markStep = int(radius / 40)
        chevron_shape = RadialGaugePlugin.rotate_ngon((x,y),
                                         [(x-int(r*1.0),y), (x-int(r*0.999),y+markStep),
                                          (x-int(r*0.97),y+markStep+markStep), (x-int(r*0.92),y),
                                          (x-int(r*0.97),y-markStep-markStep), (x-int(r*0.999),y-markStep)
                                          ],90
                                         )
        a_marker = []
        
        step_angle = 0
        if start_angle != 0:
            _start = start_angle
        else:
            _start = start_angle
        if stop_angle != 0:
            _stop = stop_angle
        else:
            _stop = stop_angle
        if _start > _stop:
            lo_ang = _stop
            hi_ang = _start
            dir_step = 1
        else:
            lo_ang = _start
            hi_ang = _stop
            dir_step = 0
            
        step_angle = (hi_ang - lo_ang) / (num_chevrons+1)
        markers = []
        chevron_count = 0
        #print("Start:{},Stop:{},step:{}, num_chevs:{}.".format(_start,_stop,step_angle,num_chevrons))
        
        for mark in range(num_chevrons+2):
            if dir_step == 0:
                chevron = RadialGaugePlugin.rotate_ngon((x,y),chevron_shape,_start+(step_angle*chevron_count))
            if dir_step == 1:
                chevron = RadialGaugePlugin.rotate_ngon((x,y),chevron_shape,_start-(step_angle*chevron_count))
            markers.append(chevron)
            chevron_count += 1
        return markers
    
    @staticmethod
    def map_value_to_angle(value, value_min, value_max, angle_min, angle_max):
        """ Maps a value of one range to a angle of another range."""
        # Map value within a range to an angle within another range
        _value = value
        if type(_value) != type(1):
            _value = 0
        return ((_value - value_min) / (value_max - value_min)) * (angle_max - angle_min) + angle_min
