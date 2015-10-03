class Model:
    '''
    Base class for all models.
    '''

    def __init__(self, **kwargs):
        self.init_fields()

        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise AttributeError


class Chart(Model):
    '''
    A collection of data related to a single chart, including metadata and notes.

    Fields:
        author: the name of the author of the chart.
        difficulty: the named difficulty of the chart
        rating: the numeric difficulty of the chart

        measures: list of measures in the chart
    '''

    def init_fields(self):
        self.author = None
        self.difficulty = None
        self.rating = None

        self.measures = []


class Song(Model):
    '''
    Metadata about a song, and all of the charts associated with it.

    Fields:
        title: title of the song
        banner: filename of the banner for the song
        bg: filename of the background image for the song
        music: filename of the song
        offset: offset (in seconds)
        sample_st: start time (in seconds) of the sample
        sample_len: length (in seconds) of the sample
        bpms: the BPM range of the song, as a string
        charts: list of charts in the song
    '''

    def init_fields(self):
        self.title = ''
        self.artist = ''
        self.banner = ''
        self.bg = ''
        self.music = ''
        self.offset = 0
        self.sample_st = 0
        self.sample_len = 0
        self.bpms = ''

        self.charts = []


class Measure(Model):
    '''
    Data and notes about a single measure in a chart (usually 4 beats)

    Fields:
        rows: number of rows in this measure
        notes: list of notes in this measure
        time: time (in seconds) between the start of the song and the start of this measure
        bpms: list of 2-tuples (time in seconds from start of measure, bpm) of
              bpm changes in this measure.
              must have at least 1 specifying the initial bpm of the measure
    '''

    def init_fields(self):
        self.rows = 0
        self.time = 0
        self.bpms = []

        self.notes = []

    def duration(self):
        '''
        Calculate the duration (in seconds) of this measure based on its bpms
        Assumes 4/4 time (all simfiles are 4/4)

        :return: the seconds that this measure lasts
        '''
        duration = 0
        total_beats = 0
        for i, bpm in enumerate(self.bpms[1:]):
            prev_bpm = self.bpms[i]
            time_diff = bpm[0] - prev_bpm[0]
            duration += time_diff
            beats = time_diff * prev_bpm[1] / 60  # b = s * b/min / (60 s/min)
            total_beats += beats
        duration += (4 - total_beats) * 60 / self.bpms[-1][1]  # account for last bpm section

        return duration


class Note(Model):
    '''
    A single note in a chart.

    Fields:
        position: the position (LDUR) of this note. Should be specified as one of the
                  POSITION_ constants
        offset: the offset (in rows) from the start of the measure to the start of this note
        note_type: the type of note. Should be specified as one of the TYPE_ constants
    '''

    POSITION_LEFT = 0
    POSITION_DOWN = 1
    POSITION_UP = 2
    POSITION_RIGHT = 3

    TYPE_NONE = '0'
    TYPE_END = '3'

    def __init__(self, **kwargs):
        raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def init_fields(self):
        self.position = 0
        self.offset = 0
        self.note_type = 0


class Tap(Note):
    '''
    A type of note that only has to be pressed once.
    '''

    TYPE_NORMAL = '1'
    TYPE_MINE = 'M'
    TYPES = [TYPE_NORMAL, TYPE_MINE]

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def init_fields(self):
        super().init_fields()


class Hold(Note):
    '''
    A type of note that must be held.

    Fields:
        duration: the duration (in measures) this note should last
    '''

    TYPE_HOLD = '2'
    TYPE_ROLL = '4'
    TYPES = [TYPE_HOLD, TYPE_ROLL]

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def init_fields(self):
        super().init_fields()
        self.duration = 0
