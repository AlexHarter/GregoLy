def parse_gabc_header(gabc_header):
    gabc_header_lines = gabc_header.split(";\n")
    if gabc_header_lines[-1] == "":
        gabc_header_lines.pop(-1)

    header_entries = {}
    for line in gabc_header_lines:
        key, value = line.split(":", 1)  # in case there are colons in the value
        header_entries.update({key.strip(): value.strip()})

    return header_entries


# test
test_gabc_header = r"""
name:Deus Israel;
office-part:Introitus;
mode:3;
user-notes: LU 1288;
transcriber:Andrew Hinkley & Patrick Williams;
commentary: Tob. 7:15 & 8:19, Ps. 127:1;
annotation: IN. III;
"""
print(parse_gabc_header(test_gabc_header))
