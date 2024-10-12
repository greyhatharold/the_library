import customtkinter as ctk
from typing import Callable, Dict, Any, List, Optional
from controller import Controller
import os
from PIL import Image
from logger import logger

class GUI:
    def __init__(self, controller: Controller, get_user_data_dir: Callable[[], str]):
        self.controller: Controller = controller
        self.dark_mode: bool = self.controller.load_theme_preference()
        self.get_user_data_dir: Callable[[], str] = get_user_data_dir
        self.settings_file: str = os.path.join(self.get_user_data_dir(), "settings.json")
        self.data_file: str = os.path.join(self.get_user_data_dir(), "library_data.json")
        self.setup_gui()
    
    @logger.log_execution_time
    def setup_gui(self) -> None:
        """Set up the main GUI components."""
        try:
            ctk.set_appearance_mode("dark" if self.dark_mode else "light")
            ctk.set_default_color_theme("blue")

            self.root: ctk.CTk = ctk.CTk()
            self.root.title("The Library")
            self.root.geometry("1000x600")

            self.setup_sidebar()
            self.setup_main_content()
            self.setup_settings_window()
            self.setup_status_bar()

            logger.info("GUI setup completed successfully")
        except Exception as e:
            logger.error(f"Error in setup_gui: {str(e)}", exc_info=True)
            self.show_error("An error occurred while setting up the GUI.")

    @logger.log_execution_time
    def setup_sidebar(self) -> None:
        """Set up the sidebar with navigation buttons."""
        try:
            sidebar: ctk.CTkFrame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
            sidebar.pack(side="left", fill="y", padx=10, pady=10)

            logo: ctk.CTkLabel = ctk.CTkLabel(sidebar, text="The Library", font=("Helvetica", 20, "bold"))
            logo.pack(pady=20)

            buttons: List[tuple] = [
                ("Home", self.show_home),
                ("Collections", self.show_collections),
                ("Search", self.show_search),
                ("Settings", self.show_settings)
            ]

            for text, command in buttons:
                btn: ctk.CTkButton = ctk.CTkButton(sidebar, text=text, command=command)
                btn.pack(pady=10, padx=20)
                self.create_tooltip(btn, f"Go to {text}")

            logger.debug("Sidebar setup completed")
        except Exception as e:
            logger.error(f"Error in setup_sidebar: {str(e)}", exc_info=True)
            self.show_error("An error occurred while setting up the sidebar.")

    @logger.log_execution_time
    def setup_main_content(self) -> None:
        """Set up the main content area with different frames."""
        try:
            self.main_content: ctk.CTkFrame = ctk.CTkFrame(self.root)
            self.main_content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

            self.home_frame: ctk.CTkFrame = self.create_home_frame()
            self.collections_frame: ctk.CTkFrame = self.create_collections_frame()
            self.search_frame: ctk.CTkFrame = self.create_search_frame()

            self.show_home()
            logger.debug("Main content setup completed")
        except Exception as e:
            logger.error(f"Error in setup_main_content: {str(e)}", exc_info=True)
            self.show_error("An error occurred while setting up the main content area.")

    def create_home_frame(self) -> ctk.CTkFrame:
        """Create and return the home frame."""
        frame: ctk.CTkFrame = ctk.CTkFrame(self.main_content)
        label: ctk.CTkLabel = ctk.CTkLabel(frame, text="Welcome to The Library", font=("Helvetica", 24))
        label.pack(pady=20)
        return frame

    def create_collections_frame(self) -> ctk.CTkFrame:
        """Create and return the collections frame."""
        frame: ctk.CTkFrame = ctk.CTkFrame(self.main_content)
        label: ctk.CTkLabel = ctk.CTkLabel(frame, text="Collections", font=("Helvetica", 20))
        label.pack(pady=10)

        collections: List[Dict[str, Any]] = self.controller.get_collections()
        for collection in collections:
            btn: ctk.CTkButton = ctk.CTkButton(frame, text=collection['name'], command=lambda c=collection: self.show_collection_items(c))
            btn.pack(pady=5)

        add_collection_btn: ctk.CTkButton = ctk.CTkButton(frame, text="Add New Collection", command=self.add_new_collection)
        add_collection_btn.pack(pady=10)

        return frame

    def create_search_frame(self) -> ctk.CTkFrame:
        """Create and return the search frame."""
        frame: ctk.CTkFrame = ctk.CTkFrame(self.main_content)
        label: ctk.CTkLabel = ctk.CTkLabel(frame, text="Search", font=("Helvetica", 20))
        label.pack(pady=10)

        search_entry: ctk.CTkEntry = ctk.CTkEntry(frame, placeholder_text="Enter search term...")
        search_entry.pack(pady=10)

        search_btn: ctk.CTkButton = ctk.CTkButton(frame, text="Search", command=lambda: self.perform_search(search_entry.get()))
        search_btn.pack(pady=10)

        self.search_results: ctk.CTkTextbox = ctk.CTkTextbox(frame, height=300)
        self.search_results.pack(pady=10, fill="both", expand=True)

        return frame

    def show_home(self) -> None:
        """Display the home frame."""
        self.clear_main_content()
        self.home_frame.pack(fill="both", expand=True)

    def show_collections(self) -> None:
        """Display the collections frame."""
        self.clear_main_content()
        self.collections_frame.pack(fill="both", expand=True)

    def show_search(self) -> None:
        """Display the search frame."""
        self.clear_main_content()
        self.search_frame.pack(fill="both", expand=True)

    def show_settings(self) -> None:
        """Display the settings window."""
        try:
            self.settings_window.deiconify()
            logger.info("Settings window displayed")
        except Exception as e:
            logger.error(f"Error displaying settings window: {str(e)}")
            self.show_error("An error occurred while opening the settings window.")

    def clear_main_content(self) -> None:
        """Clear all widgets from the main content area."""
        for widget in self.main_content.winfo_children():
            widget.pack_forget()

    @logger.log_execution_time
    def setup_settings_window(self) -> None:
        """Set up the settings window."""
        try:
            self.settings_window: ctk.CTkToplevel = ctk.CTkToplevel(self.root)
            self.settings_window.title("Settings")
            self.settings_window.geometry("300x150")
            self.settings_window.withdraw()

            theme_label: ctk.CTkLabel = ctk.CTkLabel(self.settings_window, text="Theme")
            theme_label.pack(pady=10)

            self.theme_switch: ctk.CTkSwitch = ctk.CTkSwitch(self.settings_window, text="Dark Mode", command=self.toggle_theme)
            self.theme_switch.pack(pady=10)
            self.theme_switch.select() if self.dark_mode else self.theme_switch.deselect()

            close_button: ctk.CTkButton = ctk.CTkButton(self.settings_window, text="Close", command=self.settings_window.withdraw)
            close_button.pack(pady=10)

            logger.debug("Settings window setup completed")
        except Exception as e:
            logger.error(f"Error in setup_settings_window: {str(e)}", exc_info=True)
            self.show_error("An error occurred while setting up the settings window.")

    @logger.log_execution_time
    def toggle_theme(self) -> None:
        """Toggle between light and dark themes."""
        try:
            self.dark_mode = self.theme_switch.get()
            theme: str = "dark" if self.dark_mode else "light"
            ctk.set_appearance_mode(theme)
            self.controller.save_theme_preference(self.dark_mode)
            logger.info(f"Theme changed to {theme}")
        except Exception as e:
            logger.error(f"Error toggling theme: {str(e)}", exc_info=True)
            self.show_error("An error occurred while changing the theme.")

    def setup_status_bar(self) -> None:
        """Set up the status bar at the bottom of the main window."""
        self.status_bar: ctk.CTkLabel = ctk.CTkLabel(self.root, text="Ready", anchor="w")
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=5)

    def show_error(self, message: str) -> None:
        """Display an error message in the status bar."""
        self.status_bar.configure(text=f"Error: {message}", text_color="red")
        logger.error(message)

    def show_success(self, message: str) -> None:
        """Display a success message in the status bar."""
        self.status_bar.configure(text=message, text_color="green")
        logger.info(message)

    def create_tooltip(self, widget: ctk.CTkBaseClass, text: str) -> None:
        """Create a tooltip for a widget."""
        def enter(event: Any) -> None:
            self.tooltip: ctk.CTkToplevel = ctk.CTkToplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            label: ctk.CTkLabel = ctk.CTkLabel(self.tooltip, text=text, corner_radius=4, fg_color="gray75", text_color="black")
            label.pack(ipadx=5, ipady=5)
            self.tooltip.geometry(f"+{event.x_root+15}+{event.y_root+10}")

        def leave(event: Any) -> None:
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def load_icon(self, filename: str) -> Optional[ctk.CTkImage]:
        """Load an icon image."""
        try:
            return ctk.CTkImage(Image.open(os.path.join("assets", "icons", filename)), size=(20, 20))
        except Exception as e:
            logger.error(f"Error loading icon {filename}: {str(e)}")
            return None

    @logger.log_execution_time
    def add_new_collection(self) -> None:
        """Add a new collection."""
        name: Optional[str] = ctk.CTkInputDialog(text="Enter collection name:", title="New Collection").get_input()
        if name:
            success: bool = self.controller.add_collection(name)
            if success:
                self.show_success(f"Collection '{name}' added successfully.")
                self.update_collections_frame()
            else:
                self.show_error(f"Failed to add collection '{name}'.")

    def update_collections_frame(self) -> None:
        """Update the collections frame with the latest collections."""
        self.collections_frame = self.create_collections_frame()
        if self.main_content.winfo_children()[0] == self.collections_frame:
            self.show_collections()

    @logger.log_execution_time
    def show_collection_items(self, collection: Dict[str, Any]) -> None:
        """Display items in a collection."""
        self.clear_main_content()
        frame: ctk.CTkFrame = ctk.CTkFrame(self.main_content)
        frame.pack(fill="both", expand=True)

        label: ctk.CTkLabel = ctk.CTkLabel(frame, text=f"Items in {collection['name']}", font=("Helvetica", 20))
        label.pack(pady=10)

        items: List[Dict[str, Any]] = self.controller.get_items_in_collection(collection['name'])
        for item in items:
            item_frame: ctk.CTkFrame = ctk.CTkFrame(frame)
            item_frame.pack(pady=5, padx=10, fill="x")

            name_label: ctk.CTkLabel = ctk.CTkLabel(item_frame, text=item['name'])
            name_label.pack(side="left", padx=5)

            category_label: ctk.CTkLabel = ctk.CTkLabel(item_frame, text=f"Category: {item['category']}")
            category_label.pack(side="left", padx=5)

            price_label: ctk.CTkLabel = ctk.CTkLabel(item_frame, text=f"Price: ${item['price']:.2f}")
            price_label.pack(side="left", padx=5)

        add_item_btn: ctk.CTkButton = ctk.CTkButton(frame, text="Add New Item", command=lambda: self.add_new_item(collection['name']))
        add_item_btn.pack(pady=10)

    @logger.log_execution_time
    def add_new_item(self, collection_name: str) -> None:
        """Add a new item to a collection."""
        dialog: ctk.CTkToplevel = ctk.CTkToplevel(self.root)
        dialog.title("Add New Item")
        dialog.geometry("300x200")

        name_entry: ctk.CTkEntry = ctk.CTkEntry(dialog, placeholder_text="Item Name")
        name_entry.pack(pady=5)

        category_entry: ctk.CTkEntry = ctk.CTkEntry(dialog, placeholder_text="Category")
        category_entry.pack(pady=5)

        price_entry: ctk.CTkEntry = ctk.CTkEntry(dialog, placeholder_text="Price")
        price_entry.pack(pady=5)

        def submit() -> None:
            name: str = name_entry.get()
            category: str = category_entry.get()
            try:
                price: float = float(price_entry.get())
            except ValueError:
                self.show_error("Invalid price. Please enter a number.")
                return

            item: Dict[str, Any] = {"name": name, "category": category, "price": price}
            success: bool = self.controller.add_item(collection_name, item)
            if success:
                self.show_success(f"Item '{name}' added to '{collection_name}' successfully.")
                self.show_collection_items({"name": collection_name})
                dialog.destroy()
            else:
                self.show_error(f"Failed to add item '{name}' to '{collection_name}'.")

        submit_btn: ctk.CTkButton = ctk.CTkButton(dialog, text="Add Item", command=submit)
        submit_btn.pack(pady=10)

    @logger.log_execution_time
    def perform_search(self, search_term: str) -> None:
        """Perform a search and display results."""
        results: List[Dict[str, Any]] = self.controller.search_items(search_term)
        self.search_results.delete("1.0", ctk.END)
        if results:
            for item in results:
                self.search_results.insert(ctk.END, f"Name: {item['name']}, Category: {item['category']},Price: ${item['price']:.2f}\n")
        else:
            self.search_results.insert(ctk.END, "No results found.")

    @logger.log_execution_time
    def run(self):
        """Run the main GUI loop."""
        try:
            self.root.mainloop()
            logger.info("GUI main loop started")
        except Exception as e:
            logger.error(f"Error in GUI main loop: {str(e)}", exc_info=True)