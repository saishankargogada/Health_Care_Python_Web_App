from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace 'YOUR_CHATGPT_API_KEY' with your actual ChatGPT API key
CHATGPT_API_KEY ='CHATGPT_API_KEY'
CHATGPT_API_URL = 'https://api.openai.com/v1/chat/completions'

# Define the available health conditions and severity levels
HEALTH_CONDITIONS = ['Cold', 'Fever', 'Headache']
SEVERITY_LEVELS = ['Mild', 'Moderate', 'Severe']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        condition = request.form['condition']
        severity = request.form['severity']
        message = request.form['message']
        
        # Call the generate_chat_response function to get the chatbot's response
        response = generate_chat_response(condition, severity, message)
        return render_template('index.html', response=response)
    
    # Render the index.html template with the available health conditions and severity levels
    return render_template('index.html', conditions=HEALTH_CONDITIONS, severities=SEVERITY_LEVELS)

def generate_chat_response(condition, severity, message):
    prompt = f"You have a {severity} case of {condition}. {message}"
    # Prepare the payload for the ChatGPT API request
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'system', 'content': 'You are a helpdesk assistant.'},
                     {'role': 'user', 'content': prompt}]
    }
    headers = {
        'Authorization': f'Bearer {CHATGPT_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Send a POST request to the ChatGPT API to get the chatbot's response
    response = requests.post(CHATGPT_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        chat_response = data['choices'][0]['message']['content']
        return chat_response
    else:
        return 'Error: Failed to generate chat response.'

if __name__ == '__main__':
    app.run(debug=True)
