from io import StringIO

import pytest

import serialize
import models
from models import Tap, Hold

PROPERTIES_STR = """#TITLE:Foo;
#SUBTITLE:;
#ARTIST:Bar;
#TITLETRANSLIT:;
#SUBTITLETRANSLIT:;
#ARTISTTRANSLIT:;
#CREDIT:;
#BANNER:foo.png;
#BACKGROUND:bar.png;
#LYRICSPATH:;
#CDTITLE:./CDTITLES/Dancing Stage SuperNOVA.png;
#MUSIC:foo.ogg;
#OFFSET:1.337;
#SAMPLESTART:133.700;
#SAMPLELENGTH:13.370;
#SELECTABLE:YES;
#DISPLAYBPM:125.000-400.000;
#STOPS:;
#BGCHANGES:;
#BPMS:;
"""


@pytest.fixture
def song():
    return models.Song(
        title='Foo',
        artist='Bar',
        banner='foo.png',
        bg='bar.png',
        music='foo.ogg',
        offset=0,
        sample_st=133.7,
        sample_len=13.37,
        bpms='125.000-400.000'
    )


def test_serialize_song_properties(song):
    f = StringIO()
    serialize.serialize_song(song, f)

    assert f.getvalue() == PROPERTIES_STR

SONG_WITH_CHART = """#TITLE:Foo;
#SUBTITLE:;
#ARTIST:Bar;
#TITLETRANSLIT:;
#SUBTITLETRANSLIT:;
#ARTISTTRANSLIT:;
#CREDIT:;
#BANNER:foo.png;
#BACKGROUND:bar.png;
#LYRICSPATH:;
#CDTITLE:./CDTITLES/Dancing Stage SuperNOVA.png;
#MUSIC:foo.ogg;
#OFFSET:0.000;
#SAMPLESTART:133.700;
#SAMPLELENGTH:13.370;
#SELECTABLE:YES;
#DISPLAYBPM:125.000-400.000;
#STOPS:;
#BGCHANGES:;
#BPMS:0.000=240.000;
#NOTES:
     dance-single:
     foo:
     Beginner:
     3:
     0.000,0.000,0.000,0.000,0.000:
0000
0000
0000
0000
0000
0000
0000
0000
;
"""


def test_serialize_song_with_chart(song):
    chart = models.Chart(
        author='foo',
        difficulty='Beginner',
        rating=3
    )
    chart.measures.append(models.Measure(
        rows=8,
        bpms=[(0, 240)],
        time=0
    ))
    song.charts.append(chart)

    f = StringIO()
    serialize.serialize_song(song, f)

    assert f.getvalue() == SONG_WITH_CHART


def test_collect_bpms():
    chart = models.Chart()
    chart.measures.append(models.Measure(
        time=0.00,
        bpms=[(0.00, 240.00)],
        rows=4
    ))
    chart.measures.append(models.Measure(
        time=1.00,
        bpms=[(0.00, 240.00), (2, 120.00)],
        rows=4
    ))
    bpm_string = serialize.collect_bpms(chart)

    assert bpm_string == '0.000=240.000,2.000=120.000'


CHART_SIMPLE = '''#NOTES:
     dance-single:
     foo:
     Beginner:
     3:
     0.000,0.000,0.000,0.000,0.000:
M000
0000
0010
0001
;
'''


def test_serialize_chart_simple():
    chart = models.Chart()
    chart.author = 'foo'
    chart.difficulty = 'Beginner'
    chart.rating = 3

    measure = models.Measure(
        time=0.00,
        bpms=[(0.00, 240.00)],
        rows=4
    )
    measure.notes.append(Tap(
        position=Tap.POSITION_LEFT,
        note_type=Tap.TYPE_MINE,
        offset=0
    ))
    measure.notes.append(Tap(
        position=Tap.POSITION_RIGHT,
        note_type=Tap.TYPE_NORMAL,
        offset=3
    ))
    measure.notes.append(Tap(
        position=Tap.POSITION_UP,
        note_type=Tap.TYPE_NORMAL,
        offset=2
    ))

    chart.measures.append(measure)

    assert serialize.serialize_chart(chart) == CHART_SIMPLE

CHART_HOLD = '''#NOTES:
     dance-single:
     foo:
     Beginner:
     3:
     0.000,0.000,0.000,0.000,0.000:
0000
0400
0320
0000
0000
0000
0030
0000
;
'''


def test_serialize_chart_hold():
    chart = models.Chart()
    chart.author = 'foo'
    chart.difficulty = 'Beginner'
    chart.rating = 3

    measure = models.Measure(
        time=0.00,
        bpms=[(0.00, 240.00)],
        rows=8
    )
    measure.notes.append(Hold(
        position=Hold.POSITION_DOWN,
        note_type=Hold.TYPE_ROLL,
        offset=1,
        duration=0.25
    ))
    measure.notes.append(Hold(
        position=Hold.POSITION_UP,
        note_type=Hold.TYPE_HOLD,
        offset=2,
        duration=0.625
    ))

    chart.measures.append(measure)

    assert serialize.serialize_chart(chart) == CHART_HOLD

CHART_HOLD_LONG = '''#NOTES:
     dance-single:
     foo:
     Beginner:
     3:
     0.000,0.000,0.000,0.000,0.000:
0000
0000
0020
0400
,
0300
0002
0033
0000
;
'''


def test_serialize_chart_hold_long():
    chart = models.Chart()
    chart.author = 'foo'
    chart.difficulty = 'Beginner'
    chart.rating = 3

    first_measure = models.Measure(
        time=0.00,
        bpms=[(0.00, 240.00)],
        rows=4
    )
    first_measure.notes.append(Hold(
        position=Hold.POSITION_DOWN,
        note_type=Hold.TYPE_ROLL,
        offset=3,
        duration=0.5
    ))
    first_measure.notes.append(Hold(
        position=Hold.POSITION_UP,
        note_type=Hold.TYPE_HOLD,
        offset=2,
        duration=1.25
    ))
    second_measure = models.Measure(
        time=1.00,
        bpms=[(0.00, 240.00)],
        rows=4
    )
    second_measure.notes.append(Hold(
        position=Hold.POSITION_RIGHT,
        note_type=Hold.TYPE_HOLD,
        offset=1,
        duration=0.5
    ))

    chart.measures.append(first_measure)
    chart.measures.append(second_measure)

    assert serialize.serialize_chart(chart) == CHART_HOLD_LONG

CHART_HOLD_LONG_DIFFERENT_LENS = '''#NOTES:
     dance-single:
     foo:
     Beginner:
     3:
     0.000,0.000,0.000,0.000,0.000:
0000
2000
0000
3400
,
0300
0000
0000
0000
0000
0000
0000
0000
;
'''


def test_serialize_chart_hold_long_different_lens():
    chart = models.Chart()
    chart.author = 'foo'
    chart.difficulty = 'Beginner'
    chart.rating = 3

    first_measure = models.Measure(
        time=0.00,
        bpms=[(0.00, 240.00)],
        rows=4
    )
    first_measure.notes.append(Hold(
        position=Hold.POSITION_DOWN,
        note_type=Hold.TYPE_ROLL,
        offset=3,
        duration=0.375
    ))
    first_measure.notes.append(Hold(
        position=Hold.POSITION_LEFT,
        note_type=Hold.TYPE_HOLD,
        offset=1,
        duration=0.75
    ))
    second_measure = models.Measure(
        time=1.00,
        bpms=[(0.00, 240.00)],
        rows=8
    )

    chart.measures.append(first_measure)
    chart.measures.append(second_measure)

    assert serialize.serialize_chart(chart) == CHART_HOLD_LONG_DIFFERENT_LENS
