import streamlit as st
import requests

# TMDB API key (replace with your key)
api_key = 'e9049fef70036ad6e036411e17e24ac4'

# Search for a movie by title
def search_movie(query):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}'
    response = requests.get(url)
    data = response.json()

    if 'results' not in data:
        st.error("No results found.")
        return []
    
    return data['results']

# Fetch movie recommendations from TMDB based on movie ID
def fetch_recommendations(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'results' not in data:
        st.error("No recommendations found.")
        return []

    return data['results']

# Fetch the poster URL for the movie
def fetch_poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# Streamlit UI
st.title("FindMovie: A Movie Recommendation System")

# Search bar for movies
search_query = st.text_input("Search for a movie:")

# Perform search if the user enters a query
if search_query:
    movies = search_movie(search_query)

    if movies:
        st.write(f"Results for '{search_query}':")
        cols = st.columns(5)  # Display 5 posters per row

        for i, movie in enumerate(movies):
            with cols[i % 5]:  # Cycle through columns for each movie
                poster_url = fetch_poster_url(movie['poster_path'])
                if poster_url:
                    # Make the poster clickable, leading to the movie's TMDB page
                    st.markdown(f'<a href="https://www.themoviedb.org/movie/{movie["id"]}" target="_blank"><img src="{poster_url}" width="150"/></a>', unsafe_allow_html=True)
                else:
                    st.write("Poster not available")
