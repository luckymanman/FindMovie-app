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

# Fetch the poster URL for the movie
def fetch_poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# Function to toggle dark/light mode
def toggle_mode():
    if 'mode' not in st.session_state:
        st.session_state.mode = 'dark'  # Default to dark mode

    # Minimalist button at the top-right corner
    st.markdown("""
        <style>
            .theme-button {
                position: fixed;
                top: 20px;
                right: 20px;
                background-color: transparent;
                color: white;
                border: 1px solid #888;
                padding: 8px 12px;
                font-size: 14px;
                cursor: pointer;
                border-radius: 5px;
                z-index: 100;
            }

            .theme-button:hover {
                background-color: #444;
            }
        </style>
    """, unsafe_allow_html=True)

    # Switch button text based on current theme
    button_text = "Switch to Dark Mode" if st.session_state.mode == 'light' else "Switch to Light Mode"

    # Button action
    if st.markdown(f'<button class="theme-button" onclick="window.location.reload()">{button_text}</button>', unsafe_allow_html=True):
        st.session_state.mode = 'light' if st.session_state.mode == 'dark' else 'dark'


# Apply styles based on the selected mode
def apply_styles():
    if st.session_state.mode == 'dark':
        # Dark mode styles
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

                /* Responsive Columns */
                @media only screen and (max-width: 600px) {
                    .stColumn { flex: 1 1 50%; }
                    .movie-img { width: 100%; }
                }

                @media only screen and (min-width: 601px) and (max-width: 1024px) {
                    .stColumn { flex: 1 1 33%; }
                    .movie-img { width: 100%; }
                }

                @media only screen and (min-width: 1025px) {
                    .stColumn { flex: 1 1 18%; }
                    .movie-img { width: 150px; }
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        # Light mode styles
        st.markdown("""
            <style>
                body {
                    background-color: #f0f0f0;
                    color: black;
                }

                .cool-title {
                    font-size: 48px;
                    font-weight: bold;
                    background: linear-gradient(to left, #ff6347, #6a5acd, #32cd32);
                    -webkit-background-clip: text;
                    color: transparent;
                    text-align: center;
                    animation: fadeIn 2s ease-out;
                    text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                }

                @keyframes fadeIn {
                    0% { opacity: 0; }
                    100% { opacity: 1; }
                }

                .stTextInput>div>div>input {
                    background-color: #ffffff;
                    color: black;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 12px;
                    width: 100%;
                    max-width: 600px;
                }

                .stButton>button {
                    background-color: #dddddd;
                    color: black;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                }

                .stButton>button:hover {
                    background-color: #cccccc;
                }

                .movie-card {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin: 10px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                }

                .movie-card:hover {
                    transform: scale(1.05);
                    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
                }

                .movie-img {
                    border-radius: 15px;
                    transition: transform 0.3s ease;
                }

                .movie-img:hover {
                    transform: scale(1.1);
                }

                /* Responsive Columns */
                @media only screen and (max-width: 600px) {
                    .stColumn { flex: 1 1 50%; }
                    .movie-img { width: 100%; }
                }

                @media only screen and (min-width: 601px) and (max-width: 1024px) {
                    .stColumn { flex: 1 1 33%; }
                    .movie-img { width: 100%; }
                }

                @media only screen and (min-width: 1025px) {
                    .stColumn { flex: 1 1 18%; }
                    .movie-img { width: 150px; }
                }
            </style>
        """, unsafe_allow_html=True)

# Streamlit UI
toggle_mode()  # Add the toggle button to switch between modes
apply_styles()  # Apply the selected mode styles

# Cool system title
st.markdown('<h1 class="cool-title">FindMovie: A Movie Recommendation System</h1>', unsafe_allow_html=True)

# Search bar for movies
search_query = st.text_input("Search for a movie:", placeholder="Enter movie name...", key="search_query")

# Add a search button
search_button = st.button("Search")

# Perform search if the user enters a query or clicks the button
if search_query or search_button:
    movies = search_movie(search_query)

    if movies:
        st.write(f"Results for '{search_query}':")
        
        # Display movies in a grid layout with responsive columns
        cols = st.columns(5)  # Display 5 posters per row on large screens
        for i, movie in enumerate(movies):
            with cols[i % 5]:  # Cycle through columns for each movie
                poster_url = fetch_poster_url(movie['poster_path'])
                if poster_url:
                    # Movie poster without a title box beneath
                    st.markdown(f'''
                        <div class="movie-card">
                            <a href="https://www.themoviedb.org/movie/{movie["id"]}" target="_blank">
                                <img src="{poster_url}" class="movie-img" />
                            </a>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.write("Poster not available")
