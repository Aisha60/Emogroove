import pandas as pd
import os

# Load the dataset
file_path = 'data_moods.xlsx'
df = pd.read_excel(file_path)

def recommend_songs_by_emotion(emotion):
    def map_emotion_to_mood(x):
        if x == "Disgust":
            return df[df['mood'].isin(['Happy', 'Calm'])]
        elif x == "Angry":
            return df[df['mood'].isin(['Calm'])]
        elif x == "Fear":
            return df[df['mood'].isin(['Energetic', 'Calm'])]
        elif x == "Happy":
            return df[df['mood'].isin(['Happy', 'Energetic'])]
        elif x == "Sad":
            return df[df['mood'].isin(['Sad', 'Calm'])]
        elif x == "Surprise":
            return df[df['mood'].isin(['Energetic', 'Happy'])]
        return pd.DataFrame()  # Return an empty DataFrame if the emotion is not recognized

    # Filter songs based on the given emotion
    filtered_df = map_emotion_to_mood(emotion)
    playlist = filtered_df.head(30)  # Limit to at most 30 songs
    
    songs = []
    if not playlist.empty:
        for index, row in playlist.iterrows():
            song_info = f"{row['name']} - {row['album']} by {row['artist']}"
            songs.append(song_info)
    else:
        top_songs = df.nlargest(30, 'popularity')
        for index, row in top_songs.iterrows():
            song_info = f"{row['name']} - {row['album']} by {row['artist']}"
            songs.append(song_info)
    
    # Ensure the static directory exists
    static_dir = 'static'
    os.makedirs(static_dir, exist_ok=True)
    
    # Write the recommended songs to a text file in the static folder
    file_path = os.path.join(static_dir, 'recommended_songs.txt')
    with open(file_path, 'w') as file:
        for song in songs:
            file.write(f"{song}\n")
    return songs

def get_emotion_from_file():
    file_name = 'predicted_emotion.txt'
    try:
        with open(file_name, 'r') as file:
            emotion = file.read().strip().capitalize()
            if emotion:
                return emotion
            else:
                raise ValueError("The file is empty.")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_name}' was not found.")
