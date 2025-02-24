### Functions
"""
print("Creating output...")

f = open("template.ly", "r")
ly_output = f.read()

ly_output = ly_output.replace("%ly_metadata", ''.join(ly_metadata))
ly_output = ly_ouput.replace("%ly_melody", ly_melody)
ly_output = ly_output.replace("%ly_lyrics", ly_lyrics)
ly_output = ly_output.replace(
    "%annotation",
    f"instrumentName = {gabc_header_dictionary['annotation']}")

from datetime import date
date = datetime.now().strftime("%Y-%m-%d")
ly_template_interpolated = ly_template_interpolated.replace("%DATE", date)

with open("target/chant.ly", "w") as file:
    file.write(ly_template_interpolated)
print(ly_template_interpolated)

print("Compiling .ly file to .pdf...")
import subprocess
subprocess.run(['lilypond' 'chant.ly'])
"""
