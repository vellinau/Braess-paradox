from simulation_pkg.plot_tools import util
from celluloid import Camera
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os.path


def iterated_results(df, xlabel, filename=""):
    '''
    Plot sim results based on parameter changing during iterations.
    '''
    from config import static_plotdir

    fig = plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.plot(df["parameter_values"], df["mean_costs"])
    plt.ylabel("Łączny koszt drogi", fontsize=14), plt.xlabel(xlabel, fontsize=14)
    plt.ylim(60, 90)
    plt.subplot(1, 2, 2)
    if filename == "t_connector":
        for path in df["decision_count"].keys():
            plt.plot(df["parameter_values"], df["decision_count"][path], label=path)
        plt.ylabel("Liczba kierowców na drodze", fontsize=14), plt.xlabel(xlabel, fontsize=14)
        plt.legend(fontsize=12)
    elif filename == "bus_penalty_v2":
        plt.plot(df["parameter_values"], data["bus_count"]["CD - bus"][index], "bo", label="Bus CD")
        plt.ylabel("Liczba pasażerów", fontsize=14), plt.xlabel(xlabel, fontsize=14)
        plt.legend()
    elif filename == "bus_penalty_c1":
        plt.plot(df["parameter_values"], data["bus_count"]["AC - bus"][index], "ro", label="Bus AC")
        plt.ylabel("Liczba pasażerów", fontsize=14), plt.xlabel(xlabel, fontsize=14)
        plt.ylim(-100, 4100)
        plt.legend()
    if filename != "":
        plt.savefig(os.path.join(static_plotdir, filename))
    plt.close()
    return fig


def dynamic(df, filename='', framerate=30):
    '''
    Animate and save selected simulation.
    '''
    from config import dynamic_plotdir

    names = ["AB", "AC", "AC - bus", "Buspas", "Łącznik", "BD", "CD", "CD - bus"]
    frame_coef = int(framerate/12)
    costs = util.make_cost(df)
    counts = util.make_counts(df, costs, int(df["mean_costs"][0]))
    progression = util.make_progression(costs, framerate=frame_coef)
    camera = Camera(plt.figure(figsize=(32, 18)))
    points = [[None] * len(names), [None] * len(names)]
    plt.axis('off')
    start_minutes = {}
    for name in names:
        i = 0
        while counts[name][i] == 0 and i < int(df["mean_costs"][0]) - 1:
            i += 1
        if i == int(df["mean_costs"][0]) - 1:
            i = 0
        start_minutes[name] = i

    for frame in range(int(df["mean_costs"][0]) * frame_coef):
        minute = int(np.floor(frame/frame_coef))
        plt.plot([0, 3, 6], [0, 4, 0], '--', color='k', alpha=0.3)
        plt.plot([0, 3, 6], [0, -4, 0], '--', color='k', alpha=0.3)
        plt.plot([3, 3], [4, -4], '--', color='k', alpha=0.3)
        arc = patches.Arc((3, 0), 8, 6, ls='--', angle=90, alpha=0.3, theta1=90, theta2=270)
        plt.gca().add_patch(arc)
        sizes = [None] * len(names)

        for name in names:
            local_minute = minute - start_minutes[name]
            index = names.index(name)
            size = counts[name][minute] * 2
            if size > 0 and local_minute * frame_coef < len(progression[name][0]):
                points[0][index] = progression[name][0][local_minute * frame_coef]
                points[1][index] = progression[name][1][local_minute * frame_coef]
                offset = 0.15 * len(str(int(size/2))) / 4
                plt.annotate(str(int(size/2)), xy=(points[0][index], points[1][index]), xytext=(
                    points[0][index] - offset, points[1][index] + np.sqrt(size)/180), fontsize=30)
            else:
                points[0][index], points[1][index] = None, None
            sizes[index] = size

        plt.scatter(*points, color="c", s=sizes, alpha=0.8)
        plt.text(6, -4, f"t = {minute}", fontsize=60)
        plt.text(5.95, 3.20, (f'łącznik: {costs["Łącznik"]} \nbuspas: {costs["Buspas"]} \n'
                              f'bus 1: {costs["AC - bus"] - costs["AC"] :+g} \n'
                              f'bus 2: {costs["CD - bus"] - costs["CD"] :+g}'),
                 fontsize=40)
        camera.snap()

    # Finishing touches (1 second)
    for _ in range(framerate):
        plt.plot([0, 3, 6], [0, 4, 0], '--', color='k', alpha=0.3)
        plt.plot([0, 3, 6], [0, -4, 0], '--', color='k', alpha=0.3)
        plt.plot([3, 3], [4, -4], '--', color='k', alpha=0.3)
        arc = patches.Arc((3, 0), 8, 6, ls='--', angle=90, alpha=0.3, theta1=90, theta2=270)
        plt.gca().add_patch(arc)
        sizes = [None] * len(names)

        for name in names:
            index = names.index(name)
            size = counts[name][-1] * 2
            if size > 0:
                points[0][index] = progression[name][0][-2]
                points[1][index] = progression[name][1][-2]
                offset = 0.15 * len(str(int(size/2))) / 4
                plt.annotate(str(int(size/2)), xy=(points[0][index], points[1][index]), xytext=(
                    points[0][index] - offset, points[1][index] + np.sqrt(size)/180), fontsize=30)
            else:
                points[0][index], points[1][index] = None, None
            sizes[index] = size

        minute = len(counts[name])
        plt.scatter(*points, color="c", s=sizes, alpha=0.8)
        plt.text(6, -4, f"t = {minute}", fontsize=60)
        plt.text(5.95, 3.20, (f'łącznik: {costs["Łącznik"]} \nbuspas: {costs["Buspas"]} \n'
                              f'bus 1: {costs["AC - bus"] - costs["AC"] :+g} \n'
                              f'bus 2: {costs["CD - bus"] - costs["CD"] :+g}'),
                 fontsize=40)
        camera.snap()

    anim = camera.animate(blit=False)
    if filename == '':
        filename = (f'connect.{costs["Łącznik"]}__buspas.{costs["Buspas"]}__'
                    f'cbus.{costs["AC - bus"] - costs["AC"]}__'
                    f'vbus.{costs["CD - bus"] - costs["CD"]}.mp4')
    anim.save(os.path.join(dynamic_plotdir, filename), fps=framerate, bitrate=-1)
