#set page(
  paper: "a4",
  margin: (top: 2cm, bottom: 2cm, left: 1.5cm, right: 1.5cm),
  header: context {
    if counter(page).get().first() > 1 [
      #align(center)[#text(size: 8pt, fill: luma(120))[Minimum Polyhex Containing All One-Sided n-Hexes]]
    ]
  },
  footer: context {
    let current = counter(page).get().first()
    let total = counter(page).final().first()
    align(center)[#text(size: 8pt, fill: luma(120))[Page #current of #total]]
  },
)
#set text(font: "New Computer Modern", size: 9pt)

#align(center)[
  #text(size: 16pt, weight: "bold")[Minimum Polyhex Containing All One-Sided n-Hexes]
  #v(0.3em)
  #text(size: 10pt)[$a(n)$ = minimum number of hexagonal cells in an edge-connected polyhex that contains, under some rotation and translation, every one-sided $n$-hex. Pieces are equivalent up to rotation only (reflections are distinct).]
  #v(0.2em)
  #text(size: 10pt)[$a(1..7) = 1, 2, 4, 7, 11, 15, 21$]
  #v(0.2em)
  #text(size: 8pt, style: "italic")[Computed by Peter Exley, March 2026]
]
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)
#v(0.3em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(1) = 1$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[1 cells, 1 one-sided $n$-hexes, bbox 1 x 1, solved in 0.0s]
]
#v(0.2em)
#align(center)[
#box(width: 1.47cm, height: 1.32cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.2718cm, 0.6582cm), (1.0028cm, 1.1241cm), (0.4648cm, 1.1241cm), (0.1958cm, 0.6582cm), (0.4648cm, 0.1922cm), (1.0028cm, 0.1922cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(2) = 2$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[2 cells, 1 one-sided $n$-hexes, bbox 1 x 2, solved in 0.0s]
]
#v(0.2em)
#align(center)[
#box(width: 1.47cm, height: 2.29cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.2718cm, 0.6582cm), (1.0028cm, 1.1241cm), (0.4648cm, 1.1241cm), (0.1958cm, 0.6582cm), (0.4648cm, 0.1922cm), (1.0028cm, 0.1922cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.2718cm, 1.6358cm), (1.0028cm, 2.1017cm), (0.4648cm, 2.1017cm), (0.1958cm, 1.6358cm), (0.4648cm, 1.1699cm), (1.0028cm, 1.1699cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(3) = 4$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[4 cells, 3 one-sided $n$-hexes, bbox 2 x 3, solved in 0.0s]
]
#v(0.2em)
#align(center)[
#box(width: 2.31cm, height: 3.27cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.2718cm, 1.1470cm), (1.0028cm, 1.6129cm), (0.4648cm, 1.6129cm), (0.1958cm, 1.1470cm), (0.4648cm, 0.6811cm), (1.0028cm, 0.6811cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 0.6582cm), (1.8494cm, 1.1241cm), (1.3114cm, 1.1241cm), (1.0425cm, 0.6582cm), (1.3114cm, 0.1922cm), (1.8494cm, 0.1922cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 1.6358cm), (1.8494cm, 2.1017cm), (1.3114cm, 2.1017cm), (1.0425cm, 1.6358cm), (1.3114cm, 1.1699cm), (1.8494cm, 1.1699cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 2.6134cm), (1.8494cm, 3.0794cm), (1.3114cm, 3.0794cm), (1.0425cm, 2.6134cm), (1.3114cm, 2.1475cm), (1.8494cm, 2.1475cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(4) = 7$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[7 cells, 10 one-sided $n$-hexes, bbox 4 x 3, solved in 0.0s]
]
#v(0.2em)
#align(center)[
#box(width: 4.01cm, height: 4.25cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.2718cm, 0.6582cm), (1.0028cm, 1.1241cm), (0.4648cm, 1.1241cm), (0.1958cm, 0.6582cm), (0.4648cm, 0.1922cm), (1.0028cm, 0.1922cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 1.1470cm), (1.8494cm, 1.6129cm), (1.3114cm, 1.6129cm), (1.0425cm, 1.1470cm), (1.3114cm, 0.6811cm), (1.8494cm, 0.6811cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 2.1246cm), (1.8494cm, 2.5905cm), (1.3114cm, 2.5905cm), (1.0425cm, 2.1246cm), (1.3114cm, 1.6587cm), (1.8494cm, 1.6587cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 1.6358cm), (2.6961cm, 2.1017cm), (2.1581cm, 2.1017cm), (1.8891cm, 1.6358cm), (2.1581cm, 1.1699cm), (2.6961cm, 1.1699cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 2.6134cm), (2.6961cm, 3.0794cm), (2.1581cm, 3.0794cm), (1.8891cm, 2.6134cm), (2.1581cm, 2.1475cm), (2.6961cm, 2.1475cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 3.5911cm), (2.6961cm, 4.0570cm), (2.1581cm, 4.0570cm), (1.8891cm, 3.5911cm), (2.1581cm, 3.1252cm), (2.6961cm, 3.1252cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.8118cm, 2.1246cm), (3.5428cm, 2.5905cm), (3.0048cm, 2.5905cm), (2.7358cm, 2.1246cm), (3.0048cm, 1.6587cm), (3.5428cm, 1.6587cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(5) = 11$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[11 cells, 33 one-sided $n$-hexes, bbox 3 x 6, solved in 1.0s]
]
#v(0.2em)
#align(center)[
#box(width: 3.16cm, height: 6.20cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.2718cm, 1.6358cm), (1.0028cm, 2.1017cm), (0.4648cm, 2.1017cm), (0.1958cm, 1.6358cm), (0.4648cm, 1.1699cm), (1.0028cm, 1.1699cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.2718cm, 2.6134cm), (1.0028cm, 3.0794cm), (0.4648cm, 3.0794cm), (0.1958cm, 2.6134cm), (0.4648cm, 2.1475cm), (1.0028cm, 2.1475cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 2.1246cm), (1.8494cm, 2.5905cm), (1.3114cm, 2.5905cm), (1.0425cm, 2.1246cm), (1.3114cm, 1.6587cm), (1.8494cm, 1.6587cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 3.1023cm), (1.8494cm, 3.5682cm), (1.3114cm, 3.5682cm), (1.0425cm, 3.1023cm), (1.3114cm, 2.6364cm), (1.8494cm, 2.6364cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 4.0799cm), (1.8494cm, 4.5458cm), (1.3114cm, 4.5458cm), (1.0425cm, 4.0799cm), (1.3114cm, 3.6140cm), (1.8494cm, 3.6140cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 0.6582cm), (2.6961cm, 1.1241cm), (2.1581cm, 1.1241cm), (1.8891cm, 0.6582cm), (2.1581cm, 0.1922cm), (2.6961cm, 0.1922cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 1.6358cm), (2.6961cm, 2.1017cm), (2.1581cm, 2.1017cm), (1.8891cm, 1.6358cm), (2.1581cm, 1.1699cm), (2.6961cm, 1.1699cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 2.6134cm), (2.6961cm, 3.0794cm), (2.1581cm, 3.0794cm), (1.8891cm, 2.6134cm), (2.1581cm, 2.1475cm), (2.6961cm, 2.1475cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 3.5911cm), (2.6961cm, 4.0570cm), (2.1581cm, 4.0570cm), (1.8891cm, 3.5911cm), (2.1581cm, 3.1252cm), (2.6961cm, 3.1252cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 4.5687cm), (2.6961cm, 5.0346cm), (2.1581cm, 5.0346cm), (1.8891cm, 4.5687cm), (2.1581cm, 4.1028cm), (2.6961cm, 4.1028cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 5.5464cm), (2.6961cm, 6.0123cm), (2.1581cm, 6.0123cm), (1.8891cm, 5.5464cm), (2.1581cm, 5.0805cm), (2.6961cm, 5.0805cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(6) = 15$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[15 cells, 147 one-sided $n$-hexes, bbox 6 x 6, solved in 14.0s]
]
#v(0.2em)
#align(center)[
#box(width: 5.70cm, height: 4.74cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.2718cm, 2.1246cm), (1.0028cm, 2.5905cm), (0.4648cm, 2.5905cm), (0.1958cm, 2.1246cm), (0.4648cm, 1.6587cm), (1.0028cm, 1.6587cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.2718cm, 3.1023cm), (1.0028cm, 3.5682cm), (0.4648cm, 3.5682cm), (0.1958cm, 3.1023cm), (0.4648cm, 2.6364cm), (1.0028cm, 2.6364cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 1.6358cm), (1.8494cm, 2.1017cm), (1.3114cm, 2.1017cm), (1.0425cm, 1.6358cm), (1.3114cm, 1.1699cm), (1.8494cm, 1.1699cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 2.6134cm), (1.8494cm, 3.0794cm), (1.3114cm, 3.0794cm), (1.0425cm, 2.6134cm), (1.3114cm, 2.1475cm), (1.8494cm, 2.1475cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 3.5911cm), (1.8494cm, 4.0570cm), (1.3114cm, 4.0570cm), (1.0425cm, 3.5911cm), (1.3114cm, 3.1252cm), (1.8494cm, 3.1252cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 2.1246cm), (2.6961cm, 2.5905cm), (2.1581cm, 2.5905cm), (1.8891cm, 2.1246cm), (2.1581cm, 1.6587cm), (2.6961cm, 1.6587cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 3.1023cm), (2.6961cm, 3.5682cm), (2.1581cm, 3.5682cm), (1.8891cm, 3.1023cm), (2.1581cm, 2.6364cm), (2.6961cm, 2.6364cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 4.0799cm), (2.6961cm, 4.5458cm), (2.1581cm, 4.5458cm), (1.8891cm, 4.0799cm), (2.1581cm, 3.6140cm), (2.6961cm, 3.6140cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.8118cm, 1.6358cm), (3.5428cm, 2.1017cm), (3.0048cm, 2.1017cm), (2.7358cm, 1.6358cm), (3.0048cm, 1.1699cm), (3.5428cm, 1.1699cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.8118cm, 2.6134cm), (3.5428cm, 3.0794cm), (3.0048cm, 3.0794cm), (2.7358cm, 2.6134cm), (3.0048cm, 2.1475cm), (3.5428cm, 2.1475cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (4.6584cm, 1.1470cm), (4.3894cm, 1.6129cm), (3.8514cm, 1.6129cm), (3.5825cm, 1.1470cm), (3.8514cm, 0.6811cm), (4.3894cm, 0.6811cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (4.6584cm, 2.1246cm), (4.3894cm, 2.5905cm), (3.8514cm, 2.5905cm), (3.5825cm, 2.1246cm), (3.8514cm, 1.6587cm), (4.3894cm, 1.6587cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (5.5051cm, 0.6582cm), (5.2361cm, 1.1241cm), (4.6981cm, 1.1241cm), (4.4291cm, 0.6582cm), (4.6981cm, 0.1922cm), (5.2361cm, 0.1922cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (5.5051cm, 1.6358cm), (5.2361cm, 2.1017cm), (4.6981cm, 2.1017cm), (4.4291cm, 1.6358cm), (4.6981cm, 1.1699cm), (5.2361cm, 1.1699cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (5.5051cm, 2.6134cm), (5.2361cm, 3.0794cm), (4.6981cm, 3.0794cm), (4.4291cm, 2.6134cm), (4.6981cm, 2.1475cm), (5.2361cm, 2.1475cm))]
  ]
]
]
]
#v(0.5em)
#block(breakable: false, width: 100%)[
#align(center)[
  #text(size: 11pt, weight: "bold")[$a(7) = 21$]#text(size: 8pt, fill: rgb("#27AE60"), weight: "bold")[ \[PROVED\]]
  #h(0.5em)
  #text(size: 8pt)[21 cells, 620 one-sided $n$-hexes, bbox 8 x 5, solved in 1797.2s]
]
#v(0.2em)
#align(center)[
#box(width: 7.39cm, height: 5.72cm)[
  #place(top + left)[
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.2718cm, 3.1023cm), (1.0028cm, 3.5682cm), (0.4648cm, 3.5682cm), (0.1958cm, 3.1023cm), (0.4648cm, 2.6364cm), (1.0028cm, 2.6364cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (1.2718cm, 4.0799cm), (1.0028cm, 4.5458cm), (0.4648cm, 4.5458cm), (0.1958cm, 4.0799cm), (0.4648cm, 3.6140cm), (1.0028cm, 3.6140cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 0.6582cm), (1.8494cm, 1.1241cm), (1.3114cm, 1.1241cm), (1.0425cm, 0.6582cm), (1.3114cm, 0.1922cm), (1.8494cm, 0.1922cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 1.6358cm), (1.8494cm, 2.1017cm), (1.3114cm, 2.1017cm), (1.0425cm, 1.6358cm), (1.3114cm, 1.1699cm), (1.8494cm, 1.1699cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 2.6134cm), (1.8494cm, 3.0794cm), (1.3114cm, 3.0794cm), (1.0425cm, 2.6134cm), (1.3114cm, 2.1475cm), (1.8494cm, 2.1475cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.1184cm, 3.5911cm), (1.8494cm, 4.0570cm), (1.3114cm, 4.0570cm), (1.0425cm, 3.5911cm), (1.3114cm, 3.1252cm), (1.8494cm, 3.1252cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 1.1470cm), (2.6961cm, 1.6129cm), (2.1581cm, 1.6129cm), (1.8891cm, 1.1470cm), (2.1581cm, 0.6811cm), (2.6961cm, 0.6811cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 2.1246cm), (2.6961cm, 2.5905cm), (2.1581cm, 2.5905cm), (1.8891cm, 2.1246cm), (2.1581cm, 1.6587cm), (2.6961cm, 1.6587cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 3.1023cm), (2.6961cm, 3.5682cm), (2.1581cm, 3.5682cm), (1.8891cm, 3.1023cm), (2.1581cm, 2.6364cm), (2.6961cm, 2.6364cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (2.9651cm, 4.0799cm), (2.6961cm, 4.5458cm), (2.1581cm, 4.5458cm), (1.8891cm, 4.0799cm), (2.1581cm, 3.6140cm), (2.6961cm, 3.6140cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.8118cm, 1.6358cm), (3.5428cm, 2.1017cm), (3.0048cm, 2.1017cm), (2.7358cm, 1.6358cm), (3.0048cm, 1.1699cm), (3.5428cm, 1.1699cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.8118cm, 2.6134cm), (3.5428cm, 3.0794cm), (3.0048cm, 3.0794cm), (2.7358cm, 2.6134cm), (3.0048cm, 2.1475cm), (3.5428cm, 2.1475cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.8118cm, 3.5911cm), (3.5428cm, 4.0570cm), (3.0048cm, 4.0570cm), (2.7358cm, 3.5911cm), (3.0048cm, 3.1252cm), (3.5428cm, 3.1252cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (3.8118cm, 4.5687cm), (3.5428cm, 5.0346cm), (3.0048cm, 5.0346cm), (2.7358cm, 4.5687cm), (3.0048cm, 4.1028cm), (3.5428cm, 4.1028cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (4.6584cm, 3.1023cm), (4.3894cm, 3.5682cm), (3.8514cm, 3.5682cm), (3.5825cm, 3.1023cm), (3.8514cm, 2.6364cm), (4.3894cm, 2.6364cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (4.6584cm, 4.0799cm), (4.3894cm, 4.5458cm), (3.8514cm, 4.5458cm), (3.5825cm, 4.0799cm), (3.8514cm, 3.6140cm), (4.3894cm, 3.6140cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (4.6584cm, 5.0576cm), (4.3894cm, 5.5235cm), (3.8514cm, 5.5235cm), (3.5825cm, 5.0576cm), (3.8514cm, 4.5916cm), (4.3894cm, 4.5916cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (5.5051cm, 3.5911cm), (5.2361cm, 4.0570cm), (4.6981cm, 4.0570cm), (4.4291cm, 3.5911cm), (4.6981cm, 3.1252cm), (5.2361cm, 3.1252cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (5.5051cm, 4.5687cm), (5.2361cm, 5.0346cm), (4.6981cm, 5.0346cm), (4.4291cm, 4.5687cm), (4.6981cm, 4.1028cm), (5.2361cm, 4.1028cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (6.3518cm, 4.0799cm), (6.0828cm, 4.5458cm), (5.5448cm, 4.5458cm), (5.2758cm, 4.0799cm), (5.5448cm, 3.6140cm), (6.0828cm, 3.6140cm))]
    #place(top + left)[#polygon(fill: rgb("#1ABC9C"), stroke: 0.3pt + black, (7.1984cm, 4.5687cm), (6.9294cm, 5.0346cm), (6.3914cm, 5.0346cm), (6.1224cm, 4.5687cm), (6.3914cm, 4.1028cm), (6.9294cm, 4.1028cm))]
  ]
]
]
]
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)