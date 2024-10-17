#!/usr/bin/env python
# coding: utf-8

# # Init
# ## Import Libraries
print("Importing modules..")
import argparse
import re
from datetime import datetime
import subprocess

# ## Take in user arguments
# - /path/to/file.gabc
# - in which rhythmic system to interpret
#   - "P" *P*roportional
#   - "S" Classical *S*olesmes
#   - "V" *V*atican 
# - key (default: as close to C4-C5 as possible, within two accidentals)
# - interpretive options
#   - presence of special neumes (default: yes to all)
#   - explicit notation of special neumes (default: neume noteheads)
# - aesthetic options
#   - presence of custodes (default: yes)
#   - staff color (default: dark red)


print("Processing user arguments...")
parser = argparse.ArgumentParser(description="Process some mutually exclusive flags.")
group = parser.add_mutually_exclusive_group(required=False)

group.add_argument("-P", "--proportional", action="store_true", help="Enable option P")
group.add_argument("-S", "--solesmes", action="store_true", help="Enable option S")
group.add_argument("-V", "--vatican", action="store_true", help="Enable option V")

# Add an argument for the file path
parser.add_argument("-f", "--file", type=str, help="Path to the input file")

args = parser.parse_args()

# If neither S nor V is set, set P to True by default
if not (args.solesmes or args.vatican):
    args.proportional = True

if args.proportional:
    print("Proportional option is enabled.\n")
elif args.solesmes:
    print("Classical Solesmes option is enabled.\n")
elif args.vatican:
    print("Vatican Edition option is enabled.\n")
else:
    print("Proportional option is enabled. (default)")

# Handle the file path argument
if args.file:
    print(f"Using input file: {args.file}")
else:
    print("No input file specified.")

# ## Define LilyPond Template # is this even necessary? Well, maybe if I want to customize macros...
print("Defining LilyPond template...") 
# LilyPond Emmentaler Font Reference:
# https://lilypond.org/doc/v2.24/Documentation/notation/the-emmentaler-font#vaticana-glyphs

ly_template = r"""
\version "2.24.4"

\header {
%ly_metadata
}

oriscus = {
  \once \override NoteHead.stencil = #ly:text-interface::print
  \once \override NoteHead.text = \markup \musicglyph "noteheads.ssolesmes.oriscus"
  \once \set fontSize = 3
}

quilisma = {
  \once \override NoteHead.stencil = #ly:text-interface::print
  \once \override NoteHead.text = \markup \musicglyph "noteheads.svaticana.quilisma"
  \once \set fontSize = 3
  \once \override Stem.transparent = ##t
}

initioDebilis = {
  \once \set fontSize = -3
  \once \override Stem.transparent = ##t
}

liquescentDiminutive = {
  \once \set fontSize = -3
}

liquescentAugmentativeAscending = {
  \once \override NoteHead.stencil = #ly:text-interface::print
  \once \override NoteHead.text = \markup \musicglyph "noteheads.ssolesmes.auct.asc"
  \once \set fontSize = 3
}

liquescentAugmentativeDescending = {
  \once \override NoteHead.stencil = #ly:text-interface::print
  \once \override NoteHead.text = \markup \musicglyph "noteheads.ssolesmes.auct.desc"
  \once \set fontSize = 3
}

quarterBar = {
  \bar ","
}

halfBar = {
  \bar ";"
}

fullBar = {
  \bar "|"
}

doubleBar = {
  \finalis
}

global = {
  \key c \major
  \candenzaOn
  \omit Staff.TimeSignature
  \override Staff.StaffSymbol.color = #darkred
}

melody = \transpose c c \relative c'' {
  \global

  %ly_melody
}

text = \lyricmode {
  %ly_lyrics
}

\score {
  <<
  \new Staff {
    \context Voice = "vocal" { \melody }
  }
  \new Lyrics \lyricsto "vocal" \text
  >>
  \layout {
    \context {
      \Staff
      %annotation
      \consists Custos_engraver
      \override Custos.style = #'medicaea
    }
  }
}
% score generated from https://github.com/AlexHarter/GregoLy on <%DATE>
"""
# export template
with open("template.ly", "w") as file:
    file.write(ly_template)

# ## Import and Split GABC
print("Importing and splitting .gabc file...")
with open(args.file, 'r') as file:
    gabc = file.read()

#print(f"Full GABC:\n{gabc}")

gabc_header = gabc.split("%%")[0]
gabc_body = gabc.split("%%")[1]

#print(f"GABC Header:\n{gabc_header}")
#print(f"GABC Body:\n{gabc_body}")


# # Parse Data
print("Parsing data...")
# ## Parse Header
# ### Example Input/Output
# #### Example Input
"""
name:Deus Israel;
office-part:Introitus;
mode:3;
user-notes: LU 1
288;
transcriber:Andrew Hinkley & Patrick Williams;
commentary: Tob. 7:15 & 8:19, Ps. 127:1;
annotation: IN. III;
"""
# #### Desired Output
# - sometimes, LilyPond has a different keyword, e.g. "title" instead of gabc's "name"
"""
title = "Deus Israel"
office-part = "Introitus"
mode = 3
user-notes = "LU 1288"
transcriber = "Andrew Hinkley & Patrick Williams"
commentary = "Tob. 7:15 & 8:19, Ps. 127:1"
annotation = "IN. III"
"""
# ### Header Parser
print("Parsing header...")
gabc_header = gabc_header.strip()
if gabc_header[-1] == ";":
    gabc_header = gabc_header[:-1]
gabc_header_entries = gabc_header.split(";\n")
gabc_header_dictionary = {}
for entry in gabc_header_entries:
    #print(entry) # testing
    key, value = entry.split(":", 1) # in case there are colons in the value
    gabc_header_dictionary.update({key.strip(): value.strip()})
ly_metadata = []
#print(gabc_header_dictionary) # testing
# replace gabc term with ly term when different, e.g. name -> title
if "name" in gabc_header_dictionary:
    gabc_header_dictionary["title"] = gabc_header_dictionary.pop("name")
for key, value in gabc_header_dictionary.items():
    ly_metadata.append(f"  {key} = \"{value}\"\n")
# test
#print(f"LilyPond Metadata:\n{ly_metadata}")


# ## Parse Body
# ### Define Pitch Datasets and Functions
# - Not affected by school of rhythmic interpretation

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
    special_nuemes = ("none", "oriscus", "quilisma", "initio_debilis")
    liquescence = ("none", "diminutive", "augmentative_ascending", "augmenetative_descending")

    def __init__(self, pitch_class, octave=4, duration="8", special_nueme="none", liquescence="none", first_in_syllable=False, last_in_syllable=False):
        self.pitch_class = pitch_class
        self.octave = octave
        self.duration = duration
        self.special_nueme = special_nueme
        self.liquescence = liquescence
        self.first_in_syllable = first_in_syllable
        self.last_in_syllable = last_in_syllable
    
    # this function is kept simple because the complex formatting will be
    # specific to context
    def __str__(self):
        return f"{pitch_class}{duration}"

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
# ###### Desired Lyrics Output
r"""
DE -- us Is -- ra -- \markup {"el" *}
con -- jún -- gat vos,
et ip -- se sit vo -- bís -- cum,
"""
# ##### Proportionalist Parsing Function
# #### Classical Solesmes
if args.solesmes:
    print("Classical Solesmes not currently supported")
# #### Vatican Edition
# - Rather than symbols attached to nuemes, this one will look for barlines and spacing indicating morae vocis.
if args.vatican:
    print("Vatican Edition not currently supported")
# ### Body Parser
print("Parsing body...")
# #### Lyrics Parser
print("Parsing lyrics...")
# extract lyrics
ly_lyrics = ""
parsing_lyrics = False
first_syllable = True
for i, c in enumerate(gabc_body):
    if c == ")":
        parsing_lyrics = True
        if i < len(gabc_body) - 1:
            if gabc_body[i+1] != " ":
                ly_lyrics += " -- "
    elif c == "(":
        parsing_lyrics = False
    elif parsing_lyrics == True:
        ly_lyrics += c
ly_lyrics = ly_lyrics.strip()

# format lyrics
## intonation/asterisk
match = re.search(r'(\w+)\s*\*', ly_lyrics)
if match:
    last_syllable = match.group(1)
    ly_lyrics = re.sub(r'(\w+)\s\*', fr'\\markup {{"{last_syllable}" *}}', ly_lyrics)

# #### Melody Parser
print("Parsing melody...")
ly_melody = "(LilyPond Melody)"

# # Output
# - import data, interpolate from template, and return

ly_template_interpolated = ly_template
ly_template_interpolated = ly_template_interpolated.replace("%ly_metadata", ''.join(ly_metadata))
ly_template_interpolated = ly_template_interpolated.replace("%ly_melody", ly_melody)
ly_template_interpolated = ly_template_interpolated.replace("%ly_lyrics", ly_lyrics)
ly_template_interpolated = ly_template_interpolated.replace(
    "%annotation", 
    f"instrumentName = {gabc_header_dictionary['annotation']}")
date = datetime.now().strftime("%Y-%m-%d")
ly_template_interpolated = ly_template_interpolated.replace("%DATE", date)

with open("chant.ly", "w") as file:
    file.write(ly_template_interpolated)
print(ly_template_interpolated)
# ## Compile .ly file using lilypond cli
#subprocess.run(['lilypond' 'chant.ly'])

