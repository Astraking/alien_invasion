import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """ Initialise game and create a screen object"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion 1.0")

    # Create an instance to store game stats
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Adding Play button.
    play_button = Button(ai_settings, screen, "Play")


    # Make a ship.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Creating an alien fleet
    gf.create_fleet(ai_settings, screen, ship, aliens)



    # Main loop for the game
    gf.check_high_score_file(stats, sb)

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, bullets, aliens, ship)
        gf.update_screen(ai_settings, screen, ship, stats, sb, aliens, bullets, play_button)


run_game()



