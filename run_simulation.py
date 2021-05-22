from simulation_pkg import simulation, theoretical
from simulation_pkg.plot_tools import plot

df, raw_data = simulation.run()
theoretical.check(df)
# print(''.join(raw_data.log)) # to get text log
plot.dynamic(df)
