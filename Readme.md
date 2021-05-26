# Braess paradox simulator

Simulate and create animations of traffic on a simple graph meant to illustrate the consequences of **Braess paradox!** The base graphs are in *\\schematics* directory.

## Cases implemented

In the package, we've implemented all of the base cases, as seen below (number *X.* corresponds to the *grafX.png* file in *\\schematics*). Other than that, we've implemented / tried to implement a few other functionalities, that came up either during the brainstorming, or as a natural generalization of work already done.

Different types of graph can be 'unlocked' via config.py. For 'classic' cases, stick to NUM_INIT_CARS = NUM_CARS = 4000.

 0. **(Virtually) no connector** --  set T_CONNECTOR >= 25 (with N = 4000).
 1. **Connector as a teleport** -- set T_CONNECTOR = 0.
 2. **With a 'penalty' for using the connector** -- set T_CONNECTOR > 0.
 3. **With bus penalty (no one chooses it)** -- set both BUS_PENALTY's > 0.
 3.5. **With bus premium** -- set at least one BUS_PENALTY < 0.
 4. **With bus-lanes** -- set T_BUSLANE != -1 (and > 0).
 5. **With cars not entering all at once** -- not working correctly:
	 * to access, set NUM_INIT_CARS < NUM_CARS and T_INTER > 0;
	 * how to set T_INTER for continuous flow? (open problem);
	 * and other things that wouldn't work right...
 6. **Untraditional cases** -- modify one of the following variables:
	 * T_ROAD_CONST != 45;
	 * COEF_ROAD_VAR != 0.01;
	 * NUM_CARS != 4000.
 7. **Combo cases** -- try more than one thing at once, like cases 2 + 4!

Only cases 0, 1, 2, 3 (without 3.5), 4 have solid, tested theoretical background. Run other cases at your own risk; possibly the simulator may not find the Nash equilibrium.
 
## Plotting and visualization

With methods from this package, you can either plot iterated results for simulations with one increasing variable, or animate results to an .mp4 file. Examples can be seen in *\\results* directory, in *\\plots_static* and *\\plots_dynamic* folders, respectively.

## Course webpage
> https://usosweb.mimuw.edu.pl/kontroler.php?_action=katalog2/przedmioty/pokazPrzedmiot&kod=1000-1S20MPZ

## Authors
Paweł Brachaczek, Jan Osowski (theoretical results, schematics)