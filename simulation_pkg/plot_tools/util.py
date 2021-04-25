import numpy as np


def make_ellipse(resolution, theta1=0, theta2=180):
    '''
    Find coordinates of part of lower half-ellipse with selected resolution.
    '''
    x0 = 3
    a = 3  # x center, half width
    y0 = 0
    b = 4  # y center, half height
    x = a * np.cos(np.linspace(- (90 - theta1/2)/90 * np.pi,
                               (theta2/2 - 90)/90 * np.pi, resolution)) + x0
    x = np.sort(x)
    y = -np.sqrt(1 - ((x-x0)/a)**2) * b + y0
    return x, y


def make_line(resolution, startpoint, endpoint):
    '''
    Find coordinates of line from one point to another with selected resolution.
    '''
    x = np.linspace(startpoint[0], endpoint[0], resolution)
    y = np.linspace(startpoint[1], endpoint[1], resolution)
    return x, y


def make_cost(data):
    '''
    Count the costs from data about players' decisions.
    '''
    from config import T_ROAD_CONST, COEF_ROAD_VAR, T_CONNECTOR, T_BUSLANE, BUS_PENALTY_C1, BUS_PENALTY_V2

    names = ["AB", "AC", "AC - bus", "Buspas", "Łącznik", "BD", "CD", "CD - bus"]
    cost = {"AB": int(data["decision_count"]["AB"][0] * COEF_ROAD_VAR), "AC": int(T_ROAD_CONST),
            "AC - bus": int(T_ROAD_CONST + BUS_PENALTY_C1), "Buspas": int(T_BUSLANE),
            "Łącznik": int(T_CONNECTOR), "BD": int(T_ROAD_CONST),
            "CD": int((data["decision_count"]["CD"][0]) * COEF_ROAD_VAR),
            "CD - bus": int((data["decision_count"]["CD"][0]) * COEF_ROAD_VAR + BUS_PENALTY_V2)}
    return cost


def make_counts(data, cost, minutes):
    '''
    Determine how many cars were at different roads after each full minute.
    '''
    names = ["AB", "AC", "AC - bus", "Buspas", "Łącznik", "BD", "CD", "CD - bus"]
    counts = {}
    for name in names:
        counts[name] = [0] * minutes
        for minute in range(minutes):
            if name in ["AB", "AC"] and minute <= cost[name]:
                counts[name][minute] = data["decision_count"][name][0]
            elif name in ["AC - bus", "Buspas"] and minute <= cost[name]:
                counts[name][minute] = data["bus_count"][name][0]
            elif name == "Łącznik" and cost["AB"] <= minute <= cost["AB"] + cost[name]:
                counts[name][minute] = data["decision_count"][name][0]
            elif name == "BD" and minutes - cost[name] <= minute:
                counts[name][minute] = data["decision_count"][name][0]
            elif name == "CD" and minutes - cost[name] <= minute:
                counts[name][minute] = data["decision_count"][name][0] - \
                    data["bus_count"]["CD - bus"][0]
            elif name == "CD - bus" and minutes - cost[name] <= minute:
                counts[name][minute] = data["bus_count"][name][0]
    return counts


def make_progression(costs, framerate: int):
    '''
    Find dynamic coordinates of car progressing from one point to another based on chosen road and its cost.
    '''
    from config import T_BUSLANE

    if T_BUSLANE != -1:
        progression = {"AB": make_line(costs["AB"] * framerate, (0, 0), (3, 4)),
                       "AC": make_line(0, (0, 0), (3, -4)),
                       "AC - bus": make_line(costs["AC"] * framerate, (0, 0), (3, -4)),
                       "Buspas": make_ellipse(max(costs["Buspas"] * framerate, 0), 0, 180),
                       "Łącznik": make_line(costs["Łącznik"] * framerate, (3, 4), (3, -4)),
                       "BD": make_line(costs["BD"] * framerate, (3, 4), (6, 0)),
                       "CD": make_line(0, (3, -4), (6, 0)),
                       "CD - bus": make_line(max(costs["CD - bus"] * framerate, 0), (3, -4), (6, 0))}
    else:
        progression = {"AB": make_line(costs["AB"] * framerate, (0, 0), (3, 4)),
                       "AC": make_line(costs["AC"] * framerate, (0, 0), (3, -4)),
                       "AC - bus": make_ellipse(costs["AC"] * framerate, 0, 90),
                       "Buspas": make_ellipse(max(costs["Buspas"] * framerate, 0), 0, 180),
                       "Łącznik": make_line(costs["Łącznik"] * framerate, (3, 4), (3, -4)),
                       "BD": make_line(costs["BD"] * framerate, (3, 4), (6, 0)),
                       "CD": make_line(costs["CD"] * framerate, (3, -4), (6, 0)),
                       "CD - bus": make_ellipse(max(costs["CD - bus"] * framerate, 0), 90, 180)}
    return progression
