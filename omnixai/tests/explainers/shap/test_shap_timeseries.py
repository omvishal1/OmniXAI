import unittest
import numpy as np
import pandas as pd
from omnixai.utils.misc import set_random_seed
from omnixai.data.timeseries import Timeseries
from omnixai.explainers.timeseries.agnostic.shap import ShapTimeseries


class TestShapTimeseries(unittest.TestCase):

    def setUp(self) -> None:
        set_random_seed()
        x = np.random.randn(200, 5)
        x[:, 0] = np.array(range(x.shape[0])) * 0.1
        y = np.random.randn(3, 5)
        y[:, 0] = np.array(range(y.shape[0])) * 0.1

        self.training_data = Timeseries(
            data=x,
            timestamps=list(range(x.shape[0])),
            variable_names=list('x' * (i + 1) for i in range(x.shape[1]))
        )
        timestamps = pd.to_datetime(list(range(y.shape[0])), unit='s')
        self.test_data = Timeseries(
            data=y,
            timestamps=[v for v in timestamps],
            variable_names=list('x' * (i + 1) for i in range(x.shape[1]))
        )
        self.predict_function = lambda xs: np.array([np.sum(z[:, 0]) for z in xs.values])

    def test(self):
        set_random_seed()
        explainer = ShapTimeseries(
            training_data=self.training_data,
            predict_function=self.predict_function
        )
        explanations = explainer.explain(self.test_data)
        scores = explanations.get_explanations(index=0)["scores"]["x"].values
        self.assertAlmostEqual(scores[0], -9.673, delta=1e-3)
        self.assertAlmostEqual(scores[1], -9.673, delta=1e-3)
        self.assertAlmostEqual(scores[2], -9.673, delta=1e-3)


if __name__ == "__main__":
    unittest.main()
