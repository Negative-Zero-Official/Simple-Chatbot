from sentence_transformers import SentenceTransformer, util
import json
import tkinter as tk
from tkinter import simpledialog

class SimpleChatbot:
    def __init__(self, memory_file="chatbot_memory.json"):
        self.memory_file = memory_file
        self.responses = self.load_memory()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def train(self, question, response):
        self.responses[question.lower()] = response
        self.save_memory()

    def get_response(self, user_input):
        user_input = user_input.lower()
        if not self.responses:
            self.responses = {}

        input_embedding = self.model.encode(user_input, convert_to_tensor=True)
        best_match, best_score = None, 0

        for question in self.responses.keys():
            question_embedding = self.model.encode(question, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(input_embedding, question_embedding).item()

            if similarity > best_score:
                best_match, best_score = question, similarity

        if best_score > 0.75:
            return self.responses[best_match]
        else:
            new_response = simpledialog.askstring("Input", "I don't know how to respond to that. How should I reply? (Type --opt-out if you don't want to add anything to memory)")
            if new_response.lower() == "--opt-out":
                return "Got it. I won't add anything to memory."
            self.train(user_input, new_response)
            return "Got it. I'll remember that next time."

    def save_memory(self):
        with open(self.memory_file, 'w') as file:
            json.dump(self.responses, file)

    def load_memory(self):
        try:
            with open(self.memory_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Some error occurred while loading the memory file.")
            return {}

def chatgpt_typing_effect(text_widget, text, delay=50, chunk_size=2):
    def type_character(i=0):
        if i < len(text):
            text_widget.config(state='normal')
            text_widget.insert(tk.END, text[i:i+chunk_size])
            text_widget.config(state='disabled')
            text_widget.yview(tk.END)
            text_widget.after(delay, type_character, i+chunk_size)
        else:
            text_widget.config(state='normal')
            text_widget.insert(tk.END, "\n")
            text_widget.config(state='disabled')
            text_widget.yview(tk.END)
    type_character()

class ChatbotGUI:
    def __init__(self, root):
        self.bot = SimpleChatbot()
        self.root = root
        self.root.title("Simple Chatbot")

        self.chat_log = tk.Text(root, state='disabled', wrap='word')
        self.chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(padx=10, pady=10, fill=tk.X)

        self.entry = tk.Entry(self.entry_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        self.display_message("Bot: Hi there! Type \"bye\" to exit.", typing_effect = True)

    def send_message(self, event=None):
        user_input = self.entry.get()
        if user_input.lower() == "bye":
            self.display_message("Bot: Goodbye!")
            self.root.quit()
        else:
            self.display_message(f"You: {user_input}")
            response = self.bot.get_response(user_input)
            self.display_message(f"Bot: {response}", typing_effect=True)
        self.entry.delete(0, tk.END)

    def display_message(self, message, typing_effect=False):
        if typing_effect:
            chatgpt_typing_effect(self.chat_log, message)
        else:
            self.chat_log.config(state='normal')
            self.chat_log.insert(tk.END, message + "\n")
            self.chat_log.config(state='disabled')
            self.chat_log.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatbotGUI(root)
    root.mainloop()