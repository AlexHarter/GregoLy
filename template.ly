
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
