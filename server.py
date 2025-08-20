from flask import Flask, render_template, request, session, redirect, url_for # main server stuff
from flask_socketio import SocketIO, emit # more server stuff(messages)
import subprocess # to open the port if not opened already | Linux only?
import socket # only to get the local IP address
import markdown # message formatting(bold, italic)
import time # append time at the end of messages
import json # message file? maybe
import os # message file management

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

messages = ['Welcome to the chat server!\nRemember: <bold>CHILL OUT</bold>']  # Store chat messages here

local_time = time.strftime("%I:%M %p")  # Get the local 12-hour time

# Open the port using subprocess (for firewall configuration)
def open_port(port):
    try:
        subprocess.run(["sudo", "ufw", "allow", f"{port}/tcp"], check=True)
        print(f"Port {port} opened successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to open port {port}: {e}")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', messages=messages)

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonymous')
    raw_msg = data['message']
    if raw_msg.startswith('/'):
        if username != 'admin' and username != 'storm':
            emit('message', {'message': 'You are not authorized to use this command.'}, broadcast=True)
            return
        elif raw_msg == '/clear':
            messages.clear()
            emit('message', {'message': 'Chat cleared.'}, broadcast=True)
    msg = markdown.markdown(f"{username}: {raw_msg}")
    if msg.startswith("<p>") and msg.endswith("</p>"):
        msg = msg[3:-4]  # Strip the <p> tags
    messages.append(f"{msg} <small>{local_time}</small>")  # Append time to the message
    emit('message', {'message': msg + f"    <small>{local_time}</small>"}, broadcast=True) # would be "username: message"
def save_messages():
    with open('messages.json', 'w') as f:
        json.dump(messages, f)
def load_messages():
    if os.path.exists('messages.json'):
        with open('messages.json', 'r') as f:
            return json.load(f)
    return ['Welcome to the chat server!\nRemember: CHILL OUT']

@app.route('/admin')
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/about')
def about():
    return render_template('about.html')

@socketio.on('connect')
def handle_connect():
    username = session.get('username', 'Anonymous')
    join_message = f"{username} has joined the chat."
    messages.append(join_message)
    emit('message', {'message': join_message}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username', 'Anonymous')
    leave_message = f"{username} has left the chat."
    messages.append(leave_message)
    emit('message', {'message': leave_message}, broadcast=True)

if __name__ == "__main__":
    port = 8000
    ip = socket.gethostbyname(socket.gethostname())
    #open_port(port)
    socketio.run(app, host=ip, port=port)
