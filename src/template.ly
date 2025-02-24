% font reference:
%% https://lilypond.org/doc/v2.24/Documentation/notation/the-emmentaler-font#vaticana-glyphs

\version "2.24.4"

\header {
  %ly_metadata

  %end
}

oriscus = {
  %default_oriscus
  \once \override NoteHead.stencil = #ly:text-interface::print
  \once \override NoteHead.text = \markup \musicglyph "noteheads.ssolesmes.oriscus"
  \once \set fontSize = 3
  %end
}

quilisma = {
  %default_quilisma
  \once \override NoteHead.stencil = #ly:text-interface::print
  \once \override NoteHead.text = \markup \musicglyph "noteheads.svaticana.quilisma"
  \once \set fontSize = 3
  \once \override Stem.transparent = ##t
  %end
}

initioDebilis = {
  %default_initioDebilis
  \once \set fontSize = -3
  \once \override Stem.transparent = ##t
  %end
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
  \bar "'"
}

halfBar = {
  \bar ";"
}

fullBar = {
  \bar "|"
}

doubleBar = {
  \bar "||"
}

global = {
  \key c \major
  \omit Staff.TimeSignature
  \candenzaOn
  \override Staff.StaffSymbol.color = #darkred
}

melody = \transpose c c \relative c'' {
  \global

  %ly_melody

  %end
}

text = \lyricmode {
  %ly_lyrics

  %end
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
