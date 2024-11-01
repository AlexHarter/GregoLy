
\version "2.24.4"

\header {
  office-part = "Introitus"
  mode = "3"
  user-notes = "LU 1288"
  transcriber = "Andrew Hinkley & Patrick Williams"
  commentary = "Tob. 7:15 & 8:19, Ps. 127:1"
  annotation = "IN. III"
  title = "Deus Israel"

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

  (LilyPond Melody)
}

text = \lyricmode {
  DE -- us Is -- ra -- \markup {"el" *} con -- jún -- gat vos,  et i -- pse sit vo -- bís -- cum,  qui mi -- sér -- tus est  du -- ó -- bus ú -- ni -- cis:  et nunc, Dó -- mi -- ne,  fac e -- os plé -- ni -- us  be -- ne -- dí -- ce -- re te. <i>T. P.</i> Al -- le -- lú -- ia.  al -- le -- lú -- ia.  <i>Ps.</i> Be -- á -- ti o -- mnes qui ti -- ment Dó -- mi -- num : * qui ám -- bu -- lant in vi -- is e -- jus.  Gló -- ri -- a Pa -- tri...  Spi -- rí -- tu -- i San -- cto...  Et nunc, et sem -- per...  E u o u a e.
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
      instrumentName = IN. III
      \consists Custos_engraver
      \override Custos.style = #'medicaea
    }
  }
}
% score generated from https://github.com/AlexHarter/GregoLy on <2024-10-17>
