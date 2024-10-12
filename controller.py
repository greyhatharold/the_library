from typing import List, Dict, Any, Optional
from model import CollectionManager
from logger import logger
import json

class Controller:
    """
    Controller class that manages interactions between the GUI and the CollectionManager.
    """

    @logger.log_execution_time
    def __init__(self, get_user_data_dir: callable) -> None:
        self.get_user_data_dir: callable = get_user_data_dir
        self.collection_manager: CollectionManager = CollectionManager(self.get_user_data_dir)
        logger.info("Controller initialized successfully")

    @logger.log_execution_time
    def load_theme_preference(self) -> bool:
        """
        Load the user's theme preference from the settings file.

        Returns:
            bool: True if dark mode is preferred, False for light mode. 
                  Defaults to True if no preference is found.
        """
        try:
            return self.collection_manager.load_theme_preference()
        except FileNotFoundError:
            logger.warning("Settings file not found. Using default theme.")
            return True
        except json.JSONDecodeError:
            logger.error("Invalid JSON in settings file. Using default theme.")
            return True
        except Exception as e:
            logger.error(f"Error loading theme preference: {str(e)}", exc_info=True)
            return True  # Default to dark mode in case of error

    @logger.log_execution_time
    def save_theme_preference(self, is_dark_mode: bool) -> bool:
        """
        Save the user's theme preference to a settings file.

        Args:
            is_dark_mode (bool): True if dark mode is selected, False otherwise.

        Returns:
            bool: True if the preference was saved successfully, False otherwise.
        """
        try:
            return self.collection_manager.save_theme_preference(is_dark_mode)
        except PermissionError:
            logger.error("Permission denied when saving theme preference.")
            return False
        except IOError as e:
            logger.error(f"I/O error occurred when saving theme preference: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error saving theme preference: {str(e)}", exc_info=True)
            return False

    @logger.log_execution_time
    def add_collection(self, name: str) -> bool:
        """
        Add a new collection to the library.

        Args:
            name (str): The name of the collection to add.

        Returns:
            bool: True if the collection was added successfully, False otherwise.
        """
        try:
            logger.info(f"Attempting to add collection: {name}")
            return self.collection_manager.add_collection(name)
        except ValueError as e:
            logger.error(f"Invalid collection name: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error adding collection: {str(e)}", exc_info=True)
            return False

    @logger.log_execution_time
    def add_item(self, collection_name: str, item: Dict[str, Any]) -> bool:
        """
        Add a new item to a specified collection.

        Args:
            collection_name (str): The name of the collection to add the item to.
            item (Dict[str, Any]): A dictionary containing the item's details.

        Returns:
            bool: True if the item was added successfully, False otherwise.
        """
        try:
            logger.info(f"Attempting to add item to collection '{collection_name}'")
            return self.collection_manager.add_item(collection_name, item)
        except KeyError:
            logger.error(f"Collection '{collection_name}' not found.")
            return False
        except ValueError as e:
            logger.error(f"Invalid item data: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error adding item: {str(e)}", exc_info=True)
            return False

    @logger.log_execution_time
    def get_collections(self) -> List[Dict[str, Any]]:
        """
        Retrieve all collections from the library.

        Returns:
            List[Dict[str, Any]]: A list of all collections.
        """
        try:
            return self.collection_manager.get_collections()
        except Exception as e:
            logger.error(f"Error retrieving collections: {str(e)}", exc_info=True)
            return []

    @logger.log_execution_time
    def get_items_in_collection(self, collection_name: str) -> List[Dict[str, Any]]:
        """
        Retrieve all items in a specified collection.

        Args:
            collection_name (str): The name of the collection to retrieve items from.

        Returns:
            List[Dict[str, Any]]: A list of items in the specified collection.
        """
        try:
            return self.collection_manager.get_items_in_collection(collection_name)
        except KeyError:
            logger.error(f"Collection '{collection_name}' not found.")
            return []
        except Exception as e:
            logger.error(f"Error retrieving items from collection: {str(e)}", exc_info=True)
            return []

    @logger.log_execution_time
    def search_items(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for items in the library based on a search term.

        Args:
            search_term (str): The term to search for in item names or categories.

        Returns:
            List[Dict[str, Any]]: A list of items matching the search term.
        """
        try:
            return self.collection_manager.search_items(search_term)
        except ValueError as e:
            logger.error(f"Invalid search term: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error searching items: {str(e)}", exc_info=True)
            return []

    @logger.log_execution_time
    def get_categories(self) -> List[str]:
        """
        Retrieve all predefined categories.

        Returns:
            List[str]: A list of all predefined categories.
        """
        try:
            return self.collection_manager.get_categories()
        except Exception as e:
            logger.error(f"Error retrieving categories: {str(e)}", exc_info=True)
            return []