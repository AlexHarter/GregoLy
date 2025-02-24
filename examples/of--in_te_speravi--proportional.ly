\version "2.24.4"

\header {
  title = "In te speravi"
  subtitle = "Offertory for the Feast of the Holy Family"
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
  \bar ","
}

fullBar = {
  \bar "|"
}

doubleBar = {
  \bar "||"
}

global = {
  \key d \minor
  \omit Staff.TimeSignature
  \cadenzaOn
  \override Staff.StaffSymbol.color = #darkred
}

melody = \transpose c c \relative c' {
  \global
  % In te speravi *
  a8 c4( d8[ e]) d4 f( d \quilisma e16 f4 g f) f8([ f] f4 e c \quilisma d16 f4 \initioDebilis e16 d4) \quarterBar
  
  % Domine:
  d4 d( \quilisma e16 f8[ e] f4) e( d2) \halfBar
  
  % dixi:
  d4( f) f8([ f] f4 g a) \quarterBar
  
  % Tu es Deus meus, *
  f4( g \initioDebilis f16 d4) d( \quilisma e16 f4 \initioDebilis e16 d4) d( \quilisma e16 f4 g8[ f \oriscus f e] f4) f( e) \halfBar
  
  % in manibus tuis
  f8([ g a g] a4) f( f \initioDebilis e16 d4) f( f g f) f \halfBar
  
  % tempora mea.
  f8([ f] f4) d4( c) c8([ e] d4) d( e d2) \doubleBar
  
}

text = \lyricmode {
  In you have I put my trust, O Lord; \markup { * "I"} said: You are my God, my des -- ti -- ny is in your hands.
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
      instrumentName = "OF. II"
      \consists Custos_engraver
      \override Custos.style = #'medicaea
    }
  }
}
