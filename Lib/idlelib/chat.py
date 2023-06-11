import tkinter as tk
from tkinter import ttk
import openai

class Chat:

    # Function called in Editor.py to launch event
    def show_chat(parent):
        # Gets API key from file
        key = Chat.get_api_key()
        if key:
            # If the key exists.....
            # Create an ai model
            openai.api_key = key
            models = openai.Model.list()
            # Create the process and run ir
            chat_app = Chat()
            chat_app.run()


    # Run process
    def run(self):
        self.window.mainloop()


    # Use to close the process when closing the window
    def terminate(self):
        # Fixes the error
        self.window.destroy()
        self.window.quit()  # Exit the tkinter event loop


    # Grabs API key from the file    
    def get_api_key():
        open_window = True
        try:
            # If the key exists return it
            with open("API_KEY.txt", "r") as file:
                api_key = file.readline().strip()
                if api_key:
                    return api_key

        except FileNotFoundError:
            # File does not exist
            with open("API_KEY.txt", "w") as file:
                pass

        if open_window:
            # If the file or api key does not exists....
            # Launch the window to ask for it
            Chat.api_key_window()
            with open("API_KEY.txt", "r") as file:
                api_key = file.readline().strip()
                if api_key:
                    return api_key


    # Tkinter window to ask for api key
    def api_key_window():
        # Function to use the submit button
        def submit():
            # Format the key
            entered_api_key = entry.get().strip()
            if entered_api_key:
                # write the key to the file
                with open("API_KEY.txt", "w") as file:
                    file.write(entered_api_key)

        # Called when window is closed or submittion is done
        def on_close():
            root.destroy()
            root.quit()

        # Setting up the tkinter window
        root = tk.Tk()
        root.title("ChatGPT")
        root.geometry("500x400")
        root.configure(bg="#f0f0f0")
        # Set up the protocol when window is closes
        root.protocol("WM_DELETE_WINDOW", on_close)
        label = tk.Label(root, text="Please enter your API key:", font=("Arial", 12), bg="#f0f0f0")
        label.pack(pady=10)
        # Set up the entry box
        entry = tk.Entry(root, width=60, font=("Arial", 12))
        entry.pack()

        submit_button_style = ttk.Style()
        submit_button_style.configure("SubmitButton.TButton", font=("Arial", 12))

        # calles the submit function
        submit_button = ttk.Button(root, text="Submit", style="SubmitButton.TButton", command=submit)
        submit_button.pack(pady=10)

        # Runs the window
        root.mainloop()


    # The chat event itself
    def __init__(self):
        # Setup the tkinter window
        self.window = tk.Tk()
        self.window.title("ChatGPT")
        self.window.geometry("500x400")
        self.window.configure(bg="#f0f0f0")

        # Bind the close protocol
        self.window.protocol("WM_DELETE_WINDOW", self.terminate)

        # The tabs interface
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Create the chat tab
        self.create_chat_tab()

        # Create the general tab
        self.create_general_tab()


    # Creates the chat tab............
    def create_chat_tab(self):
        # Create a new tab for chat
        chat_tab = ttk.Frame(self.notebook)
        self.notebook.add(chat_tab, text="Python")

        # Create the chat display
        self.chat_box = tk.Text(chat_tab, height=15, width=60, state=tk.DISABLED,
                                bg="#ffffff", fg="#000000", font=("Arial", 12))
        self.chat_box.pack(pady=10)

        # Create a vertical scrollbar for the chat display
        scrollbar = tk.Scrollbar(chat_tab)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the chat display to work with the scrollbar
        self.chat_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.chat_box.yview)

        # Create the user input field
        self.entry = tk.Entry(chat_tab, width=60, font=("Arial", 12))
        self.entry.pack(pady=10)

        # Create the send button
        send_button_style = ttk.Style()
        send_button_style.configure("SendButton.TButton", font=("Arial", 12))
        self.send_button = ttk.Button(chat_tab, text="Send", style="SendButton.TButton",
                                      command=self.send_message)
        self.send_button.pack()


    # Creates the general tab................
    def create_general_tab(self):
        # Create a new tab for general
        general_tab = ttk.Frame(self.notebook)
        self.notebook.add(general_tab, text="General")

        # Create the general display
        self.general_box = tk.Text(general_tab, height=15, width=60, state=tk.DISABLED,
                                   bg="#ffffff", fg="#000000", font=("Arial", 12))
        self.general_box.pack(pady=10)

        # Create a vertical scrollbar for the general display
        scrollbar = tk.Scrollbar(general_tab)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the general display to work with the scrollbar
        self.general_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.general_box.yview)

        # Create the user input field
        self.general_entry = tk.Entry(general_tab, width=60, font=("Arial", 12))
        self.general_entry.pack(pady=10)

        # Create the send button
        send_button_style = ttk.Style()
        send_button_style.configure("SendButton.TButton", font=("Arial", 12))
        self.general_send_button = ttk.Button(general_tab, text="Send", style="SendButton.TButton",
                                              command=self.send_general_message)
        self.general_send_button.pack()


    # Message is sent to ai model to process
    def send_message(self, entry=None, chat_box=None):
        # Creating a text entry and chat box
        if not entry:
            entry = self.entry
        if not chat_box:
            chat_box = self.chat_box

        message = entry.get()
        # Formatting the question
        if message.strip() != "":
            chat_box.configure(state=tk.NORMAL)
            chat_box.insert(tk.END, "User: " + message + "\n")
            chat_box.configure(state=tk.DISABLED)
            entry.delete(0, tk.END)
            # Process user message here
            # Generate AI response
            models = openai.Model.list()

            # Send to openai model
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": message + ", please link me to the python documentation link"}]
            )

            response = chat_completion.choices[0].message.content
            chat_box.configure(state=tk.NORMAL)
            chat_box.insert(tk.END, response + "\n")
            chat_box.configure(state=tk.DISABLED)


    # Same thing as before normal send_message
    def send_general_message(self):
        message = self.general_entry.get()
        if message.strip() != "":
            self.general_box.configure(state=tk.NORMAL)
            self.general_box.insert(tk.END, "User: " + message + "\n")
            self.general_box.configure(state=tk.DISABLED)
            self.general_entry.delete(0, tk.END)
            # Process user message here for the general tab
            # Generate AI response for the general tab
            models = openai.Model.list()

            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}]
            )

            response = chat_completion.choices[0].message.content
            self.general_box.configure(state=tk.NORMAL)
            self.general_box.insert(tk.END, response + "\n")
            self.general_box.configure(state=tk.DISABLED)