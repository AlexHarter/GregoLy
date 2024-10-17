
ly_lyrics = ""
parsing_lyrics = False
first_syllable = True
gabc_body = "(c4) DE(gj)us(jjj_) Is(jj)ra(jj)el(jj) *(,)"
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
ly_lyrics.strip()
print(ly_lyrics)
