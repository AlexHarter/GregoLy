note_liquescence = {
    "" :None,
    ">":"augmentative_ascending",
    "<":"augmentative_descending",
    "~":"diminutive",
}
note_lengthening = {
    "" :None,
    "_":"episema",
    ".":"morae"
}

# formatting
# gabc notates position on a staff rather than absolute pitches, so that's the main conversion I have to do for lilypond
gabc_positions_with_position_ints = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11,
    "m": 12,
}
gabc_positions = gabc_positions_with_position_ints.keys()
clefs_with_position_int_of_do = {
    "c1": 3,
    "c2": 5,
    "c3": 7,
    "c4": 9,
    "f1": 0,
    "f2": 2,
    "f3": 4,
    "f4": 6,
    "cb1":3,
    "cb2":5,
    "cb3":7,
    "cb4":9,
}
clefs = clefs_with_position_int_of_do.keys()
note_kinds = {
    ""  :"punctum",
    "0" :"hollow_punctum",
    "w" :"quilisma",
    "o" :"oriscus",
    "," :"quarter_bar",
    ";" :"half_bar",
    ":" :"full_bar",
    "::":"double_bar",
    #clefs :"clef"
}
distance_from_do_with_ly_pitch_classes = {
    -9: "a",
    -8: "b",
    -7: "c",
    -6: "d",
    -5: "e",
    -4: "f",
    -3: "g",
    -2: "a",
    -1: "b",
     0: "c",
     1: "d",
     2: "e",
     3: "f",
     4: "g",
     5: "a",
     6: "b",
}

class Note:
    def __init__(
        self,
        kind="punctum",
        position=None,
        lengthening=None,
        liquescence=None,
        vertical_episema=False
        ):

        self.kind = kind
        self.position = position
        self.lengthening = lengthening
        self.liquescence = liquescence
        self.vertical_episema = vertical_episema

    def __str__(self):
        return f"kind={self.kind};position={self.position};lengthening={self.lengthening};liquescence={self.liquescence};vertical_episema={self.vertical_episema}."

class Syllable:
    def __init__(self, text="", tie=True,  melody="", notes=[]):
        self.text = text
        self.tie = tie
        self.melody = melody
        self.notes = notes

    def __str__(self):
        notes_str = "\n".join(str(note) for note in self.notes)
        return f"text=\"{self.text}\";tie={self.tie};melody=\"{self.melody}\";notes:\n{notes_str}"

def gabc_position_to_ly_pitch_class(clef, gabc_position):
    distance_from_do = (
        gabc_positions_with_position_ints[gabc_position]
        - clefs_with_position_int_of_do[clef]
    )
    ly_pitch_class = distance_from_do_with_ly_pitch_classes[distance_from_do]
    return ly_pitch_class
