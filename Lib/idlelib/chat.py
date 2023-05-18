import tkinter as tk
from tkinter import ttk

class Chat:

    def show_chat(parent):
        chat_app = Chat()
        chat_app.run()

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ChatGPT")
        self.window.geometry("500x400")
        self.window.configure(bg="#f0f0f0")

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

# Create an instance of the Chat class

