import csv
import numpy as np


# Calcula a distancia euclidiana entre 2 pontos.
def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1-x2)**2))


# Retorna uma lista de listas de floats vindos do csv passado.
def create_list_csv(csv_name):
    with open(csv_name, 'r') as file:
        file_csv = csv.reader(file, delimiter=';')
        file_list = list()
        for row in file_csv:
            file_list.append(np.array([float(i) for i in row]))
        return file_list


# Retorna a decisao do KNN sobre a vaga estar ocupada(1) ou nao(0) com base na 
# training_list passada.
def KNN_decision(test, training_list):
    # No calculo das distancia precisa do slicing :-1 para remover o label no final.
    distances = [euclidean_distance(test[:-1], hist[:-1]) for hist in training_list]
    # Pega o indice dos 3 mais proximos.
    knn_indexs = np.argsort(distances)[:3]
    # Acessa a classe da vaga dos indices dos 3 mais proximos na training_list. 
    best_of_three = (training_list[knn_indexs[0]][-1], training_list[knn_indexs[1]][-1], training_list[knn_indexs[2]][-1])
    majority = sum(best_of_three)
    return 1 if majority >= 2 else 0
