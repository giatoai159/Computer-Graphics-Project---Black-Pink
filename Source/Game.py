import pygame
import Shaders.load as shader
from OpenGL.GL import *
from pygame.locals import *
from Globals import *
from Player import Player
from Scene import Scene


class Game:
    def __init__(self, game_name, icon=None):
        self.game_name = game_name
        self.icon = icon
        self.timer = pygame.time.Clock()
        self.is_running = True
        # Game variables
        self.flying = False
        self.game_over = False
        # PyGame Initialization
        pygame.init()
        while not pygame.get_init():
            print("PyGame Initialization Failed.")

        self.game_window = pygame.display.set_mode((display[0], display[1]), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(self.game_name)
        glViewport(0, 0, display[0], display[1])
        # pygame.display.set_icon(pygame.image.load(self.icon))
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glClearColor(1, 1, 1, 1)
        shader.compile_shader()

    def loop(self):
        player = Player(0, 0, 51, 36)
        bg = Scene("Textures/bg.png")
        # platform_1 = Platform(-200, -325, 300, 70)
        while self.is_running:
            self.timer.tick(60)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.is_running = False
                if event.type == KEYDOWN:
                    if event.key == K_UP and self.flying is False and self.game_over is False:
                        self.flying = True
            player.move_handling(self.flying, self.game_over)
            # mouse = pygame.mouse.get_pos()
            # print(mouse[0]-640, mouse[1]-360) # Print mouse position with OpenGL Oxy base (0, 0)
            # print("Colliding: ", check_collision(player, platform_1))
            glUseProgram(shader.program)
            bg.draw()
            player.draw()
            glUseProgram(0)
            pygame.display.flip()


def check_collision(player, collided_object):
    collision_x = player.x + player.width / 2 >= collided_object.x - collided_object.width / 2 and collided_object.x + collided_object.width / 2 >= player.x - player.width / 2
    collision_y = player.y + player.height / 2 >= collided_object.y - collided_object.height / 2 and collided_object.y + collided_object.height / 2 >= player.y - player.height / 2
    return collision_x and collision_y
"""
class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(2)

        mod_x = self.x * 2 / display[0]
        mod_y = self.y * 2 / display[1]
        mod_width = self.width / display[0]
        mod_height = self.height / display[1]

        self.pos_data = [
            -mod_width + mod_x, -mod_height + mod_y, 0,
            mod_width + mod_x, -mod_height + mod_y, 0,
            mod_width + mod_x, mod_height + mod_y, 0,
            -mod_width + mod_x, mod_height + mod_y, 0
        ]
        self.pos_data = np.array(self.pos_data, dtype=np.float32)

        self.color_data = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
            1.0, 0.0, 1.0
        ]
        self.color_data = np.array(self.color_data, dtype=np.float32)

        glBindVertexArray(self.vao)

        # Position processing
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
        glBufferData(GL_ARRAY_BUFFER, self.pos_data.nbytes, self.pos_data, GL_DYNAMIC_DRAW)

        platform_pos = glGetAttribLocation(shader.program, 'aPos')
        glVertexAttribPointer(platform_pos, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        # Color processing

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
        glBufferData(GL_ARRAY_BUFFER, self.color_data.nbytes, self.color_data, GL_STATIC_DRAW)

        platform_color = glGetAttribLocation(shader.program, 'aColor')
        glVertexAttribPointer(platform_color, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def render_platform(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, 4)
        glBindVertexArray(0)

"""



