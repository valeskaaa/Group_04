import pytest
import pandas as pd
from movie_dataset import MovieDataset

@pytest.fixture
def dataset():
    return MovieDataset()

def test_movie_type(dataset):
    with pytest.raises(Exception):
        dataset.movie_type("ten")
    result = dataset.movie_type(10)
    assert isinstance(result, pd.DataFrame)
    assert 'Movie_Type' in result.columns
    assert 'Count' in result.columns

def test_actor_count(dataset):
    result = dataset.actor_count()
    assert isinstance(result, pd.DataFrame)
    assert 'Number_of_Actors' in result.columns
    assert 'Movie_Count' in result.columns

def test_actor_distributions(dataset):
    with pytest.raises(Exception):
        dataset.actor_distributions(123, 180, 160)
    with pytest.raises(Exception):
        dataset.actor_distributions("Male", "tall", 160)
    with pytest.raises(Exception):
        dataset.actor_distributions("Male", 180, "short")
    result = dataset.actor_distributions("All", 180, 160)
    assert isinstance(result, pd.DataFrame)