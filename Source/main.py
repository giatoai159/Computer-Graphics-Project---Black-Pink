from packages import *

display = (1280, 720)
icon = ""
name = "Black Pink"
timer = pygame.time.Clock()

# Color constant
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


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
    fullscreen = False  # Variable for fullscreen
    monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1, 0.5, 0.7, 1)
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == KEYDOWN:
                if event.key == K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        game_window = pygame.display.set_mode(monitor_size, DOUBLEBUF | OPENGL | pygame.FULLSCREEN)
                    else:
                        game_window = pygame.display.set_mode((game_window.get_width(), game_window.get_height()),
                                                              DOUBLEBUF | OPENGL | pygame.RESIZABLE)
        glBegin(GL_QUADS)
        glColor3f(1, 0, 0)
        glVertex2f(-0.1, -0.1)
        glVertex2f(0.2, -0.1)
        glVertex2f(0.2, 0.3)
        glVertex2f(-0.1, 0.3)
        glEnd()
        pygame.display.flip()


main()


pygame.quit()
