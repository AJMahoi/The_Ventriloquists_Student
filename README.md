# The Ventriloquist's Student

## About the Project

The Ventriloquist's Student is a game I developed as part of my programming project. It is inspired by games such as Crossy Road, where the player has to navigate through traffic and avoid obstacles to reach their destination safely.

The aim of the game is to guide the player through different lanes of traffic and reach the school without losing all their lives. The game was developed using Python and Pygame.

I wanted to create a game that was enjoyable to play whilst also allowing me to develop my programming skills and learn more about game development.

## Features

- **Main menu:** Players can choose to start a game, view statistics, read the credits or quit.
- **Difficulty selection:** Players can choose a difficulty level before starting the game.
- **Traffic system:** The game includes cars, buses and bicycles moving through different lanes.
- **Lives system:** Players start with five lives and must avoid traffic to stay in the game.
- **Countdown:** A countdown takes place before the game begins, giving the player time to get ready.
- **Music:** Different music tracks are used for the menu and different difficulty levels.
- **Statistics:** A SQLite database stores game statistics, including games played, wins, losses, win rate and completion times.
- **Interactive menus:** Buttons respond to the mouse position, making the menu more interactive.

## Technologies Used

- **Python** – used to develop the main game and its logic.
- **Pygame** – used to create the game window, display graphics, handle user input and play music.
- **SQLite** – used to store game statistics in a database.
- **Visual Studio Code** – used to write and organise the code.

## Project Structure

The project is split across several Python files, with different parts of the game handled separately.

- `main.py` – initialises the game, sets up the main menu and starts the game.
- `Actions.py` – contains action-related code.
- `GameLogic.py` – contains game logic.
- `Music.py` – handles music playback.
- `Objects.py` – contains game objects.
- `Screens.py` – handles different screens.
- `StartGame.py` – contains code for starting the game.
- `Statistics.py` – handles game statistics.
- `Downloader.py` – contains download or setup-related functionality.

The game also uses image and audio files, as well as a SQLite database for storing statistics.

## How to Run the Game

### Requirements

- Python 3
- Pygame
- The project's image and audio files

### Instructions

1. Download or clone the project.
2. Open the project folder in Visual Studio Code.
3. Install Pygame if it is not already installed (though I created a module to try and install it for you):

   ```bash
   python -m pip install pygame
   ```

4. Make sure the image and audio folders are in the correct locations.
5. Run the main Python file:

   ```bash
   python main.py
   ```

**Note:** The game uses image and audio paths relative to the project folders, so these files need to remain in the expected locations for everything to load correctly.

## What I Learned

Developing this game gave me experience with Python and helped me improve my problem-solving and debugging skills.

I worked with several different parts of game development, including handling user input, managing traffic, setting up game menus, playing music and storing information in a database.

I also learnt more about splitting a project into separate files so that different parts of the game can be managed independently.

## Future Improvements

There are several things I could improve or add to the game in the future, such as:

- Improving the graphics and animations.
- Adding more levels and obstacles.
- Making the difficulty progression more varied.
- Improving the statistics screen.
- Adding more automated tests to check that the game behaves as expected.

## Author

Developed by me (AJMahoi) as part of my programming project using Python and Pygame.