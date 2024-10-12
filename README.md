# The Library Application

The Library is a desktop application designed to manage collections of items such as books, movies, music, and games. Allowing for a way for users to interact with their collections, add new items, search for items, and manage their preferences.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Components](#components)
  - [GUI](#gui)
  - [Controller](#controller)
  - [DataManager](#datamanager)
  - [CollectionManager](#collectionmanager)
  - [Main](#main)
- [Installation](#installation)
- [Usage](#usage)

## Features

- **Collection Management**: Create, view, and manage collections of items.
- **Item Management**: Add, view, and manage items within collections.
- **Search Functionality**: Search for items across all collections.
- **Theme Preference**: Toggle between light and dark themes.
- **Persistent Storage**: Save and load collections and settings from files.

## Architecture

The application follows a Model-View-Controller (MVC) architecture:

- **Model**: Manages the data and business logic (handled by `CollectionManager`).
- **View**: Represents the user interface (handled by `GUI`).
- **Controller**: Acts as an intermediary between the model and the view (handled by `Controller`).

## Components

### GUI

- **File**: `gui.py`
- **Description**: The GUI component is built using the `customtkinter` library. It provides a user-friendly interface for interacting with collections and items. It includes features like a sidebar for navigation, main content area for displaying collections and items, and a settings window for theme preferences.

### Controller

- **File**: `controller.py`
- **Description**: The Controller manages interactions between the GUI and the CollectionManager. It handles user actions from the GUI and updates the model accordingly. It also manages theme preferences and error handling.

### DataManager

- **File**: `data_manager.py`
- **Description**: The DataManager is responsible for data operations such as adding collections and items, retrieving collections, and saving/loading data to/from files. It ensures data integrity and handles errors during data operations.

### CollectionManager

- **File**: `model.py`
- **Description**: The CollectionManager is the core of the model. It manages the collections and items, ensuring data consistency and providing methods for data manipulation. It also handles theme preferences and data persistence.

### Main

- **File**: `main.py`
- **Description**: The entry point of the application. It sets up logging, initializes the Controller and GUI, and starts the main application loop. It also handles cleanup operations when the application exits.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/the-library.git
   cd the-library
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

- **Navigating the GUI**: Use the sidebar to navigate between Home, Collections, Search, and Settings.
- **Managing Collections**: Add new collections and items using the provided buttons and dialogs.
- **Searching**: Enter a search term in the search frame to find items across all collections.
- **Theme Preference**: Toggle between light and dark themes in the settings window.
