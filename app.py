"""
Streamlit App: Movie & Actor Insights

This application provides movie and actor analysis, chronological trends,
and AI-based genre classification using the CMU Movie Dataset.
"""

import ast  # Standard library first
import streamlit as st  # Third-party imports
import matplotlib.pyplot as plt
import seaborn as sns
from ollama import chat, ChatResponse
from movie_dataset import MovieDataset  # First-party import

# Initialize the MovieDataset instance
test_instance = MovieDataset()

# Set Streamlit page configuration
st.set_page_config(page_title="Movie & Actor Insights", page_icon="🎬", layout="wide")

# Sidebar Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Movie & Actor Analysis", "Chronological Trends", "Genre Classification (AI)"],
)

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
        n = st.number_input(
            "Select N (Top N Movie Types):",
            min_value=1,
            max_value=50,
            value=10,
            step=1,
        )
        movie_type_df = test_instance.movie_type(n)

        fig_type, ax_type = plt.subplots()
        ax_type.bar(
            movie_type_df["Movie_Type"],
            movie_type_df["Count"],
            color="skyblue",
            edgecolor="black",
        )
        ax_type.set_xlabel("Movie Type")
        ax_type.set_ylabel("Count")
        ax_type.set_title("Top Movie Types")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig_type)

    def plot_actor_count_histogram():
        """
        Plots a histogram of the number of actors per movie.
        Displays the distribution of movies based on the number of actors.
        """
        st.header("Actor Count Histogram")
        actor_count_df = test_instance.actor_count()

        fig_actor, ax_actor = plt.subplots()
        ax_actor.bar(
            actor_count_df["Number_of_Actors"],
            actor_count_df["Movie_Count"],
            color="lightcoral",
            edgecolor="black",
        )
        ax_actor.set_xlabel("Number of Actors")
        ax_actor.set_ylabel("Movie Count")
        ax_actor.set_title("Movies by Number of Actors")
        st.pyplot(fig_actor)

    def plot_actor_height_distribution():
        """
        Plots the height distribution of actors based on selected gender and height range.
        Allows the user to filter by gender and specify minimum and maximum heights.
        """
        st.header("Actor Height Distribution")
        gender = st.selectbox(
            "Select Gender:",
            ["All"]
            + list(test_instance.character_metadata["actor_gender"].dropna().unique()),
        )

        col1, col2 = st.columns(2)
        with col1:
            min_height = st.number_input(
                "Minimum Height (m):", min_value=1.0, max_value=2.5, value=1.5, step=0.01
            )
        with col2:
            max_height = st.number_input(
                "Maximum Height (m):", min_value=1.0, max_value=2.5, value=2.0, step=0.01
            )

        actor_dist_df = test_instance.actor_distributions(
            gender, max_height, min_height, plot=False
        )
        fig_height, ax_height = plt.subplots()
        sns.kdeplot(actor_dist_df["actor_height"], ax=ax_height, color="blue", fill=True)
        ax_height.set_ylabel("Density")
        ax_height.set_xlabel("Actor Height (m)")
        ax_height.set_title("Actor Height Distribution")
        st.pyplot(fig_height)

    plot_movie_type_histogram()
    plot_actor_count_histogram()
    plot_actor_height_distribution()


# --------------------------------------------
# Tab 2: Chronological Trends
# --------------------------------------------
elif page == "Chronological Trends":
    st.title("Chronological Trends")
    genres = [
        "Drama",
        "Comedy",
        "Action",
        "Thriller",
        "Horror",
        "Romance Film",
        "Science Fiction",
        "Fantasy",
        "Mystery",
        "Documentary",
    ]
    selected_genre = st.selectbox("Select a Genre:", [None] + genres)
    releases_df = test_instance.releases(selected_genre)

    st.header("Movies Released Over Time")
    fig_release, ax_release = plt.subplots(figsize=(10, 6))
    ax_release.bar(
        releases_df.index, releases_df["Movie_Count"], color="royalblue", edgecolor="black"
    )
    ax_release.set_xlabel("Year")
    ax_release.set_ylabel("Number of Movies Released")
    ax_release.set_title("Movie Releases Per Year")
    st.pyplot(fig_release)

    st.header("Actor Births Over Time")
    birth_mode = st.selectbox("Select Aggregation Mode:", ["Year", "Month"])
    births_df = test_instance.ages("Y" if birth_mode == "Year" else "M")

    fig_birth, ax_birth = plt.subplots(figsize=(10, 6))
    ax_birth.bar(births_df.index, births_df["Birth_Count"], color="green", edgecolor="black")
    ax_birth.set_xlabel(birth_mode)
    ax_birth.set_ylabel("Number of Births")
    ax_birth.set_title(f"Actor Births Per {birth_mode}")
    st.pyplot(fig_birth)


# --------------------------------------------
# Tab 3: Genre Classification (AI-Based)
# --------------------------------------------
elif page == "Genre Classification (AI)":
    st.title("Random Movie Information")
    valid_movies = test_instance.movie_metadata[
        (test_instance.movie_metadata["wiki_movie_id"].isin(test_instance.plot_summaries["wiki_movie_id"]))
        & (test_instance.movie_metadata["genres"].notna())
    ]

    if st.button("Shuffle"):
        if valid_movies.empty:
            st.error("No movies with summaries and genres available.")
        else:
            movie = valid_movies.sample(1).iloc[0]
            movie_id = movie["wiki_movie_id"]
            movie_title = movie["movie_name"]
            movie_summary = test_instance.plot_summaries[
                test_instance.plot_summaries["wiki_movie_id"] == movie_id
            ]["plot_summary"].values[0]

            # Replacing `eval()` with `ast.literal_eval()` for security
            movie_genres = list(ast.literal_eval(movie["genres"]).values())

            st.markdown(f"### {movie_title}\n\n{movie_summary}")
            st.text_area("Genres", ", ".join(movie_genres))

            response = chat(
                model="mistral",
                messages=[
                    {
                        "role": "user",
                        "content": f"Classify the following movie summary into genres: {movie_summary}. "
                        "Only list the genres, separated by commas. Do not include any additional information or brackets.",
                    }
                ],
            )
            llm_genres = response.get("message", {}).get("content", "").strip()

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

            fig_score, ax_score = plt.subplots()
            ax_score.bar(
                ["Database Genres", "LLM Genres", "Matching Genres"],
                [len(database_genres), len(identified_genres), len(matching_genres)],
                color=["skyblue", "lightcoral", "lightgreen"],
            )
            ax_score.set_ylabel("Count")
            ax_score.set_title("Genre Detection Score")
            st.pyplot(fig_score)
