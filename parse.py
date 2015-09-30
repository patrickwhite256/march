import models

FIELD_LABEL_MAP = {
    'title': 'TITLE',
    'banner': 'BANNER',
    'bg': 'BACKGROUND',
    'music': 'MUSIC',
    'offset': 'OFFSET',
    'sample_st': 'SAMPLESTART',
    'sample_len': 'SAMPLELENGTH',
    'bpms': 'DISPLAYBPM'
}

NUMERIC_FIELDS = ['offset', 'sample_st', 'sample_len']


def parse_song(song_file):
    """
    Parses a song from a simfile.

    :param song_file: a file object with the contents of the simfile
    :return: an instance of models.Song
    """

    song = models.Song()

    contents = song_file.read()

    # all relevant parts are between # and ;
    parts = [_.split('#')[1] for _ in contents.split(';')[:-1]]

    inverse_map = {v: k for k, v in FIELD_LABEL_MAP.items()}
    for part in parts:
        split = part.split(':')
        key = split[0]
        value = ','.join(split[1:])
        if key == 'NOTES':
            chart = parse_chart(value)
            song.charts.append(chart)
        else:
            try:
                field = inverse_map[key]
                if field in NUMERIC_FIELDS:
                    value = float(value)
                setattr(song, field, value)
            except KeyError:  # there are attrs we don't care about
                pass

    return song


def parse_chart(chart_contents):
    """
    Parses a chart.

    :param chart_contents: the contents of the chart, starting at dance-single and including
                           all of the measures in the chart.
    :return: an instance of models.Chart
    """
    chart = models.Chart()
    parts = [_.strip() for _ in chart_contents.split(':')]
    chart.author = parts[1]
    chart.difficulty = parts[2]
    chart.rating = int(parts[3])
    measure_strings = parts[5].split(',')

    holds = [None, None, None, None]

    for measure_string in measure_strings:
        measure = models.Measure()
        rows = [_ for _ in measure_string.splitlines() if _]  # discard empty lines
        measure.rows = len(rows)

        for row_count, row in enumerate(rows):
            for hold in holds:
                if hold:
                    hold[1] += 1/len(rows)
            for i, note_char in enumerate(row):
                if note_char == models.Note.TYPE_NONE:
                    continue
                elif note_char == models.Note.TYPE_END:
                    note, duration = holds[i]
                    note.duration = duration
                    holds[i] = None
                elif note_char in models.Tap.TYPES:
                    note = models.Tap(
                        position=i,
                        offset=row_count,
                        note_type=note_char
                    )

                    measure.notes.append(note)
                elif note_char in models.Hold.TYPES:
                    note = models.Hold(
                        position=i,
                        offset=row_count,
                        note_type=note_char
                    )

                    measure.notes.append(note)

                    holds[i] = [note, 1/len(rows)]

        chart.measures.append(measure)

    return chart
