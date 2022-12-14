import sys
import pygame
from bullet import Bullet
from alien import Alien
from pygame import mixer
from time import sleep
import json

# This initialization allows adding music and sound effects
mixer.init()
filename = 'highscores.json'


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play"""

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        # Reset game stats
        ai_settings.initialize_dynamic_settings()
        # Hide cursor
        pygame.mouse.set_visible(False)
        # Reset the game stats
        stats.reset_stats()
        stats.game_active = True

        # Reset scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_screen(ai_settings, screen, ship, stats, sb, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen"""

    screen.fill(ai_settings.bg_color)
    # Redraw all bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score formation
    sb.show_score()

    # Adding button in inactive game state
    if not stats.game_active:
        play_button.draw_button()

    # Making the most recently drawn screen visible
    pygame.display.flip()

    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Check whether an alien has been hit
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # Changing the first bool value to a False will create a
    # high-powered bullet that will
    # only disappear at the top of the screen

    if collisions:
        # Play music if alien is hit

        mixer.music.load('soundtrack/mixkit-retro-video-game-bubble-laser-277.wav')
        mixer.music.set_volume(0.5)
        mixer.music.play()
        for aliens in collisions.values():
            # making sure every alien hit is awarded
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        mixer.music.load('soundtrack/fleet_destroyed.wav')
        mixer.music.set_volume(.75)
        mixer.music.play()
        # Destroy existing bullets and create new fleet
        bullets.empty()
        sleep(1.0)
        ai_settings.increase_speed()
        # Increase level
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)



def get_number_aliens_x(ai_settings, alien_width):
    """Calculating the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height)
                         - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):

    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        # Play music
        mixer.music.load('soundtrack/big-impact-7054.mp3')
        mixer.music.set_volume(1.0)
        mixer.music.play()
        # Clear aliens and bullets
        aliens.empty()
        bullets.empty()
        # Pause
        sleep(1.0)
        # Create new alien fleet and center ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

    else:
        mixer.music.load('soundtrack/game_over.wav')
        mixer.music.set_volume(1.0)
        mixer.music.play()
        stats.game_active = False
        store_high_score(stats)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # Check if aliens have reached bottom of screen
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Same as ship getting hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, sb, screen, bullets, aliens, ship):
    """ Update the position the alien fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def store_high_score(stats):
    with open(filename, 'w') as hs:
        json.dump(int(stats.high_score), hs)


def load_high_score(stats):
    with open(filename) as hs:
        stats.high_score = json.load(hs)


def check_high_score_file(stats, sb):
    """To check for the presence of the high score file
    and load high score"""
    try:
        load_high_score(stats)
        sb.prep_high_score()
    except FileNotFoundError:
        pass
