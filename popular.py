import streamlit as st
import pickle
import pandas as pd
import requests
from bokeh.models.widgets import Div
import streamlit as st
import webbrowser
import time
import random

st.title("Top popular movies")
@st.cache_data
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


popular_movies = movies[movies['vote_average'] > 8.0]
popular_movie_ids = popular_movies['id']
popular_movie_tags=popular_movies['tags']

num_columns = 3  # Number of columns to display the movie names and posters
chunk_size = (len(popular_movie_ids) + num_columns - 1) // num_columns
movie_chunks = [popular_movie_ids[i:i + chunk_size] for i in range(0, len(popular_movie_ids), chunk_size)]

col1, col2, col3 = st.columns(num_columns)

with col1:
    for movie_id in movie_chunks[0]:
        movie_name = movies[movies['id'] == movie_id]['title'].values[0]
        movie_tags = movies[movies['id'] == movie_id]['tags'].values[0]
        movie_poster = fetch_poster(movie_id)
        st.image(movie_poster, use_column_width=True)
        st.write(movie_name)
        info = st.button("click for description", key=f"info_button_{movie_id}")
        if info:
            st.write(movie_tags)
        watch = st.button("watch for free", key=f"info_button_{movie_tags}")
        if watch:
            # If the description is not already shown, display it
            url = 'https://movie-web.app/search/movie/'+movie_name
            webbrowser.open_new_tab(url)


        # Display the full movie name as a scrolling bar


with col2:
    for movie_id in movie_chunks[1]:
        movie_name = movies[movies['id'] == movie_id]['title'].values[0]
        movie_tags = movies[movies['id'] == movie_id]['tags'].values[0]
        movie_poster = fetch_poster(movie_id)
        st.image(movie_poster, use_column_width=True)
        st.write(movie_name)

        info = st.button("click for description", key=f"info_button_{movie_id}")
        if info:
            st.write(movie_tags)
        watch = st.button("watch for free", key=f"info_button_{movie_tags}")
        if watch:
            # If the description is not already shown, display it
            movie_name = movie_name
            formatted_name = movie_name.replace(" ", "-")
            url='https://movie-web.app/search/movie/'+movie_name
            #url = 'https://www.justchill.tv/search?query='+movie_name+'&type=movie'
            webbrowser.open_new_tab(url)


with col3:
    for movie_id in movie_chunks[2]:
        movie_name = movies[movies['id'] == movie_id]['title'].values[0]
        movie_tags = movies[movies['id'] == movie_id]['tags'].values[0]
        movie_poster = fetch_poster(movie_id)
        st.image(movie_poster, use_column_width=True)
        st.write(movie_name)
        info = st.button("click for description", key=f"info_button_{movie_id}")

        description_container = st.empty()  # Create an empty container for the movie description
            
        if info:
            st.write(movie_tags)
        watch = st.button("watch for free", key=f"info_button_{movie_tags}")

        if watch:
            # If the description is not already shown, display it
            url='https://movie-web.app/search/movie/'+movie_name
            #url = 'https://www.justchill.tv/search?query='+movie_name+'&type=movie'
            webbrowser.open_new_tab(url)
        
        