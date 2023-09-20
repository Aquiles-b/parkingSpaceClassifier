import cv2 as cv
import numpy as np
from skimage import feature
import csv
import os

# Retorna um historama da imagem passada.
def make_histogram(img, label_space):
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    lbp = feature.local_binary_pattern(img_gray, 8, 3, method='default')
    hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 256), range=(0, 255))
    # Coloca o label 0 (vazio) ou 1 (ocupado) no final do histograma.
    hist = np.append(hist, label_space)
    return list(hist)


# Escreve a lista de histogramas no final do arquivo csv.
def write_histograms(csv_name, hist_list):
    with open(csv_name, mode='a', newline=None) as hist_csv:
        writer = csv.writer(hist_csv, delimiter=';')
        writer.writerows(hist_list)


# Escreve em um csv o vetor de caracteristicas de todas as imagens 
# (indo de 16 em 16) dentro do diretorio imgs_dir.
def register_imgs_histogram_csv(csv_name, imgs_dir, label_space):
    imgs = os.listdir(imgs_dir)
    hist_list = list()
    counter = 0
    for img in imgs:
        img = cv.imread(os.path.join(imgs_dir, img))
        hist_list.append(make_histogram(img, label_space))
        counter += 1
        if (counter == 16):
            counter = 0
            write_histograms(csv_name, hist_list)
            hist_list.clear()
    write_histograms(csv_name, hist_list)


# Cria um csv de histogramas com delimitador ; de todas as imagens em imgs_path.
def create_csv_segmented_imgs(csv_name, imgs_path):
    for parking in os.listdir(imgs_path):
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
                        register_imgs_histogram_csv(csv_name, imgs_dir, label_space)


if __name__ == '__main__':
    imgs_path = os.path.join('PKLotSegmented', 'treino')
    if not os.path.exists(imgs_path):
        print('Erro: Caminho dos dados para treino nao encontrado.')
        exit(1)
    csv_name = 'featuresVector.csv'
    create_csv_segmented_imgs(csv_name, imgs_path)
