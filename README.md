EmoGroove: Real-time Emotion-Detection based Music Recommendar

**Project Idea:** 
"EmoGroove" is an innovative application that leverages real-time facial expression analysis to 
recommend music tailored to users' emotional states. Through webcam capture, the application 
detects users' facial expressions, interprets their mood, and suggests music that aligns with their 
emotional state.

**Tools/Techniques:**
Python:
Utilized for back-end development and NLP tasks.
Ensures seamless integration of all project components.

OpenCV (Open Source Computer Vision Library):
Implemented for facial detection and expression recognition.
Captures users' emotional cues from webcam input.

Dlib:
Used for precise facial landmark detection.
Enhances the accuracy of emotion recognition algorithms.

Emotion file:
Curated a comprehensive database containing emotions and corresponding music genres or songs.
Enables precise recommendations based on detected moods.

Facial Expression Detection:
Model: Used pre-trained CNN models from Hugging Face's library for facial expression recognition.
Implementation: Employed OpenCV for facial detection and Dlib for landmark detection. Then, utilized the pre-trained CNN model to recognize facial expressions.
Integration: Combined these components to detect users' facial expressions in real-time.

Flask:
Python library used to integrate the back-end model with the web interface.

Web Interface:
Developed using HTML, CSS, and JavaScript.

Excel Files:
Used for saving music recommendations and captured emotions.
