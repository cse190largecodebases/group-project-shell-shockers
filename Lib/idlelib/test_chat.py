from idlelib.chat import Chat
import unittest
from tkinter import Tk
import tkinter as tk
from unittest.mock import patch, MagicMock
import os


class ChatTest(unittest.TestCase):
   ## Tests to see if it opens the correct file
    @patch("builtins.open")
    def test_get_api_key_with_file(self, mock_open):
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.readline.return_value = "my_api_key"
        api_key = Chat.get_api_key()
        self.assertEqual(api_key, "my_api_key")

    ## Tests to see if it grabs the correct API key
    def test_get_api_key_exists(self):
        # Create a test file with a valid API key
        with open("API_KEY.txt", "w") as file:
            file.write("VALID_API_KEY")

        # Call the get_api_key method
        api_key = Chat.get_api_key()

        # Assert that the returned API key is correct
        self.assertEqual(api_key, "VALID_API_KEY")

        # Clean up the test file
        os.remove("API_KEY.txt")

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

   ## Mocks the AI repsonse and makes sure the text box displays the user
   ## and 'AI' repsonse
    @patch("openai.Model.list")
    @patch("openai.ChatCompletion.create")
    def test_send_message(self, mock_create, mock_list):
        # Create an instance of the Chat class
        chat_app = Chat()

        # Define a custom function to mock openai.Model.list()
        def mock_model_list():
            mock_model = MagicMock()
            mock_model.id = "gpt-3.5-turbo"
            return [mock_model]

        # Define a custom function to mock openai.ChatCompletion.create()
        def mock_chat_completion(*args, **kwargs):
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "AI response"
            return mock_response

        # Assign the custom functions as the side effects of the mocked methods
        mock_list.side_effect = mock_model_list
        mock_create.side_effect = mock_chat_completion

        # Set up the initial state of the chat box and entry field
        chat_app.entry.insert(tk.END, "User message")
        chat_app.chat_box.configure(state=tk.NORMAL)
        chat_app.chat_box.insert(tk.END, "Previous message\n")
        chat_app.chat_box.configure(state=tk.DISABLED)

        # Call the send_message method
        chat_app.send_message()

        # Check if the AI response is correctly added to the chat box
        chat_app.chat_box.configure(state=tk.NORMAL)
        chat_text = chat_app.chat_box.get("1.0", tk.END).strip()
        self.assertEqual(chat_text, "Previous message\nUser: User message\nAI response")
        chat_app.chat_box.configure(state=tk.DISABLED)

        # Check if the entry field is cleared
        entry_text = chat_app.entry.get()
        self.assertEqual(entry_text, "")

        # Check if openai.Model.list and openai.ChatCompletion.create were called with the correct arguments
        mock_list.assert_called_once()
        mock_create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "User message, please link me to the python documentation link"}]
        )


   ## Mocks the AI repsonse and makes sure the text box displays the user
    ## and 'AI' repsonse
    @patch("openai.Model.list")
    @patch("openai.ChatCompletion.create")
    def test_send_general_message(self, mock_create, mock_list):
        # Create an instance of the Chat class
        chat_app = Chat()

        # Define a custom function to mock openai.Model.list()
        def mock_model_list():
            mock_model = MagicMock()
            mock_model.id = "gpt-3.5-turbo"
            return [mock_model]

        # Define a custom function to mock openai.ChatCompletion.create()
        def mock_chat_completion(*args, **kwargs):
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "AI response"
            return mock_response

        # Assign the custom functions as the side effects of the mocked methods
        mock_list.side_effect = mock_model_list
        mock_create.side_effect = mock_chat_completion

        # Set up the initial state of the chat box and entry field
        chat_app.general_entry.insert(tk.END, "User message")
        chat_app.general_box.configure(state=tk.NORMAL)
        chat_app.general_box.insert(tk.END, "Previous message\n")
        chat_app.general_box.configure(state=tk.DISABLED)

        # Call the send_general_message method
        chat_app.send_general_message()

        # Check if the AI response is correctly added to the chat box
        chat_app.general_box.configure(state=tk.NORMAL)
        chat_text = chat_app.general_box.get("1.0", tk.END).strip()
        expected_text = "Previous message\nUser: User message\nAI response"
        self.assertEqual(chat_text, expected_text)
        chat_app.general_box.configure(state=tk.DISABLED)

        # Check if the entry field is cleared
        entry_text = chat_app.general_entry.get()
        self.assertEqual(entry_text, "")

        # Check if openai.Model.list and openai.ChatCompletion.create were called with the correct arguments
        mock_list.assert_called_once()
        mock_create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "User message"}]
        )


    # def test_submit_button(self):
    #     # Create a dummy file to simulate existing API_KEY.txt
    #     with open("API_KEY.txt", "w") as file:
    #         file.write("dummy_api_key")

    #     # Run the api_key_window() function
    #     Chat.api_key_window()

    #     # Simulate entering a new API key in the entry widget
    #     root = tk._default_root
    #     entry_widget = root.children['.!entry']
    #     entry_widget.insert(0, "new_api_key")

    #     # Simulate clicking the submit button
    #     submit_button = root.children['.!button']
    #     submit_button.invoke()

    #     # Verify that the new API key is written to the file
    #     with open("API_KEY.txt", "r") as file:
    #         content = file.read()
    #     self.assertEqual(content, "new_api_key")

    #     # Clean up the dummy file
    #     os.remove("API_KEY.txt")



if __name__ == '__main__':
    unittest.main()