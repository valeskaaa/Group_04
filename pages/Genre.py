import streamlit as st
import random
import matplotlib.pyplot as plt
from movie_dataset import MovieDataset
from ollama import chat, ChatResponse

# Create an instance of MovieDataset
test_instance = MovieDataset()

# Set page configuration
st.set_page_config(page_title="Random Movie Information", page_icon="🎬", layout="wide")

# Streamlit page title
st.title("Random Movie Information")

# Filter movies with existing summaries and genres
valid_movies = test_instance.movie_metadata[
    (test_instance.movie_metadata["wiki_movie_id"].isin(test_instance.plot_summaries["wiki_movie_id"])) &
    (test_instance.movie_metadata["genres"].notna())
]

# Shuffle button
if st.button("Shuffle"):
    # Ensure there are valid movies to choose from
    if valid_movies.empty:
        st.error("No movies with summaries and genres available.")
    else:
        # Select a random movie from the filtered list
        random_index = random.randint(0, len(valid_movies) - 1)
        movie = valid_movies.iloc[random_index]
        movie_id = movie["wiki_movie_id"]
        
        # Get the movie title and summary
        movie_title = movie["movie_name"]
        plot_summary_row = test_instance.plot_summaries[test_instance.plot_summaries["wiki_movie_id"] == movie_id]
        
        if not plot_summary_row.empty:
            movie_summary = plot_summary_row["plot_summary"].values[0]
        else:
            movie_summary = "Summary not available."
        
        # Get the movie genres
        movie_genres = eval(movie["genres"]).values()
        
        # Display the information in text boxes
        st.markdown(f"### {movie_title}\n\n{movie_summary}")
        st.text_area("Genres", ", ".join(movie_genres))
        
        # Use local LLM to classify the genre
        response: ChatResponse = chat(model='mistral', messages=[
            {
                'role': 'user',
                'content': f'Classify the following movie summary into genres: {movie_summary}. Only list the genres, separated by commas. Do not include any additional information or brackets.',
            },
        ])
        
        # Extract and display the genre classification
        llm_genres = response.message.content.strip()
        st.text_area("Genre by LLM", llm_genres)
        
        # Normalize and compare genres
        identified_genres = set([genre.strip().lower() for genre in llm_genres.split(",")])
        database_genres = set([genre.strip().lower() for genre in movie_genres])
        
        matching_genres = identified_genres.intersection(database_genres)
        
        if matching_genres:
            st.markdown("### Successfully Detected Genres")
            st.markdown(", ".join(matching_genres))
        
        if identified_genres.issubset(database_genres):
            st.success("The genres identified by the LLM are contained in the database genres.")
        else:
            st.warning("The genres identified by the LLM are not fully contained in the database genres.")
        
        # Visualization of the score
        genre_counts = {
            "Database Genres": len(database_genres),
            "LLM Genres": len(identified_genres),
            "Matching Genres": len(matching_genres)
        }
        
        fig, ax = plt.subplots()
        ax.bar(genre_counts.keys(), genre_counts.values(), color=["skyblue", "lightcoral", "lightgreen"])
        ax.set_ylabel("Count")
        ax.set_title("Genre Detection Score")
        st.pyplot(fig)