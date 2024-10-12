import unittest
from model import CollectionManager
import os
import json
from datetime import datetime, timedelta
from logger import logger

class TestCollectionManager(unittest.TestCase):
    def setUp(self):
        self.get_user_data_dir = lambda: os.path.join(os.path.dirname(__file__), 'test_data')
        self.manager = CollectionManager(self.get_user_data_dir)

    def tearDown(self):
        # Clean up any test files
        test_files = ['test_save.json', 'invalid.json', 'invalid_structure.json', 'test_settings.json']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

    def test_add_collection(self):
        self.assertTrue(self.manager.add_collection("Test Collection"))
        self.assertFalse(self.manager.add_collection("Test Collection"))  # Duplicate
        self.assertEqual(len(self.manager.collections), 1)

    def test_add_item(self):
        self.manager.add_collection("Test Collection")
        self.assertTrue(self.manager.add_item("Test Collection", "Test Item"))
        self.assertFalse(self.manager.add_item("Test Collection", "Test Item"))  # Duplicate
        self.assertFalse(self.manager.add_item("Non-existent Collection", "Test Item"))

    def test_save_and_load(self):
        self.manager.add_collection("Test Collection")
        self.manager.add_item("Test Collection", "Test Item")
        self.assertTrue(self.manager.save_to_file("test_save.json"))
        
        new_manager = CollectionManager(self.get_user_data_dir)
        self.assertTrue(new_manager.load_from_file("test_save.json"))
        self.assertEqual(len(new_manager.collections), 1)
        self.assertEqual(new_manager.collections[0]["name"], "Test Collection")
        self.assertEqual(new_manager.collections[0]["items"], ["Test Item"])

    def test_max_collections(self):
        manager = CollectionManager(self.get_user_data_dir, max_collections=3)
        self.assertTrue(manager.add_collection("Collection 1"))
        self.assertTrue(manager.add_collection("Collection 2"))
        self.assertTrue(manager.add_collection("Collection 3"))
        self.assertFalse(manager.add_collection("Collection 4"))

    def test_empty_collection_name(self):
        self.assertFalse(self.manager.add_collection(""))
        self.assertFalse(self.manager.add_collection("   "))

    def test_invalid_collection_name_type(self):
        self.assertFalse(self.manager.add_collection(123))
        self.assertFalse(self.manager.add_collection(None))

    def test_get_collections(self):
        self.manager.add_collection("Collection 1")
        self.manager.add_collection("Collection 2")
        collections = self.manager.get_collections()
        self.assertEqual(len(collections), 2)
        self.assertEqual(collections[0]["name"], "Collection 1")
        self.assertEqual(collections[1]["name"], "Collection 2")

    def test_add_item_to_nonexistent_collection(self):
        self.assertFalse(self.manager.add_item("Non-existent Collection", "Test Item"))

    def test_add_invalid_item_type(self):
        self.manager.add_collection("Test Collection")
        self.assertFalse(self.manager.add_item("Test Collection", 123))
        self.assertFalse(self.manager.add_item("Test Collection", None))

    def test_save_to_invalid_file(self):
        self.manager.add_collection("Test Collection")
        self.assertFalse(self.manager.save_to_file("/invalid/path/file.json"))

    def test_load_from_nonexistent_file(self):
        self.assertFalse(self.manager.load_from_file("nonexistent_file.json"))

    def test_load_invalid_json(self):
        with open("invalid.json", "w") as f:
            f.write("Invalid JSON content")
        self.assertFalse(self.manager.load_from_file("invalid.json"))

    def test_load_invalid_data_structure(self):
        with open("invalid_structure.json", "w") as f:
            json.dump({"key": "value"}, f)
        self.assertFalse(self.manager.load_from_file("invalid_structure.json"))

    def test_collection_creation_time(self):
        self.manager.add_collection("Test Collection")
        collection = self.manager.collections[0]
        created_at = datetime.fromisoformat(collection["created_at"])
        self.assertLess(datetime.now() - created_at, timedelta(seconds=1))

    def test_multiple_items_in_collection(self):
        self.manager.add_collection("Test Collection")
        self.manager.add_item("Test Collection", "Item 1")
        self.manager.add_item("Test Collection", "Item 2")
        self.manager.add_item("Test Collection", "Item 3")
        self.assertEqual(len(self.manager.collections[0]["items"]), 3)

    def test_case_sensitivity_collection_names(self):
        self.assertTrue(self.manager.add_collection("Test Collection"))
        self.assertTrue(self.manager.add_collection("test collection"))
        self.assertEqual(len(self.manager.collections), 2)

    def test_case_sensitivity_items(self):
        self.manager.add_collection("Test Collection")
        self.assertTrue(self.manager.add_item("Test Collection", "Test Item"))
        self.assertTrue(self.manager.add_item("Test Collection", "test item"))
        self.assertEqual(len(self.manager.collections[0]["items"]), 2)

    def test_load_theme_preference(self):
        # Test when settings file doesn't exist
        self.assertTrue(self.manager.load_theme_preference())

        # Test when settings file exists with valid data
        with open(os.path.join(self.get_user_data_dir(), 'settings.json'), 'w') as f:
            json.dump({"dark_mode": False}, f)
        self.assertFalse(self.manager.load_theme_preference())

        # Test with invalid JSON
        with open(os.path.join(self.get_user_data_dir(), 'settings.json'), 'w') as f:
            f.write("Invalid JSON")
        self.assertTrue(self.manager.load_theme_preference())

    def test_save_theme_preference(self):
        self.assertTrue(self.manager.save_theme_preference(True))
        self.assertTrue(self.manager.save_theme_preference(False))

        # Test with permission error (this might not work on all systems)
        os.chmod(self.get_user_data_dir(), 0o444)  # Read-only
        self.assertFalse(self.manager.save_theme_preference(True))
        os.chmod(self.get_user_data_dir(), 0o777)  # Restore permissions

    def test_get_items_in_collection(self):
        self.manager.add_collection("Test Collection")
        self.manager.add_item("Test Collection", "Item 1")
        self.manager.add_item("Test Collection", "Item 2")
        items = self.manager.get_items_in_collection("Test Collection")
        self.assertEqual(len(items), 2)
        self.assertIn("Item 1", items)
        self.assertIn("Item 2", items)

        # Test with non-existent collection
        with self.assertRaises(KeyError):
            self.manager.get_items_in_collection("Non-existent Collection")

    def test_search_items(self):
        self.manager.add_collection("Collection 1")
        self.manager.add_item("Collection 1", "Apple")
        self.manager.add_item("Collection 1", "Banana")
        self.manager.add_collection("Collection 2")
        self.manager.add_item("Collection 2", "Cherry")

        results = self.manager.search_items("a")
        self.assertEqual(len(results), 2)
        self.assertIn("Apple", [item['name'] for item in results])
        self.assertIn("Banana", [item['name'] for item in results])

        results = self.manager.search_items("cherry")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Cherry")

        # Test with empty search term
        with self.assertRaises(ValueError):
            self.manager.search_items("")

    def test_get_categories(self):
        categories = self.manager.get_categories()
        self.assertIsInstance(categories, list)
        self.assertTrue(all(isinstance(category, str) for category in categories))

if __name__ == '__main__':
    unittest.main()