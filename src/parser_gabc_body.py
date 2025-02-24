import gregolib as gl

def parse_gabc_body(gabc_body):
    syllable = gl.Syllable()
    syllables = []
    
    parsing_mode = "lyrics" # default

    for i,c in enumerate(gabc_body):
        # detect parsing mode change
        if c == "(":
            parsing_mode = "melody"
            continue
        elif c == ")":
            # process parsed text
            if syllable.text != " ":
                syllable.text = syllable.text.strip()
            if i < len(gabc_body) - 1:
                if gabc_body[i+1] == " ":
                    syllable.tie = False
            syllable.notes = parse_syllable_melody(syllable.melody)
            syllables.append(syllable)
            
            syllable = gl.Syllable()
            parsing_mode = "lyrics"

            # process parsed melody
            
            continue
            
        # parsing based on mode
        elif parsing_mode == "lyrics":
            syllable.text += c
        elif parsing_mode == "melody":
            # clef check
                
            syllable.melody += c
        
    return syllables

def parse_syllable_melody(syllable_melody):
    notes = []
    note = gl.Note()

    for i,c in enumerate(syllable_melody):
        match c:
            case c if c in gl.gabc_positions:
                if note.position != None:
                    notes.append(note)
                note = gl.Note(position=c)
            case c if c in gl.note_kinds:
                note.kind = gl.note_kinds[c]
            case c if c in gl.note_lengthening:
                note.lengthening = gl.note_lengthening[c]
            case c if c in gl.note_liquescence:
                note.liquescence = gl.note_liquescence[c]
            """
            if i < len(gabc_body) - 4:
                if gabc_body[i:i+3] in gl.clefs:
                    clef = gabc_body[i:i+3]
                    continue
                elif gabc_body[i:i+4] in gl.clefs:
                    clef = gabc_body[i:i+4]
                    continue
            """
                
    notes.append(note)
    
    return notes

#test
gabc_body = r"(c4) DE(gj)us(jjj_) Is(h_)ra(h_0!iWj_//kjjo_)el(ji__) *(,) con(gh~)jún(hjij)gat(ih~) vos,(h_) (;) et(g_) i(h_)pse(g_) sit(gfh_) vo(h_)bís(h_0!iwji.__H~rG~rhv_)cum,(hg.__) (;) qui(gh/ji) mi(j_)sér(j_)tus(jjj_) est(h_) (;) du(h_)ó(h_)bus(hfh_) ú(h_//ivHG_0)ni(hg)cis:(g._) (;) et(g_) nunc,(hj) Dó(i_//jjg_//h_//jjh_)mi(hf__!gwhgh_)ne,(hg__) (;) fac(g_) e(-gh_)os(h_) plé(h_0!iWj_)ni(g_)us(gh__) (;) be(f_)ne(f_)dí(efOh_)ce(h_)re(gf__//hvGF_0gv_) te.(e._) <i>T. P.</i>(::) Al(e<_)le(f_)lú(gf~)ia.(g_) (;) al(gf~)le(ge__/f_0!gwhg__)lú(ghghFD__!eWf_//ge~)ia.(e._) (::) <i>Ps.</i> Be(g)á(hi)ti(i_) o(i_)mnes(i_) qui(j_) ti(k_)ment(j_) Dó(j_)mi(ih)num :(jjj._) *(:) qui(hg) ám(hi~)bu(i_)lant(i_) in(jjji) vi(hg)is(h_) e(i>_)jus.(gOh.__) (::) Gló(g_)ri(hi)a(i_) Pa(i_)tri...(i_) (::) Spi(j_)rí(k_)tu(j_)i(j_) San(ih~)cto...(jjj._) (::) Et(j_) nunc,(k_) et(j_) sem(ih~)per...(jjj._) (::) E(i_) u(jjji) o(hg) u(h_) a(i_) e.(gOh._) (::)"

syllables = parse_gabc_body(gabc_body)

for syllable in syllables:
    print(syllable.__str__())
