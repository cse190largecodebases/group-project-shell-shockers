import tkinter as tk
from tkinter import ttk
## Find a way to import a chatgpt api key
class Chat:

    def show_chat(parent):
        Chat.get_api_key()
        chat_app = Chat()
        chat_app.run()

    def get_api_key():
        open_window = True
        try:
            with open("API_KEY.txt", "r") as file:
                api_key = file.readline().strip()
                if api_key:
                    open_window = False
                    return api_key

        except FileNotFoundError:
            with open("API_KEY.txt", "w") as file:
                pass

        if open_window:
            Chat.api_key_window()        
    
    def api_key_window():
        def submit():
            entered_api_key = entry.get().strip()
            if entered_api_key:
                root.destroy()
                with open("API_KEY.txt", "w") as file:
                    file.write(entered_api_key)
                    root.quit()
                return entered_api_key

        root = tk.Tk()
        root.title("ChatGPT")
        root.geometry("500x400")
        root.configure(bg="#f0f0f0")

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

        # Create the chat display
        self.chat_box = tk.Text(self.window, height=15, width=60, state=tk.DISABLED,
                                bg="#ffffff", fg="#000000", font=("Arial", 12))
        self.chat_box.pack(pady=10)

        # Create a vertical scrollbar for the chat display
        scrollbar = tk.Scrollbar(self.window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the chat display to work with the scrollbar
        self.chat_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.chat_box.yview)

        # Create the user input field
        self.entry = tk.Entry(self.window, width=60, font=("Arial", 12))
        self.entry.pack(pady=10)

        # Create the send button
        send_button_style = ttk.Style()
        send_button_style.configure("SendButton.TButton", font=("Arial", 12))
        self.send_button = ttk.Button(self.window, text="Send", style="SendButton.TButton",
                                      command=self.send_message)
        self.send_button.pack()

    def run(self):
        self.window.mainloop()

    def terminate(self):
        self.window.destroy()
        self.window.quit()  # Exit the tkinter event loop


    def send_message(self):
        message = self.entry.get()
        if message.strip() != "":
            self.chat_box.configure(state=tk.NORMAL)
            self.chat_box.insert(tk.END, "User: " + message + "\n")
            self.chat_box.configure(state=tk.DISABLED)
            self.entry.delete(0, tk.END)
            # Process user message here
            # Generate AI response
            response = "AI: This is the AI's response."
            self.chat_box.configure(state=tk.NORMAL)
            self.chat_box.insert(tk.END, response + "\n")
            self.chat_box.configure(state=tk.DISABLED)