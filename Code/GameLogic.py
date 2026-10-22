"""This module focuses on the logic of the game, including collision detection,
player respawn, and player reset."""


def reset_player():
    """Reset the player to the initial position and settings."""
    from Objects import Player
    from Main import WIDTH, HEIGHT, player_size, player_speed

    return Player(WIDTH // 2, HEIGHT - player_size, player_size, player_speed)


def check_collision(player, rect_x, rect_y, rect_width, rect_height):
    """Check if the player collides with a given rectangle."""
    return (
        player.x < rect_x + rect_width
        and player.x + player.size > rect_x
        and player.y < rect_y + rect_height
        and player.y + player.size > rect_y
    )


def respawn_player(player, checkpoint_y, player_lives):
    """Handle player respawn with a 3-second delay, flashing effect, and a lost life message."""
    import pygame
    import time
    from Main import (
        screen,
        clock,
        WIDTH,
        HEIGHT,
        school_image,
        school_x,
        school_y,
        bus_lane_bottom,
        car_lane_bottom,
        car_lane_top,
        bus_lane_top,
        cyclist_lane_1,
        cyclist_lane_2,
        lane_spacing,
        cyclist_lane_height,
        ROAD_GREY,
        WHITE,
        SOFT_RED,
        heart_image,
        player_lives,
        PAVEMENT_GREY,
        road_height,
    )

    respawn_start_time = time.time()
    font = pygame.font.SysFont(None, 48)  # Font for the lost life message

    while time.time() - respawn_start_time < 3:  # 3-second delay
        screen.fill(PAVEMENT_GREY)
        screen.blit(school_image, (school_x, school_y))  # Draw the school image

        # Draw lanes
        for lane in [bus_lane_bottom, car_lane_bottom, car_lane_top, bus_lane_top]:
            pygame.draw.rect(
                screen, ROAD_GREY, (0, lane - road_height // 2, WIDTH, road_height)
            )
            for i in range(0, WIDTH, 40):
                pygame.draw.line(screen, WHITE, (i, lane), (i + 20, lane), 2)

        pygame.draw.rect(
            screen,
            ROAD_GREY,
            (
                0,
                cyclist_lane_2 - cyclist_lane_height // 2 - 20,
                WIDTH,
                cyclist_lane_height * 2 + lane_spacing + 20,
            ),
        )
        for i in range(0, WIDTH, 40):
            pygame.draw.line(
                screen, WHITE, (i, cyclist_lane_1), (i + 20, cyclist_lane_1), 2
            )
            pygame.draw.line(
                screen, WHITE, (i, cyclist_lane_2), (i + 20, cyclist_lane_2), 2
            )

        # Flashing effect
        if (
            int((time.time() - respawn_start_time) * 5) % 2 == 0
        ):  # Flash every 0.2 seconds
            player.draw()

        # Display "You lost a life!" message
        lost_life_text = font.render("You lost a life!", True, SOFT_RED)
        screen.blit(
            lost_life_text, (WIDTH // 2 - lost_life_text.get_width() // 2, HEIGHT // 2)
        )

        pygame.display.update()
        clock.tick(120)

    # Display lives as hearts after the respawn screen
    for i in range(player_lives):  # Use the updated player_lives value
        screen.blit(heart_image, (WIDTH - 40 * (i + 1), 10))

    # Respawn the player at the last checkpoint
    player.y = checkpoint_y
