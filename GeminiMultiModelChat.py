import google.generativeai as ai
from keys import API_KEY  # Import API key from a separate file for security
import time
import random

# Configure API key
ai.configure(api_key=API_KEY)

# List all models
print("Fetching list of all available models...\n")
models = []

try:
    list_models = ai.list_models()
    for idx, model in enumerate(list_models, start=1):
        models.append(model)
        supports_chat = "generateContent" in model.supported_generation_methods
        print(f"{idx}. Name: {model.name}")
        print(f"   Supports generateContent: {'Yes' if supports_chat else 'No'}")
except Exception as e:
    print(f"Error fetching models: {e}")
    exit()

if not models:
    print("No models found. Exiting.")
    exit()

print("_" * 100)

# Model selection
print("\nEnter the number of a model to start chatting with.")
print("Type '0' to exit.\n")

while True:
    try:
        choice = int(input(f"Select a model (3-35) [other models don't support]: "))
        if choice == 0:
            print("Exiting program.")
            exit()
        elif 1 <= choice <= len(models):
            selected_model_obj = models[choice - 1]
            selected_model_name = selected_model_obj.name
            if "generateContent" not in selected_model_obj.supported_generation_methods:
                print("Warning: This model does NOT support `generateContent` and may not work for chat.")
            break
        else:
            print("Invalid number. Try again.")
    except ValueError:
        print("Please enter a valid number.")

# Load the selected model
try:
    model = ai.GenerativeModel(selected_model_name)
    chat = model.start_chat()
except Exception as e:
    print(f"Failed to load or start chat with model: {e}")
    exit()

model_name = model.model_name.split('/')[-1]
print(f"\nCurrent Selected Model: {model_name}")
print("Chatbot: Hello! (Type 'exit' to end the conversation)\n")


def instant_typing_effect(text):
    """Simulates a smooth typing effect."""
    if "each on a new line" in text.lower() or "each on new line" in text.lower():
        text = text.replace(", ", "\n").replace(" ", "\n")

    words = text.split()
    if len(words) <= 10:
        print(text)
        return

    for i, word in enumerate(words):
        print(word, end=" ", flush=True)
        if i % 10 == 0:
            time.sleep(random.uniform(0.12, 0.18))
        elif any(p in word for p in [".", ",", "?", "!"]):
            time.sleep(random.uniform(0.08, 0.12))

    print()


# Chat loop
while True:
    msg = input("You: ").strip()
    if not msg:
        print("Please type something.")
        continue
    if msg.lower() == "exit":
        print("Goodbye!")
        break
    try:
        response = chat.send_message(msg)
        print("Chatbot:", end=" ", flush=True)
        instant_typing_effect(response.text)
    except Exception as e:
        print(f"Error during message exchange: {e}")
