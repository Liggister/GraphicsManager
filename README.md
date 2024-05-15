# GraphicsManager
[git](https://github.com/Liggister/GraphicsManager.git)
### Authors comments
It always seems to me that 80% of my projects is setting up the graphics side of it, and it tends to become a bit of a spagetti-code.
So i wrote GraphicsManager, to handle the graphics side of {insert your project name here}, allowing you to focus on the fun side of your programming project.

There is a discord server for this project; [Liggister_Discord](https://discord.gg/wFsTng5VNE)

This is a work-in-process and is offered as is, beware dragons ahead!
#### A brief thank you to our contributers, your contribution is unvaluable!
* [Ahnlak](https://github.com/ahnlak) Beta-tester, Licensing-guru

## Deploying GraphicsManager
You will need a Raspberry Pico (or a compatible board) loaded with Pimoroni Micropython UF2-file, check the Pimoroni readme for instructions.
 https://github.com/pimoroni/pimoroni-pico?tab=readme-ov-file#micropython

Installing the graphics_manager on the pico is as simple as copying the "graphics_manager" folder to your pico by using thonny IDE for instance.
Its important that this folder is placed directly into the "root" of your Pico, so the path of the folder is exactly "/graphics_manager/..." and not "/somefolder/graphics_manager/..."

Inside the graphics_manager folder you will find a "graphics_manager_demo.py" file that you should be able to run as-is after you copied the 
You may need to adjust the parameters for your display, so start by getting your display working by following the apropriate guide, then use all of the parameters you used to create your display=PicoGraphics instance to create the internal display instance in the GraphicsManager class.
The graphics_manager_demo.py file is probably quite helpful in demonstrating how to use this package.

## Using GraphicsManager
#### Creating the instance
To use this package in your own project, you must first import the package and create a GraphicsManager instance:
```python
from graphics_manager import GraphicsManager, plugins
gman = GraphicsManager()
```
#### Adding Display
Adding the GraphicsManager alone is meaningless as it has no display or objects to be rendered onto the display.
We create a instance of the PicoGraphics class inside the GraphicsManager instance, "gman":
```python
gman.add_display(PicoGraphics, class_kwargs=dict(display=DISPLAY_PICO_DISPLAY_2, rotate=0, pen_type=PEN_P4) )
```
The add_display step is designed to take the same init arguments as you would normally use to create your display=PicoGraphics instance, so make sure that your selected display, rotation and pen_type is configured for your device.
#### Adding Plugins
Adding graphical objects as plugins:
```python
gman.add_plugin("my_textbox","text_box",((120,190),(200,50)))
```
To break it down a bit, the add_plugin method takes 3 parameters, name, plugin name, the gague position and size as well as optional keyword parameters.
```python #pseudo-code:
gman.add_plugin(
    name, # string; your provided name for the object, will be used to reference that particular object.
    plugin_name, # the name of the plugin you wish to add.
        ( position=tuple(x,y), size=tuple(width,height), kwargs)
```
The object_parameters must always pass two tuples; position & size, and may have optional keyword arguments.
##### Gauges
The package includes 2 gauges, a linear gauge and a radial gauge.
All gauges have a update method that accepts a new value to update the gauge indicator position, and they do offer a way to configure how large value is to be expected.
By providing the optional keyword "max_value" and/or "min_value" when creating the gauge instance, you can configure both ends.
If i for instance wish to create a "battery_level_gauge", i may only wish to display values between 3.7V and 4.4V, so when the battery is at 3.7V, the gauge reads zero.

##### Radial Gauge and Funky Clock Plugin Exceptions
All the plugins use the same parameters, but radial gauge and clock handles them differently.
For all the other plugins, position is used to define the upper left corner of the graphical object, 
while the radial gauge and clock handles position as the center of rotation, the middle of the clock.

The size tuple is always width(x),height(y), except for the radial gauge and clock, where width is the radius of the gauge/clock, 
height inverts the sense of direction for the gauge indicator needle, moving the zero mark to the other end of the gauge.
The radial gauge also offers keywords for setting starting and ending angles, to define the sweep area of the gauge indicator needle and more:
```python
gman.add_plugin("my_radial_gauge","radial_gauge",((185,90),(70,1)),start_angle=0,stop_angle=-90,full_range=False,min_value=0,max_value=100))
```
The above code snippet will add a radial gauge at X=185,y=90, with the radius of 70.
The starting angle is defined as 0, meaning zero value should point straight up, stop angle is defined as -90, so the gauge will sweep counterclockwize to "straight to the left" but since size[1] == 1, the gauge will be inverted, starting from the ending angle and sweeping to the starting angle.
The full_range of the gauge is configured to be False as default, so omitting the "full_range=False" would result in the exact same behaviour.
But if the full_range is set to True, then the Zero value of the gauge is placed in the center, showing the positive and negative values on each side of the middle.

#### Updating the gauges and Rendering
The GraphicsManager offers two methods to be called from your main program loop.
```python
gman.update("my_textbox","Hello!") # object_name must be string, new_value type depends on the object.
gman.update("my_radial_gauge",52) # object_name must be string, new_value type depends on the object.
while True:
    gman.render() # This method will call all the object.render methods in the same order they were added.
```

