import tkinter as tk
from tkinter import ttk
import openai

class Chat:
    def show_chat(parent):
        print(type(openai.api_key))
        key = Chat.get_api_key()
        if key:
            openai.api_key = key
            models = openai.Model.list()
            chat_app = Chat()
            chat_app.run()

    def get_api_key():
        open_window = True
        try:
            with open("API_KEY.txt", "r") as file:
                api_key = file.readline().strip()
                if api_key:
                    return api_key

        except FileNotFoundError:
            with open("API_KEY.txt", "w") as file:
                pass

        if open_window:
            Chat.api_key_window()
            with open("API_KEY.txt", "r") as file:
                api_key = file.readline().strip()
                if api_key:
                    return api_key

    def api_key_window():
        def submit():
            entered_api_key = entry.get().strip()
            if entered_api_key:
                root.destroy()
                with open("API_KEY.txt", "w") as file:
                    file.write(entered_api_key)
                    root.quit()

        def on_close():
            root.destroy()
            root.quit()

        root = tk.Tk()
        root.title("ChatGPT")
        root.geometry("500x400")
        root.configure(bg="#f0f0f0")
        root.protocol("WM_DELETE_WINDOW", on_close)

        label = tk.Label(root, text="Please enter your API key:", font=("Arial", 12), bg="#f0f0f0")
        label.pack(pady=10)

        entry = tk.Entry(root, width=60, font=("Arial", 12))
        entry.pack()

        submit_button_style = ttk.Style()
        submit_button_style.configure("SubmitButton.TButton", font=("Arial", 12))

        submit_button = ttk.Button(root, text="Submit", style="SubmitButton.TButton", command=submit)
        submit_button.pack(pady=10)

        root.mainloop()

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ChatGPT")
        self.window.geometry("500x400")
        self.window.configure(bg="#f0f0f0")

        # Bind the window close event to the terminate method
        self.window.protocol("WM_DELETE_WINDOW", self.terminate)

        # Create a tabbed interface
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Create the chat tab
        self.create_chat_tab()

        # Create the general tab
        self.create_general_tab()

        # Create a button to add new tabs
        # self.add_tab_button = ttk.Button(self.window, text="Add Tab", command=self.add_tab)
        # self.add_tab_button.pack(pady=10)

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

    def run(self):
        self.window.mainloop()

    def terminate(self):
        self.window.destroy()
        self.window.quit()  # Exit the tkinter event loop


    def send_message(self, entry=None, chat_box=None):
        if not entry:
            entry = self.entry
        if not chat_box:
            chat_box = self.chat_box

        message = entry.get()
        if message.strip() != "":
            chat_box.configure(state=tk.NORMAL)
            chat_box.insert(tk.END, "User: " + message + "\n")
            chat_box.configure(state=tk.DISABLED)
            entry.delete(0, tk.END)
            # Process user message here
            # Generate AI response
            models = openai.Model.list()

            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": message + ", please link me to the python documentation link"}]
            )

            response = chat_completion.choices[0].message.content
            chat_box.configure(state=tk.NORMAL)
            chat_box.insert(tk.END, response + "\n")
            chat_box.configure(state=tk.DISABLED)

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