""" Copyright (cc) 2024, developer@liggist.se. Read the licence.txt file for details."""
# File Version 1,0,0
from .gm_plugin import GM_Plugin,BoundingBox # <- GM_Plugin is plugin-base, BoundingBox is a named tuple.
from .text_box import TextBoxPlugin # <- Text field plugin
from .linear_gauge import LinearGaugePlugin # <- Linear gauge plugin
from .radial_gauge import RadialGaugePlugin # <- Radial gauge plugin
from .funky_clock import FunkyClockPlugin # <- Analog Clock