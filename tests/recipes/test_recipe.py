import pytest
import numpy as np
import pandas as pd
from icu_benchmarks.recipes.recipe import Recipe

@pytest.fixture()
def example_df():
    rand_state = np.random.RandomState(42)
    df = pd.DataFrame({
        'id': [1] * 6 + [2] * 4,
        'time': np.concatenate((np.arange(6), np.arange(4))),
        'y': rand_state.normal(size=(10, )),
        'x1': rand_state.normal(loc=10, scale=5, size=(10, )),
        'x2': rand_state.binomial(n=1, p=0.3, size=(10, ))
    })
    return df

def test_empty_prep_return_df(example_df):
    rec = Recipe(example_df)
    assert rec.prep().__class__ == pd.DataFrame

def test_empty_bake_return_df(example_df):
    rec = Recipe(example_df)
    assert rec.bake().__class__ == pd.DataFrame

def test_init_roles(example_df):
    rec = Recipe(example_df, ['y'], ['x1', 'x2'], ['id']) # FIXME: add squence when merged
    assert rec.data.roles['y'] == ['outcome']
    assert rec.data.roles['x1'] == ['predictor']
    assert rec.data.roles['x2'] == ['predictor']
    assert rec.data.roles['id'] == ['group']

