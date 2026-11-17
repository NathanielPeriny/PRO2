"""Tests du module modele."""

import numpy as np
import pytest
from sklearn.metrics import mean_absolute_error

from modele import calculer_mae


def test_mae_valeur_connue():
    """Sur un petit exemple calcule a la main : (0,2 + 0,3 + 0,1) / 3 = 0,2."""
    assert calculer_mae([3.5, 2.8, 3.9], [3.3, 3.1, 3.8]) == pytest.approx(0.2)


def test_mae_egale_scikit_learn():
    """Notre MAE (NumPy) donne le meme resultat que celle de scikit-learn."""
    reel = np.array([2.0, 3.0, 3.5, 4.0])
    predit = np.array([2.5, 2.9, 3.0, 3.8])
    assert calculer_mae(reel, predit) == pytest.approx(mean_absolute_error(reel, predit))