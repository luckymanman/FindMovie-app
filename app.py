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
st.set_page_config(page_title="FindMovie", page_icon="🎬", layout="wide")

# Apply dark mode theme using Streamlit's custom CSS
st.markdown("""
    <style>
        body {
            background-color: #141414;
            color: white;
        }
        .css-1d391kg {
            background-color: #141414;
        }
        .stTextInput>div>div>input {
            background-color: #333;
            color: white;
        }
        .stTextInput label {
            color: white;
        }
        .stButton>button {
            background-color: #e50914;
            color: white;
        }
        .stMarkdown {
            color: white;
        }
        .movie-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 10px;
            margin: 5%;
        }
        .movie-title {
            color: white;
            font-size: 14px;
            text-align: center;
            font-weight: bold;
        }
        .movie-img {
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
        }
        .movie-img:hover {
            transform: scale(1.1);
        }
        .search-bar {
            width: 100%;
            max-width: 600px;
            margin-bottom: 20px;
        }
        .stTextInput>div>div>input {
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("FindMovie: A Movie Recommendation System")
st.markdown("### Search and discover new movies")

# Search bar for movies with dark theme
search_query = st.text_input("Search for a movie:", placeholder="Search for a movie...", key="search_query", label_visibility="collapsed", help="Enter movie title here")

# Perform search if the user enters a query
if search_query:
    movies = search_movie(search_query)

    if movies:
        st.write(f"Results for '{search_query}':")
        
        # Grid Layout for displaying movies, keeping a closer alignment
        cols = st.columns(5)  # Display 5 posters per row
        
        for i, movie in enumerate(movies):
            with cols[i % 5]:  # Cycle through columns for each movie
                poster_url = fetch_poster_url(movie['poster_path'])
                if poster_url:
                    # Movie Poster with hover effect
                    st.markdown(f'''
                        <div class="movie-card">
                            <a href="https://www.themoviedb.org/movie/{movie["id"]}" target="_blank">
                                <img src="{poster_url}" class="movie-img" width="150"/>
                            </a>
                            <div class="movie-title">{movie["title"]}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.write("Poster not available")
