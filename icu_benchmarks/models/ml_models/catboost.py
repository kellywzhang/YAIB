import gin
import catboost as cb
import numpy as np
import wandb

from icu_benchmarks.contants import RunMode
from icu_benchmarks.models.wrappers import MLWrapper
@gin.configurable
class CBClassifier(MLWrapper):
    _supported_run_modes = [RunMode.classification]

    def __init__(self, *args, **kwargs):
        self.model = self.set_model_args(cb.CatBoostClassifier, *args, **kwargs)
        super().__init__(*args, **kwargs)

    def predict(self, features):
        """Predicts labels for the given features."""
        return self.model.predict_proba(features)
