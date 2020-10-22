import pygame
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from pygame.locals import *
import glm
display = (1280, 720)
icon = ""
name = "Test"
timer = pygame.time.Clock()

shader_program = None


# Creating a vertex shader
vertex_shader_code = """
#version 330

layout (location = 0) in vec3 pos;
layout (location = 1) in vec3 color;

out vec3 newColor;

void main()
{
    gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
    newColor = color;
}
"""

fragment_shader_code = """
#version 330

in vec3 newColor;
out vec4 outColor;

void main()
{
    outColor = vec4(newColor.x, newColor.y, newColor.z, 1.0);
}
"""


def shader_compile():
    global shader_program
    shader_program = compileProgram(compileShader(vertex_shader_code, GL_VERTEX_SHADER),
                                    compileShader(fragment_shader_code, GL_FRAGMENT_SHADER))


class Rectangle:
    # vao = glGenVertexArrays(1)
    def __init__(self, x, y, vao=None, vbo=None, size=1, pos_data=None, color_data=None):
        self.x = x
        self.y = y
        self.size = size
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(2)

        mod_x = self.x*2/display[0]
        mod_y = self.y*2/display[1]

        self.pos_data = [
            -0.027+mod_x, -0.05+mod_y, 0,
            0.027+mod_x, -0.05+mod_y, 0,
            0.027+mod_x, 0.05+mod_y, 0,
            -0.027+mod_x, 0.05+mod_y, 0
        ]
        self.pos_data = np.array(self.pos_data, dtype=np.float32)
        self.pos_data = self.size * self.pos_data

        self.color_data = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
            1.0, 0.0, 1.0
        ]
        self.color_data = np.array(self.color_data, dtype=np.float32)

    def create_rectangle(self):
        glBindVertexArray(self.vao)

        # Position processing
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
        glBufferData(GL_ARRAY_BUFFER, self.pos_data.nbytes, self.pos_data, GL_DYNAMIC_DRAW)

        rectangle_pos = glGetAttribLocation(shader_program, 'pos')
        glVertexAttribPointer(rectangle_pos, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        # Color processing
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
        glBufferData(GL_ARRAY_BUFFER, self.color_data.nbytes, self.color_data, GL_STATIC_DRAW)

        rectangle_color = glGetAttribLocation(shader_program, 'color')
        glVertexAttribPointer(rectangle_color, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render_rectangle(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, 4)
        glBindVertexArray(0)

    def move(self, vel_x, vel_y):
        self.x += vel_x
        self.y += vel_y
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
        vel_x = vel_x*2/display[0]
        vel_y = vel_y*2/display[1]
        self.pos_data[0] += vel_x
        self.pos_data[3] += vel_x
        self.pos_data[6] += vel_x
        self.pos_data[9] += vel_x
        self.pos_data[1] += vel_y
        self.pos_data[4] += vel_y
        self.pos_data[7] += vel_y
        self.pos_data[10] += vel_y
        glBufferData(GL_ARRAY_BUFFER, self.pos_data.nbytes, self.pos_data, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


def quit_game():
    pygame.quit()
    sys.exit()


def main():
    # PyGame Initialization
    pygame.init()
    while not pygame.get_init():
        print("PyGame Initialization Failed.")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.RESIZABLE)  # Set game width and height
    pygame.display.set_caption(name)  # Set game title
    # _icon = pygame.image.load(icon)  # Load icon
    # pygame.display.set_icon(_icon)  # Set game icon
    glViewport(0, 0, display[0], display[1])

    # Game variables
    x_velocity = 10
    is_jump = False
    jump_count = 10
    shader_compile()

    rect = Rectangle(500, -340)
    rect.create_rectangle()

    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1, 1, 1, 1)
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT] and rect.x < (display[0]/2)-20:
            rect.move(x_velocity, 0)
        if keys[K_LEFT] and rect.x > -((display[0]/2)-20):
            rect.move(-x_velocity, 0)
        if not is_jump:

            if keys[K_SPACE] or keys[K_UP]:
                is_jump = True
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                rect.move(0, (jump_count**2)*0.5*neg)
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 10

        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == VIDEORESIZE:
                glViewport(0, 0, event.w, event.h)

        glUseProgram(shader_program)
        rect.render_rectangle()
        glUseProgram(0)
        pygame.display.flip()  # = glfw.swap_buffers(window)
        timer.tick(60)


if __name__ == '__main__':
    main()

pygame.quit()
