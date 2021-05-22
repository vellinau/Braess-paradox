def check(df):
    '''
    Check whether simulation results do not disagree with theoretical properties of the model.
    '''
    from config import T_ROAD_CONST, COEF_ROAD_VAR, T_CONNECTOR, T_BUSLANE, BUS_PENALTY_C1, BUS_PENALTY_V2, NUM_CARS, NUM_INIT_CARS

    if T_ROAD_CONST == 45 and COEF_ROAD_VAR == 0.01 and NUM_CARS == 4000 and NUM_INIT_CARS == 4000 and BUS_PENALTY_C1 > 0 and BUS_PENALTY_V2 > 0:
        if T_BUSLANE == -1:
            if 0 <= T_CONNECTOR <= 5:
                assert df['mean_costs'][0] == 80 + T_CONNECTOR
                assert df['decision_count']['Łącznik'][0] == 4000
            if 5 < T_CONNECTOR <= 25:
                assert df['mean_costs'][0] == 90 - T_CONNECTOR
                assert df['decision_count']['AC'][0] == 100*T_CONNECTOR - 500
                assert df['decision_count']['Łącznik'][0] == 5000 - 200*T_CONNECTOR
            if 25 < T_CONNECTOR:
                assert df['mean_costs'][0] == 65
                assert df['decision_count']['AC'][0] == 2000
                assert df['decision_count']['Łącznik'][0] == 0
        if T_BUSLANE > 0 and T_CONNECTOR == 0:
            if 5 <= BUS_PENALTY_V2 <= 45 and 90 - BUS_PENALTY_V2 <= T_BUSLANE <= 85:
                assert df['mean_costs'][0] == T_BUSLANE
                assert df['decision_count']['AC'][0] == 0
                assert df['decision_count']['Łącznik'][0] == 100*(45 - BUS_PENALTY_V2)
                assert df['bus_count']['Buspas'][0] == 100*(85 - T_BUSLANE)
            if 0 <= BUS_PENALTY_V2 <= 45 and 80 <= T_BUSLANE <= 80 + BUS_PENALTY_V2:
                assert df['mean_costs'][0] == T_BUSLANE
                assert df['decision_count']['Łącznik'][0] == 50*(T_BUSLANE - BUS_PENALTY_V2)
                assert df['bus_count']['Buspas'][0] == 4000 - 50*(T_BUSLANE - BUS_PENALTY_V2)
            if BUS_PENALTY_V2 >= 45 and 45 <= T_BUSLANE <= 85:
                assert df['mean_costs'][0] == T_BUSLANE
                assert df['decision_count']['BD'][0] == 100*(T_BUSLANE - 45)
                assert df['bus_count']['Buspas'][0] == 4000 - 100*(T_BUSLANE - 45)
            if 5 <= BUS_PENALTY_V2 <= 45 and T_BUSLANE >= 85:
                assert df['mean_costs'][0] == 85
                assert df['decision_count']['BD'][0] == 100*(BUS_PENALTY_V2 - 5)
                assert df['decision_count']['Łącznik'][0] == 4000 - 100*(BUS_PENALTY_V2 - 5)
            if BUS_PENALTY_V2 >= 45 and T_BUSLANE >= 85:
                assert df['mean_costs'][0] == 85
                assert df['decision_count']['BD'][0] == 4000
            if 0 <= BUS_PENALTY_V2 <= 5 and T_BUSLANE >= 80 + BUS_PENALTY_V2:
                assert df['mean_costs'][0] == 80 + BUS_PENALTY_V2
                assert df['decision_count']['Łącznik'][0] == 4000
            if BUS_PENALTY_V2 >= T_BUSLANE and T_BUSLANE <= 45:
                assert df['mean_costs'][0] == T_BUSLANE
                assert df['bus_count']['Buspas'][0] == 4000
