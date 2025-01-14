import streamlit as st
import requests

# TMDB API key (replace with your key)
api_key = 'e9049fef70036ad6e036411e17e24ac4'

# Fetch genres
def fetch_genres():
    url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    return data.get('genres', [])

# Fetch popular movies for a specific genre
def fetch_popular_movies_by_genre(genre_id):
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}&sort_by=popularity.desc'
    response = requests.get(url)
    data = response.json()
    return data.get('results', [])

# Fetch the poster URL for the movie
def fetch_poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# Apply dark mode styles
def apply_styles():
    st.markdown("""
        <style>
            body {
                background-color: #121212;
                color: white;
            }
            .cool-title {
                font-size: 48px;
                font-weight: bold;
                background: linear-gradient(to left, #ff6347, #6a5acd, #32cd32);
                -webkit-background-clip: text;
                color: transparent;
                text-align: center;
                animation: fadeIn 2s ease-out;
                text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.7);
            }
            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            .stTextInput>div>div>input {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 12px;
                width: 100%;
                max-width: 600px;
            }
            .stButton>button {
                background-color: #444444;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: #555555;
            }
            .movie-card {
                display: flex;
                flex-direction: column;
                align-items: center;
                margin: 10px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .movie-card:hover {
                transform: scale(1.05);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.7);
            }
            .movie-img {
                border-radius: 15px;
                transition: transform 0.3s ease;
            }
            .movie-img:hover {
                transform: scale(1.1);
            }
        </style>
    """, unsafe_allow_html=True)

# Streamlit UI
apply_styles()  # Apply dark mode styles

# Cool system title
st.markdown('<h1 class="cool-title">FindMovie: A Movie Recommendation System</h1>', unsafe_allow_html=True)

# Fetch genres from TMDB API
genres = fetch_genres()

# Genre dropdown
selected_genre = st.selectbox("Select a Genre:", [genre['name'] for genre in genres])

# Find the genre ID based on the selected genre
selected_genre_id = next(genre['id'] for genre in genres if genre['name'] == selected_genre)

# Fetch popular movies for the selected genre
if selected_genre:
    st.markdown(f"## Popular movies in the '{selected_genre}' genre:")
    genre_movies = fetch_popular_movies_by_genre(selected_genre_id)
    
    if genre_movies:
        cols = st.columns(5)
        for i, movie in enumerate(genre_movies):
            with cols[i % 5]:  # Cycle through columns for each movie
                poster_url = fetch_poster_url(movie['poster_path'])
                if poster_url:
                    st.markdown(f'''
                        <div class="movie-card">
                            <a href="https://www.themoviedb.org/movie/{movie["id"]}" target="_blank">
                                <img src="{poster_url}" class="movie-img" />
                            </a>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.write("Poster not available")
