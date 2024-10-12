import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from logger import logger

class DataManager:
    """
    Manages data operations for collections and items in the library system.
    """

    @logger.log_execution_time
    def __init__(self):
        """
        Initialize the DataManager with empty collections and predefined categories.
        """
        self.collections: List[Dict[str, Any]] = []
        self.categories: List[str] = ["Book", "Movie", "Music", "Game"]
        self.settings_file = "settings.json"
        logger.info("DataManager initialized")

    @logger.log_execution_time
    def add_collection(self, name: str) -> bool:
        """
        Add a new collection to the library.

        Args:
            name (str): The name of the collection to add.

        Returns:
            bool: True if the collection was added successfully, False otherwise.

        Raises:
            TypeError: If the name is not a string.
            ValueError: If the name is empty or just whitespace.
        """
        try:
            if not isinstance(name, str):
                raise TypeError("Collection name must be a string")
            if not name.strip():
                raise ValueError("Collection name cannot be empty or just whitespace")
            
            if any(c['name'] == name for c in self.collections):
                logger.warning(f"Collection '{name}' already exists")
                return False
            
            new_collection = {
                "name": name,
                "items": [],
                "created_at": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat()
            }
            self.collections.append(new_collection)
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
        Add a new item to a specified collection.

        Args:
            collection_name (str): The name of the collection to add the item to.
            item (Dict[str, Any]): The item to add.

        Returns:
            bool: True if the item was added successfully, False otherwise.

        Raises:
            TypeError: If collection_name is not a string or item is not a dictionary.
            ValueError: If the collection is not found or required item fields are missing.
        """
        try:
            if not isinstance(collection_name, str):
                raise TypeError("Collection name must be a string")
            if not isinstance(item, dict):
                raise TypeError("Item must be a dictionary")
            
            collection = next((c for c in self.collections if c["name"] == collection_name), None)
            if not collection:
                raise ValueError(f"Collection '{collection_name}' not found")
            
            required_fields = ['name', 'category', 'price']
            if not all(field in item for field in required_fields):
                raise ValueError(f"Item must contain all required fields: {', '.join(required_fields)}")
            
            if any(existing_item['name'] == item['name'] for existing_item in collection["items"]):
                logger.warning(f"Item '{item['name']}' already exists in collection '{collection_name}'")
                return False
            
            collection["items"].append(item)
            collection["last_modified"] = datetime.now().isoformat()
            logger.info(f"Item '{item['name']}' added to collection '{collection_name}'")
            return True
        except (TypeError, ValueError) as e:
            logger.error(f"Error adding item: {str(e)}")
            return False
        except Exception as e:
            logger.exception(f"Unexpected error adding item: {str(e)}")
            return False

    @logger.log_execution_time
    def get_collections(self) -> List[Dict[str, Any]]:
        """
        Retrieve all collections.

        Returns:
            List[Dict[str, Any]]: A list of all collections.
        """
        logger.info(f"Retrieved {len(self.collections)} collections")
        return self.collections

    @logger.log_execution_time
    def get_items_in_collection(self, collection_name: str) -> List[Dict[str, Any]]:
        """
        Retrieve all items in a specified collection.

        Args:
            collection_name (str): The name of the collection to retrieve items from.

        Returns:
            List[Dict[str, Any]]: A list of items in the specified collection.

        Raises:
            ValueError: If the collection is not found.
        """
        try:
            collection = next((c for c in self.collections if c["name"] == collection_name), None)
            if not collection:
                raise ValueError(f"Collection '{collection_name}' not found")
            logger.info(f"Retrieved {len(collection['items'])} items from collection '{collection_name}'")
            return collection["items"]
        except ValueError as e:
            logger.error(f"Error getting items from collection: {str(e)}")
            return []
        except Exception as e:
            logger.exception(f"Unexpected error getting items from collection '{collection_name}': {str(e)}")
            return []

    @logger.log_execution_time
    def save_to_file(self, filename: str) -> bool:
        """
        Save the current library state to a file.

        Args:
            filename (str): The name of the file to save to.

        Returns:
            bool: True if the save operation was successful, False otherwise.

        Raises:
            IOError: If there's an error writing to the file.
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
        Load library state from a file.

        Args:
            filename (str): The name of the file to load from.

        Returns:
            bool: True if the load operation was successful, False otherwise.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            json.JSONDecodeError: If there's an error decoding the JSON from the file.
            ValueError: If the loaded data is not in the expected format.
        """
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File '{filename}' does not exist")
            
            with open(filename, 'r') as f:
                loaded_data = json.load(f)
            
            if not isinstance(loaded_data, list):
                raise ValueError("Loaded data is not a list")
            
            if not all(isinstance(item, dict) and self._validate_collection(item) for item in loaded_data):
                raise ValueError("Not all items in loaded data are valid collections")
            
            self.collections = loaded_data
            logger.info(f"Successfully loaded {len(self.collections)} collections from {filename}")
            return True
        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from file '{filename}': {str(e)}")
            return False
        except ValueError as e:
            logger.error(f"Invalid data format in file '{filename}': {str(e)}")
            return False
        except Exception as e:
            logger.exception(f"Unexpected error loading from file '{filename}': {str(e)}")
            return False

    def _validate_collection(self, collection: Dict[str, Any]) -> bool:
        """
        Validate the structure of a collection.

        Args:
            collection (Dict[str, Any]): The collection to validate.

        Returns:
            bool: True if the collection is valid, False otherwise.
        """
        required_keys = ['name', 'items', 'created_at', 'last_modified']
        return all(key in collection for key in required_keys) and isinstance(collection['items'], list)

    @logger.log_execution_time
    def get_categories(self) -> List[str]:
        """
        Retrieve all predefined categories.

        Returns:
            List[str]: A list of all predefined categories.
        """
        logger.info(f"Retrieved {len(self.categories)} categories")
        return self.categories

    @logger.log_execution_time
    def search_items(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search for items across all collections based on a search term.

        Args:
            search_term (str): The term to search for in item names and categories.

        Returns:
            List[Dict[str, Any]]: A list of items matching the search term.
        """
        results = []
        try:
            search_term_lower = search_term.lower()
            for collection in self.collections:
                for item in collection['items']:
                    if search_term_lower in item.get('name', '').lower() or search_term_lower in item.get('category', '').lower():
                        results.append(item)
            logger.info(f"Search for '{search_term}' returned {len(results)} results")
            return results
        except Exception as e:
            logger.exception(f"Error during item search: {str(e)}")
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