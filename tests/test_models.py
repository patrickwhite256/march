import models


def test_measure_duration_simple():
    a = models.Measure()
    a.bpms = [(0, 240)]

    assert a.duration() == 1


def test_measure_duration_bpm_change():
    a = models.Measure()
    a.bpms = [(0, 180), (2/3, 360)]

    assert a.duration() == 1


def test_measure_duration_multiple_bpm_change():
    a = models.Measure()
    a.bpms = [(0, 240), (0.5, 120), (0.75, 360)]

    assert a.duration() == 1
