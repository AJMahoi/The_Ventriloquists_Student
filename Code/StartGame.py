"""This module contains the start_game function, which initialises and runs the game."""


def start_game(spawn_rate):
    """Start the game with the selected difficulty."""
    import pygame
    import random
    import time
    from Music import play_music, stop_music
    from GameLogic import check_collision, respawn_player, reset_player
    from Main import (
        main_menu,
        easy_music_path,
        medium_music_path,
        hard_music_path,
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
        SOFT_GREEN,
        heart_image,
        player_size,
        PAVEMENT_GREY,
        SOFT_BLUE,
        SOFT_GREEN,
        road_height,
        WIDTH,
        HEIGHT,
        clock,
        screen,
        countdown_time,
        player_lives,
        player_lives,
        player_size,
        BIKE,
        CAR,
        BUS,
        num_lanes,
    )
    from Screens import display_end_screen
    from Objects import Vehicle
    from Statistics import update_stats

    # Updated difficulty names with new spawn rates
    difficulty_name = {12: "Easy", 8: "Medium", 4: "Hard"}.get(spawn_rate, "Unknown")

    # Play appropriate music for the difficulty
    if spawn_rate == 12:
        play_music(easy_music_path)
    elif spawn_rate == 8:
        play_music(medium_music_path)
    elif spawn_rate == 4:
        play_music(hard_music_path)

    player = reset_player()
    player_lives = 5
    start_time = time.time()
    vehicles = [[] for _ in range(6)]

    # Recalculate lane speeds for every game mode selection
    lane_speeds = [random.randint(4, 8) for _ in range(6)]

    running = True
    movement_allowed = False
    last_spawned_lane = None

    while running:
        screen.fill(PAVEMENT_GREY)
        screen.blit(school_image, (school_x, school_y))

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

        # Draw the "Menu" button under the lives, positioned slightly higher
        menu_button = pygame.Rect(
            WIDTH - 150, 50, 140, 50
        )  # Adjusted y-coordinate to 50
        mouse_pos = pygame.mouse.get_pos()
        if menu_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen, (100, 149, 237), menu_button
            )  # Darker blue for hover
        else:
            pygame.draw.rect(screen, SOFT_BLUE, menu_button)

        menu_text = pygame.font.SysFont(None, 36).render("Menu", True, WHITE)
        screen.blit(
            menu_text,
            (
                menu_button.x + menu_button.width // 2 - menu_text.get_width() // 2,
                menu_button.y + menu_button.height // 2 - menu_text.get_height() // 2,
            ),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.collidepoint(event.pos):
                    # Update stats as a loss and return to the main menu
                    update_stats(difficulty_name.lower(), 0, False)
                    stop_music()
                    main_menu()
                    return

        elapsed_time = int(time.time() - start_time)
        if elapsed_time < countdown_time:
            font = pygame.font.SysFont(None, 72)
            countdown_text = font.render(
                f"{countdown_time - elapsed_time}", True, WHITE
            )
            screen.blit(countdown_text, (WIDTH // 2 - 20, HEIGHT // 2))
        else:
            movement_allowed = True

        if random.randint(1, spawn_rate) == 1:
            lane_index = random.choice(
                [i for i in range(num_lanes) if i != last_spawned_lane]
            )
            if lane_index in [4, 5]:
                vehicle_type = BIKE
            elif lane_index in [0, 3]:
                vehicle_type = BUS
            else:
                vehicle_type = CAR

            if not vehicles[lane_index] or (
                (
                    vehicles[lane_index][-1].direction == 1
                    and vehicles[lane_index][-1].x > vehicles[lane_index][-1].width
                )
                or (
                    vehicles[lane_index][-1].direction == -1
                    and vehicles[lane_index][-1].x
                    < WIDTH - vehicles[lane_index][-1].width
                )
            ):
                # Pass the recalculated speed for the lane to the Vehicle
                vehicles[lane_index].append(
                    Vehicle(lane_index, vehicle_type, lane_speeds[lane_index])
                )
                last_spawned_lane = lane_index

        for lane_vehicles in vehicles:
            for vehicle in lane_vehicles:
                vehicle.move()
                vehicle.draw()

        if movement_allowed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if player.x > 0:
                    player.move(-player.speed, 0)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if player.x < WIDTH - player.size:
                    player.move(player.speed, 0)
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if player.y > 0:
                    player.move(0, -player.speed)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if player.y < HEIGHT - player_size:
                    player.move(0, player.speed)

        for lane_vehicles in vehicles:
            for vehicle in lane_vehicles:
                if check_collision(
                    player, vehicle.x, vehicle.y, vehicle.width, vehicle.height
                ):
                    player_lives -= 1
                    player = reset_player()
                    respawn_player(
                        player, HEIGHT - player_size, player_lives
                    )  # Respawn at the bottom
                    if player_lives == 0:
                        # Update database for loss
                        update_stats(difficulty_name.lower(), 0, False)
                        retry = display_end_screen(
                            "Game Over!", elapsed_time - countdown_time, 5, SOFT_RED
                        )
                        if not retry:  # If "Menu" is clicked
                            stop_music()  # Stop difficulty music
                            main_menu()  # Return to the main menu
                        break

        if check_collision(
            player,
            school_x,
            school_y,
            school_image.get_width(),
            school_image.get_height(),
        ):
            # Update database for win
            update_stats(difficulty_name.lower(), elapsed_time - countdown_time, True)
            retry = display_end_screen(
                "You Win!", elapsed_time - countdown_time, 5 - player_lives, SOFT_GREEN
            )
            if not retry:  # If "Menu" is clicked
                stop_music()  # Stop difficulty music
                main_menu()  # Return to the main menu
            break

        player.draw()

        if movement_allowed:
            elapsed_time = int(time.time() - start_time - countdown_time)
            font = pygame.font.SysFont(None, 36)
            time_text = font.render(
                f"Time: {max(0, elapsed_time)} seconds", True, WHITE
            )
            difficulty_text = font.render(
                f"Difficulty: {difficulty_name}", True, WHITE
            )  # Display difficulty
            screen.blit(time_text, (10, 10))
            screen.blit(
                difficulty_text, (10, 50)
            )  # Position difficulty text below the timer

            for i in range(player_lives):
                screen.blit(heart_image, (WIDTH - 40 * (i + 1), 10))

        pygame.display.update()
        clock.tick(120)
