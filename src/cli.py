import argparse
import subprocess

"""
- accept user input, call parsing and formatting functions, customize output
- arguments
  - /path/to/file.gabc
  - in which rhythmic system to interpret
    - "P" *P*roportional
    - "S" Classical *S*olesmes
    - "V" *V*atican 
  - key (default: as close to C4-C5 as possible, within two accidentals)
  - interpretive options
    - presence of special neumes (default: yes to all)
    - explicit notation of special neumes (default: neume noteheads)
  - aesthetic options
    - presence of custodes (default: yes)
    - staff color (default: dark red)
"""

parser = argparse.ArgumentParser(description="Process some mutually exclusive flags.")
group = parser.add_mutually_exclusive_group(required=False)

parser.add_argument("-F", "--file", type=str, help="Path to the input .gabc file")

# TODO - for now, just Proportional
group.add_argument(
    "-P", "--proportional", action="store_true", help="Proportional Mode"
)
group.add_argument("-S", "--solesmes", action="store_true", help="Solesmes Mode")
group.add_argument("-V", "--vatican", action="store_true", help="Vatican Mode")

""" TODO - for now, just focus on defaults
group.add_argument("--staffcolor", type=bool, help="Staff color.  Default: Dark Red")
group.add_argument("--custodes", type=bool, help="Presence of custodes at the end of systems")
group.add_argument("--quilisma", type=str, help="How to notate the quilisma neumes.")
group.add_argument("--oriscus", type=str, help="How to notate the oriscus neumes")
group.add_argument("--key", type=str, help="Desired key of the score.  Default: As close to C4-C5 as possible, within two accidentals.")
"""

args = parser.parse_args()

if args.proportional:
    print("Proportional option is enabled.\n")
elif args.solesmes:
    print("Classical Solesmes option is not currently supported.\n")
    exit()
elif args.vatican:
    print("Vatican Edition option is not currently supported.\n")
    exit()
else:
    if not (args.solesmes or args.vatican):
        args.proportional = True
    print("Proportional option is enabled. (default)\n")

if args.file:
    print(f"Using input file: {args.file}")
else:
    print("No input file specified.")
    exit()

print("Importing .gabc file...")
with open(args.file, "r") as file:
    gabc = file.read()


def compile_lilypond(ly_file):
    try:
        subprocess.run(["lilypond", ly_file], check=True)
        print("Compilation successful!")
    except subprocess.CalledProcessError as e:
        print("Error during compilation:", e)
