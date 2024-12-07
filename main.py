#!/usr/bin/env python
# coding: utf-8

print("Importing modules..")
import argparse
import re
from datetime import datetime
import subprocess

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

print("Importing and splitting .gabc file...")
with open(args.file, 'r') as file:
    gabc = file.read()

#print(f"Full GABC:\n{gabc}")

gabc_header = gabc.split("%%")[0]
gabc_body = gabc.split("%%")[1]

#print(f"GABC Header:\n{gabc_header}")
#print(f"GABC Body:\n{gabc_body}")

print("Parsing data...")

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

if args.solesmes:
    print("Classical Solesmes not currently supported")

if args.vatican:
    print("Vatican Edition not currently supported")

print("Parsing body...")

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

print("Parsing melody...")
ly_melody = "(LilyPond Melody)"

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

subprocess.run(['lilypond' 'chant.ly'])
