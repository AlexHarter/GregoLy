
# datasets
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
    "m": 12
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
    "f4": 6
}
clefs = clefs_with_position_int_of_do.keys()
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
     6: "b"
}
# functions
def gabc_position_to_ly_pitch_class(clef, gabc_position):
    distance_from_do = gabc_positions_with_position_ints[gabc_position] - clefs_with_position_int_of_do[clef]
    ly_pitch_class = distance_from_do_with_ly_pitch_classes[distance_from_do]
    return ly_pitch_class
#TODO move to LyNote class?

# test gabc_position_to_ly_pitch_class()
"""
example_clef = "c4"
example_gabc_position = "i"
example_output = gabc_position_to_ly_pitch_class(example_clef, example_gabc_position)
print(example_output)
"""
# classes
class LyNote:
    durations = ("1", "2", "4", "4.", "8", "16")
    octaves = (3, 4, 5)
    special_nuemes = (None, "oriscus", "quilisma", "initio_debilis")
    liquescence = (None, "diminutive", "augmentative_ascending", "augmenetative_descending")

    def __init__(self, 
                 pitch_class, 
                 octave=4, # change to octave_shift? or a contour ascending/descending attribute?
                 duration="8", 
                 special_nueme=None, 
                 liquescence=None, 
                 first_in_syllable=False, 
                 last_in_syllable=False,
                 nuematic_break=False):
        self.pitch_class = pitch_class
        self.octave = octave
        self.duration = duration
        self.special_nueme = special_nueme
        self.liquescence = liquescence
        self.first_in_syllable = first_in_syllable
        self.last_in_syllable = last_in_syllable
        self.nuematic_break=nuematic_break

    # this function is kept simple because the complex formatting will need to happen in an outside function 
    # because the output will depend on context
    def __str__(self):
        return f"{self.pitch_class}{self.duration}"

# ### Define Rhythm Interpretation-Specific Functions
# - I choose a separate function for the melody within the syllable because it is guaranteed to be self-contained, apart from the clef.
#   - This helps with slurs, beaming, and alterations.
# - What are the rules for accidentals? I think that they last for the word, so that will have to be handled outside of this function
# #### Proportionalist
# ##### Example Input/Output
# ###### Example Input
r"""
(c4) DE(gj)us(jjj_) Is(h_)ra(h_0!iWj_//kjjo_)el(ji__) *(,)
con(gh~)jún(hjij)gat(ih~) vos,(h_) (;)
et(g_) i(h_)pse(g_) sit(gfh_) vo(h_)bís(h_0!iwji.__H~rG~rhv_)cum,(hg.__) (;)
"""

# ###### Desired Melody Output
r"""
g8([ c]) c([ c] c4) a a( \quilisma b16 c4 d8[ c] \oriscus c4) c( b) \bar "'"
g8([ \liquescentDiminutive a]) a([ c b c]) b([ \liquescentDiminutive a]) a4 \bar "," \break
g4 a g g8([ f] a4) a a( \quilisma b16 c4 b4. a16[ g] a4) a( g2) \bar ","
"""

# ##### Proportionalist Parsing Function
gabc_body = r"""
(c4) DE(gj)us(jjj_) Is(h_)ra(h_0!iWj_//kjjo_)el(ji__) *(,)
"""
# extract melody
ly_notes = []
clef_defined = False
parsing_melody = False
for i, c in enumerate(gabc_body):
    if clef_defined == True:
        if c in gabc_positions: #pitch
            note = LyNote(pitch_class=gabc_position_to_ly_pitch_class(clef, c))
            if gabc_body[i-1] == "("
                note.first_in_syllable = True
            ly_notes.append(note)
        elif c == "_": #episema
            ly_notes[-1].duration = "4"
            if gabc_body[i+1] == "_":
                ly_notes[-2].duration = "4"
            elif gabc_body[i+1] == ".":
                ly_notes[-1].duration = "4."
        elif c == ".":
            ly_notes[-1].duration = "2"
        elif c == "W": #quilisma
            ly_notes[-1].duration = "16"
            ly_notes[-1].special_nueme = "quilisma"
        elif c == "o": #oriscus
            ly_notes[-1].special_nueme = "oriscus"
        elif c == ")":
            parsing_mode = False
            ly_notes[-1].last_in_syllable = True
    elif clef_defined == False:
        if c == "(":
            print("Looking for clef...")
            print(f"Checking if {gabc_body[i+1:i+3]} is a clef...")
            if gabc_body[i+1:i+3] in clefs:
                print(f"Defining clef as {gabc_body[i+1:i+3]}...")
                clef = gabc_body[i+1:i+3]
                clef_defined = True


# format ly_notes to ly_melody
ly_melody = ""

for note in ly_notes:
    ly_melody += note.__str__()
print(ly_melody)
