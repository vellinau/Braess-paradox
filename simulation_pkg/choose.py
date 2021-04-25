def choose(hw, decision_point, type=None):
    '''
    Make a choice for the car at selected decision points.
    '''
    costs, min_cost = {}, {}
    if decision_point == 0:
        # At the first junction, GPS predicts traffic for the next one. No future cars
        costs[("VC", hw.lane_v1)] = [hw.coef_road_var * (hw.lane_v1.count + 1), [hw.t_road_const]]
        costs[("bus", hw.lane_c1)] = [hw.t_road_const + hw.bus_penalty_c1, []]
        if hw.t_buslane == -1:
            # Graf3: no buslane, lower road with car or bus penalty
            increment = 0.5
            costs[("CC", hw.lane_c1)] = [hw.t_road_const, []]
            costs_v2 = [hw.coef_road_var * (hw.predicted_v2_count + 0.5),
                        hw.coef_road_var * (hw.predicted_v2_count + 0.5) + hw.bus_penalty_v2]
            costs[("CC", hw.lane_c1)][1].extend(costs_v2)
        else:
            # Graf4: buslane, lower road with bus penalty only
            increment = 1
            costs[("buslane", hw.buslane)] = [hw.t_buslane, [0]]
            costs_v2 = [hw.coef_road_var * (hw.predicted_v2_count + 1) + hw.bus_penalty_v2]
        costs[("bus", hw.lane_c1)][1].extend(costs_v2)
        costs[("VC", hw.lane_v1)][1].extend([t + hw.t_connector for t in costs_v2])

        predicted_connector = {}
        for key in costs.keys():
            min_cost[key] = costs[key][0] + min(costs[key][1])
            if key == ("VC", hw.lane_v1) and min(costs_v2) + hw.t_connector <= min(costs[key][1]):
                predicted_connector[key] = True
            else:
                predicted_connector[key] = False
        type, lane = min(min_cost, key=min_cost.get)
        hw.predicted_v2_count += predicted_connector[type, lane] * increment
        bus = (type == "bus")
        connector = predicted_connector[type, lane]
        if type == "bus":
            type, bus = "CC", True
        return type, lane, bus, connector

    if decision_point == 1:
        if type == "VC":
            # Upper road
            type, lane, bus = "CC", hw.lane_c2, False
        elif type in ["CC", "bus"]:
            # Lower road
            if hw.t_buslane == -1:
                bus = hw.bus_penalty_v2 <= 0
                type, lane = "VC", hw.lane_v2
            else:
                type, lane, bus = "VC", hw.lane_v2, True
        return type, lane, bus
