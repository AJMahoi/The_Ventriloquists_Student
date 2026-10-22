"""This module contains the Vehicle and Player classes for the game."""


class Vehicle:
    def __init__(self, lane_index, vehicle_type, speed):
        """Initialise a vehicle with lane index, type, and speed."""
        from Main import (
            lanes,
            vehicle_width,
            vehicle_height,
            WIDTH,
            SOFT_BLUE,
            SOFT_RED,
            SOFT_GREEN,
            CAR,
            BUS,
            BIKE,
        )

        self.lane_index = lane_index
        self.y = lanes[lane_index] - vehicle_height // 2
        self.vehicle_type = vehicle_type
        self.speed = speed  # Use the passed speed instead of global lane_speeds

        # Set direction based on lane index
        if lane_index in [0, 1]:  # Bottom 2 lanes
            self.direction = -1
        elif lane_index in [2, 3]:  # Middle 2 lanes
            self.direction = 1
        else:
            self.direction = -1 if lane_index % 2 == 0 else 1

        if self.vehicle_type == CAR:
            self.width, self.height, self.colour = (
                vehicle_width,
                vehicle_height,
                SOFT_BLUE,
            )
        elif self.vehicle_type == BUS:
            self.width, self.height, self.colour = (
                vehicle_width + 80,
                vehicle_height + 20,
                SOFT_RED,
            )
        elif self.vehicle_type == BIKE:
            self.width, self.height, self.colour = (
                vehicle_width - 20,
                vehicle_height - 20,
                SOFT_GREEN,
            )

        self.x = -self.width if self.direction == 1 else WIDTH
        self.y = lanes[lane_index] - self.height // 2

    def move(self):
        """Move the vehicle based on its speed and direction."""
        self.x += self.speed * self.direction

    def draw(self):
        """Draw the vehicle on the screen."""
        import pygame
        from Main import screen

        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))


class Player:
    def __init__(self, x, y, size, speed):
        """Initialise the player with position, size, and speed."""
        self.x, self.y, self.size, self.speed = x, y, size, speed

    def move(self, dx, dy):
        """Move the player by a specified amount."""
        self.x += dx
        self.y += dy

    def draw(self):
        """Draw the player on the screen."""
        import pygame
        from Main import screen, BLUE

        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size))
