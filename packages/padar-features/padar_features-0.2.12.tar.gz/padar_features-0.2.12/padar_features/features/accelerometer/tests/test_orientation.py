import numpy as np
from ....libs.signal_processing.signal_generator import SignalGenerator
from ..orientation import OrientationFeature
import os
import pandas as pd

def test_constant():
    generator = SignalGenerator(sr=50)
    data = generator.constant()
    data[:,0] = 1
    data[:,1] = 0
    data[:,2] = 0
    ori = OrientationFeature(data, subwin_samples = 50 * 2)
    ori.estimate_orientation(unit='rad')
    angles = ori.median_angles()
    assert np.allclose(angles, [0, np.pi / 2, np.pi / 2])


def test_standing():
    standing_file = os.path.join(os.path.dirname(__file__), 'standing.csv')
    standing_data = pd.read_csv(standing_file, parse_dates=[0], infer_datetime_format=True)
    standing_data = standing_data.values[:,1:]
    ori = OrientationFeature(standing_data, subwin_samples = 80 * 2)
    ori.estimate_orientation(unit='deg')
    angles = ori.median_angles()
    assert angles.values[0, 0] > 85 and angles.values[0, 0] < 105
    assert angles.values[0, 1] > 170
    assert angles.values[0, 2] > 85 and angles.values[0, 2] < 105