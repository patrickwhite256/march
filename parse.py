import re
import models

FIELD_LABEL_MAP = {
    'title': 'TITLE',
    'banner': 'BANNER',
    'bg': 'BACKGROUND',
    'artist': 'ARTIST',
    'music': 'MUSIC',
    'offset': 'OFFSET',
    'sample_st': 'SAMPLESTART',
    'sample_len': 'SAMPLELENGTH',
    'bpms': 'DISPLAYBPM'
}

NUMERIC_FIELDS = ['offset', 'sample_st', 'sample_len']

COMMENT_RE = re.compile('\s*(\/\/.*)?$')  # strip whitespace and comments


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
    bpm_changes = None
    for part in parts:
        split = part.split(':')
        key = split[0]
        value = ':'.join(split[1:])
        if key == 'NOTES':
            chart = parse_chart(value)
            song.charts.append(chart)
        if key == 'BPMS':
            bpm_changes = value.split(',')
        else:
            try:
                field = inverse_map[key]
                if field in NUMERIC_FIELDS:
                    value = float(value)
                setattr(song, field, value)
            except KeyError:  # there are attrs we don't care about
                pass

    for chart in song.charts:
        apply_bpms(chart, bpm_changes, song.offset)

    return song


def parse_chart(chart_contents):
    """
    Parses a chart.

    :param chart_contents: the contents of the chart, starting at dance-single and including
                           all of the measures in the chart.
    :return: an instance of models.Chart
    """

    chart = models.Chart()
    chart_contents = '\n'.join([COMMENT_RE.sub('', _) for _ in chart_contents.splitlines()])
    parts = [_.strip() for _ in chart_contents.split(':')]
    chart.author = parts[1]
    chart.difficulty = parts[2]
    chart.rating = int(parts[3])
    measure_strings = parts[5].split(',')

    holds = [None, None, None, None]

    for measure_string in measure_strings:
        measure = models.Measure()
        rows = [_.strip() for _ in measure_string.splitlines() if _]
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


def apply_bpms(chart, bpm_changes, offset):
    """
    Applies a list of BPM changes to a chart.
    Calculates and applies the 'time' field of measures

    :param chart: a models.Chart object
    :param bpm_changes: a list of bpm changes, in the format "b.bbb=b.bbb", sorted by the first element
    :param offset: the offset, in seconds, from the time of the start of the song
    """

    bpms = [{'start_beats': float(b.split('=')[0]), 'bpm': float(b.split('=')[1])} for b in bpm_changes]

    bpm_it = iter(bpms)
    current_bpm, next_bpm = next(bpm_it), next(bpm_it, None)

    time = -offset
    beats = 0
    for measure in chart.measures:
        measure.time = time
        if next_bpm is not None and next_bpm['start_beats'] == beats:
            current_bpm, next_bpm = next_bpm, next(bpm_it, None)
        measure.bpms.append((0, current_bpm['bpm']))

        while next_bpm is not None and next_bpm['start_beats'] < beats + 4:
            measure.bpms.append((next_bpm['start_beats'] - beats, next_bpm['bpm']))
            current_bpm, next_bpm = next_bpm, next(bpm_it, None)
        time = round(time + measure.duration(), 6)  # minimize fp error
        beats += 4
