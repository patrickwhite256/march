import models

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

CHART_TEMPLATE = '''#NOTES:
     dance-single:
     {author}:
     {difficulty}:
     {rating}:
     0.000,0.000,0.000,0.000,0.000:
{notes}
;
'''

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


def serialize_chart(chart):
    """
    Serialize a chart to a string.

    :param chart: the models.Chart object to serialize

    :return: a string containing the serialized chart
    """
    measures = []
    for measure in chart.measures:
        notes = [['0', '0', '0', '0'] for _ in range(0, measure.rows)]
        measures.append(notes)

    for i, measure in enumerate(chart.measures):
        for note in measure.notes:
            measures[i][note.offset][note.position] = note.note_type
            if note.note_type in models.Hold.TYPES:
                target_measure_index = int(i + note.offset / measure.rows + note.duration)
                target_measure = chart.measures[target_measure_index]
                target_offset = round(((note.offset / measure.rows + note.duration) % 1) * target_measure.rows)
                measures[target_measure_index][target_offset][note.position] = models.Note.TYPE_END
    notes = '\n,\n'.join(
        ['\n'.join(
            [''.join(row) for row in measure_list]
            ) for measure_list in measures]
    )
    format_dict = chart.__dict__
    format_dict['notes'] = notes
    return CHART_TEMPLATE.format(**format_dict)


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
