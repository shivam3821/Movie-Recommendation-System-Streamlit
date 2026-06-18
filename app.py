import streamlit as st
import pandas as pd
import pickle 
import requests

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"

        params = {
            "api_key": API_KEY,
            "language": "en-US"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("poster_path"):
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

        return None

    except requests.exceptions.RequestException as e:
        print("TMDB Error:", e)
        return None

def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api --> tmbd api
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


movies = pickle.load(open('movies.pkl','rb'))
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    'Select the movie name', movies_list
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.text(names[0])
        if posters[0]:
            st.image(posters[0], width=200)
        else:
            st.write("Poster not available")
    
    with c2:
        st.text(names[1])
        if posters[1]:
            st.image(posters[1], width=200)
        else:
            st.write("Poster not available")
    
    with c3:
        st.text(names[2])
        if posters[2]:
            st.image(posters[2], width=200)
        else:
            st.write("Poster not available")
    
    with c4:
        st.text(names[3])
        if posters[3]:
            st.image(posters[3], width=200)
        else:
            st.write("Poster not available")
        
    with c5:
        st.text(names[4])
        if posters[4]:
            st.image(posters[4], width=200)
        else:
            st.write("Poster not available")