from io import StringIO

import pytest

import serialize
import models

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
#SAMPLESTART:133.7;
#SAMPLELENGTH:13.37;
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
        offset=1.337,
        sample_st=133.7,
        sample_len=13.37,
        bpms='125.000-400.000'
    )


def test_serialize_song_properties(song):
    f = StringIO()
    serialize.serialize_song(song, f)

    assert f.getvalue() == PROPERTIES_STR


def test_collect_bpms():
    chart = models.Chart()
    chart.measures.append(models.Measure(
        time=0.00,
        bpms=[(0.00, 240.00)]
    ))
    chart.measures.append(models.Measure(
        time=1.00,
        bpms=[(0.00, 240.00), (0.5, 120.00)]
    ))
    bpm_string = serialize.collect_bpms(chart)

    assert bpm_string == '0.000=240.000,1.500=120.000'
