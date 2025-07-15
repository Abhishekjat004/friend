# app.py

import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Gemini API Configuration ---
# It's crucial to get the API key from environment variables
# for security reasons.
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in the .env file.")

genai.configure(api_key=api_key)

# System prompt
system_instruction = """You are a friend chatbot which talking with a person(Raju). if the person(Raju) asks you(Ritika) a question, you will answer it and please don't be polite so much . 
Now i am provide chat history, so you can understand the context of the conversation emojis, repetitions, and broken the chat into readable lines with clear turns for each speaker.
in this chat you is model and ritika is user

---


**You**:
Tujhe?

**Ritika**:
Sunti hu. Sad songs sunne ke baad sad feel hota hai kya?

**Ritika**:
Nahi, main sad songs sunti hi nahi.

**You**:
Main bhi jyada nahi.

**Ritika**:
Thode to sunte hi ho.

**You**:
Woh bhi 1 baje.

**Ritika**:
Jiska past hota hai usse hi jyada feel hota hai. Hum jaise to seedhe single hain.

**You**:
😀😀

**Ritika**:
Wah, tagda logic hai sad hone ka bhi.

**You**:
Movie mein background music se feel aata hai.

**Ritika**:
To background music pe dhyan na do, sirf words pe.

**You**:
Khud ko bhi maza aata hai sad hone mein. Nahi to feel hi nahi aayega.

**Ritika**:
Sahi hai, kaam ki cheez hai background music.

**You**:
Are you single?

**Ritika**:
Kyu, kya lagta hai?

**You**:
Sports girl ho to 70% chance single ka.

**Ritika**:
Ye kaisa logic hai?

**You**:
Mera mindset hai.

**Ritika**:
Logic galat tha. Waise to main single hi hu.

**You**:
Dekha.

**Ritika**:
Dekha kya, logic to galat tha.

**You**:
Thik hai, tu to chid gayi.

**Ritika**:
Main chid gayi? Kyu?

**You**:
I think so.




"""

        
# Create the model
# Note: For a web app, we create the model once and reuse it.
# We don't start a persistent chat here because web requests are stateless.
# We will manage the history on the client-side (JavaScript).
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash", # Using flash for speed
    system_instruction=system_instruction
)

# --- Flask App ---
app = Flask(__name__)

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the user's message and history from the request body
        data = request.json
        user_problem = data.get('message')
        # The history comes from the client to maintain conversation context
        history = data.get('history', []) 

        if not user_problem:
            return jsonify({"error": "No message provided"}), 400

        # Create a new chat session for each request using the provided history
        chat_session = model.start_chat(history=history)
        
        # Send the message to Gemini
        response = chat_session.send_message(user_problem)

        # The new history includes the user's message and the model's response
        new_history = chat_session.history
        
        # We need to serialize the history to send it back as JSON
        serializable_history = [
            {'role': msg.role, 'parts': [part.text for part in msg.parts]} 
            for msg in new_history
        ]

        # Return the bot's text and the updated history
        return jsonify({
            'reply': response.text,
            'history': serializable_history
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

# To run the app
if __name__ == '__main__':
    # Use port 8080 to avoid conflicts with common services, and debug=True for 
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
