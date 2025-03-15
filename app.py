import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import random
from movie_dataset import MovieDataset
from ollama import chat, ChatResponse

# Initialize the MovieDataset instance
test_instance = MovieDataset()

# Set Streamlit page configuration
st.set_page_config(page_title="Movie & Actor Insights", page_icon="🎬", layout="wide")

# Sidebar Navigation
page = st.sidebar.radio("Navigation", ["Movie & Actor Analysis", "Chronological Trends", "Genre Classification (AI)"])

# --------------------------------------------
# Tab 1: Movie & Actor Analysis
# --------------------------------------------
if page == "Movie & Actor Analysis":
    st.title("Movie Dataset Analysis")
    
    def plot_movie_type_histogram():
        """
        Plots a histogram of the top N movie types.
        Allows the user to select the number of top movie types to display.
        """
        st.header("Movie Type Histogram")
        n = st.number_input("Select N (Top N Movie Types):", min_value=1, max_value=50, value=10, step=1)
        movie_type_df = test_instance.movie_type(n)
        
        fig, ax = plt.subplots()
        ax.bar(movie_type_df["Movie_Type"], movie_type_df["Count"], color="skyblue", edgecolor="black")
        ax.set_xlabel("Movie Type")
        ax.set_ylabel("Count")
        ax.set_title("Top Movie Types")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    
    def plot_actor_count_histogram():
        """
        Plots a histogram of the number of actors per movie.
        Displays the distribution of movies based on the number of actors.
        """
        st.header("Actor Count Histogram")
        actor_count_df = test_instance.actor_count()
        
        fig, ax = plt.subplots()
        ax.bar(actor_count_df["Number_of_Actors"], actor_count_df["Movie_Count"], color="lightcoral", edgecolor="black")
        ax.set_xlabel("Number of Actors")
        ax.set_ylabel("Movie Count")
        ax.set_title("Movies by Number of Actors")
        st.pyplot(fig)
    
    def plot_actor_height_distribution():
        """
        Plots the height distribution of actors based on selected gender and height range.
        Allows the user to filter by gender and specify minimum and maximum heights.
        """
        st.header("Actor Height Distribution")
        gender = st.selectbox("Select Gender:", ["All"] + list(test_instance.character_metadata["actor_gender"].dropna().unique()))
        
        col1, col2 = st.columns(2)
        with col1:
            min_height = st.number_input("Minimum Height (m):", min_value=1.0, max_value=2.5, value=1.5, step=0.01)
        with col2:
            max_height = st.number_input("Maximum Height (m):", min_value=1.0, max_value=2.5, value=2.0, step=0.01)
        
        actor_dist_df = test_instance.actor_distributions(gender, max_height, min_height, plot=False)
        fig, ax = plt.subplots()
        sns.kdeplot(actor_dist_df["actor_height"], ax=ax, color="blue", fill=True)
        ax.set_ylabel("Density")
        ax.set_xlabel("Actor Height (m)")
        ax.set_title("Actor Height Distribution")
        st.pyplot(fig)
    
    plot_movie_type_histogram()
    plot_actor_count_histogram()
    plot_actor_height_distribution()

# --------------------------------------------
# Tab 2: Chronological Trends
# --------------------------------------------
elif page == "Chronological Trends":
    st.title("Chronological Trends")
    genres = ["Drama", "Comedy", "Action", "Thriller", "Horror", "Romance Film", "Science Fiction", "Fantasy", "Mystery", "Documentary"]
    selected_genre = st.selectbox("Select a Genre:", [None] + genres)
    releases_df = test_instance.releases(selected_genre)
    
    st.header("Movies Released Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(releases_df.index, releases_df["Movie_Count"], color="royalblue", edgecolor="black")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies Released")
    ax.set_title("Movie Releases Per Year")
    st.pyplot(fig)
    
    st.header("Actor Births Over Time")
    birth_mode = st.selectbox("Select Aggregation Mode:", ["Year", "Month"])
    births_df = test_instance.ages("Y" if birth_mode == "Year" else "M")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(births_df.index, births_df["Birth_Count"], color="green", edgecolor="black")
    ax.set_xlabel(birth_mode)
    ax.set_ylabel("Number of Births")
    ax.set_title(f"Actor Births Per {birth_mode}")
    st.pyplot(fig)

# --------------------------------------------
# Tab 3: Genre Classification (AI-Based)
# --------------------------------------------
elif page == "Genre Classification (AI)":
    st.title("Random Movie Information")
    valid_movies = test_instance.movie_metadata[(test_instance.movie_metadata["wiki_movie_id"].isin(test_instance.plot_summaries["wiki_movie_id"])) & (test_instance.movie_metadata["genres"].notna())]
    
    if st.button("Shuffle"):
        if valid_movies.empty:
            st.error("No movies with summaries and genres available.")
        else:
            movie = valid_movies.sample(1).iloc[0]
            movie_id = movie["wiki_movie_id"]
            movie_title = movie["movie_name"]
            movie_summary = test_instance.plot_summaries[test_instance.plot_summaries["wiki_movie_id"] == movie_id]["plot_summary"].values[0]
            movie_genres = eval(movie["genres"]).values()
            
            st.markdown(f"### {movie_title}\n\n{movie_summary}")
            st.text_area("Genres", ", ".join(movie_genres))
            response: ChatResponse = chat(model='mistral', messages=[{"role": "user", "content": f"Classify the following movie summary into genres: {movie_summary}. Only list the genres, separated by commas. Do not include any additional information or brackets."}])
            llm_genres = response.message.content.strip()
            st.text_area("Genre by LLM", llm_genres)
            identified_genres = set(genre.strip().lower() for genre in llm_genres.split(","))
            database_genres = set(genre.strip().lower() for genre in movie_genres)
            matching_genres = identified_genres.intersection(database_genres)
            
            if matching_genres:
                st.markdown("### Successfully Detected Genres")
                st.markdown(", ".join(matching_genres))
            if identified_genres.issubset(database_genres):
                st.success("The genres identified by the LLM are contained in the database genres.")
            else:
                st.warning("The genres identified by the LLM are not fully contained in the database genres.")
            
            fig, ax = plt.subplots()
            ax.bar(["Database Genres", "LLM Genres", "Matching Genres"], [len(database_genres), len(identified_genres), len(matching_genres)], color=["skyblue", "lightcoral", "lightgreen"])
            ax.set_ylabel("Count")
            ax.set_title("Genre Detection Score")
            st.pyplot(fig)