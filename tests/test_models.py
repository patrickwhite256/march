import models
import pytest


@pytest.fixture
def measure():
    return models.Measure(rows=4)


def test_measure_duration_simple(measure):
    measure.bpms = [(0, 240)]

    assert measure.duration() == 1


def test_measure_duration_bpm_change(measure):
    measure.bpms = [(0, 180), (2, 360)]

    assert measure.duration() == 1


def test_measure_duration_multiple_bpm_change(measure):
    measure.bpms = [(0, 240), (2, 120), (3, 360)]

    assert measure.duration() == 1
