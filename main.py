import logging
import os
import sys
from pathlib import Path
from typing import Callable, Optional
from controller import Controller
from gui import GUI
import customtkinter as ctk

def setup_logging() -> None:
    """Set up logging configuration for the application."""
    try:
        user_dir: str = os.path.expanduser("~")
        log_dir: str = os.path.join(user_dir, "The_Library")
        os.makedirs(log_dir, exist_ok=True)
        log_file: str = os.path.join(log_dir, "the_library.log")

        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console: logging.StreamHandler = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter: logging.Formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        sys.exit(1)

def get_base_dir() -> str:
    try:
        if getattr(sys, 'frozen', False):
            return sys._MEIPASS
        else:
            return os.path.dirname(os.path.abspath(__file__))
    except Exception as e:
        logging.error(f"Error getting base directory: {str(e)}")
        raise
    
def get_user_data_dir() -> str:
    """
    Get the user data directory for storing application data.

    Returns:
        str: The path to the user data directory.

    Raises:
        OSError: If there's an error creating the directory.
    """
    try:
        home: Path = Path.home()
        if sys.platform == "win32":
            user_data_dir: Path = home / "AppData/Local/TheLibrary"
        elif sys.platform == "darwin":
            user_data_dir: Path = home / "Library/Application Support/TheLibrary"
        user_data_dir.mkdir(parents=True, exist_ok=True)
    
        return str(user_data_dir)
    except OSError as e:
        logging.error(f"Error creating user data directory: {str(e)}")
        raise

def main() -> None:
    setup_logging()
    logger: logging.Logger = logging.getLogger(__name__)
    logger.info("Starting The Library application")
    
    try:
        logger.info("Initializing Controller")
        controller: Controller = Controller(get_user_data_dir)
        logger.info("Controller initialized successfully")
        
        logger.info("Initializing GUI")
        gui: GUI = GUI(controller, get_user_data_dir)
        logger.info("GUI initialized successfully")
        
        logger.info("Running GUI")
        gui.run()
        logger.info("GUI run completed")
    except Exception as e:
        logger.exception(f"A critical error occurred while running the application: {str(e)}")
        print(f"A critical error occurred: {str(e)}")
        print("Please check the log file for more details.")
    finally:
        logger.info("Cleaning up resources")
        cleanup_ctk(logger)

def cleanup_ctk(logger: logging.Logger) -> None:
    try:
        if hasattr(ctk, 'destroy'):
            ctk.destroy()
        elif hasattr(ctk, 'quit'):
            ctk.quit()
        else:
            logger.warning("No method found to destroy CustomTkinter context")
        logger.info("CustomTkinter context cleanup attempted")
    except Exception as e:
        logger.error(f"Error during CustomTkinter context cleanup: {e}")

if __name__ == "__main__":
    main()