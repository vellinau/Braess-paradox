from numpy.random import poisson
from simulation_pkg import *
from statistics import mean
import simpy


class Results(object):
    def __init__(self, num_cars):
        '''
        Initialize following raw results:
            - .log: text log from simulation,
            - .costs: list of cost per car index,
            - .choices: list of all 3 choices per car index,
            - .bus: list of all 2 bus choices per car index.
        '''
        self.log = []
        self.costs = [None] * num_cars
        self.choices = [[None] * num_cars, [None] * num_cars, [None] * num_cars]
        self.bus = [[None] * num_cars, [None] * num_cars]


def setup(env, t_road_const, coef_road_var, t_connector, t_inter, t_buslane, bus_penalty_c1,
          bus_penalty_v2, max_num_cars, num_init_cars, results):
    '''
    Create a highway system, n initial cars, and keep creating cars approx. every t_inter minutes.
    '''

    # Create the highway system
    hw = Highway(env, t_road_const, coef_road_var, t_connector, t_inter, t_buslane, bus_penalty_c1,
                 bus_penalty_v2, max_num_cars)
    # GPS predictions: Without any connector, exactly half of initial cars would go V2
    if t_buslane == -1:
        cost_bus_c1 = min(0, bus_penalty_c1)
        hw.predicted_v2_count = num_init_cars/2 - \
            min(0, (bus_penalty_v2 + cost_bus_c1) / coef_road_var)/2
    else:
        cost_bus_c1 = bus_penalty_c1
        hw.predicted_v2_count = 0
    # Create 'num_init_cars' initial cars
    for i in range(num_init_cars):
        env.process(car(env, i, hw, results))

    # Create more cars while the simulation is running, with GPS predictions
    while i + 1 < max_num_cars:
        previous_v2_count = hw.lane_v2.count
        yield env.timeout(poisson(t_inter))
        i += 1
        env.process(car(env, i, hw, results))
        if coef_road_var * hw.predicted_v2_count < t_road_const - t_connector:
            hw.predicted_v2_count += 0.5
    # Correction for cars that leave V2 road
        hw.predicted_v2_count += 0.5 - max(hw.lane_v2.count - previous_v2_count, 0)


def run(iterations=1, add_max=0, parameter_position=3):
    '''
    Run simulation and extract useful data. Change iterations > 1 to iterate parameter (determined
    by parameter_position) over an interval of [current_value, current_value+add_max].
    '''
    from config import T_ROAD_CONST, COEF_ROAD_VAR, T_CONNECTOR, T_INTER, T_BUSLANE, BUS_PENALTY_C1, BUS_PENALTY_V2, NUM_CARS, NUM_INIT_CARS

    data = {"mean_costs": [None] * iterations, "parameter_values": [None] * iterations,
            "decision_count": {"AB": [None] * iterations, "AC": [None] * iterations,
                               "BD": [None] * iterations, "CD": [None] * iterations, "Łącznik": [None] * iterations},
            "bus_count": {"AC - bus": [None] * iterations, "CD - bus": [None] * iterations,
                          "Buspas": [None] * iterations}}
    add_iterated = 0
    # Create an environment and start the setup process
    env = simpy.Environment()
    parameters = [env, T_ROAD_CONST, COEF_ROAD_VAR, T_CONNECTOR, T_INTER,
                  T_BUSLANE, BUS_PENALTY_C1, BUS_PENALTY_V2, NUM_CARS, NUM_INIT_CARS]
    for index in range(iterations):
        raw_data = Results(NUM_CARS)
        parameters.append(raw_data)
        env.process(setup(*tuple(parameters)))
        env.run()
        assert raw_data.costs == [mean(raw_data.costs)] * NUM_CARS
        if iterations > 1:
            add_iterated = add_max / (iterations - 1)
        data["parameter_values"][index] = parameters[parameter_position]
        parameters[parameter_position] += add_iterated
        data["mean_costs"][index] = mean(raw_data.costs)
        data["decision_count"]["AB"][index] = raw_data.choices[0].count("VC")
        data["decision_count"]["AC"][index] = raw_data.choices[0].count("CC")
        data["decision_count"]["Łącznik"][index] = sum(raw_data.choices[1])
        data["decision_count"]["BD"][index] = raw_data.choices[2].count("CC")
        data["decision_count"]["CD"][index] = raw_data.choices[2].count("VC")
        data["bus_count"]["AC - bus"][index] = sum(raw_data.bus[0])
        data["bus_count"]["CD - bus"][index] = sum(raw_data.bus[1])
        data["bus_count"]["Buspas"][index] = raw_data.choices[0].count("buslane")
    return data, raw_data
