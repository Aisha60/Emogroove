from flask import Flask, render_template, request, jsonify, redirect, url_for, session

import subprocess
import pandas as pd
import os
from musicRecommender import recommend_songs_by_emotion, get_emotion_from_file

app = Flask(__name__)
app.secret_key = 'my_hciProject'

# Load the dataset
file_path = 'data_moods.xlsx'
df = pd.read_excel(file_path)

def read_users_from_file():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                fields = line.strip().split(':')
                if len(fields) == 3:
                    username, password, email = fields
                    users[username] = {'password': password, 'email': email}
    return users

# Load users at startup
users = read_users_from_file()

#entry point is login page
@app.route ('/')
def login():
    return render_template('login.html')

#serve assets 
@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)

# Authenticate the data given by user against the saved data
@app.route('/login', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username]['password'] == password:
        session['username'] = username
        return redirect(url_for('home'))
    else:
        return render_template('login.html', error='Invalid credentials')

# Register new user
@app.route('/signup')
def signup():
    return render_template('sign_up.html')

# Register new user and then redirect to login page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username in users :
            return render_template('sign_up.html', error='Username already exists. Choose another')
        else:
            users[username] = {'password': password, 'email': email}
            with open('users.txt', 'a') as f:
                f.write(f'{username}:{password}:{email}\n')
            return redirect(url_for('login'))
    return render_template('sign_up.html')

# render home page to user
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login', error = "Please login first to continue"))

# render webcam page 
@app.route('/webcam', methods = ['GET'])
def webcam():
    if 'username' in session:
        return render_template('web_cam.html')
    else:
        return redirect(url_for('login'))
    
# open webcam capture image and redirects to recommend route 
@app.route('/captureImage' , methods = ['GET'])
def captureImage():
    if 'username' in session:
        try:
            subprocess.run(['python', 'emotiondetection.py'])
            emotion = get_emotion_from_file()
            return redirect(url_for('recommend', emotion=emotion))
        except Exception as e:
            return str(e), 500
    else:
        return redirect(url_for('login', error="Please login first to continue"))

# recommend songs based on captured emotion 
@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        emotion = get_emotion_from_file()
        songs = recommend_songs_by_emotion(emotion)
        return render_template('playlist.html', songs=songs, emotion=emotion)
    except Exception as e:
        return str(e), 500

# renders feedback page for users
@app.route('/feedback', methods = ['POST' , 'GET'])
def feedback():
    if request.method == 'GET':
        return render_template('feedback.html')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
