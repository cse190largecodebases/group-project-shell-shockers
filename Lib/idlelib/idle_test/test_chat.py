import unittest
from tkinter import Tk
from chat import Chat

class ChatTest(unittest.TestCase):
    ## Tests the text a user sends will be the same one used or processing and displaying
    def test_send_message(self):
        chat_app = Chat()

        initial_text = "Initial text"
        chat_app.chat_box.insert("1.0", initial_text)  # Set initial text

        message = "Test message"
        chat_app.entry.insert(0, message)  # Set the message to be sent
        chat_app.send_message()  # Call the send_message method

        expected_text = "User: " + message
        actual_text = chat_app.chat_box.get("1.0", "end")  # Get the updated text from chat_box
        actual_text = actual_text.split("AI:")[0].rstrip()  # Remove text after and including "AI:", and remove trailing whitespace

        self.assertEqual(actual_text, expected_text)




if __name__ == '__main__':
    unittest.main()
