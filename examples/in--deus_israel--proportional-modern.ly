\version "2.24.4"

#(set-global-staff-size 24)

\header {
  %{name%} title = "Deus Israel"
  office-part = "Introitus"
  mode = 3
  user-notes = "LU 1288"
  transcriber = "Andrew Hinkley & Patrick Williams"
  %{commentary%} composer = "Tob. 7:15 & 8:19, Ps. 127:1"
  annotation = "IN. III"
}

global = {
  \key c \major
  \cadenzaOn
  \omit Staff.TimeSignature
  \override Staff.StaffSymbol.color = #darkred
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
  \once \set fontSize = 4
}

liquescentAugmentativeDescending = {
  \once \override NoteHead.stencil = #ly:text-interface::print
  \once \override NoteHead.text = \markup \musicglyph "noteheads.ssolesmes.auct.desc"
  \once \set fontSize = 4
}

quarterBar = {
  \bar "'"
}

quarterBarAsterisk = {
  \quarterBar
  \once \override Score.TextScript.extra-offset = #'(-1.75 . -1.25)
  _ \markup { \with-color "red" * }
}

halfBar = {
  \bar ","
}

halfBarAsterisk = {
  \halfBar
  \once \override Score.TextScript.extra-offset = #'(-1.5 . -1.25)
  _ \markup { \with-color "red" * }
}
  

fullBar = {
  \bar "|"
}

doubleBar = {
  \bar "||"
}

doubleBarTP = {
  \doubleBar
  \once \override Score.TextScript.extra-offset = #'(-1.75 . -1.25)
  _ \markup { \italic \with-color "red" T.P. }
}

temporePaschale = {
  \once \override Score.TextScript.extra-offset = #'(-0.75 . -1.35)
  s2._\markup { \italic \with-color "red" T.P. }
}

verse = {
  \once \override Score.TextScript.extra-offset = #'(-0.75 . -1)
  s2.._\markup { \italic \with-color "red" ℣. }
}

melody = \transpose c c \relative c'' {
  \global

  % Deus Israel *
  g8([ c]) c([ c] c4) a a( \quilisma b16 c4 d8[ c] \oriscus c4) c( b) \quarterBarAsterisk
  % conjungat vos,
  g8([ \liquescentDiminutive a]) a([ c b c]) b([ \liquescentDiminutive a]) a4 \halfBar
  % et ipse sit vobiscum
  g4 a g g8([ f] a4) a a( \quilisma b16 c4 b4. a16[ g] a4) a( g2) \halfBar
  g8([ a c b]) c4 c c8([ c] c4) a \halfBar
  a4 a a8([ f] a4) a4( b8[ a] g4) a8([ g]) g2 \halfBar
  g4 a8([ c]) b4( c8[ c] g4 a c8[ c] a4) a4( f \quilisma g16 a8[ g] a4) a4( g) \halfBar
  g4 \initioDebilis g16( a4) a a( \quilisma b16 c4) g g( a) \halfBar
  f4 f e8([ \oriscus f8] a4) a g( f a8[ g] f4 g) e2 \doubleBar \break
  
  \temporePaschale \liquescentAugmentativeAscending e4 f4 g8([ \liquescentDiminutive f]) g4 \halfBar
  g8([ \liquescentDiminutive f]) g4( e f \quilisma g16 a4 g) g8([ a g a] f4 d \quilisma e16 f4 g8[ \liquescentDiminutive e]) e2 \doubleBar \break
  
  \verse g4 a8([ b]) b4 b b c d c c b8([ a]) c([ c] c2) \halfBarAsterisk
  a8([ g]) a([ \liquescentDiminutive b]) b4 b c8([ c c b]) a([ g]) a4 \liquescentAugmentativeDescending b \oriscus g4( a2) \doubleBar
  
  g4 a8([ b]) b4 b b \doubleBar
  c4 d c c b8([ \liquescentDiminutive a]) c([ c] c2) \doubleBar
  c4 d c b8([ \liquescentDiminutive a]) c([ c] c2) \doubleBar \break
  b4 c8([ c c b]) a([ g]) a4 b \oriscus g4( a2) \doubleBar \break
}

text = \lyricmode {
  DE -- us Is -- ra -- el
  con -- jún -- gat vos,
  et ip -- se sit vo -- bís -- cum,
  qui mi -- sér -- tus est
  du -- ó -- bus ú -- ni -- cis:
  et nunc, Dó -- mi -- ne,
  fac e -- os plé -- ni -- us
  be -- ne -- dí -- ce -- re te.
  
  %{T.P.%} Al -- le -- lú -- ia,
  al -- le -- lú -- ia.
  
  Be -- á -- ti om -- nes qui ti -- ment Dó -- mi -- num: %*
  qui ám -- bu -- lant in vi -- is e -- jus.
  
  Gló -- ri -- a Pa -- tri...
  Spi -- rí -- tu -- i Sanc -- to...
  Et nunc, et sem -- per...
  E u o u a e.
}

\score {
  <<
  \new Staff {
    \context Voice = "vocal" { \melody }
  }
  \new Lyrics \lyricsto "vocal" \text
  >>
  \layout {
    ragged-last = ##t
    \context {
      \Staff
      %{annotation%} instrumentName = "IN.III"
      \consists Custos_engraver
      \override Custos.style = #'medicaea
    }
  }
}

% score generated from https://github.com/AlexHarter/GregoLy on <DATE>
