import csv
import numpy as np

# Calcula a distancia euclidiana entre 2 pontos.
def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1-x2)**2))

# Retorna uma lista de listas de inteiros vindos do csv passado.
def create_list_csv(csv_name):
    with open(csv_name, 'r') as file:
        file_csv = csv.reader(file, delimiter=';')
        file_list = list()
        for row in file_csv:
            file_list.append(np.array([int(i) for i in row]))
        return file_list


training_list = create_list_csv('training_featuresVector.csv')
test_list = create_list_csv('test_featuresVector.csv')

# No calculo das distancia precisa do slicing :-1 para remover o label no final.
distances = [euclidean_distance(test_list[0][:-1], hist[:-1]) for hist in training_list]

# Pega o indice dos 3 mais proximos.
knn_indexs = np.argsort(distances)[:3]

best_of_three = (training_list[knn_indexs[0]][-1], training_list[knn_indexs[1]][-1], training_list[knn_indexs[2]][-1])
majority = sum(best_of_three)

if majority >= 2:
    print('Ocupada')
else:
    print('Vazia')

print(best_of_three)
