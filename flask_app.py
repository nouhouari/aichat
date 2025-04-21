from twilio.rest import Client
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from trainingdata import data

app = Flask(__name__)

account_sid = 'XXXXXXXXXXXX'
auth_token = 'XXXXXXXXXXX'

client = Client(account_sid, auth_token)
genai.configure(api_key='XXXXXXXXXXXXXXXXX')
model = genai.GenerativeModel('gemini-1.5-flash')
chat_session = model.start_chat(history=data)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/whatsapp', methods=['POST'])
def handle_whatsapp():
  # Get the message from Twilio
  message_body = request.form.get('Body')
  from_number = request.form.get('From')
  print(message_body)
  print(from_number)
  send_message(message_body, from_number)
  return jsonify({'status': 'success'})

def send_message(msg, to):
  # Send a response to the user
  client.messages.create(
      from_='whatsapp:+14155238886',
      body=call_ai(msg),
      to=to)
      # The user's WhatsApp number

def call_ai(prompt):
  print("prompt: " + prompt)
  response = chat_session.send_message(prompt)
  print("Response: " + response.text)
  if (len(response.text) >= 1600):
    res = response.text[:1590]+'...'
  else:
    res = response.text
  return res

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
