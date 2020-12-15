import numpy as np
import pygame
import glm
from OpenGL.GL import *
from Globals import *
from pygame.locals import *


class Player:
    def __init__(self, x, y, width, height):
        # Player position
        self.x = x
        self.y = y
        # Player rotation
        self.angle = 0.0 # Degree
        # Player size
        self.width = width
        self.height = height
        # Movement handling
        self.playing = False
        self.is_jump = False
        self.velocity = 0
        self.counter = 0
        # Player texture
        self.index = 0
        self.images = []
        for num in range(1, 4):
            img = pygame.image.load(f"Textures/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        # Modify input coordinates to put OpenGL coordinate system which is from -1 to 1
        mod_x = self.x * 2 / display[0]
        mod_y = self.y * 2 / display[1]
        mod_width = self.width / display[0]
        mod_height = self.height / display[1]
        # Player position data
        self.pos_data = [
            -mod_width + mod_x, -mod_height + mod_y, 0,  # Bottom left
            mod_width + mod_x, -mod_height + mod_y, 0,  # Bottom right
            mod_width + mod_x, mod_height + mod_y, 0,  # Top right
            -mod_width + mod_x, mod_height + mod_y, 0  # Top left
        ]
        self.pos_data = np.array(self.pos_data, dtype=np.float32)  # Convert to numpy array
        # Player texture data
        self.tex_coord_data = [
            0.0, 0.0,  # Bottom left
            1.0, 0.0,  # Bottom right
            1.0, 1.0,  # Top right
            0.0, 1.0,  # Top left
        ]
        self.tex_coord_data = np.array(self.tex_coord_data, dtype=np.float32)  # Convert to numpy array
        # Generate a vertex array object for player
        self.vao = glGenVertexArrays(1)
        # And bind the vertex array
        glBindVertexArray(self.vao)
        # Generate a vertex buffer object for the VAO
        self.vbo = glGenBuffers(2)  # Generate 2, one for position data, one for texture data
        # Position processing
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
        glBufferData(GL_ARRAY_BUFFER, self.pos_data.nbytes, self.pos_data, GL_DYNAMIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        # Texture processing
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
        glBufferData(GL_ARRAY_BUFFER, self.tex_coord_data.nbytes, self.tex_coord_data, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
        # Texture binding to the current VBO
        self.texture = glGenTextures(3)
        for i in range(0,3):

            glBindTexture(GL_TEXTURE_2D, self.texture[i])

            texture_width = self.images[i].get_width()  # Get texture width
            texture_height = self.images[i].get_height()  # Get texture height

            texture_data = pygame.image.tostring(self.images[i], "RGBA", True)  # Get image data to a string

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
        self.rotate(self.angle)
        glBindTexture(GL_TEXTURE_2D, self.texture[self.index])
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, 4)
        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.rotate(-self.angle)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        dx = dx * 2 / display[0]
        dy = dy * 2 / display[1]
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])

        if dx != 0:
            self.pos_data[0] += dx
            self.pos_data[3] += dx
            self.pos_data[6] += dx
            self.pos_data[9] += dx
        if dy != 0:
            self.pos_data[1] += dy
            self.pos_data[4] += dy
            self.pos_data[7] += dy
            self.pos_data[10] += dy

        glBufferData(GL_ARRAY_BUFFER, self.pos_data.nbytes, self.pos_data, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    # Params:
    #   Deg: specify the angle that the bird is pointing to
    def rotate(self, deltaDegree):  # WIP
        if deltaDegree == 0:
            return

        dx = self.x * 2 / display[0]
        dy = self.y * 2 / display[1]
        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(dx, dy, 0))
        transform = glm.rotate(transform, glm.radians(deltaDegree), glm.vec3(0.0, 0.0, 1.0))
        transform = glm.translate(transform, glm.vec3(-dx, -dy, 0))

        xy1 = glm.vec4(self.pos_data[0], self.pos_data[1], 0, 1)
        xy2 = glm.vec4(self.pos_data[3], self.pos_data[4], 0, 1)
        xy3 = glm.vec4(self.pos_data[6], self.pos_data[7], 0, 1)
        xy4 = glm.vec4(self.pos_data[9], self.pos_data[10], 0, 1)
        res_xy1 = transform * xy1
        res_xy2 = transform * xy2
        res_xy3 = transform * xy3
        res_xy4 = transform * xy4
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])

        self.pos_data[0] = res_xy1[0]
        self.pos_data[1] = res_xy1[1]
        self.pos_data[3] = res_xy2[0]
        self.pos_data[4] = res_xy2[1]
        self.pos_data[6] = res_xy3[0]
        self.pos_data[7] = res_xy3[1]
        self.pos_data[9] = res_xy4[0]
        self.pos_data[10] = res_xy4[1]

        glBufferData(GL_ARRAY_BUFFER, self.pos_data.nbytes, self.pos_data, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def move_handling(self, flying, game_over, flap_sound):
        jump = False

        if flying is True:
            jump = pygame.mouse.get_pressed(3)[0] | pygame.key.get_pressed()[K_UP]
            self.velocity -= gravity_speed
            if self.velocity < gravity:
                self.velocity = -gravity
            if self.y > -270:
                self.move(0, self.velocity)
            self.angle = self.velocity * 1.1

        if game_over is False:
            if jump and self.is_jump is False:
                self.is_jump = True
                self.velocity = jump_height
                self.move(0, self.velocity)
                flap_sound.play()
            if not jump:
                self.is_jump = False
            # Animation handling
            self.counter += 1
            if self.counter > 5:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
