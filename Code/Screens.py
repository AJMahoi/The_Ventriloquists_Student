"""This module contains functions to display the end screen, main menu, and credits."""


def display_end_screen(message, time_taken, lives_lost, colour):
    """Display the end screen with a message, time taken, and lives lost."""
    import pygame
    from Main import screen, WIDTH, HEIGHT, PAVEMENT_GREY, WHITE, SOFT_GREEN, SOFT_RED

    while True:
        screen.fill(PAVEMENT_GREY)
        font = pygame.font.SysFont(None, 72)
        message_text = font.render(message, True, colour)
        time_text = font.render(f"Time Taken: {time_taken} seconds", True, WHITE)
        lives_text = font.render(f"Lives Lost: {lives_lost}", True, WHITE)
        menu_text = font.render("Menu", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)

        # Draw the text
        screen.blit(
            message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 3)
        )
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2))
        screen.blit(
            lives_text, (WIDTH // 2 - lives_text.get_width() // 2, HEIGHT // 2 + 50)
        )

        # Draw the menu and quit buttons with hover effect
        menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
        quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 220, 200, 50)

        mouse_pos = pygame.mouse.get_pos()
        if menu_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (0, 200, 0), menu_button)  # Darker green for hover
        else:
            pygame.draw.rect(screen, SOFT_GREEN, menu_button)

        if quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (200, 0, 0), quit_button)  # Darker red for hover
        else:
            pygame.draw.rect(screen, SOFT_RED, quit_button)

        # Draw the button text
        screen.blit(
            menu_text,
            (
                menu_button.x + menu_button.width // 2 - menu_text.get_width() // 2,
                menu_button.y + menu_button.height // 2 - menu_text.get_height() // 2,
            ),
        )
        screen.blit(
            quit_text,
            (
                quit_button.x + quit_button.width // 2 - quit_text.get_width() // 2,
                quit_button.y + quit_button.height // 2 - quit_text.get_height() // 2,
            ),
        )

        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.collidepoint(event.pos):
                    return False  # Return to the main menu
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()


def display_menu():
    """Display the main menu with Start, Stats, Credits, and Quit buttons."""
    import pygame
    from Main import screen, WIDTH, HEIGHT, PAVEMENT_GREY, WHITE, SOFT_BLUE, SOFT_RED
    from statistics import display_stats

    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 48)

    while True:
        screen.fill(PAVEMENT_GREY)
        title_text = font.render("Main Menu", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6))

        # Define Stats and Quit buttons
        stats_button = pygame.Rect(10, 10, 150, 50)  # Top-left corner
        quit_button = pygame.Rect(WIDTH - 160, 10, 150, 50)  # Top-right corner

        # Mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()

        # Draw Stats button with hover effect
        if stats_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen, (100, 149, 237), stats_button
            )  # Darker blue for hover
        else:
            pygame.draw.rect(screen, SOFT_BLUE, stats_button)

        stats_text = small_font.render("Stats", True, WHITE)
        screen.blit(
            stats_text,
            (
                stats_button.x + stats_button.width // 2 - stats_text.get_width() // 2,
                stats_button.y
                + stats_button.height // 2
                - stats_text.get_height() // 2,
            ),
        )

        # Draw Quit button with hover effect
        if quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (200, 0, 0), quit_button)  # Darker red for hover
        else:
            pygame.draw.rect(screen, SOFT_RED, quit_button)

        quit_text = small_font.render("Quit", True, WHITE)
        screen.blit(
            quit_text,
            (
                quit_button.x + quit_button.width // 2 - quit_text.get_width() // 2,
                quit_button.y + quit_button.height // 2 - quit_text.get_height() // 2,
            ),
        )

        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if stats_button.collidepoint(event.pos):
                    display_stats()  # Call a function to display stats
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()


def display_credits():
    """Display the credits screen."""
    import pygame
    from Main import screen, WIDTH, HEIGHT, PAVEMENT_GREY, WHITE, SOFT_BLUE
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

    while True:
        screen.fill(PAVEMENT_GREY)

        # Title
        title_text = font.render("Credits", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 8))

        # Credits content
        credits = [
            "Game created by: AJMahoi",
            "School image: Artistic depiction of the SMCC on Google Maps",
            "Music credits (from Friday Night Funkin'):",
            "- Menu: Defeat (Instrumental)",
            "- Easy Difficulty: Forestall Desire (Instrumental)",
            "- Medium Difficulty: Round-A-Bout (Instrumental)",
            "- Hard Difficulty: Fatality (Instrumental)",
        ]

        for i, line in enumerate(credits):
            text = small_font.render(line, True, WHITE)
            screen.blit(
                text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4 + i * 40)
            )

        # Back button
        back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
        mouse_pos = pygame.mouse.get_pos()

        if back_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen, (100, 149, 237), back_button
            )  # Darker blue for hover
        else:
            pygame.draw.rect(screen, SOFT_BLUE, back_button)

        back_text = small_font.render("Back", True, WHITE)
        screen.blit(
            back_text,
            (
                back_button.x + back_button.width // 2 - back_text.get_width() // 2,
                back_button.y + back_button.height // 2 - back_text.get_height() // 2,
            ),
        )

        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return  # Go back to the main menu
