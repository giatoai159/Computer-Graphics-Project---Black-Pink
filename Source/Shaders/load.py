from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from Globals import vertex_shader_code, fragment_shader_code

program = None


def compile_shader():
    global program
    program = compileProgram(compileShader(vertex_shader_code.read(), GL_VERTEX_SHADER),
                             compileShader(fragment_shader_code.read(), GL_FRAGMENT_SHADER))
