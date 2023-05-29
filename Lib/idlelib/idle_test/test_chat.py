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

    ## Makes sure the window launches correctly when called
    def test_show_chat(self):
        chat_app = Chat()
        chat_app.window.update()  # Update the window to ensure correct geometry calculations
        window_title = chat_app.window.title()
        window_geometry = chat_app.window.geometry()

        expected_title = "ChatGPT"
        expected_width = 500
        expected_height = 400

        self.assertEqual(window_title, expected_title)

        # Extract width and height from the window geometry string
        # Keeps adding random vlaues to height with each rerun ie '400+260+160'
        # So spilting to get rid of the additional values and getting the base height
        geometry_parts = window_geometry.split('+')
        actual_geometry = geometry_parts[0]
        actual_width, actual_height = map(int, actual_geometry.split('x'))

        self.assertEqual(actual_width, expected_width)
        self.assertEqual(actual_height, expected_height)


if __name__ == '__main__':
    unittest.main()
