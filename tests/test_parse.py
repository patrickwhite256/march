from io import StringIO

import pytest

import parse
from models import Tap, Hold, Note

ATTR_SONG = '''#TITLE:foo;
#BANNER:foo.png;
#BACKGROUND:bar.png;
#MUSIC:foo.ogg;
#OFFSET:1.337;
#SAMPLESTART:133.7;
#SAMPLELENGTH:13.37;
#DISPLAYBPM:13.3-133.7;
'''


def test_parse_song_attrs():
    song_file = StringIO(ATTR_SONG)

    song = parse.parse_song(song_file)

    assert song.title == 'foo'
    assert song.banner == 'foo.png'
    assert song.bg == 'bar.png'
    assert song.music == 'foo.ogg'
    assert song.offset == 1.337
    assert song.sample_st == 133.7
    assert song.sample_len == 13.37
    assert song.bpms == '13.3-133.7'

ATTR_CHART = '''
     dance-single:
     foo:
     Beginner:
     3:
     0.135,0.176,0.000,0.000,0.000:
0000
0000
0000
0000
'''


def test_parse_chart_attrs():
    chart = parse.parse_chart(ATTR_CHART)

    assert chart.author == 'foo'
    assert chart.difficulty == 'Beginner'
    assert chart.rating == 3

MEASURE_CHART = '''
     dance-single:
     foo:
     Beginner:
     3:
     0.135,0.176,0.000,0.000,0.000:
1201
0000
00M0
0300
'''


def test_parse_chart_measure():
    chart = parse.parse_chart(MEASURE_CHART)

    assert len(chart.measures) == 1

    measure = chart.measures[0]
    assert len(measure.notes) == 4

    required_notes = [
        Tap(position=Note.POSITION_LEFT, note_type=Tap.TYPE_NORMAL, offset=0),
        Tap(position=Note.POSITION_RIGHT, note_type=Tap.TYPE_NORMAL, offset=0),
        Hold(position=Note.POSITION_DOWN, note_type=Hold.TYPE_HOLD, offset=0, duration=1),
        Tap(position=Note.POSITION_UP, note_type=Tap.TYPE_MINE, offset=2)
    ]

    for note in required_notes:
        assert note in measure.notes

LONG_HOLD_CHART = '''
     dance-single:
     foo:
     Beginner:
     3:
     0.135,0.176,0.000,0.000,0.000:
0400
0000
0000
0000
,
0000
0000
0000
0300
0000
0000
0000
0000
'''


def test_parse_long_hold():
    chart = parse.parse_chart(LONG_HOLD_CHART)

    assert len(chart.measures) == 2

    assert len(chart.measures[0].notes) == 1
    assert len(chart.measures[1].notes) == 0

    ideal_note = Hold(note_type=Hold.TYPE_ROLL, offset=0, duration=1.5, position=Note.POSITION_DOWN)
    assert chart.measures[0].notes[0] == ideal_note

COMMENT_CHART = '''
     dance-single:
     foo:
     Beginner:
     3:
     0.135,0.176,0.000,0.000,0.000:
0000
0000
0000 //comment: comment
0000//comment
, // lol, comment
0000
0000    //comment!
0000
0000
   //whitespace only line
0000
0000
//comment
0000
0000
'''


def test_parse_strip_comments():
    chart = parse.parse_chart(COMMENT_CHART)

    assert len(chart.measures) == 2

    assert chart.measures[0].rows == 4
    assert chart.measures[1].rows == 8


MULTI_HOLD_CHART = '''
     dance-single:
     foo:
     Beginner:
     3:
     0.135,0.176,0.000,0.000,0.000:
0400
0000
0020
0030
,
0000
0020
0030
0300
0002
0003
0000
0000
'''


def test_parse_multiple_holds():
    chart = parse.parse_chart(MULTI_HOLD_CHART)

    assert len(chart.measures) == 2

    assert len(chart.measures[0].notes) == 2
    assert len(chart.measures[1].notes) == 2

    first_measure_notes = [
        Hold(note_type=Hold.TYPE_ROLL, offset=0, duration=1.5, position=Note.POSITION_DOWN),
        Hold(note_type=Hold.TYPE_HOLD, offset=2, duration=0.5, position=Note.POSITION_UP),
    ]

    second_measure_notes = [
        Hold(note_type=Hold.TYPE_HOLD, offset=1, duration=0.25, position=Note.POSITION_UP),
        Hold(note_type=Hold.TYPE_HOLD, offset=4, duration=0.25, position=Note.POSITION_RIGHT),
    ]

    for note in first_measure_notes:
        assert note in chart.measures[0].notes
    for note in second_measure_notes:
        assert note in chart.measures[1].notes

FUCKY_CHART = '''
     dance-single:
     foo:
     Beginner:
     3:
     0.135,0.176,0.000,0.000,0.000:
1001
0000
0000
0000
,  0021
0000
0030
0000
'''


def test_parse_chart_fucky_spacing():
    chart = parse.parse_chart(FUCKY_CHART)

    assert len(chart.measures) == 2

    assert len(chart.measures[0].notes) == 2
    assert len(chart.measures[1].notes) == 2

N_MEASURES = 8


@pytest.fixture
def basic_chart():
    chart = '''
     dance-single:
     foo:
     Beginner:
     3:
     0.135,0.176,0.000,0.000,0.000:
'''
    measures = []
    for i in range(0, N_MEASURES):
        measure = ''
        for i in range(0, 4):
            measure += '0000\n'
        measures.append(measure)

    chart += ',\n'.join(measures)

    return parse.parse_chart(chart)


def test_apply_bpms_basic(basic_chart):
    bpm_changes = ['0.0=240.00']
    parse.apply_bpms(basic_chart, bpm_changes, 0)

    for i in range(0, N_MEASURES):
        assert basic_chart.measures[i].bpms == [(0, 240)]
        assert basic_chart.measures[i].duration() == 1


def test_apply_bpms_change(basic_chart):
    bpm_changes = ['0.0=240.00', '6.0=120.00']
    parse.apply_bpms(basic_chart, bpm_changes, 0)

    assert basic_chart.measures[0].duration() == 1
    assert basic_chart.measures[0].bpms == [(0, 240)]
    assert basic_chart.measures[1].duration() == 1.5
    assert basic_chart.measures[1].bpms == [(0, 240), (2, 120)]
    for i in range(2, N_MEASURES):
        assert basic_chart.measures[i].duration() == 2
        assert basic_chart.measures[i].bpms == [(0, 120)]


def test_apply_bpms_change_on_measure(basic_chart):
    bpm_changes = ['0.0=240.00', '4.0=120.00']
    parse.apply_bpms(basic_chart, bpm_changes, 0)

    assert basic_chart.measures[0].bpms == [(0, 240)]
    assert basic_chart.measures[0].duration() == 1
    for i in range(1, N_MEASURES):
        assert basic_chart.measures[i].bpms == [(0, 120)]
        assert basic_chart.measures[i].duration() == 2
