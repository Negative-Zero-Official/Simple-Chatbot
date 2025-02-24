# Simple Chatbot

This is a basic chatbot that uses sentence embeddings to find the best response to user input. It can learn new responses and remember them for future interactions.

## Features

- Responds to predefined questions
- Learns new responses from user input
- Uses sentence embeddings for similarity matching
- Saves and loads responses from a JSON file

## Requirements

- Python 3.6+
- `sentence-transformers` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Negative-Zero-Official/Simple-Chatbot
    cd Simple-Chatbot
    ```

2. Run the code:
    ```sh
    python chatbot.py
    ```
    OR
   ```sh
   python chatbot-gui.py
   ```

## Files

- [chatbot.py](https://github.com/Negative-Zero-Official/Simple-Chatbot/blob/main/chatbot.py): Main script for the chatbot.
- [chatbot_memory.json](https://github.com/Negative-Zero-Official/Simple-Chatbot/blob/main/chatbot_memory.json): JSON file that stores the chatbot's memory of questions and responses.

## Example

```
$ python chatbot.py
Bot: Type "bye" to exit.
You: Hello
Bot: Hi there! How can I help you?
You: What is AI?
Bot: AI stands for Artificial Intelligence, which is the simulation of human intelligence in machines.
You: bye
Bot: Goodbye!
```
