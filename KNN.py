import csv
import re
import os
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


# Faz todos os testes da @teste_list usando a @training_list e retorna uma matriz
# de confusao em forma de dict, sendo:
# ------------------------
# | keys | Quantidade de: |
# ------------------------
# | 'TP' | True Positive  |
# | 'TN' | True Negative  |
# | 'FP' | False Positive |
# | 'FN' | False Negative |
# ------------------------
def make_test(test_list, training_list):
    confusion_mtx = {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}
    for test in test_list:
        model_decision = KNN_decision(test, training_list)
        if (test[-1] == 1):
            if (model_decision == 1):
                confusion_mtx['TP'] += 1
            else:
                confusion_mtx['FN'] += 1
        else:
            if (model_decision == 1):
                confusion_mtx['FP'] += 1
            else:
                confusion_mtx['TN'] += 1

    return confusion_mtx


def inicialize_csv_header(csv_name):
    header = ['Parking_test', 'Training_list by', 'Accuracy', 'OER', 'TP', 'TN', 'FP', 'FN']
    with open(csv_name, mode='w', newline='') as result_csv:
        writer = csv.writer(result_csv, delimiter=';')
        writer.writerow(header)


def write_test_info_csv(csv_name, parking_name, training_name, con_mtx):
    num_testes = con_mtx['TP'] + con_mtx['TN'] + con_mtx['FP'] + con_mtx['FN']
    accuracy = (con_mtx['TP'] + con_mtx['TN']) / num_testes
    oer = 1.0 - accuracy
    parking_name = parking_name.split('_')[2].split('.')[0]
    if '_' in training_name:
        training_name = training_name.split('_')[2].split('.')[0]
    # Parking_test; training_list; accuracy; OER; TP; TN; FP; FN
    line_for_csv = [parking_name, training_name, accuracy, oer, con_mtx['TP'], con_mtx['TN'], con_mtx['FP'], con_mtx['FN']]
    with open(csv_name, mode='a', newline='') as info_test:
        writer = csv.writer(info_test, delimiter=';')
        writer.writerow(line_for_csv)


# Aplica o KNN na combinacao de teste e treino passada e retorna uma matriz de confusao.
def KNN_test_combination(test_name, training_name):
    teste_list = create_list_csv(test_name)
    training_list = create_list_csv(training_name)
    con_mtx = make_test(teste_list, training_list)
    return con_mtx;


# Faz KNN usando todos os arquivos de teste (usa muita RAM).
def test_with_all_trainings(csv_name, csv_dir, test_name_list, training_name_list):
    training_set = list()
    for training_name in training_name_list:
        training_set += create_list_csv(os.path.join(csv_dir, training_name))
    for test_name in test_name_list:
        test = create_list_csv(os.path.join(csv_dir, test_name))
        con_mtx = make_test(test, training_set)
        write_test_info_csv(csv_name, test_name, 'All trainings', con_mtx)


def run_tests_KNN():
    csv_dir_name = 'parkings_NFV_csv'
    if not os.path.exists(csv_dir_name):
        print('Diretorio de testes e treinos nao encontrado.')
        exit(1)
    training_re = r'training*'
    test_re = r'test*'
    files_csv = os.listdir(csv_dir_name)
    training_name_list = [f for f in files_csv if re.match(training_re, f)]
    test_name_list = [f for f in files_csv if re.match(test_re, f)]
    if (len(test_name_list) == 0 or len(training_name_list) == 0):
        print('Nao foi possivel localizar os arquivos de teste e treino.')
        exit(1)
    csv_name = 'results_KNN.csv'
    inicialize_csv_header(csv_name)

    for test_name in test_name_list:
        for training_name in training_name_list:
            con_mtx = KNN_test_combination(os.path.join(csv_dir_name, test_name), os.path.join(csv_dir_name, training_name))
            write_test_info_csv(csv_name, test_name, training_name, con_mtx)

    test_with_all_trainings(csv_name, csv_dir_name, test_name_list, training_name_list)


if __name__ == '__main__':
    run_tests_KNN()
