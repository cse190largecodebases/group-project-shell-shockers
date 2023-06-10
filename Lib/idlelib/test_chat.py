import unittest
from tkinter import Tk
import tkinter as tk
from idlelib.chat import Chat
from unittest.mock import patch

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


    ## Tests the launch of the chat event
    @patch('idlelib.chat.Chat.get_api_key')
    @patch('idlelib.chat.Chat')
    def test_show_chat2(self, mock_Chat, mock_get_api_key):
        mock_get_api_key.return_value = True

        Chat.show_chat(None)

        mock_get_api_key.assert_called_once()
        mock_Chat.assert_called_once()
        mock_Chat.return_value.run.assert_called_once()

   ## Tests if window process terminates correctly
   ## Tests window 
    def test_terminate(self):
        chat_app = Chat()
        # Checking the window launch correctly
        self.assertTrue(chat_app.window.winfo_exists())

        # Call the terminate method
        chat_app.terminate()

        # Check if the window is destroyed
        # Will throw an error since it no longer exists
        # Asserting the error is thrown
        with self.assertRaises(tk.TclError):
            chat_app.window.winfo_exists()

    ## Tests the API_KEY file is made
    def test_get_api_key_file_exists(self):
        # Create a temporary API_KEY.txt file
        with open("API_KEY.txt", "w") as file:
            file.write("test_api_key")

        api_key = Chat.get_api_key()

        self.assertEqual(api_key, "test_api_key")

    ## Tests the API_KEY file does not exist
    def test_get_api_key_file_not_exists(self):
        api_key = Chat.get_api_key()

        self.assertIsNotNone(api_key)

    ## Tests to see that the api_key_window closes correctly
    ## Tests a fixed bug
    def test_api_key_window_close(self):
        # Create a flag to check if the window was closed
        self.window_closed = False

        # Define a custom on_close function that sets the flag to True
        def on_close():
            root.destroy()
            root.quit()
            self.window_closed = True

        # Override the api_key_window method in the Chat class with the custom function
        Chat.api_key_window = on_close

        # Create a root window
        root = tk.Tk()

        # Call the api_key_window method
        Chat.api_key_window()

        # Verify that the window was closed
        self.assertTrue(self.window_closed)

    ## Test it writes the api key correctly with a file exisiting
    def test_get_api_key_existing_file_with_key(self):
        # Create a temporary API_KEY.txt file with a key
        with open("API_KEY.txt", "w") as file:
            file.write("123456")

        # Call get_api_key
        api_key = Chat.get_api_key()

        # Verify that the API key is returned correctly
        self.assertEqual(api_key, "123456")

    ## Tests if the api returns none
    def test_get_api_key_existing_file_without_key(self):
        # Create an empty API_KEY.txt file
        with open("API_KEY.txt", "w") as file:
            pass

        # Call get_api_key
        api_key = Chat.get_api_key()

        # Verify that None is returned
        self.assertIsNone(api_key)


if __name__ == '__main__':
    unittest.main()