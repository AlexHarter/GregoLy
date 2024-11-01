import re

text = "Is -- ra -- el *"
match = re.search(r'(\w+)\s\*', text)
print(f"match is {match}")
if match:
    # Capture the last syllable (the word before the asterisk)
    last_syllable = match.group(1)
    print(f"last syllable is {last_syllable}")
    # Replace the asterisk with the desired format \markup {"syllable" *}
    text = re.sub(r'(\w+)\s*\*', fr'\\markup {{"{last_syllable}" *}}', text)

print(text)
