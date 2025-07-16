import tkinter as tk
from modules.assistant import PersonalAssistantApp  # Import the assistant app from assistant.py

def main():
    # Create the main window
    root = tk.Tk()
    # Initialize the personal assistant app
    app = PersonalAssistantApp(root)
    # Run the Tkinter event loop
    root.mainloop()

# Entry point of the script
if __name__ == "__main__":
    main()
