"""This module is responsible for displaying the difficulty selection screen
and handling user input."""


def select_difficulty():
    """Display a difficulty selection screen with a Back button."""
    import pygame
    from Main import screen, WIDTH, HEIGHT, WHITE, PAVEMENT_GREY, SOFT_BLUE, SOFT_RED
    from Music import stop_music

    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 48)

    # Updated difficulty options with new spawn rates
    difficulties = [("Easy", 12), ("Medium", 8), ("Hard", 4)]
    buttons = []

    # Create buttons for each difficulty
    for i, (label, _) in enumerate(difficulties):
        button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 3 + i * 100, 300, 60)
        buttons.append((button_rect, label))

    # Back button
    back_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 3 + 300, 300, 60)

    while True:
        screen.fill(PAVEMENT_GREY)
        title_text = font.render("Select Difficulty", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6))

        # Draw buttons with hover effect
        mouse_pos = pygame.mouse.get_pos()
        for button_rect, label in buttons:
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(
                    screen, (100, 149, 237), button_rect
                )  # Darker blue for hover
            else:
                pygame.draw.rect(screen, SOFT_BLUE, button_rect)

            label_text = small_font.render(label, True, WHITE)
            screen.blit(
                label_text,
                (
                    button_rect.x
                    + button_rect.width // 2
                    - label_text.get_width() // 2,
                    button_rect.y
                    + button_rect.height // 2
                    - label_text.get_height() // 2,
                ),
            )

        # Draw Back button with hover effect
        if back_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (200, 0, 0), back_button)  # Darker red for hover
        else:
            pygame.draw.rect(screen, SOFT_RED, back_button)

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
                for i, (button_rect, _) in enumerate(buttons):
                    if button_rect.collidepoint(event.pos):
                        stop_music()  # Stop menu music
                        return difficulties[i][
                            1
                        ]  # Return the spawn rate for the selected difficulty
                if back_button.collidepoint(event.pos):
                    return  # Go back to the main menu
