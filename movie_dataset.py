import os
import tarfile
import requests
import pandas as pd
from pathlib import Path
from typing import Optional, Dict
from pydantic import BaseModel, ConfigDict


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
        """Downloads the dataset from the specified URL if it does not already exist."""
        print(f"Downloading {self.dataset_filename}...")

        try:
            response = requests.get(self.base_url + self.dataset_filename, stream=True)
            response.raise_for_status()

            with open(self.dataset_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print("Download complete.")

        except requests.exceptions.RequestException as e:
            print(f"Download failed: {e}")

    def extract_dataset(self):
        """Extracts the dataset archive into the designated directory."""
        print("Extracting dataset...")

        try:
            with tarfile.open(self.dataset_path, "r:gz") as tar:
                tar.extractall(path=self.download_dir)
            print("Extraction complete.")
        except tarfile.TarError as e:
            print(f"Error extracting dataset: {e}")

    def load_all_datasets(self):
        """
        Dynamically loads all .tsv and .txt files from the extracted directory into Pandas DataFrames.
        - Each dataset is stored in a dictionary (dataframes) using the filename (without extension) as the key.
        """

        if not self.extracted_dir.exists():
            print(f"Error: Extracted directory {self.extracted_dir} does not exist.")
            return

        for file_path in self.extracted_dir.glob("*"):
            if file_path.suffix in [".tsv", ".txt"]:  # Load only relevant file types
                self.load_dataset(file_path, sep="\t")
        
    def load_dataset(self, file_path: Path, sep: str = "\t"):
        """
        Loads a dataset file into a Pandas DataFrame and stores it in dataframes.

        Args:
            file_path (Path): Path to the dataset file.
            sep (str): Separator used in the file (default is tab-separated).
        """
        dataset_name = file_path.stem.replace('.', '_') # Extract filename without extension

        print(f"Checking file: {file_path}")  # Debugging line

        try:
            df = pd.read_csv(file_path, sep="\t", header=None)

            # Apply column names if recognized
            if dataset_name in self.column_names:
                df.columns = self.column_names[dataset_name]

            setattr(self, dataset_name, df)  # Dynamically set as attribute
            print(f"Loaded dataset: {dataset_name}, Shape: {df.shape}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            setattr(self, dataset_name, None)
    
    def movie_type(self, N: int = 10) -> pd.DataFrame:
        """
        Returns a DataFrame with the N most common movie types (genres) and their counts.
        """
        if not isinstance(N, int):
            raise Exception("N must be an integer.")

        if not hasattr(self, "movie_metadata") or self.movie_metadata is None:
            raise Exception("Movie metadata is not loaded.")

        genre_series = self.movie_metadata["genres"].dropna()
        genre_list = genre_series.str.split(", ")
        genre_counts = pd.Series([genre for sublist in genre_list for genre in sublist]).value_counts()

        result_df = genre_counts.head(N).reset_index()
        result_df.columns = ["Movie_Type", "Count"]

        return result_df