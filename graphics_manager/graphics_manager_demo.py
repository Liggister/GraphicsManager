""" Copyright (cc) 2024, developer@liggist.se. Read the licence.txt file for details."""
# GraphicsManager Demo file, file revision 1.0.2
from graphics_manager import GraphicsManager
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4

## Create the instance of GraphicsManager and provide a display:
gman = GraphicsManager()
### In case you wish to change the color palette:
# gmain = GraphicsManager( colors=[ (0,0,0),(10,10,90),(220,5,180),(250,200,255),(180,160,250)] )
gman.add_display(PicoGraphics, class_kwargs=dict(display=DISPLAY_PICO_DISPLAY_2,
                                   rotate=0,
                                   pen_type=PEN_P4))

## Add the varying objects you wish to display:
## Adding a Plugin
# All plugins accept 3 positional arguments, graphicmanager instance, A position tuple, and a size tuple.
# The gman instance is used to call the varying draw methods to render the object onto the display
# The position tuple (X,Y) defines the upper left corner of the gauge, or the center of a radial gauge.
# The size tuple (width, height) defines the size of the gauge, or the radius,direction for a radial gauge.
# Each gauge can be added in two ways, eather by first creating the gauge instance and pass that instance to
# the graphics manager, or by passing the class instancing as argument.


gman.add_plugin("funkyClock", "funky_clock", ((260, 65), (135, 0)))

# Adding a simple text box plugin:
gman.add_plugin("myPlugin","text_box",((120,190),(200,50)))

# Adding some linear gauges:
gman.add_plugin("linGaugehori1", "linear_gauge", ((10,230),(90,15)),direction=0)
gman.add_plugin("linGaugehori2", "linear_gauge", ((10,210),(90,15)),direction=2)
gman.add_plugin("linGaugevert1", "linear_gauge", ((10,190),(90,15)),direction=1)
gman.add_plugin("linGaugevert2", "linear_gauge", ((30,190),(90,15)),direction=3)

gman.add_plugin("radGauge1", "radial_gauge", ((50,90),(70,1)),start_angle=180,stop_angle=90,full_range=False)
gman.add_plugin("radGauge2", "radial_gauge", ((185,90),(70,1)),start_angle=0,stop_angle=-90,full_range=False)


# future update will change this slightly and the above gman.add_object call will change to:
# gman.add_object("gauge_name","LinearGauge",(gman,(10,190),(90,15),direction=1))


# Updating a gauge can be done via the gman.update method:
gman.update("myPlugin","Hello!")
gman.update("linGauge",50)
# To display all the gauges, in the order they were added:
gman.render()

# some values to make a loop do some demo work
gauge_val = 0
gauge_max = 100
gauge_dir = 1
loopCount = 0
stringlist = ["LongerString","str"] 
show_string = 0
while True: # Our main loop
    # Modify the value to be displayed
    gauge_val += gauge_dir
    if gauge_val >= gauge_max:
        gauge_dir = -gauge_dir
        gauge_val = gauge_max
    elif gauge_val <= 0:
        gauge_dir = -gauge_dir
        gauge_val = 0
    # Update the gauges with the same value
    gman.update("some_bogus_name",gauge_val) # you will not get a error if the provided name string is not found.
    gman.update("linGaugehori1",gauge_val)
    gman.update("linGaugehori2",gauge_val)
    gman.update("linGaugevert1",gauge_val)
    gman.update("linGaugevert2",gauge_val)
    gman.update("radGauge1",gauge_val)
    gman.update("radGauge2",gauge_val)
    # Call the render method to show the results:
    gman.render()
    
    loopCount +=1
    if loopCount > 50: # only update text every so often..
        gman.update("myPlugin",stringlist[show_string])
        if show_string == 0:
            show_string = 1
        else:
            show_string = 0
        loopCount = 0