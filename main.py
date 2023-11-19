import pygame, sys
from core.config.settings import BASE_DIR, WIDTH, HEIGTH, WATER_COLOR, FPS
from core.controllers.level import Level


class Game:
    def __init__(self) -> None:
        """
        >>> Initialize the game.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("André Rufino - Game")
        self.clock = pygame.time.Clock()

        self.level = Level()

        main_sound = pygame.mixer.Sound(f"{BASE_DIR}/assets/audio/main.ogg")
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

    def run(self) -> None:
        """
        >>> Run's the game
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
