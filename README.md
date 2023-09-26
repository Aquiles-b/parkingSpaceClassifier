# parkingSpaceClassifier  
Esse projeto tem o objetivo de classificar vagas de estacionamento como ocupadas ou vazias. Foi usado como database a (Parking Lot Database)[https://web.inf.ufpr.br/vri/databases/parking-lot-database/], 
o programa é dividido em 3 etapas que giram em torno da estrutura dessa database.
## make_sets_PKLot.py:
  - Esse script percorre o diretório PKLot (ou PKLot/PKLot dependendo de como a database está no diretório do programa) recortando todas as vagas com base no XML que acompanha cada imagem, nesse processo é usado o script crop_parking_space.py.
    As imagens recortadas são distribuidas entre treino e teste dependendo da posição dos diretórios dos dias, posição ímpar vai para treino e posição par para teste. Dentro desses dois diretórios gerados, existem separações entre os estacionamentos
    presentes na PKLot (PUCPR, UFPR04 e UFPR05), dentro de cada um deles são criados outros dois diretórios separando as imagens de vagas vazias das ocupadas.

## LBP.py:
  - Gera um arquivo CSV de treino e um de teste para cada estacionamento com base na organização feita pelo make_sets_PKLot.py. Os CSVs são gerados aplicando o uso da técnica LBP, da qual é retirado um histograma como vetor de características de 256 posições
    com os valores normalizados, esse vetor é armazenado na planilha com uma posição a mais no final para identificar se representa uma vaga vazia ou ocupada.

## KNN.py:
  - Faz o arranjo de testes entre os arquivos de testes e treinos gerados no LBP.py. Usa a técnica do K-Nearest Neighbors, ela é aplicada no momento em que é apresentado um vetor de característica vindo de algum arquivo de teste e o script
    busca os 3 vetores de características mais próximos em distância euclidiana no arquivo de treino que está sendo usado no teste atual, com isso é feito um melhor de 3 para classificar a vaga. No final, é gerado uma planinha que mostra para cada teste a
    precisão do programa, overall error rate, positivos verdadeiros (TP), negativos verdadeiros (TN), positivos falsos (FP) e negativos falsos (FN).
