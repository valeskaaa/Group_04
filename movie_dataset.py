"""
Module for handling downloading, extracting, and loading the CMU Movie Dataset.
"""

import tarfile
from pathlib import Path
from typing import Optional, Dict
import requests
import pandas as pd
from pydantic import BaseModel, ConfigDict
import matplotlib.pyplot as plt
import seaborn as sns


class MovieDataset(BaseModel):
    """Class to handle downloading, extracting, and loading the CMU Movie Dataset.

    Attributes:
        base_url (str): URL for downloading the dataset.
        dataset_filename (str): Name of the dataset archive file.
        download_dir (Path): Directory where dataset will be downloaded.
        extracted_dir (Path): Directory where dataset will be extracted.
        dataset_path (Path): Full path to the downloaded archive.
        dataframes (Dict[str, Optional[pd.DataFrame]]): Dictionary holding all loaded DataFrames.
    """

    base_url: str = "http://www.cs.cmu.edu/~ark/personas/data/"
    dataset_filename: str = "MovieSummaries.tar.gz"
    download_dir: Path = Path("downloads")
    extracted_dir: Path = download_dir / "MovieSummaries"
    dataset_path: Path = download_dir / dataset_filename

    # Dictionary to store all dynamically loaded datasets
    dataframes: Dict[str, Optional[pd.DataFrame]] = {}

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    column_names: object = {
        "movie_metadata": [
            "wiki_movie_id", "freebase_movie_id", "movie_name", "release_date",
            "box_office_revenue", "runtime", "languages", "countries", "genres"
        ],
        "character_metadata": [
            "wiki_movie_id", "freebase_movie_id", "release_date", "character_name",
            "actor_dob", "actor_gender", "actor_height", "actor_ethnicity",
            "actor_name", "actor_age_at_release", "freebase_char_actor_map_id",
            "freebase_char_id", "freebase_actor_id"
        ],
        "plot_summaries": ["wiki_movie_id", "plot_summary"],
        "tvtropes_clusters": ["freebase_char_actor_map_id", "tvtrope_cluster"],
        "name_clusters": ["freebase_char_actor_map_id", "character_name"]
    }

    def __init__(self):
        """
        Initializes the MovieDataset class.
        - Creates necessary directories.
        - Downloads dataset if missing.
        - Extracts dataset if needed.
        - Dynamically loads all .tsv and .txt files into Pandas DataFrames.
        """
        super().__init__()

        # Ensure the download directory exists
        self.download_dir.mkdir(exist_ok=True)

        # Download dataset if it does not exist
        if not self.dataset_path.exists():
            self.download_dataset()

        # Extract dataset if it has not been extracted
        if not self.extracted_dir.exists():
            self.extract_dataset()

        # Load all available dataset files dynamically
        self.load_all_datasets()

    def download_dataset(self):
        """
        Downloads the dataset from the specified URL if it does not already exist.
        """
        print(f"Downloading {self.dataset_filename}...")

        try:
            response = requests.get(self.base_url + self.dataset_filename, stream=True, timeout=10)
            response.raise_for_status()

            with open(self.dataset_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print("Download complete.")

        except requests.exceptions.RequestException as e:
            print(f"Download failed: {e}")

    def extract_dataset(self):
        """
        Extracts the dataset archive into the designated directory.
        """
        print("Extracting dataset...")

        try:
            with tarfile.open(self.dataset_path, "r:gz") as tar:
                tar.extractall(path=self.download_dir)
            print("Extraction complete.")
        except tarfile.TarError as e:
            print(f"Error extracting dataset: {e}")

    def load_all_datasets(self):
        """
        Dynamically loads all .tsv and .txt files from the extracted directory into pd DataFrames.
        - Each dataset is stored in a dictionary (dataframes) 
        - using the filename (without extension) as the key.
        """
        if not self.extracted_dir.exists():
            print(f"Error: Extracted directory {self.extracted_dir} does not exist.")
            return

        for file_path in self.extracted_dir.glob("*"):
            if file_path.suffix in [".tsv", ".txt"]:  # Load only relevant file types
                self.load_dataset(file_path)

    def load_dataset(self, file_path: Path):
        """
        Loads a dataset file into a Pandas DataFrame and stores it in dataframes.

        Args:
            file_path (Path): Path to the dataset file.
        """
        dataset_name = file_path.stem.replace('.', '_')  # Extract filename without extension

        print(f"Checking file: {file_path}")  # Debugging line

        try:
            df = pd.read_csv(file_path, sep="\t", header=None)

            # Apply column names if recognized
            if dataset_name in self.column_names:
                df.columns = self.column_names[dataset_name]

            setattr(self, dataset_name, df)  # Dynamically set as attribute
            print(f"Loaded dataset: {dataset_name}, Shape: {df.shape}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error loading {file_path}: {e}")
            setattr(self, dataset_name, None)

    def movie_type(self, top_n: int = 10) -> pd.DataFrame:
        """
        Returns a DataFrame with the N most common movie types (genres) and their counts.

        Args:
            top_n (int): Number of top movie types to return. Default is 10.

        Returns:
            pd.DataFrame: DataFrame with columns "Movie_Type" and "Count".
        """
        if not isinstance(top_n, int):
            raise ValueError("top_n must be an integer.")

        if not hasattr(self, "movie_metadata") or self.movie_metadata is None:
            raise ValueError("Movie metadata is not loaded.")

        # Extract genres from the last column, which is a dictionary
        genre_series = self.movie_metadata["genres"].dropna()

        # Convert each genre dictionary into a list of genres and flatten
        genre_list = genre_series.apply(
            lambda x: list(eval(x).values())  # Assuming it's stored as a stringified dictionary
        )
        genre_flattened = [genre for sublist in genre_list for genre in sublist]

        # Count the occurrence of each genre
        genre_counts = pd.Series(genre_flattened).value_counts()

        # Create DataFrame with the top N genres
        result_df = genre_counts.head(top_n).reset_index()
        result_df.columns = ["Movie_Type", "Count"]

        return result_df

    def actor_count(self) -> pd.DataFrame:
        """
        Returns a histogram DataFrame showing the number of actors per movie vs. the movie count.
        Also, displays a histogram plot.

        The output DataFrame will have:
        - "Number_of_Actors" (unique actor count per movie)
        - "Movie_Count" (number of movies with that many actors)

        Returns:
            pd.DataFrame: DataFrame with columns "Number_of_Actors" and "Movie_Count".
        """
        if not hasattr(self, "character_metadata") or self.character_metadata is None:
            raise ValueError("Character metadata is not loaded.")

        # Ensure required columns exist
        required_columns = {"wiki_movie_id", "actor_name"}
        if not required_columns.issubset(self.character_metadata.columns):
            missing_cols = required_columns - set(self.character_metadata.columns)
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Count the number of unique actors per movie
        actor_counts = self.character_metadata.groupby("wiki_movie_id")["actor_name"].nunique()

        # Create a histogram DataFrame: How many movies have X number of actors?
        histogram = actor_counts.value_counts().reset_index()
        histogram.columns = ["Number_of_Actors", "Movie_Count"]

        # Sort the results in ascending order of number of actors
        histogram = histogram.sort_values(by="Number_of_Actors")

        # --- PLOT THE HISTOGRAM ---
        plt.figure(figsize=(10, 6))
        plt.bar(histogram["Number_of_Actors"],
                histogram["Movie_Count"],
                color="skyblue",
                edgecolor="black")
        plt.xlabel("Number of Actors per Movie")
        plt.ylabel("Movie Count")
        plt.title("Histogram of Number of Actors per Movie")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        # Show the plot
        plt.show()

        return histogram

    def actor_distributions(
        self, gender: str, max_height: float, min_height: float, plot: bool = False
    ) -> pd.DataFrame:
        """
        Filters actor data based on gender and height range, 
        - and optionally plots the height distribution.

        Args:
            gender (str): "All" or a specific gender from the dataset.
            max_height (float): Maximum height threshold.
            min_height (float): Minimum height threshold.
            plot (bool, optional): If True, plots a histogram or density plot. Default is False.

        Returns:
            pd.DataFrame: Filtered actor dataset.
        """
        # Ensure valid input types
        if not isinstance(gender, str):
            raise ValueError("Gender must be a string.")
        if not isinstance(max_height, (int, float)) or not isinstance(min_height, (int, float)):
            raise ValueError("Height limits must be numerical values.")

        # Ensure the dataset is loaded
        if not hasattr(self, "character_metadata") or self.character_metadata is None:
            raise ValueError("Character metadata is not loaded.")

        # Ensure required columns exist
        required_columns = {"actor_gender", "actor_height"}
        if not required_columns.issubset(self.character_metadata.columns):
            raise ValueError(f"Missing required columns: {required_columns - set(self.character_metadata.columns)}")

        # Convert heights to numerical, forcing errors to NaN
        self.character_metadata["actor_height"] = pd.to_numeric(
            self.character_metadata["actor_height"], errors="coerce"
        )

        # Drop missing height values
        df = self.character_metadata.dropna(subset=["actor_height"]).copy()

        # Standardize height units: Convert values > 10 (likely in cm) to meters
        df.loc[df["actor_height"] > 10, "actor_height"] /= 100

        # Apply gender filter
        valid_genders = df["actor_gender"].dropna().unique().tolist() + ["All"]
        if gender != "All":
            if gender not in valid_genders:
                raise ValueError(f"Invalid gender value. Must be one of: {valid_genders}")
            df = df[df["actor_gender"] == gender]

        # Apply height range filter
        df = df[(df["actor_height"] >= min_height) & (df["actor_height"] <= max_height)]

        # If plot is True, create a density plot
        if plot:
            plt.figure(figsize=(10, 6))
            sns.kdeplot(df["actor_height"], color="blue", alpha=0.5)
            plt.ylabel("Density")
            plt.title(f"Density Plot of Actor Heights ({gender})")
            plt.xlabel("Actor Height (m)")
            plt.grid(axis="y", linestyle="--", alpha=0.7)
            plt.show()

        return df

    def releases(self, genre: Optional[str] = None) -> pd.DataFrame:
        """
        Creates a DataFrame showing the number of movies released per year.

        Args:
            genre (Optional[str]): If provided, 
            - filters the data to include only movies of the given genre.

        Returns:
            pd.DataFrame: A DataFrame with columns ["Year", "Movie_Count"]
            - showing the number of movies released each year.
        """
        if not hasattr(self, "movie_metadata") or self.movie_metadata is None:
            raise ValueError("Movie metadata is not loaded.")

        if "release_date" not in self.movie_metadata.columns or "genres" not in self.movie_metadata.columns:
            raise ValueError("Required columns (release_date, genres) are missing from the dataset.")

        # Convert release_date to datetime and extract the year
        self.movie_metadata["release_date"] = pd.to_datetime(
            self.movie_metadata["release_date"], errors="coerce"
        )
        self.movie_metadata["Year"] = self.movie_metadata["release_date"].dt.year

        # Drop rows with missing years
        df = self.movie_metadata.dropna(subset=["Year"]).copy()

        # Filter by genre if specified
        if genre:
            df = df[df["genres"].apply(
                lambda x: genre in eval(x).values() if pd.notna(x) else False)]

        # Count movies per year
        releases_per_year = (
            df["Year"].value_counts().sort_index().to_frame(name="Movie_Count").astype(int)
        )
        releases_per_year.index = releases_per_year.index.astype(int)
        releases_per_year.index.name = "Year"

        return releases_per_year

    def ages(self, mode: str = 'Y') -> pd.DataFrame:
        """
        Computes the number of births per year or per month of the year.

        Args:
            mode (str): 'Y' for year-based aggregation, 'M' for month-based aggregation.

        Returns:
            pd.DataFrame: A DataFrame showing the count of actor births per selected mode.
        """
        if not hasattr(self, "character_metadata") or self.character_metadata is None:
            raise ValueError("Character metadata is not loaded.")

        if "actor_dob" not in self.character_metadata.columns:
            raise ValueError("Required column 'actor_dob' is missing from the dataset.")

        # Convert actor_dob to datetime
        self.character_metadata["actor_dob"] = pd.to_datetime(
            self.character_metadata["actor_dob"], errors="coerce"
        )

        # Default to Year if invalid mode is passed
        mode = mode.upper()
        if mode not in ['Y', 'M']:
            mode = 'Y'

        if mode == 'Y':
            births = (
                self.character_metadata["actor_dob"]
                .dt.year.value_counts()
                .sort_index()
                .to_frame(name="Birth_Count")
                .astype(int)
            )
            births.index = births.index.astype(int)
            births.index.name = "Year"
        else:
            births = self.character_metadata["actor_dob"].dt.month.value_counts().sort_index().to_frame(
                name="Birth_Count"
            ).astype(int)
            births.index = births.index.astype(int)
            births.index.name = "Month"

        return births
