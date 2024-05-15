""" Copyright (cc) 2024, developer@liggist.se. Read the licence.txt file for details."""
from graphics_manager.plugins import GM_Plugin, BoundingBox
import machine
import time
import math


class FunkyClockPlugin(GM_Plugin):
    def __init__(self, graphics_manager, position, size, **kwargs):
        super().__init__(graphics_manager, position, size)
        self.version = (1,0,0,1)
        self.size = size[0]
        self.radius = int(self.size / 2)
        self.x = position[0]
        self.y = position[1]
        self.lastSecond = 0
        self.lastSecEvent = 0
    
    def getClock(self):
        timestamp = machine.RTC().datetime()
        cHour = timestamp[4]
        cMinute = timestamp[5]
        cSecond = timestamp[6]
        if cSecond != self.lastSecond:
            self.lastSecond = cSecond
            self.lastSecEvent = time.ticks_ms()
        cMillis = time.ticks_ms() - self.lastSecEvent
        return cHour, cMinute, cSecond, cMillis

    def getAngles(self, hour, minute, second, millis):
        hourAngle = int((hour * 30) + (minute * 0.5))
        minuteAngle = int((minute * 6) + (second * 0.1))
        secondAngle = int(second * 6) + (millis * 0.006)
        deciSecAngle = int((millis/100) * 36)
        return hourAngle, minuteAngle, secondAngle, deciSecAngle

    def rotate(self, origin, point, radangle):
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(radangle) * (px - ox) - math.sin(radangle) * (py - oy)
        qy = oy + math.sin(radangle) * (px - ox) + math.cos(radangle) * (py - oy)
        return int(qx), int(qy)

    def drawFace(self, frame):
        r = self.radius
        markStep = int(self.size / 50)
        markerShape = [(self.x+(r*0.96),self.y),(self.x+(r*0.94),self.y+markStep),(self.x+(r*0.90),self.y+markStep+markStep),(self.x+(r*0.85),self.y),(self.x+(r*0.90),self.y-markStep-markStep),(self.x+(r*0.94),self.y-markStep)]
        marker = []
        #render clock face:
        self.graphics_manager.select_color(0) # behind-the-clock-color
        self.graphics_manager.draw_circ(self.x, self.y, r) # black circle
        if frame:
            self.graphics_manager.select_color(2) # clock frame color
            self.graphics_manager.draw_circ(self.x, self.y, r-markStep) # outer frame
            self.graphics_manager.select_color(1) # clock face color
            self.graphics_manager.draw_circ(self.x, self.y, r-int(r/13)) # inner clock face
        # hour and minute markers
        i = 12
        self.graphics_manager.select_color(2) # clock frame color
        while i > 0:
            marker = []
            for point in markerShape: #for item in clockHand:
                pX,pY = point
                oX,oY = self.rotate((self.x,self.y),(pX,pY),math.radians(i*30))
                marker.append( (oX,oY) )
            self._render(2, marker)
            i -= 1

    def drawHand(self, angle, length, width):
        clockHand = [(0,-7),(2,-8),(16,-20),(4,-28),(7,-35),(10,-36),(0,-45),(-10,-36),(-5,-35),(-1,-28),(7,-20),(-2,-8)]
        chShadow = [(0,-5),(4,-7),(18,-19),(6,-27),(9,-35),(12,-38),(2,-47),(-8,-34),(-3,-33),(1,-26),(9,-18),(1,-5)]
        rotGon = []
        rotGonShadow = []
        if length <= 0: length = 1
        if width <= 0: width = 1
        
        for item in clockHand:
            iX = int(item[0] * width) + self.x
            iY = int(item[1] * length) + self.y
            oX = 0
            oY = 0
            if angle:
                oX,oY = self.rotate((self.x,self.y),(iX,iY),math.radians(angle))
            else:
                oX = iX
                oY = iY
            rotGon.append((oX,oY))
        
        for item in chShadow:
            iX = int(item[0] * width) + self.x
            iY = int(item[1] * length) + self.y
            oX = 0
            oY = 0
            if angle:
                oX,oY = self.rotate((self.x,self.y),(iX,iY),math.radians(angle))
            else:
                oX = iX
                oY = iY
            rotGonShadow.append((oX,oY))
        
        self._render(1, rotGonShadow)
        self._render(3, rotGon)
    
    def render(self):
        self.funkyClock()
    
    def _render(self, color, ngon):
        self.graphics_manager.select_color(self.graphics_manager.palette[color])
        self.graphics_manager.draw_ngon(ngon)

    def funkyClock(self):
        self.drawFace(True)
        hA, mA, sA, miA = self.getAngles(*self.getClock())
        self.drawHand(hA, self.size*0.007, self.size*0.005)
        self.drawHand(mA, self.size*0.009, self.size*0.003)
        self.drawHand(sA, self.size*0.01, self.size*0.0015)
