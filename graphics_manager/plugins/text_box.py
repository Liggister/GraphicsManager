""" Copyright (cc) 2024, developer@liggist.se. Read the licence.txt file for details."""
from graphics_manager.plugins import GM_Plugin, BoundingBox

class TextBoxPlugin(GM_Plugin):
    def __init__(self, graphics_manager,position,size,**kwargs):
        """ Text box plugin constructor.
        :param graphics_manager: The graphics manager instance.
        :param position: The position of the text box, (x,y), marking the upper left corner of the text box.
        :param size: The size of the text box, (width,height).
        kwargs: Additional keyword arguments:
        textscale: The scale of the text. Will be overridden by the automatic text scaling inside the plugin.
        """
        super().__init__(graphics_manager,position,size)
        self.version = (1,0,0,6)
        self.value = ""
        self.text_scale = kwargs.get("textscale",4)
        self.bounding_box = BoundingBox(
            left=position[0],
            right=position[0]+size[0],
            top=position[1],
            bottom=position[1]+size[1]
            )
    
    def render(self):
        """ Renders the text box to the display."""
        frame_width = 4
        if self.new_value:
            text_s1_len = self.graphics_manager.draw_text_len(str(self.value),1)
            text_space = (self.bounding_box.right - self.bounding_box.left) - (frame_width + frame_width + 10)
            self.text_scale = int(text_space/text_s1_len)
            text_len = self.graphics_manager.draw_text_len(str(self.value),self.text_scale)
            attempt_counter = 0
            wrong_size = False
            if text_len <= (self.bounding_box.right - self.bounding_box.left) - (5 + frame_width + frame_width):
                wrong_size = True
            if text_len >= (self.bounding_box.right - self.bounding_box.left) - (frame_width + frame_width):
                wrong_size = True
            text_height = self.text_scale * 8
            if text_height >= (self.bounding_box.bottom - self.bounding_box.top) - (5 + frame_width + frame_width):
                wrong_size = True
            if wrong_size:
                print("Wrong size!")
            no_bigger = False
            while wrong_size:
                wrong_size = False
                text_height = self.text_scale * 8
                text_len = self.graphics_manager.draw_text_len(str(self.value),self.text_scale)
                if text_height >= (self.bounding_box.bottom - self.bounding_box.top) - ( frame_width + frame_width):
                    wrong_size = True
                    print("to high")
                    self.text_scale = int( ( (self.bounding_box.bottom - self.bounding_box.top) - (2 + frame_width + frame_width) ) / 8)
                        
                    no_bigger = True
                elif text_len <= (self.bounding_box.right - self.bounding_box.left) - (20 + frame_width + frame_width):
                    if no_bigger == False:
                        wrong_size = True
                        print("+")
                        self.text_scale += 1
                elif text_len >= (self.bounding_box.right - self.bounding_box.left) - 5:
                    wrong_size = True
                    print("-")
                    self.text_scale -= 1
                attempt_counter +=1
                if self.text_scale <= 2 or self.text_scale >= 6:
                    print("counter:{}, scale:{}.".format(attempt_counter, self.text_scale))
                    break
                if attempt_counter >= 10:
                    print("!")
                    break
            self.new_value = False
            # print("text len={}, scale= {}.".format(text_len,self.text_scale))
        # Render the value in a box/frame
        _char_height = 10
        start_x = self.bounding_box.left
        start_y = self.bounding_box.top
        width = self.bounding_box.right - self.bounding_box.left
        height = self.bounding_box.bottom - self.bounding_box.top
        # Draw the Frame first:
        self.graphics_manager.select_color(self.graphics_manager.palette[2])
        self.graphics_manager.draw_rect(start_x,start_y,width,height)
        
        start_x += frame_width
        start_y += frame_width
        width -= frame_width+frame_width
        height -= frame_width+frame_width
        text_len = self.graphics_manager.draw_text_len(str(self.value),scale=self.text_scale)
        text_height = (_char_height * self.text_scale) + (_char_height)
        text_pos_x = start_x + (int(width/2)-int(text_len/2))
        text_pos_y = start_y + ((int(height/2) - int(int(_char_height/3) * self.text_scale)))
        self.graphics_manager.select_color(self.graphics_manager.palette[1])
        self.graphics_manager.draw_rect(start_x,start_y,width,height)  # draw the info-box background
        # self.graphics_manager.select_color(self.graphics_manager.palette[2])
        # self.graphics_manager.draw_text(str(self.value),text_pos_x-2,text_pos_y-4,500,self.text_scale)  # draw text shadow
        self.graphics_manager.select_color(self.graphics_manager.palette[3])
        self.graphics_manager.draw_text(str(self.value),text_pos_x,text_pos_y,500,self.text_scale)  # draw text
     