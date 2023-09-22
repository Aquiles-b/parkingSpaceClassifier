import cv2 as cv
import numpy as np
from skimage import feature
import csv
import os

# Normaliza o histograma usando o metodo min-max.
def normalize_hist(hist):
    hist = list(hist)
    sorted_index = np.argsort(hist)
    idx_max, idx_min = sorted_index[-1], sorted_index[0]
    max, min = hist[idx_max], hist[idx_min]
    div = max - min
    for idx, num_field in enumerate(hist):
        hist[idx] = (num_field - min) / div
    return hist

# Retorna um historama vindo de um processamento LBP da imagem passada.
def make_histogram(img, label_space):
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    lbp = feature.local_binary_pattern(img_gray, 8, 3, method='default')
    hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 256), range=(0, 255))
    hist = normalize_hist(hist)
    # Coloca o label 0 (vazio) ou 1 (ocupado) no final do histograma.
    hist = np.append(hist, label_space)
    return hist


# Escreve a lista de histogramas no final do arquivo csv.
def write_histograms_csv(csv_name, hist_list):
    with open(csv_name, mode='a', newline=None) as hist_csv:
        writer = csv.writer(hist_csv, delimiter=';')
        writer.writerows(hist_list)


# Escreve em um csv o vetor de caracteristicas de cada imagem em @imgs_dir
# dentro do diretorio imgs_dir.
def register_imgs_histogram_csv(csv_name, imgs_dir, label_space):
    imgs = os.listdir(imgs_dir)
    hist_list = list()
    for img in imgs:
        img = cv.imread(os.path.join(imgs_dir, img))
        hist_list.append(make_histogram(img, label_space))
    write_histograms_csv(csv_name, hist_list)


# Cria um csv de histogramas para cada estacionamento em imgs_path com delimitador ;
def create_csv_segmented_imgs(csv_name, imgs_path):
    for parking in os.listdir(imgs_path):
        csv_name_parking = f"{csv_name}{parking}.csv"
        for wheater in os.listdir(os.path.join(imgs_path, parking)):
            for day in os.listdir(os.path.join(imgs_path, parking, wheater)):
                for space_status in os.listdir(os.path.join(imgs_path, parking, wheater, day)):
                    label_space = -1
                    imgs_dir = os.path.join(imgs_path, parking, wheater, day, space_status)
                    if space_status == 'empty':
                        label_space = 0
                    elif (space_status == 'occupied'):
                        label_space = 1
                    if label_space != -1:
                        register_imgs_histogram_csv(csv_name_parking, imgs_dir, label_space)


if __name__ == '__main__':
    imgs_path_training = os.path.join('PKLotSegmented', 'treino')
    imgs_path_test = os.path.join('PKLotSegmented', 'teste')
    if not os.path.exists(imgs_path_training) or not os.path.exists(imgs_path_test):
        print('Erro: Caminho dos dados nao encontrado ou incompleto.')
        exit(1)
    path_dir_csv = 'parkings_NFV_csv'
    os.makedirs(path_dir_csv)
    # Cria csv do treino. (NFV = Normalized Features Vector)
    create_csv_segmented_imgs(os.path.join(path_dir_csv, 'training_NFV_'), imgs_path_training)
    # Cria csv do teste.
    create_csv_segmented_imgs(os.path.join(path_dir_csv, 'test_NFV_'), imgs_path_test)
