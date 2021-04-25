import simpy
from simulation_pkg import *


class Highway(object):
    '''
    Highway assigns any incoming car onto a constant- or varying-cost (CC, VC) road.
    '''

    def __init__(self, env, t_road_const, coef_road_var, t_connector, t_inter, t_buslane,
                 bus_penalty_c1, bus_penalty_v2, num_cars):
        self.env = env
    # The division of lanes: kind of road (c,v) = (CC, VC) and number of road (1,2,B = bus)
        self.lane_c1, self.lane_c2 = simpy.Resource(env, num_cars), simpy.Resource(env, num_cars)
        self.lane_v1, self.lane_v2 = simpy.Resource(env, num_cars), simpy.Resource(env, num_cars)
        self.connector, self.buslane = simpy.Resource(env, num_cars), simpy.Resource(env, num_cars)
        self.t_road_const = t_road_const
        self.coef_road_var = coef_road_var
        self.t_connector = t_connector
        self.t_inter = t_inter
        self.t_buslane = t_buslane
        self.bus_penalty_c1, self.bus_penalty_v2 = bus_penalty_c1, bus_penalty_v2
        self.predicted_v2_count = 0

    def road(self, car, type, num_cars, bus=False):
        if type == "CC":
            yield self.env.timeout(self.t_road_const + bus * self.bus_penalty_c1)
        elif type == "VC":
            yield self.env.timeout(self.coef_road_var * num_cars + bus * self.bus_penalty_v2)
        elif type == "buslane":
            yield self.env.timeout(self.t_buslane)

    def use_connector(self, car):
        yield self.env.timeout(self.t_connector)


def car(env, index, hw, results):
    '''
    The car process (each car has a name) arrives at the highway (hw) and requests an assigment.

    It then starts the driving process. After sufficient time passes (car gets through the road),
    highway assigns a car onto another road.
        - After a CC, it chooses VC;
        - After a VC, it chooses either CC, or connector + VC.
    Then it exits our simulation.
    '''
    name = 'Car %d' % index

    type, lane, bus, connector = choose(hw, 0)
    results.choices[0][index], results.bus[0][index] = type, bus
    with lane.request() as request:
        yield request
        start = env.now
        results.log.append('%s starts going down the highway at %.2f. Road chosen: %s. \n' % (name, start,
                                                                                              type))
        yield env.process(hw.road(name, type, lane.count, bus))

    if type != "buslane":
        # Assume by the time car exist the connector cars, that were at V2 at the start, have left
        if connector == True:
            type = "CC"
            with hw.connector.request() as request:
                results.log.append('%s uses the connector! At %.2f. \n' % (name, env.now))
                yield env.process(hw.use_connector(name))

        type, lane, bus = choose(hw, 1, type)
        results.choices[1][index], results.choices[2][index], results.bus[1][index] = connector, type, bus
        with lane.request() as request:
            yield request
            results.log.append('%s continues down the highway at %.2f. Road chosen: %s. \n' % (name, env.now,
                                                                                               type))
        # We add cars from the connector, assuming they will manage to reach the lane (no impact on C2)
            yield env.process(hw.road(name, type, lane.count + hw.connector.count, bus))
            results.log.append('%s leaves the highway at %.2f. \n' % (name, env.now))
    else:
        results.choices[1][index], results.choices[2][index], results.bus[1][index] = False, "buslane", bus

    cost = env.now - start
    results.costs[index] = cost
