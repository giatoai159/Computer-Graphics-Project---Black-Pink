import Shaders.load as shader
import random
import pygame
from OpenGL.GL import *
from pygame.locals import *
from Globals import *
from Player import Player
from Scene import Scene
from Pipe import Pipe
from Button import Button


class Game:
    def __init__(self, game_name, icon=None):
        self.game_name = game_name
        self.icon = icon
        self.timer = pygame.time.Clock()
        self.is_running = True
        # Game variables
        self.flying = False
        self.game_over = False
        self.score = 0
        self.pass_pipe = False
        # Sound
        pygame.mixer.pre_init(buffer=256)
        pygame.mixer.init()
        self.theme = pygame.mixer.music.load(path_themesong)
        self.flap_sound = pygame.mixer.Sound(path_wingsound)
        self.hit_sound = pygame.mixer.Sound(path_hitsound)
        self.die_sound = pygame.mixer.Sound(path_diesound)
        self.hit_played = False
        self.score_sound = pygame.mixer.Sound(path_scoresound)
        # PyGame Initialization
        pygame.init()
        while not pygame.get_init():
            print("PyGame Initialization Failed.")

        self.game_window = pygame.display.set_mode((display[0], display[1]), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(self.game_name)
        glViewport(0, 0, display[0], display[1])
        # pygame.display.set_icon(pygame.image.load(self.icon))
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(1, 1, 1, 1)
        shader.compile_shader()

    def loop(self):
        pygame.mixer.music.play(-1)

        while self.is_running:
            # HUD
            start_button = Button(0, 30, path_buttonStart)
            ok_button = Button(0, 30, path_buttonOk)
            game_name = Button(0, 250, path_gameName)
            start_text = Button(0, 100, path_textStart)
            end_text = Button(0, 100, path_textEnd)

            # Playground
            player = Player(-150, 0, 51, 36)
            bg = Scene(path_bg, 0, 100, 864, 768)
            ground = Scene(path_ground, 0, -368, 900, 168)
            pipe_group = []
            last_pipe = pygame.time.get_ticks() - pipe_frequency

            restart = False
            self.game_over = False
            self.flying = False
            self.hit_played = False
            game_name.active = True
            start_button.active = True
            start_text.active = True
            end_text.active = False
            ok_button.active = False

            self.score = 0

            # =======
            # In-game
            while (not self.game_over or not restart) and self.is_running:
                # =======
                # Events
                is_flying = False
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.is_running = False

                    if event.type == KEYDOWN:
                        if self.game_over:
                            restart = True

                        is_flying = is_flying | event.key == K_UP

                    if event.type == MOUSEBUTTONDOWN:
                        if self.game_over:
                            restart = ok_button.isHovered()

                        is_flying = is_flying | pygame.mouse.get_pressed(3)[0]
                        is_flying = is_flying & start_button.isHovered()

                if is_flying and not self.flying and not self.game_over:
                    self.flying = True
                    start_button.active = False
                    start_text.active = False
                    game_name.active = False

                # =======================
                # Controller
                player.move_handling(self.flying, self.game_over, self.flap_sound)

                # ==============
                # Pipes handing
                if self.flying is True and self.game_over is False:
                    # Pipe random generation
                    time_now = pygame.time.get_ticks()
                    if time_now - last_pipe > pipe_frequency:
                        pipe_height = random.randint(-150, 250)
                        btm_pipe = Pipe(display[0], pipe_height, 78, 568, False)
                        top_pipe = Pipe(display[0], pipe_height, 78, 568, True)
                        pipe_group.append(btm_pipe)
                        pipe_group.append(top_pipe)
                        last_pipe = time_now
                    # Delete out of screen pipes
                    if pipe_group[0].x < -350:
                        pipe_group.pop(0)
                    # Scrolling pipes
                    for i in range(0, len(pipe_group)):
                        pipe_group[i].scrolling()

                # ================
                # Check collision
                for i in range(0, len(pipe_group)):
                    if check_collision(player, pipe_group[i]):
                        self.game_over = True
                if player.y >= 425:
                    self.game_over = True
                if player.y <= -270:
                    self.game_over = True
                    self.flying = False
                if self.game_over:
                    end_text.active = True
                    ok_button.active = True

                # ============
                # Check score
                if len(pipe_group) > 0:
                    if player.x - player.width / 2 > pipe_group[0].x - pipe_group[0].width / 2 and \
                            player.x + player.width / 2 < pipe_group[0].x + pipe_group[0].width / 2 and \
                            self.pass_pipe is False:
                        self.pass_pipe = True
                    if self.pass_pipe is True:
                        if player.x - player.width / 2 > pipe_group[0].x + pipe_group[0].width / 2:
                            self.score += 1
                            self.score_sound.play()
                            self.pass_pipe = False

                # =====================
                # Scrolling the ground
                if not self.game_over:
                    ground.scrolling()

                # =======
                # Sounds
                if self.game_over is True:
                    if self.hit_played is False:
                        self.hit_sound.play()
                        self.die_sound.play()
                        self.hit_played = True

                # =======
                # Render
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glUseProgram(shader.program)
                bg.draw()
                for i in range(0, len(pipe_group)):
                    pipe_group[i].draw()
                ground.draw()
                player.draw()

                # Draw Menu
                game_name.draw()
                start_button.draw()
                start_text.draw()
                end_text.draw()
                ok_button.draw()

                # Draw Score
                i = 0
                numbers = list(str(self.score))
                length_numbers = len(numbers)
                for number in numbers:
                    path_button_score = "Textures/" + number + ".png"
                    score_text = Scene(path_button_score, 0 - (length_numbers - 1) * 25 + i * 40, 350, 36, 54)
                    score_text.draw()

                    i = i + 1

                glUseProgram(0)
                pygame.display.flip()
                self.timer.tick(fps)


def check_collision(player, collided_object):
    collision_x = player.x + player.width / 2 >= collided_object.x + leeway - collided_object.width / 2 and \
                  collided_object.x - leeway + collided_object.width / 2 >= player.x - player.width / 2
    collision_y = player.y + player.height / 2 >= collided_object.y + leeway - collided_object.height / 2 and \
                  collided_object.y - leeway + collided_object.height / 2 >= player.y - player.height / 2
    return collision_x and collision_y
