""" Copyright (cc) 2024, developer@liggist.se. Read the licence.txt file for details."""
class GraphicsManager:
    def __init__(self,**kwargs):
        """ Initialize the graphics manager instance.
        Keyword arguments:
        colors -- A list of colors to use for the pallette, in order: black, background,frame, indicator, extras...
        """
        self.version = 1,2,0,1
        self.display = None
        self.plugins = {
            "text_box": "text_box",
            "linear_gauge": "linear_gauge",
            "radial_gauge": "radial_gauge",
            "funky_clock": "funky_clock"
        }
        self.loaded_plugins = {}  # Dictionary to hold loaded plugin classes
        # pallette color index = [ black (for clearing screen), gauge background, guage frame, text & indicator color, extras...
        self.palette_values = kwargs.get("colors", [ (0,0,0),(10,10,90),(220,5,180),(250,200,255),(180,160,250),(255,160,160), (127,127,127), (255,0,0), (127,255,255) ] )
        self.palette = []
        self.objects = {}
        self.draw_rect = None
        self.draw_circ = None
        self.draw_text = None
        self.draw_text_len = None
        self.draw_ngon = None
        self.select_color = None
        self.create_color = None
        self.print_GM_version()
    
    def print_GM_version(self):
        """Print the version of the GraphicsManager class."""
        print("{} version {}.{}.{}.{} loaded.".format(self.__class__.__name__,*self.version))
    
    
    def add_display(self,DisplayClass,*args,**kwargs)->bool:
        """ Adds a display to the graphics manager.
        args: display class name
        kwargs:
            class_args: arguments to pass to the display class
            class_kwargs: keyword arguments to pass to the display class.
        """
        success = False
        class_args = kwargs.get("class_args",None)
        class_kwargs = kwargs.get("class_kwargs",None)
        try:
            if class_args != None and class_kwargs != None:
                self.display = DisplayClass(*class_args,**class_kwargs)
                #self.display.__init__(*class_args,**class_kwargs)
            elif class_kwargs != None:
                self.display = DisplayClass(**class_kwargs)
            if "colors" in kwargs:
                if len(self.palette) < 1:
                    colors = kwargs.get("colors", None)
                    self.palette_values = colors
                    for color in colors:
                        if self.create_color == None:
                            self.palette.append(self.display.create_pen(*color))
            elif len(self.palette_values) > 1 and len(self.palette) < 1:
                for color in self.palette_values:
                    self.palette.append(self.display.create_pen(*color))
            else:
                print("No colors were added!!!")
            success = True
        except IndexError:
            print("out of range!")
        if success:
            self.create_color = self.display.create_pen
            self.select_color = self.display.set_pen
            self.draw_circ = self.display.circle
            self.draw_ngon = self.display.polygon
            self.draw_rect = self.display.rectangle
            self.draw_text = self.display.text
            self.draw_text_len = self.display.measure_text
        return success
    
    def add_plugin(self, name, plugin_name, plugin_args, **kwargs):
        """Adds a plugin to the GraphicsManager.
        Parameters:
        name -- The name of the instance of the added plugin. Must be unique.
        plugin_name -- The name of the plugin to load.
        plugin_args -- Arguments to pass to the plugin class.
        kwargs -- Keyword arguments to pass to the plugin class.
        """
        if plugin_name in self.plugins:
            plugin_filename = self.plugins[plugin_name]
            if plugin_filename not in self.loaded_plugins:
                try:
                    # Import the plugin class from the module
                    if plugin_filename == "text_box":
                        from graphics_manager.plugins import TextBoxPlugin
                        plugin_class = TextBoxPlugin
                    elif plugin_filename == "linear_gauge":
                        from graphics_manager.plugins import LinearGaugePlugin
                        plugin_class = LinearGaugePlugin
                    elif plugin_filename == "radial_gauge":
                        from graphics_manager.plugins import RadialGaugePlugin
                        plugin_class = RadialGaugePlugin
                    elif plugin_filename == "funky_clock":
                        from graphics_manager.plugins import FunkyClockPlugin
                        plugin_class = FunkyClockPlugin
                    else:
                        print(f"Plugin '{plugin_filename}' not found.")
                        return
                    self.loaded_plugins[plugin_filename] = plugin_class
                except ImportError as e:
                    print(f"Error importing plugin module: {e}")
                    return
            else:
                plugin_class = self.loaded_plugins[plugin_filename]
            # Create an instance of the plugin class with provided arguments
            plugin_instance = plugin_class(self, *plugin_args, **kwargs)
            self.objects[name] = plugin_instance
            self.objects[name].print_version()
        else:
            print(f"Plugin '{plugin_name}' not found in available plugins.")
    
    def add_object(self,name,obj,**kwargs): # Add plugin instances
        """deprecated, use add_plugin() instead"""
        self.objects[name] = obj
        self.objects[name].print_version()
    
    def update(self, name, value): # Update the gauge, referenced by name.
        """Sets new value for the plugin instance.
        parameters:
        name -- The name of the instance of the plugin to update.
        value -- The new value to set.
        """
        for obj in self.objects:
            if obj == name:
                self.objects[name].update(value)
    
    def render(self): # Render all the objects onto the display. Clears and updates the display object.
        """ draws all the objects on the display. """
        if self.display != None:
            self.display.set_pen(self.palette[0])
            self.display.clear()
            for obj in self.objects:
                self.objects[obj].render()
            
            self.display.update()
        else:
            print("No display yet!")
