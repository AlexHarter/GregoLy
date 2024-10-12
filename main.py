#!/usr/bin/env python
# coding: utf-8

# # Init
# ## Import Libraries

import argparse # will use, but not yet
import regex # may or may not use
from datetime import date # will use, but not yet
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

# default: proportional
user_args = "P"
#TODO user_args = argparse()
print(f"User arguments: {user_args}")

# ## Define LilyPond Template
# LilyPond Emmentaler Font Reference:
# https://lilypond.org/doc/v2.24/Documentation/notation/the-emmentaler-font#vaticana-glyphs

ly_template = 
r"""
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

  %test ly_melody
  g8( c) c[ c] c4
  %end test
}

text = \lyricmode {
  %test ly_lyrics
  De --- us
  %end test
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
      %test annotation

      %end test
      \consists Custos_engraver
      \override Custos.style = #'medicaea
    }
  }
}
% score generated from https://github.com/AlexHarter/GregoLy on <%DATE>
"""

# ## Import and Split GABC

gabc_file_path = "tests/in--deus_israel--proportional.gabc" # example
with open(gabc_file_path, 'r') as file:
    gabc = file.read()

print(f"Full GABC:\n{gabc}")

gabc_header = gabc.split("%%")[0]
gabc_body = gabc.split("%%")[1]

print(f"GABC Header:\n{gabc_header}")
print(f"GABC Body:\n{gabc_body}")


# # Parse Data
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

#TODO remove semicolon from last entry
gabc_header_entries = gabc_header.strip().split(";\n")
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
    ly_metadata.append(f"{key} = \"{value}\"")
# test
print(f"LilyPond Metadata:\n{ly_metadata}")


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

# test
example_clef = "c4"
example_gabc_position = "i"
example_output = gabc_position_to_ly_pitch_class(example_clef, example_gabc_position)

print(example_output)

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
# [Score](tests/in--deus_israel--proportional-gregorian.pdf)

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
# [Score](tests/in--deus_israel--proportional-modern.pdf)
# ##### Proportionalist Parsing Function

def parse_gabc_syllable_melody_proportional(gabc_syllable_melody):
    return 0


# ## Classical Solesmes
# #### Vatican Edition
# - Rather than symbols attached to nuemes, this one will look for barlines and spacing indicating morae vocis.
# ### Body Parser

for i, c in enumerate(gabc_body):
    gabc_body = gabc_body.strip()

    # we expect the clef to be defined first
    if i == 0:
        if c == "(":

            if gabc_body[i+1:i+3] in clefs and gabc_body[i+3] == ")":
                clef = gabc_body[i+1:i+3]
                i += 4
            else:
                print("clef not defined")
                return 0

    elif c == "(":
        syllable_melody = ""
        while c is not ")":
            syllable_melody += c
            i += 1
        match user_args:
            case "P":
                parse_gabc_syllable_melody_proportional(syllable_melody)
            case "S":
                print("Solesmes not yet supported.")
                return 0
            case "V":
                print("Vatican not yet supported.")
                return 0
        

    if gabc_body[i+1] == " ":
        ly_lyrics += " "
    else:
        ly_lyrics += " -- "

    parsing_mode = "lyrics"
    break

    elif parsing_mode == "lyrics":
        ly_lyrics += c


# # Output
# - import data, interpolate from template, and return

with open("template.ly", "r") as file:
    ly_template = file.read()

ly_template_interpolated = ly_template
ly_template_interpolated = ly_template_interpolated.replace("% ly_metadeta", ''.join(ly_metadata))
ly_template_interpolated = ly_template_interpolated.replace("% ly_melody", ly_melody)
ly_template_interpolated = ly_template_interpolated.replace("% ly_lyrics", ly_lyrics)
ly_template_interpolated = ly_template_interpolated.replace("% annotation", f"instrumentName = {ly_metadata[\"annotation\"]}")
ly_template_interpolated = ly_template_interpolated.replace("%DATE", date.

with open("chant.ly", "w") as file:
    file.write(ly_template_interpolated)


# ## Compile .ly file using lilypond cli

#subprocess.run(['lilypond' 'output.ly'])

