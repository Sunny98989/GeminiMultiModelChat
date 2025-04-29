# Gemini AI Chatbot (Python)

A terminal-based chatbot using Google’s `google.generativeai` library to interact with Gemini models via the Generative AI API.

This script lists all available models, allows you to select one, and then starts a chat session with typing effect simulation.

---

# Features
- Model Discovery: Lists available Gemini models and their capabilities.

- Chat Interface: Smooth and dynamic chat session with real-time typing simulation.

- Conversation Management:

- View conversation history

- Save chats to timestamped text files

- Clear current session

- Model Switching: Change models on the fly without restarting the program.

- Command System: Helpful built-in commands like help, info, clear, save, exit, etc.

- Markdown & Code Styling: Enhanced formatting for bold, italic, and code blocks using colorama.

---

# Conversation Logs
Saved conversations are stored in the conversations/ directory, with filenames based on model name and timestamp.
Example:
conversations/chat_gemini-pro-vision_20250429_145330.txt

---

# Code Structure Overview:
main(): Launches and handles the chat loop.

fetch_and_display_models(): Retrieves and lists all available models.

select_model(): Handles model selection and validation.

instant_typing_effect(text): Simulates a realistic typing output.

show_help(): Displays available commands.

save_conversation(): Saves chat logs with user and bot messages.

show_model_info(): Outputs metadata about the current model.

load_model(): Prepares the model for interaction.

---

# Requirements
Make sure you have the following Python packages installed:

- pip install google-generativeai colorama
- Also, ensure you have access to the Gemini API via a valid API key.
- Python 3.7+
- Google Generative AI SDK(swdevkit)
- API Key for [Google Generative AI](https://makersuite.google.com/app)
