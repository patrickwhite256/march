PROPERTIES_TEMPLATE = """#TITLE:{title};
#SUBTITLE:;
#ARTIST:{artist};
#TITLETRANSLIT:;
#SUBTITLETRANSLIT:;
#ARTISTTRANSLIT:;
#CREDIT:;
#BANNER:foo.png;
#BACKGROUND:bar.png;
#LYRICSPATH:;
#CDTITLE:./CDTITLES/Dancing Stage SuperNOVA.png;
#MUSIC:foo.ogg;
#OFFSET:{offset};
#SAMPLESTART:{sample_st};
#SAMPLELENGTH:{sample_len};
#SELECTABLE:YES;
#DISPLAYBPM:{bpms};
#STOPS:;
#BGCHANGES:;
"""

BPM_STRING_FORMAT = '{:.3f}={:.3f}'


def serialize_song(song, f):
    """
    Serialize a song to a simfile.

    :param song: the models.Song object to serialize
    :param f: a file-like object to write to
    """
    f.write(PROPERTIES_TEMPLATE.format(**song.__dict__))
    bpm_string = ''
    if song.charts:
        bpm_string = collect_bpms(song)
    f.write('#BPMS:{};\n'.format(bpm_string))


def collect_bpms(chart):
    """
    Serialize all the BPM changes in a song into the format 't.ttt=b.bbb,t.ttt=b.bbb'

    :param chart: a models.Chart object with at least one models.Measure

    :return: a string of the format 't.ttt=b.bbb,t.ttt=b.bbb'
    """

    bpm_strings = []

    current_time, current_bpm = chart.measures[0].bpms[0]
    bpm_strings.append(BPM_STRING_FORMAT.format(0, current_bpm))
    for measure in chart.measures:
        for time, bpm in measure.bpms:
            if bpm != current_bpm:
                current_bpm = bpm
                bpm_strings.append(BPM_STRING_FORMAT.format(current_time + time, current_bpm))
        current_time += measure.duration()

    return ','.join(bpm_strings)
