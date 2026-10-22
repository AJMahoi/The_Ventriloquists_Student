"""This is the main file for the game 'The Ventriloquist's Student'.
It initialises the game, sets up the main menu, and handles the game loop.
Run this file to start the game."""

import random
import time
from pathlib import Path
import sqlite3

from Downloader import *
from Actions import *
from GameLogic import *
from Music import *
from Objects import *
from Screens import *
from StartGame import *
from Statistics import *

install_if_missing("pygame")
import pygame

# Initialise pygame
pygame.init()
DIMENSIONS = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(DIMENSIONS, pygame.DOUBLEBUF)
pygame.display.set_caption("The Ventriloquist's Student")

# Colours
WHITE = (255, 255, 255)
PAVEMENT_GREY = (128, 128, 128)  # Colour for the pavement
ROAD_GREY = (105, 105, 105)  # Colour for the roads
SOFT_RED = (255, 102, 102)
SOFT_BLUE = (173, 216, 230)
BLUE = (0, 0, 255)
SOFT_GREEN = (144, 238, 144)  # Colour for soft green

# Player settings
player_size = 30
player_x, player_y = WIDTH // 2, HEIGHT - player_size
player_speed = 2  # Speed of the player
player_lives = 5  # Number of lives the player starts with

# Vehicle settings
vehicle_width = WIDTH // 6 - 20
vehicle_height = 40
vehicles = [[] for _ in range(6)]  # List of vehicles for each lane
lane_speeds = [random.randint(4, 8) for _ in range(6)]  # Random speeds for each lane
last_spawned_lane = None  # Track the last lane where a vehicle was spawned

# Load the school image
school_image_path = Path(__file__).parent.parent / "Images" / "SMCC" / "SMCC-top.jpg"
school_image = pygame.image.load(school_image_path)

# Maintain aspect ratio while scaling the school image
original_width, original_height = school_image.get_size()
aspect_ratio = original_width / original_height
new_height = 150  # Vertical size of the school image
new_width = int(
    new_height * aspect_ratio
)  # Adjust horizontal size based on aspect ratio
school_image = pygame.transform.scale(school_image, (new_width, new_height))

school_x = WIDTH // 2 - school_image.get_width() // 2
school_y = 10

# Load the heart image
heart_image_path = Path(__file__).parent.parent / "Images" / "Icons" / "heart.png"
heart_image = pygame.image.load(heart_image_path)
heart_image = pygame.transform.scale(heart_image, (30, 30))  # Scale the heart image

# Lanes setup
num_lanes = 6  # Two bus lanes, two car lanes, and two cyclist lanes
road_height = vehicle_height + 30  # Height of the road
lane_spacing = player_size + 5  # Space between roads slightly larger than player size
cyclist_lane_height = vehicle_height - 20  # Height of cyclist lanes

# Define lane positions
centre_offset = (HEIGHT - school_y - school_image.get_height() - player_y) // 2

bus_lane_bottom = (
    HEIGHT - player_size - road_height // 2 - centre_offset - 100
)  # Shifted 100 pixels upwards
car_lane_bottom = bus_lane_bottom - road_height
gap_1 = car_lane_bottom - lane_spacing

car_lane_top = gap_1 - road_height
bus_lane_top = car_lane_top - road_height
gap_2 = bus_lane_top - lane_spacing

cyclist_lane_1 = gap_2 - road_height - 20  # Adding space above the cyclist lane
cyclist_lane_2 = (
    cyclist_lane_1 - cyclist_lane_height - 20
)  # Adding space below the cyclist lane

lanes = [
    bus_lane_bottom,
    car_lane_bottom,
    car_lane_top,
    bus_lane_top,
    cyclist_lane_1,
    cyclist_lane_2,
]

# Vehicle types
CAR, BUS, BIKE = "car", "bus", "bike"

# Game loop control
running = True
clock = pygame.time.Clock()

# Countdown settings
start_time = time.time()
countdown_time = 5  # Countdown before the game starts
movement_allowed = False  # Prevent movement during the countdown


def initialise_database():
    """Initialise the stats database if it doesn't exist."""
    db_path = Path(__file__).parent / "Table of stats.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the stats table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stats (
            difficulty TEXT PRIMARY KEY,
            games_played INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            winrate REAL DEFAULT 0.0,
            fastest_time REAL DEFAULT NULL,
            slowest_time REAL DEFAULT NULL,
            average_time REAL DEFAULT NULL
        )
    """
    )

    # Insert default rows for all difficulties if they don't exist
    for difficulty in ["all", "easy", "medium", "hard"]:
        cursor.execute(
            """
            INSERT OR IGNORE INTO stats (difficulty) VALUES (?)
        """,
            (difficulty,),
        )

    conn.commit()
    conn.close()


# Initialise pygame mixer for music
pygame.mixer.init()

# Paths to music files
menu_music_path = Path(__file__).parent.parent / "Audio" / "Defeat.mp3"
easy_music_path = Path(__file__).parent.parent / "Audio" / "Forestall Desire.mp3"
medium_music_path = Path(__file__).parent.parent / "Audio" / "Round-A-Bout.mp3"
hard_music_path = Path(__file__).parent.parent / "Audio" / "Fatality.mp3"


def main_menu():
    """Display the main menu with Start Game, Stats, Credits, and Quit options."""
    play_music(menu_music_path)  # Start playing menu music

    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 48)

    while True:
        screen.fill(PAVEMENT_GREY)
        title_text = font.render("The Ventriloquist's Student", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6))

        # Define buttons
        start_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 3, 300, 60)
        stats_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 3 + 100, 300, 60)
        credits_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 3 + 200, 300, 60)
        quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 3 + 300, 300, 60)

        # Mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()

        # Draw Start Game button with hover effect
        if start_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen, (100, 149, 237), start_button
            )  # Darker blue for hover
        else:
            pygame.draw.rect(screen, SOFT_BLUE, start_button)

        start_text = small_font.render("Start Game", True, WHITE)
        screen.blit(
            start_text,
            (
                start_button.x + start_button.width // 2 - start_text.get_width() // 2,
                start_button.y
                + start_button.height // 2
                - start_text.get_height() // 2,
            ),
        )

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

        # Draw Credits button with hover effect
        if credits_button.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen, (100, 149, 237), credits_button
            )  # Darker blue for hover
        else:
            pygame.draw.rect(screen, SOFT_BLUE, credits_button)

        credits_text = small_font.render("Credits", True, WHITE)
        screen.blit(
            credits_text,
            (
                credits_button.x
                + credits_button.width // 2
                - credits_text.get_width() // 2,
                credits_button.y
                + credits_button.height // 2
                - credits_text.get_height() // 2,
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
                if start_button.collidepoint(event.pos):
                    spawn_rate = select_difficulty()  # Go to difficulty selection
                    if spawn_rate:  # If a difficulty is selected
                        start_game(spawn_rate)
                elif stats_button.collidepoint(event.pos):
                    display_stats()  # Display stats
                elif credits_button.collidepoint(event.pos):
                    display_credits()  # Display credits
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()


# Replace the main game loop with a call to the main menu
if __name__ == "__main__":
    initialise_database()
    main_menu()
