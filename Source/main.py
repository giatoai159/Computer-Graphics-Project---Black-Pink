from packages import *

display = (800, 600)
icon = ""
name = "Black Pink"
timer = pygame.time.Clock()


def quit_game():
    pygame.quit()
    sys.exit()


def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        keys_flag = pygame.key.get_pressed()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(1, 1, 1, 1)
        pygame.display.flip()

def game_init():
    # PyGame initialization
    pygame.init()
    while not pygame.get_init():
        print("PyGame Initialization Failed.")
    # Game window properties
    game_window = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # Set game width and height
    pygame.display.set_caption(name)  # Set game title
    # _icon = pygame.image.load(icon)  # Load icon
    # pygame.display.set_icon(_icon)  # Set game icon
    # Game main loop
    main_menu()



def main():
    game_init()


main()
pygame.quit()
