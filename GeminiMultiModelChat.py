# import google.generativeai as ai
# from keys import API_KEY
# import time
# import random
#
# # Configure API key
# ai.configure(api_key=API_KEY)
#
#
# # Function to fetch and display models
# def fetch_and_display_models():
#     print("Fetching list of all available models...\n")
#     models = []
#
#     try:
#         list_models = ai.list_models()
#         for idx, model in enumerate(list_models, start=1):
#             models.append(model)
#             supports_chat = "generateContent" in model.supported_generation_methods
#             print(f"{idx}. Name: {model.name}")
#             print(f"   Supports generateContent: {'Yes' if supports_chat else 'No'}")
#     except Exception as e:
#         print(f"Error fetching models: {e}")
#         exit()
#
#     if not models:
#         print("No models found. Exiting.")
#         exit()
#
#     return models
#
#
# # Function to select a model
# def select_model(models):
#     print("\nEnter the number of a model to start chatting with.")
#     print("Type '0' to exit.\n")
#
#     while True:
#         try:
#             choice = int(input(f"Select a model (3-35) [other models don't support]: "))
#             if choice == 0:
#                 print("Exiting program.")
#                 exit()
#             elif 1 <= choice <= len(models):
#                 selected_model_obj = models[choice - 1]
#                 selected_model_name = selected_model_obj.name
#                 if "generateContent" not in selected_model_obj.supported_generation_methods:
#                     print("Warning: This model does NOT support `generateContent` and may not work for chat.")
#                 return selected_model_name
#             else:
#                 print("Invalid number. Try again.")
#         except ValueError:
#             print("Please enter a valid number.")
#
#
# def instant_typing_effect(text):
#     """Simulates a smooth typing effect."""
#     if "each on a new line" in text.lower() or "each on new line" in text.lower():
#         text = text.replace(", ", "\n").replace(" ", "\n")
#
#     words = text.split()
#     if len(words) <= 10:
#         print(text)
#         return
#
#     for i, word in enumerate(words):
#         print(word, end=" ", flush=True)
#         if i % 10 == 0:
#             time.sleep(random.uniform(0.12, 0.18))
#         elif any(p in word for p in [".", ",", "?", "!"]):
#             time.sleep(random.uniform(0.08, 0.12))
#
#     print()
#
#
# # Initial model setup
# models = fetch_and_display_models()
# print("_" * 100)
# selected_model_name = select_model(models)
#
#
# # Load the selected model
# def load_model(model_name):
#     try:
#         model = ai.GenerativeModel(model_name)
#         chat = model.start_chat()
#         model_name_short = model.model_name.split('/')[-1]
#         print(f"\nCurrent Selected Model: {model_name_short}")
#         print("Chatbot: Hello! (Type 'exit' to end the conversation, 'change_model' to switch models)\n")
#         return model, chat
#     except Exception as e:
#         print(f"Failed to load or start chat with model: {e}")
#         exit()
#
#
# model, chat = load_model(selected_model_name)
#
# # Chat loop
# while True:
#     msg = input("You: ").strip()
#     if not msg:
#         print("Please type something.")
#         continue
#
#     if msg.lower() == "exit":
#         print("Chatbot: Goodbye!")
#         break
#
#     if msg.lower() == "change_model":
#         print("_" * 100)
#         models = fetch_and_display_models()
#         print("_" * 100)
#         selected_model_name = select_model(models)
#         model, chat = load_model(selected_model_name)
#         continue
#
#     try:
#         response = chat.send_message(msg)
#         print("Chatbot:", end=" ", flush=True)
#         instant_typing_effect(response.text)
#     except Exception as e:
#         print(f"Error during message exchange: {e}")




import google.generativeai as ai
from keys import API_KEY
import time
import random
import os
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)

ai.configure(api_key=API_KEY)


def fetch_and_display_models():
    """get and show all the gemini models that are available"""
    print(f"{Fore.YELLOW}Fetching list of all available models...{Style.RESET_ALL}\n")
    models = []
    try:
        list_models = ai.list_models()
        for idx, model in enumerate(list_models, start=1):
            models.append(model)
            supports_chat = "generateContent" in model.supported_generation_methods
            print(f"{idx}. Name: {model.name}")
            print(f"   Supports generateContent: {'Yes' if supports_chat else 'No'}")
    except Exception as e:
        print(f"{Fore.RED}Error fetching models: {e}{Style.RESET_ALL}")
        exit(1)

    if not models:
        print(f"{Fore.RED}No models found. Exiting.{Style.RESET_ALL}")
        exit(1)

    return models


def select_model(models):
    """let the user pick a model from the list"""
    print(f"\n{Fore.CYAN}Enter the number of a model to start chatting with.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Type '0' to exit.{Style.RESET_ALL}\n")

    while True:
        try:
            choice = int(
                input(f"{Fore.GREEN}Select a model (1-{len(models)}) Total [chat models recommended 4 - 42]: {Style.RESET_ALL}"))
            if choice == 0:
                print("Exiting program.")
                exit(0)
            elif 1 <= choice <= len(models):
                selected_model_obj = models[choice - 1]
                selected_model_name = selected_model_obj.name
                if "generateContent" not in selected_model_obj.supported_generation_methods:
                    print(
                        f"{Fore.YELLOW}Warning: This model does NOT support `generateContent` and may not work for chat.{Style.RESET_ALL}")
                    confirm = input("Continue anyway? (y/n): ").lower()
                    if confirm != 'y':
                        continue
                return selected_model_name, selected_model_obj
            else:
                print(f"{Fore.RED}Invalid number. Try again.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")


def instant_typing_effect(text):
    """makes it look like it's typing smoothly with markdown formatting"""
    in_code_block = False
    formatted_lines = []

    lines = text.split('\n')
    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            current_line = Fore.CYAN + Style.BRIGHT + line + Style.RESET_ALL
        elif in_code_block:
            current_line = Fore.CYAN + line + Style.RESET_ALL
        else:
            # handle markdown formatting
            formatted_line = line
            # bold text
            while "**" in formatted_line:
                formatted_line = formatted_line.replace("**", Style.BRIGHT, 1)
                if "**" in formatted_line:
                    formatted_line = formatted_line.replace("**", Style.RESET_ALL, 1)

            # Italic text
            while "*" in formatted_line:
                formatted_line = formatted_line.replace("*", Style.DIM, 1)
                if "*" in formatted_line:
                    formatted_line = formatted_line.replace("*", Style.RESET_ALL, 1)

            current_line = formatted_line

        formatted_lines.append(current_line)

    formatted_text = '\n'.join(formatted_lines)

    # for very short responses, just print immediately
    if len(formatted_text.split()) <= 10:
        print(formatted_text)
        return

    # add a natural typing feel for longer stuff
    words = formatted_text.split()
    for i, word in enumerate(words):
        print(word, end=" ", flush=True)
        # pause a bit longer at the end of sentences and sometimes between words
        if any(p in word for p in [".", ",", "?", "!"]):
            time.sleep(random.uniform(0.1, 0.15))
        elif i % 8 == 0:  # sometimes pause between words
            time.sleep(random.uniform(0.05, 0.1))
        else:
            time.sleep(random.uniform(0.02, 0.05))  # Default typing speed

    print()  # for new line


def show_help():
    """Display available commands."""
    print("\n" + Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "Available Commands:" + Style.RESET_ALL)
    print(Fore.GREEN + "  help         " + Style.RESET_ALL + "- Shows this help message")
    print(Fore.GREEN + "  info         " + Style.RESET_ALL + "- Displays details about the current model")
    print(Fore.GREEN + "  change_model " + Style.RESET_ALL + "- Switch to a different model")
    print(Fore.GREEN + "  save         " + Style.RESET_ALL + "- Saves the conversation to a file")
    print(Fore.GREEN + "  clear        " + Style.RESET_ALL + "- Clears the current conversation")
    print(Fore.GREEN + "  history      " + Style.RESET_ALL + "- Shows conversation history")
    print(Fore.GREEN + "  exit         " + Style.RESET_ALL + "- End the conversation and exit")
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL + "\n")


def show_model_info(model_obj):
    """display all the info about the model you're using"""
    print("\n" + Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "Current Model Information:" + Style.RESET_ALL)
    print(f"{Fore.GREEN}Model Name:{Style.RESET_ALL} {model_obj.name}")
    print(f"{Fore.GREEN}Model Version:{Style.RESET_ALL} {model_obj.version}")
    print(f"{Fore.GREEN}Display Name:{Style.RESET_ALL} {model_obj.display_name}")
    print(f"{Fore.GREEN}Description:{Style.RESET_ALL} {model_obj.description}")
    print(f"{Fore.GREEN}Input Token Limit:{Style.RESET_ALL} {model_obj.input_token_limit}")
    print(f"{Fore.GREEN}Output Token Limit:{Style.RESET_ALL} {model_obj.output_token_limit}")

    # handle how temperature is shown - it could be a number or have a min/max
    try:
        if hasattr(model_obj.temperature, 'min') and hasattr(model_obj.temperature, 'max'):
            print(
                f"{Fore.GREEN}Temperature Range:{Style.RESET_ALL} {model_obj.temperature.min} to {model_obj.temperature.max}")
        else:
            print(f"{Fore.GREEN}Temperature:{Style.RESET_ALL} {model_obj.temperature}")
    except AttributeError:
        print(f"{Fore.GREEN}Temperature:{Style.RESET_ALL} Not specified")

    # handle top_p format problem yk float n int
    try:
        if hasattr(model_obj.top_p, 'min') and hasattr(model_obj.top_p, 'max'):
            print(f"{Fore.GREEN}Top-p Range:{Style.RESET_ALL} {model_obj.top_p.min} to {model_obj.top_p.max}")
        else:
            print(f"{Fore.GREEN}Top-p:{Style.RESET_ALL} {model_obj.top_p}")
    except AttributeError:
        print(f"{Fore.GREEN}Top-p:{Style.RESET_ALL} Not specified")

    # handle top_k format same issues as top_p
    try:
        if hasattr(model_obj.top_k, 'min') and hasattr(model_obj.top_k, 'max'):
            print(f"{Fore.GREEN}Top-k Range:{Style.RESET_ALL} {model_obj.top_k.min} to {model_obj.top_k.max}")
        else:
            print(f"{Fore.GREEN}Top-k:{Style.RESET_ALL} {model_obj.top_k}")
    except AttributeError:
        print(f"{Fore.GREEN}Top-k:{Style.RESET_ALL} Not specified")

    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL + "\n")


def save_conversation(conversation_history):
    """save the current chat to a file"""
    if not os.path.exists("conversations"):
        os.makedirs("conversations")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_name = conversation_history[0].get("model", "unknown")
    model_name = model_name.split('/')[-1] if '/' in model_name else model_name
    filename = f"conversations/chat_{model_name}_{timestamp}.txt"

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Conversation with model: {model_name}\n")
            file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            for entry in conversation_history[1:]:  # skip the model info entry
                role = "You" if entry["role"] == "user" else "Chatbot"
                file.write(f"{role}: {entry['content']}\n\n")

        print(f"\n{Fore.GREEN}Conversation saved to {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error saving conversation: {e}{Style.RESET_ALL}")


def show_history(conversation_history):
    """display what we've talked about so far"""
    if len(conversation_history) <= 1:  # Only model info entry or empty
        print(f"\n{Fore.YELLOW}No conversation history yet.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.YELLOW}Conversation History:{Style.RESET_ALL}\n")

    for entry in conversation_history[1:]:
        if entry["role"] == "user":
            print(f"{Fore.GREEN}You: {Style.RESET_ALL}{entry['content']}")
        else:
            print(f"{Fore.BLUE}Chatbot: {Style.RESET_ALL}{entry['content']}")
        print()  # empty line between messages



def load_model(model_name, model_obj):
    """Load the selected model and start a chat session."""
    try:
        # set up how the model generates text with some good defaults
        generation_config = {
            "temperature": 0.7,  # Medium creativity
            "top_p": 0.95,  # diverse but focused responses
            "top_k": 40,   # looks at the top 40 most likely words
            "max_output_tokens": 2048,  # response length
        }

        model = ai.GenerativeModel(model_name, generation_config=generation_config)
        chat = model.start_chat(history=[])

        model_name_short = model.model_name.split('/')[-1]
        print(f"\n{Fore.CYAN}Current Selected Model: {model_name_short}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Chatbot: {Style.RESET_ALL}Hello! Type a message to start chatting.")
        print(f"Use '{Fore.GREEN}help{Style.RESET_ALL}' to see available commands.\n")

        return model, chat, model_obj
    except Exception as e:
        print(f"{Fore.RED}Failed to load or start chat with model: {e}{Style.RESET_ALL}")
        exit(1)


def main():
    """this is where the chat app starts running"""

    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 60}")
    print(f"{' ' * 20}GEMINI CHAT INTERFACE")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")

    # get the list of models and let the user pick one
    models = fetch_and_display_models()
    print(Fore.YELLOW + "_" * 100 + Style.RESET_ALL)
    selected_model_name, selected_model_obj = select_model(models)

    # load the model
    model, chat, current_model_obj = load_model(selected_model_name, selected_model_obj)

    # keep track of our conversation, starting with info about the model
    model_name_short = selected_model_name.split('/')[-1]
    conversation_history = [{"role": "system", "model": model_name_short, "time": datetime.now().isoformat()}]

    # chat loop
    while True:
        try:
            msg = input(Fore.GREEN + "You: " + Style.RESET_ALL).strip()
            if not msg:
                print(f"{Fore.YELLOW}Please type something.{Style.RESET_ALL}")
                continue

            # handle commands
            if msg.lower() == "exit":
                print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                if len(conversation_history) > 1:  # If there was a conversation
                    save_option = input("Save this conversation before exiting? (y/n): ").lower()
                    if save_option == 'y':
                        save_conversation(conversation_history)
                break

            elif msg.lower() == "help":
                show_help()
                continue

            elif msg.lower() == "info":
                show_model_info(current_model_obj)
                continue

            elif msg.lower() == "change_model":
                print(Fore.YELLOW + "_" * 100 + Style.RESET_ALL)
                models = fetch_and_display_models()
                print(Fore.YELLOW + "_" * 100 + Style.RESET_ALL)
                selected_model_name, selected_model_obj = select_model(models)
                model, chat, current_model_obj = load_model(selected_model_name, selected_model_obj)

                # start a new chat history when the model changes
                model_name_short = selected_model_name.split('/')[-1]
                conversation_history = [
                    {"role": "system", "model": model_name_short, "time": datetime.now().isoformat()}]
                continue

            elif msg.lower() == "save":
                if len(conversation_history) <= 1:  # Only model info or empty
                    print(f"{Fore.YELLOW}No conversation to save yet.{Style.RESET_ALL}")
                else:
                    save_conversation(conversation_history)
                continue

            elif msg.lower() == "clear":
                # clear the chat history but keep using the same model
                model_name_short = model.model_name.split('/')[-1]
                conversation_history = [
                    {"role": "system", "model": model_name_short, "time": datetime.now().isoformat()}]
                chat = model.start_chat()
                print(f"\n{Fore.YELLOW}Conversation cleared.{Style.RESET_ALL}")
                continue

            elif msg.lower() == "history":
                show_history(conversation_history)
                continue

            # Add a user message to history
            conversation_history.append({"role": "user", "content": msg, "time": datetime.now().isoformat()})

            # show a little "thinking" animation
            print(f"{Fore.BLUE}Chatbot:{Style.RESET_ALL}", end=" ", flush=True)
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.3)
            print("\b\b\b   \b\b\b", end="", flush=True)  # Clear the dots

            # get the chatbot's response
            response = chat.send_message(msg)
            instant_typing_effect(response.text)

            # add the chatbot's response to our chat history
            conversation_history.append(
                {"role": "assistant", "content": response.text, "time": datetime.now().isoformat()})

        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Interrupted. Type 'exit' to quit or continue chatting.{Style.RESET_ALL}")
            continue
        except Exception as e:
            print(f"\n{Fore.RED}Error during message exchange: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Attempting to continue...{Style.RESET_ALL}")
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.CYAN}Program terminated by user. Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        print(f"Please check your API key and internet connection.")
