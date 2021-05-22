# Config coefficients. Outside of COEF_ROAD_VAR, please use INTEGERS ONLY.
T_ROAD_CONST = 45       # Minutes it takes to drive through the road with constant cost
COEF_ROAD_VAR = 0.01    # Through the other road, the varying cost(n) == n * this coef
T_CONNECTOR = 12        # Minutes it takes to drive through the connecting road
NUM_CARS = 4000         # Number of cars in simulation
T_INTER = 0             # Approx. how often a new car enters a simulation
NUM_INIT_CARS = 4000    # How many cars are there at the start of simulation
BUS_PENALTY_C1 = 5      # Penalties for taking a bus // taking a road rebuilt to fit a buslane
BUS_PENALTY_V2 = 5      # (no difference yet, since those cost the same)
T_BUSLANE = -1          # Minutes it takes to drive through the buslane (all at once)

static_plotdir = 'results\\plots_static\\'
dynamic_plotdir = 'results\\plots_dynamic\\'
