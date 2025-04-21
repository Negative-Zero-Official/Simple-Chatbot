from sentence_transformers import SentenceTransformer, util
import json
import sys
import time

class SimpleChatbot:
    def __init__(self, memory_file = "chatbot_memory.json"):
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
        
        input_embedding = self.model.encode(user_input, convert_to_tensor = True)
        best_match, best_score = None, 0
        
        for question in self.responses.keys():
            question_embedding = self.model.encode(question, convert_to_tensor = True)
            similarity = util.pytorch_cos_sim(input_embedding, question_embedding).item()
            
            if similarity > best_score:
                best_match, best_score = question, similarity
        
        if best_score > 0.75:
            return self.responses[best_match] + f" Cosine score: {best_score:.5f}"
        else:
            chatgpt_typing_effect(f"Cosine score: {best_score:.5f} I don't know how to respond to that. How should I reply? Enter expected output: (Type --opt-out if you don't want to add anything to memory)", chunk_size = 2)
            new_response = input()
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
            print("Some error ocurred while loading the memory file.")
            return {}

def chatgpt_typing_effect(text, delay=0.05, chunk_size=1):
    for i in range(0, len(text), chunk_size):
        sys.stdout.write(text[i:i+chunk_size])
        sys.stdout.flush()
        time.sleep(delay)
    print()

if __name__=="__main__":
    bot = SimpleChatbot()
    print("Bot: Type \"bye\" to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            chatgpt_typing_effect("Bot: Goodbye!", chunk_size = 2)
            break
        chatgpt_typing_effect(f"Bot: {bot.get_response(user_input)}", chunk_size = 2)