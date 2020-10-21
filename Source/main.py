import pygame
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from pygame.locals import *

display = (1280, 720)
icon = ""
name = "Test"
timer = pygame.time.Clock()
shader_program = None
VAO = None
VBO = None

# Creating a vertex shader
vertex_shader_code = """
#version 330

layout (location = 0) in vec3 pos;

void main()
{
    gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
}
"""

fragment_shader_code = """
#version 330

out vec4 color;

void main()
{
    color = vec4(1.0, 0.0, 0.0, 1.0);
}
"""


def shader_compile():
    global shader_program

    shader_program = compileProgram(compileShader(vertex_shader_code, GL_VERTEX_SHADER),
                                    compileShader(fragment_shader_code, GL_FRAGMENT_SHADER))


def create_triangle():
    global VAO
    global VBO
    vertices = [
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        0.0, 0.5, 0.0
    ]
    vertices = np.array(vertices, dtype=np.float32)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader_program, 'pos')
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(position)

    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glBindVertexArray(0)


def quit_game():
    pygame.quit()
    sys.exit()


def main():
    # PyGame Initialization
    pygame.init()
    while not pygame.get_init():
        print("PyGame Initialization Failed.")
    game_window = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.RESIZABLE)  # Set game width and height
    pygame.display.set_caption(name)  # Set game title
    # _icon = pygame.image.load(icon)  # Load icon
    # pygame.display.set_icon(_icon)  # Set game icon
    # glViewport(0, 0, display[0], display[1])

    shader_compile()
    create_triangle()

    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1, 1, 1, 1)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == VIDEORESIZE:
                glViewport(0, 0, event.w, event.h)
        glUseProgram(shader_program)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glUseProgram(0)
        glBindVertexArray(0)

        pygame.display.flip()  # = glfw.swap_buffers(window)


if __name__ == '__main__':

    main()

pygame.quit()
