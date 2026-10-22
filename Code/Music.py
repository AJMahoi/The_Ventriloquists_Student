"""This module contains functions to play and stop music."""


def play_music(music_path):
    """Play the specified music file in a loop."""
    import pygame

    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely


def stop_music():
    """Stop the currently playing music."""
    import pygame

    pygame.mixer.music.stop()
