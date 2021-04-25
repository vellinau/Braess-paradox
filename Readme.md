Simulating the graph that's meant to illustrate Braess paradox (cf. \\schematics).

Course webpage: https://usosweb.mimuw.edu.pl/kontroler.php?_action=katalog2/przedmioty/pokazPrzedmiot&kod=1000-1S20MPZ

Cases to implement:
  0. No connector
    Accomplished; for no connector, set T_CONNECTOR >= 25 (with N = 4000)
  1. Classic case
    Accomplished; set NUM_INIT_CARS = NUM_CARS and T_CONNECTOR = 0
  2. With a 'penalty' for using the connector
    Accomplished; set T_CONNECTOR > 0
  3. With bus penalty (no one chooses it)
    Accomplished; set both BUS_PENALTY's > 0
  3.5 What about no. of buses reducing the no. of cars?
    Normal, and social distancing versions (but is it Nash equilibrium?)
  4. With bus-lanes
    Accomplished; set T_BUSLANE != -1 (and >= 0)
  ?. With cars not entering all at once
    A bit not right
    Optimization: how to set T_INTER for continouous flow?
  ?. Randomized, with probability of ineffective allocation
    Not only ineffective GPS, but also % of people who don't use it (at one junction or at all)
  -------------------------------------------------
Things to do:
  - some more graphic representation?
  - try limiting no. of cars that can use CC road // buslane at once?
