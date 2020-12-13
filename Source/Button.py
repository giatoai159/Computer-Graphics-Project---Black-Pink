import pygame
from Globals import *
from OpenGL.GL import *
import numpy as np


class Button:
    def __init__(self, x, y, path_texture):
        self.image = pygame.image.load(path_texture)

        self.active = True

        # Position
        self.x = x
        self.y = y

        mod_x = self.x * 2 / display[0]
        mod_y = self.y * 2 / display[1]
        mod_width = self.image.get_width() / display[0]
        mod_height = self.image.get_height() / display[1]

        # Background position data
        self.pos_data = [
            -mod_width + mod_x, -mod_height + mod_y, 0,  # Bottom left
            mod_width + mod_x, -mod_height + mod_y, 0,  # Bottom right
            mod_width + mod_x, mod_height + mod_y, 0,  # Top right
            -mod_width + mod_x, mod_height + mod_y, 0  # Top left
        ]
        self.pos_data = np.array(self.pos_data, dtype=np.float32)
        # Background self.texture data
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

        # Texture filtering
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)


    def draw(self):
        if not self.active:
            return

        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, 4)
        glBindVertexArray(0)

    def isHovered(self):
        if not self.active:
            return False

        width = self.image.get_width()
        height = self.image.get_height()
        top = display[1] / 2 - self.y - height / 2
        left = self.x - width / 2 + display[0] / 2

        rect = pygame.rect.Rect(left, top, width, height)
        return rect.collidepoint(pygame.mouse.get_pos())


