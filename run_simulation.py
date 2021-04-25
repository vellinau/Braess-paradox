from simulation_pkg import simulation
from simulation_pkg.plot_tools import plot


df, raw_data = simulation.run()
# print(''.join(raw_data.log))
plot.dynamic(df)
