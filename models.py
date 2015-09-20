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
    '''

    def init_fields(self):
        self.author = None
        self.difficulty = None
        self.rating = None


class Song:
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
    '''

    def init_fields(self):
        self.title = ''
        self.banner = ''
        self.bg = ''
        self.music = ''
        self.offset = 0
        self.sample_st = 0
        self.sample_len = 0
        self.bpms = ''


class Measure:
    '''
    Data and notes about a single measure in a chart (usually 4 beats)

    Fields:
        rows: number of rows in this measure
        notes: list of notes in this measure
        time: time (in seconds) between the start of the song and the start of this measure
        bpms: list of 2-tuples (time in seconds, bpm) of bpm changes in this measure.
              if empty, assumes bpm to be the same as previous measure
    '''

    def init_fields(self):
        self.rows = 0
        self.time = 0
        self.bpms = []
        self.notes = []


class Note:
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

    def __init__(self, **kwargs):
        raise NotImplementedError

    def init_fields(self):
        self.position = 0
        self.offset = 0
        self.note_type = 0


class Tap(Note):
    '''
    A type of note that only has to be pressed once.
    '''

    TYPE_NORMAL = 1
    TYPE_MINE = 'M'

    def init_fields(self):
        super().init_fields()


class Hold(Note):
    '''
    A type of note that must be held.

    Fields:
        duration: the duration (in measures) this note should last
    '''

    TYPE_HOLD = 2
    TYPE_ROLL = 4

    def init_fields(self):
        super().init_fields()
        self.duration = 0
