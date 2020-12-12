import pygame
from Globals import *
from OpenGL.GL import *
import numpy as np


class Pipe:
    def __init__(self, x, y, width, height, is_upside_down):
        # Pipe position
        self.x = x
        self.y = y
        # Pipe size
        self.width = width
        self.height = height
        self.is_upside_down = is_upside_down
        mod_x = self.x * 2 / display[0]
        mod_y = self.y * 2 / display[1]
        mod_width = self.width / display[0]
        mod_height = self.height / display[1]

        self.image = pygame.image.load("Textures/pipe.png")
        # Background position data
        if self.is_upside_down is True:
            self.y = self.y + pipe_gap
            self.pos_data = [
                -mod_width + mod_x, -mod_height + mod_y + pipe_gap*2/display[1], 0,  # Bottom left
                mod_width + mod_x, -mod_height + mod_y + pipe_gap*2/display[1], 0,  # Bottom right
                mod_width + mod_x, mod_height + mod_y + pipe_gap*2/display[1], 0,  # Top right
                -mod_width + mod_x, mod_height + mod_y + pipe_gap*2/display[1], 0  # Top left
            ]
        else:
            self.y = self.y - pipe_gap
            self.pos_data = [
                -mod_width + mod_x, -mod_height + mod_y - pipe_gap*2/display[1], 0,  # Bottom left
                mod_width + mod_x, -mod_height + mod_y - pipe_gap*2/display[1], 0,  # Bottom right
                mod_width + mod_x, mod_height + mod_y - pipe_gap*2/display[1], 0,  # Top right
                -mod_width + mod_x, mod_height + mod_y - pipe_gap*2/display[1], 0  # Top left
            ]
        self.pos_data = np.array(self.pos_data, dtype=np.float32)
        # Background self.texture data
        if self.is_upside_down is True:
            self.tex_coord_data = [
                0.0, 1.0,  # Bottom left
                1.0, 1.0,  # Bottom right
                1.0, 0.0,  # Top right
                0.0, 0.0  # Top left
            ]
        else:
            self.tex_coord_data = [
                0.0, 0.0,  # Bottom left
                1.0, 0.0,  # Bottom right
                1.0, 1.0,  # Top right
                0.0, 1.0  # Top left
            ]

        self.tex_coord_data = np.array(self.tex_coord_data, dtype=np.float32)
        # Generate VAO and bind
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        # Generate 2 VBOs
        self.vbo = glGenBuffers(2)
        # Position processing
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
        glBufferData(GL_ARRAY_BUFFER, self.pos_data.nbytes, self.pos_data, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        # Texture coordinates processing
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
        glBufferData(GL_ARRAY_BUFFER, self.tex_coord_data.nbytes, self.tex_coord_data, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
        # Texture binding to current vbo
        self.texture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        texture_width = self.image.get_width()
        texture_height = self.image.get_height()

        texture_data = pygame.image.tostring(self.image, "RGBA", True)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_width, texture_height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        # Texture Wrapping
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
        # Texture filtering
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, 4)
        glBindVertexArray(0)

    def move(self, vel_x):
        self.x += vel_x
        vel_x = vel_x * 2 / display[0]
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
        if vel_x != 0:
            self.pos_data[0] += vel_x
            self.pos_data[3] += vel_x
            self.pos_data[6] += vel_x
            self.pos_data[9] += vel_x
        glBufferData(GL_ARRAY_BUFFER, self.pos_data.nbytes, self.pos_data, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def scrolling(self):
        ground_scroll = 0
        ground_scroll -= scroll_speed
        self.move(ground_scroll)

