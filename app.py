import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e&language=en-US'.format(movie_id)
    )
    if response.status_code == 200:
        data = response.json()
        return data.get('poster_path')  # Returns poster_path or None
    else:
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # Use the selected movie
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        
        # Fetch poster from API
        poster_path = fetch_poster(movie_id)
        if poster_path:  # Check if poster_path is valid
            recommended_movies_posters.append(f"https://image.tmdb.org/t/p/w500{poster_path}")
        else:
            recommended_movies_posters.append("https://via.placeholder.com/200x300")  # Placeholder image

    return recommended_movies, recommended_movies_posters

# Load movie data and similarity data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System') 

# Select movie from dropdown
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster, use_column_width='auto', width=150)  # Set width for clarity




