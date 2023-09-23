import numpy as np
import csv
import matplotlib.pyplot as plt


def make_results_list(csv_name):
    with open(csv_name, 'r') as file:
        file_csv = csv.reader(file, delimiter=';')
        results_list = list()
        for i, row in enumerate(file_csv):
            if i != 0:
                results_list.append(row[:3])
    for line in results_list:
        line[2] = float(line[2])

    return results_list


def show_bars(title, xlabel, y_ticks):
    plt.title(f'{title} tests', fontsize=18)
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel('Accuracy', fontsize=16)
    plt.yticks(y_ticks)
    plt.show()


results = make_results_list('results_KNN.csv')
parking_test = results[0][0]
y_ticks = [0.1 * i for i in range(0, 11)]
count = 0
for line in results:
    if line[0] != parking_test:
        show_bars(parking_test, 'Trainings set', y_ticks)
        count = 0
        parking_test = line[0]

    plt.bar(line[1], line[2], ec='black')
    plt.text(count, line[2], round(line[2], 2), ha='center', va='bottom')
    count += 1

show_bars(parking_test, 'Trainings set', y_ticks)

parkings = list()
precision_alt = list()
for line in results[-3:]:
    parkings.append(line[0])
    precision_alt.append(line[2])

show_bars(results[-1][1], 'Parkings', y_ticks)
