"""This module handles the statistics screen and database operations for the game."""


def display_stats():
    """Display the stats screen."""
    import pygame
    from pathlib import Path
    import sqlite3
    from Main import screen, WIDTH, HEIGHT, PAVEMENT_GREY, WHITE, SOFT_RED, SOFT_BLUE

    font = pygame.font.SysFont(None, 36)

    while True:
        # Fetch stats from the database each time the stats screen is displayed
        db_path = Path(__file__).parent / "Table of stats.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stats")
        stats = cursor.fetchall()
        conn.close()

        screen.fill(PAVEMENT_GREY)

        # Draw stats for each difficulty in its quadrant
        quadrants = ["all", "easy", "medium", "hard"]
        positions = [
            (WIDTH // 4, HEIGHT // 4 - 50),  # Top-left (raised up)
            (3 * WIDTH // 4, HEIGHT // 4 - 50),  # Top-right (raised up)
            (WIDTH // 4, 3 * HEIGHT // 4 - 200),  # Bottom-left (raised up)
            (3 * WIDTH // 4, 3 * HEIGHT // 4 - 200),  # Bottom-right (raised up)
        ]

        for i, (difficulty, pos) in enumerate(zip(quadrants, positions)):
            # Find stats for the current difficulty
            stat = next((s for s in stats if s[0] == difficulty), None)
            if not stat:
                continue

            # Handle None values by providing default values
            games_played = stat[1] or 0
            wins = stat[2] or 0
            losses = stat[3] or 0
            winrate = stat[4] if stat[4] is not None else 0.0
            fastest_time = stat[5] if stat[5] is not None else "N/A"
            slowest_time = stat[6] if stat[6] is not None else "N/A"
            average_time = (
                f"{stat[7]:.1f}" if stat[7] is not None else "N/A"
            )  # Display average time to 1dp

            # Display stats
            text = [
                f"Difficulty: {difficulty.capitalize()}",
                f"Games Played: {games_played}",
                f"Wins: {wins}",
                f"Losses: {losses}",
                f"Winrate: {winrate:.2f}%",
                f"Fastest Time: {fastest_time}",
                f"Slowest Time: {slowest_time}",
                f"Average Time: {average_time}",
            ]
            for j, line in enumerate(text):
                rendered_text = font.render(line, True, WHITE)
                screen.blit(
                    rendered_text,
                    (pos[0] - rendered_text.get_width() // 2, pos[1] + j * 25),
                )

        # Define button dimensions and spacing
        button_width, button_height = 200, 50
        button_spacing = 20
        total_width = 2 * button_width + button_spacing
        start_x = (WIDTH - total_width) // 2  # Centre the buttons horizontally
        y_position = HEIGHT - 80

        # Define buttons
        reset_button = pygame.Rect(start_x, y_position, button_width, button_height)
        back_button = pygame.Rect(
            start_x + button_width + button_spacing,
            y_position,
            button_width,
            button_height,
        )

        # Mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()

        # Draw Reset button
        if reset_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (200, 0, 0), reset_button)  # Darker red for hover
        else:
            pygame.draw.rect(screen, SOFT_RED, reset_button)

        reset_text = font.render("Reset", True, WHITE)
        screen.blit(
            reset_text,
            (
                reset_button.x + reset_button.width // 2 - reset_text.get_width() // 2,
                reset_button.y
                + reset_button.height // 2
                - reset_text.get_height() // 2,
            ),
        )

        # Draw Back button
        if back_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen, (100, 149, 237), back_button
            )  # Darker blue for hover
        else:
            pygame.draw.rect(screen, SOFT_BLUE, back_button)

        back_text = font.render("Back", True, WHITE)
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
                if reset_button.collidepoint(event.pos):
                    confirm_reset()  # Call the confirmation window
                elif back_button.collidepoint(event.pos):
                    return  # Go back to the main menu


def confirm_reset():
    """Display a confirmation window to reset stats."""
    import pygame
    from Main import screen, WIDTH, HEIGHT, PAVEMENT_GREY, WHITE, SOFT_RED, SOFT_GREEN

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

    while True:
        screen.fill(PAVEMENT_GREY)

        # Confirmation message
        message_text = font.render(
            "Are you sure you want to reset all stats?", True, WHITE
        )
        screen.blit(
            message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 3)
        )

        # Yes and No buttons
        yes_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 100, 50)
        no_button = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2, 100, 50)
        mouse_pos = pygame.mouse.get_pos()

        if yes_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (0, 200, 0), yes_button)  # Darker green for hover
        else:
            pygame.draw.rect(screen, SOFT_GREEN, yes_button)

        if no_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (200, 0, 0), no_button)  # Darker red for hover
        else:
            pygame.draw.rect(screen, SOFT_RED, no_button)

        yes_text = small_font.render("Yes", True, WHITE)
        no_text = small_font.render("No", True, WHITE)
        screen.blit(
            yes_text,
            (
                yes_button.x + yes_button.width // 2 - yes_text.get_width() // 2,
                yes_button.y + yes_button.height // 2 - yes_text.get_height() // 2,
            ),
        )
        screen.blit(
            no_text,
            (
                no_button.x + no_button.width // 2 - no_text.get_width() // 2,
                no_button.y + no_button.height // 2 - no_text.get_height() // 2,
            ),
        )

        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    reset_database()  # Reset the database
                    return  # Close the confirmation window
                elif no_button.collidepoint(event.pos):
                    return  # Close the confirmation window


def reset_database():
    """Reset all stats in the database."""
    import sqlite3
    from pathlib import Path

    db_path = Path(__file__).parent / "Table of stats.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Reset all stats to default values
    cursor.execute(
        """
        UPDATE stats
        SET
            games_played = 0,
            wins = 0,
            losses = 0,
            winrate = 0.0,
            fastest_time = NULL,
            slowest_time = NULL,
            average_time = NULL
    """
    )

    conn.commit()
    conn.close()


def update_stats(difficulty, time_taken, won):
    """Update the stats in the database after a game."""
    import sqlite3
    from pathlib import Path

    db_path = Path(__file__).parent / "Table of stats.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch the current stats for the difficulty
    cursor.execute("SELECT * FROM stats WHERE difficulty = ?", (difficulty,))
    current_stats = cursor.fetchone()

    if current_stats:
        (
            games_played,
            wins,
            losses,
            winrate,
            fastest_time,
            slowest_time,
            average_time,
        ) = current_stats[1:]

        # Update games played
        games_played += 1

        # Update wins and losses
        if won:
            wins += 1
        else:
            losses += 1

        # Update winrate
        winrate = (wins / games_played) * 100 if games_played > 0 else 0.0

        # Update fastest time
        if won and (fastest_time is None or time_taken < fastest_time):
            fastest_time = time_taken

        # Update slowest time
        if won and (slowest_time is None or time_taken > slowest_time):
            slowest_time = time_taken

        # Update average time
        if won:
            if average_time is None:
                average_time = time_taken
            else:
                average_time = ((average_time * (wins - 1)) + time_taken) / wins

        # Update the database with the new stats
        cursor.execute(
            """
            UPDATE stats
            SET
                games_played = ?,
                wins = ?,
                losses = ?,
                winrate = ?,
                fastest_time = ?,
                slowest_time = ?,
                average_time = ?
            WHERE difficulty = ?
        """,
            (
                games_played,
                wins,
                losses,
                winrate,
                fastest_time,
                slowest_time,
                average_time,
                difficulty,
            ),
        )

    # Update stats for "all" difficulty
    cursor.execute("SELECT * FROM stats WHERE difficulty = 'all'")
    all_stats = cursor.fetchone()

    if all_stats:
        (
            games_played,
            wins,
            losses,
            winrate,
            fastest_time,
            slowest_time,
            average_time,
        ) = all_stats[1:]

        # Update games played
        games_played += 1

        # Update wins and losses
        if won:
            wins += 1
        else:
            losses += 1

        # Update winrate
        winrate = (wins / games_played) * 100 if games_played > 0 else 0.0

        # Update fastest time
        if won and (fastest_time is None or time_taken < fastest_time):
            fastest_time = time_taken

        # Update slowest time
        if won and (slowest_time is None or time_taken > slowest_time):
            slowest_time = time_taken

        # Update average time
        if won:
            if average_time is None:
                average_time = time_taken
            else:
                average_time = ((average_time * (wins - 1)) + time_taken) / wins

        # Update the database with the new stats
        cursor.execute(
            """
            UPDATE stats
            SET
                games_played = ?,
                wins = ?,
                losses = ?,
                winrate = ?,
                fastest_time = ?,
                slowest_time = ?,
                average_time = ?
            WHERE difficulty = 'all'
        """,
            (
                games_played,
                wins,
                losses,
                winrate,
                fastest_time,
                slowest_time,
                average_time,
            ),
        )

    conn.commit()
    conn.close()
