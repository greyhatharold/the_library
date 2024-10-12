import json
import os
from datetime import datetime
from typing import Callable, List, Dict, Any, Optional
from logger import logger

class CollectionManager:
    """
    A class to manage collections of items in The Library application.

    This class handles the creation, storage, and management of collections
    and their associated items.
    """
    
    @logger.log_execution_time
    def __init__(self, get_user_data_dir: Callable[[], str]) -> None:
        """
        Initialize the CollectionManager.

        Args:
            get_user_data_dir (callable): A function that returns the path to the user data directory.

        Attributes:
            get_user_data_dir (callable): A function to get the user data directory.
            collections (List[Dict[str, Any]]): A list to store collections.
            categories (List[str]): A list of predefined item categories.
            settings_file (str): The path to the settings file.
        """
        try:
            self.get_user_data_dir: Callable[[], str] = get_user_data_dir
            self.collections: List[Dict[str, Any]] = []
            self.categories: List[str] = ["Book", "Movie", "Music", "Game"]
            self.settings_file: str = os.path.join(self.get_user_data_dir(), "settings.json")
            logger.info("CollectionManager initialized")
        except Exception as e:
            logger.error(f"Error initializing CollectionManager: {str(e)}")
            raise

    @logger.log_execution_time
    def add_collection(self, name: str) -> bool:
        """
        Add a new collection with the given name, ensuring uniqueness.
        
        Args:
            name (str): The name of the collection to add.
        
        Returns:
            bool: True if the collection was added successfully, False otherwise.
        """
        try:
            if not isinstance(name, str):
                raise TypeError("Collection name must be a string")
            if not name.strip():
                raise ValueError("Collection name cannot be empty or just whitespace")
            
            if any(c['name'] == name for c in self.collections):
                logger.warning(f"Collection '{name}' already exists")
                return False
            
            self.collections.append({
                "name": name,
                "items": [],
                "created_at": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat()
            })
            logger.info(f"Collection '{name}' added successfully")
            return True
        except (TypeError, ValueError) as e:
            logger.error(f"Error adding collection: {str(e)}")
            return False
        except Exception as e:
            logger.exception(f"Unexpected error adding collection: {str(e)}")
            return False

    @logger.log_execution_time
    def add_item(self, collection_name: str, item: Dict[str, Any]) -> bool:
        """
        Add an item to a specified collection, with duplicate checking.
        
        Args:
            collection_name (str): The name of the collection to add the item to.
            item (dict): The item to be added to the collection.
        
        Returns:
            bool: True if the item was added successfully, False otherwise.
        """
        try:
            if not isinstance(collection_name, str):
                raise TypeError("Collection name must be a string")
            if not isinstance(item, dict):
                raise TypeError("Item must be a dictionary")
            
            collection = next((c for c in self.collections if c["name"] == collection_name), None)
            if not collection:
                logger.warning(f"Collection '{collection_name}' not found")
                return False
            
            if item in collection["items"]:
                logger.warning(f"Item '{item}' already exists in collection '{collection_name}'")
                return False
            
            collection["items"].append(item)
            collection["last_modified"] = datetime.now().isoformat()
            logger.info(f"Item '{item}' added to collection '{collection_name}'")
            return True
        except TypeError as e:
            logger.error(f"Error adding item: {str(e)}")
            return False
        except Exception as e:
            logger.exception(f"Unexpected error adding item: {str(e)}")
            return False

    @logger.log_execution_time
    def get_collections(self) -> List[Dict[str, Any]]:
        """Return a list of all collections."""
        try:
            logger.info(f"Retrieved {len(self.collections)} collections")
            return self.collections
        except Exception as e:
            logger.error(f"Error retrieving collections: {str(e)}")
            return []

    @logger.log_execution_time
    def get_items_in_collection(self, collection_name: str) -> List[Dict[str, Any]]:
        """Return a list of all items in a specific collection."""
        try:
            collection = next((c for c in self.collections if c["name"] == collection_name), None)
            if not collection:
                logger.warning(f"Collection '{collection_name}' not found")
                return []
            logger.info(f"Retrieved {len(collection['items'])} items from collection '{collection_name}'")
            return collection["items"]
        except Exception as e:
            logger.exception(f"Error getting items from collection '{collection_name}': {str(e)}")
            return []

    @logger.log_execution_time
    def save_to_file(self, filename: str) -> bool:
        """
        Save the collections to a JSON file with error handling.
        
        Args:
            filename (str): The name of the file to save the collections to.
        
        Returns:
            bool: True if saved successfully, False otherwise.
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.collections, f, indent=2)
            logger.info(f"Successfully saved to {filename}")
            return True
        except IOError as e:
            logger.error(f"IOError saving to file '{filename}': {str(e)}")
            return False
        except Exception as e:
            logger.exception(f"Unexpected error saving to file '{filename}': {str(e)}")
            return False

    @logger.log_execution_time
    def load_from_file(self, filename: str) -> bool:
        """
        Load collections from a JSON file with validation.
        
        Args:
            filename (str): The name of the file to load the collections from.
        
        Returns:
            bool: True if the file was loaded successfully, False otherwise.
        """
        try:
            if not os.path.exists(filename):
                logger.error(f"File '{filename}' does not exist")
                return False
            
            with open(filename, 'r') as f:
                loaded_data = json.load(f)
            
            if not isinstance(loaded_data, list):
                raise ValueError("Loaded data is not a list")
            
            if not all(isinstance(item, dict) for item in loaded_data):
                raise ValueError("Not all items in loaded data are dictionaries")
            
            self.collections = loaded_data
            logger.info(f"Successfully loaded {len(self.collections)} collections from {filename}")
            return True
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from file '{filename}': {str(e)}")
            return False
        except ValueError as e:
            logger.error(f"Invalid data format in file '{filename}': {str(e)}")
            return False
        except Exception as e:
            logger.exception(f"Unexpected error loading from file '{filename}': {str(e)}")
            return False

    @logger.log_execution_time
    def get_categories(self) -> List[str]:
        """Return the list of predefined categories."""
        try:
            logger.info(f"Retrieved {len(self.categories)} categories")
            return self.categories
        except Exception as e:
            logger.error(f"Error retrieving categories: {str(e)}")
            return []

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
            settings = {"dark_mode": is_dark_mode}
            with open(self.settings_file, "w") as f:
                json.dump(settings, f)
            logger.info(f"Theme preference saved: Dark mode = {is_dark_mode}")
            return True
        except Exception as e:
            logger.error(f"Error saving theme preference: {str(e)}")
            return False

    @logger.log_execution_time
    def load_theme_preference(self) -> bool:
        """
        Load the user's theme preference from the settings file.

        Returns:
            bool: True if dark mode is preferred, False for light mode. 
                  Defaults to True if no preference is found.
        """
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                is_dark_mode = settings.get("dark_mode", True)
            else:
                is_dark_mode = True  # Default to dark mode if no settings file exists
            logger.info(f"Theme preference loaded: Dark mode = {is_dark_mode}")
            return is_dark_mode
        except Exception as e:
            logger.error(f"Error loading theme preference: {str(e)}")
            return True  # Default to dark mode in case of error

    @logger.log_execution_time
    def search_items(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for items across all collections based on a search term.

        Args:
            search_term (str): The term to search for in item names and categories.

        Returns:
            List[Dict[str, Any]]: A list of items matching the search term.
        """
        results: List[Dict[str, Any]] = []
        try:
            if not isinstance(search_term, str):
                raise TypeError("Search term must be a string")
            
            search_term_lower = search_term.lower()
            for collection in self.collections:
                for item in collection['items']:
                    if search_term_lower in item.get('name', '').lower() or search_term_lower in item.get('category', '').lower():
                        results.append(item)
            logger.info(f"Search for '{search_term}' returned {len(results)} results")
            return results
        except TypeError as e:
            logger.error(f"Error during item search: {str(e)}")
            return []
        except Exception as e:
            logger.exception(f"Unexpected error during item search: {str(e)}")
            return []