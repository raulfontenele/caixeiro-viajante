import numpy as np
import math
import random as rd

def criarArquivoCoordenadas():
    coorX = open("coordenadaX.txt","r")
    coorY = open("coordenadaY.txt","r")
    coorXY = open("coordenadaXY.txt",'a')

    for row in coorX:
        cx = row.replace("\n",'')
        cy = coorY.readline()
        coorXY.write(cx + "," + cy)

def criarMatrizCoordenadas():

    coorX = open("coordenadaX.txt","r")
    coorY = open("coordenadaY.txt","r")

    croms = []
    
    for row in coorX:
        coorXY = [int(row),int(coorY.readline())]
        croms.append(coorXY)

    return croms

def calcularFitness(populacao):
    # Recuperar matriz de coordenadas
    mtrCoor = criarMatrizCoordenadas()

    #Criar lista de avaliações de fitness
    fitness = np.zeros(len(populacao))

    i = 0
    for croms in populacao:
        dist = 0
        for index in range(len(croms)-2):
            dist += math.sqrt( (mtrCoor[int(croms[index])][0]- mtrCoor[int(croms[index+1])][0])**2 + (mtrCoor[int(croms[index])][1]- mtrCoor[int(croms[index+1])][1])**2   ) 
        fitness[i] = 1/dist
        i+=1
    return fitness

def criarPopulacao(tamanho):

    qtdCidades = 100

    # Criar lista com cidades
    cidades = []
    auxCidades = []
    for index in range(qtdCidades):
        cidades.append(index)

    populacao = []

    for i in range(tamanho):
        auxCidades.extend(cidades)
        cromossomo = np.zeros(qtdCidades)
        for value in range(qtdCidades):
            index = rd.randint(0,len(auxCidades)-1)
            cromossomo[value] = auxCidades[index]
            auxCidades.pop(index)
        populacao.append(cromossomo)
    
    return populacao

def roleta(populacao,fitness):

    #criar roleta
    roulette = fitness/np.sum(fitness)

    novosPais = []

    for i in range(2):

        #sortear número
        num = rd.random()

        acc = 0
        for index in range(len(fitness)):
            acc += roulette[index]
            if (num<acc):
                novosPais.append(populacao[index])
                break

    return novosPais

def crossoverOrdem(pais):
    # Verificar quantas elementos serão selecionados
    num = rd.randint(1,len(pais[0]))

    # Adquirir indices a serem mutados
    values = np.zeros(num,dtype=int)
    
    indices = []
    
    for index in range(len(pais[0])):
        indices.append(index)

    for i in range(num):
        idc = rd.randint(0,len(indices)-1)
        values[i] =  idc
        indices.pop(idc)
    
    #Descobrir cidades selecionadas
    ordem = np.zeros((2, num))

    # Descobrir posição dos elementos
    for pai in range(len(pais)):
        idx = 0
        for i in range(len(pais[0])):
            for ind in values:
                if pai == 1:
                    if pais[0][i] == pais[1][ind]:
                        ordem[1][idx] = pais[1][ind]
                        idx += 1
                else:
                    if pais[1][i] == pais[0][ind]:
                        ordem[0][idx] = pais[0][ind]
                        idx += 1

    # Realizar reordenamento
    filhos = []
    for p in range(len(pais)):
        idx = 0 
        filho = np.zeros(len(pais[0]))
        for i in range(len(pais[0])):
            if i in values:
                filho[i] = ordem[p][idx]
                idx+=1
            else:
                filho[i] = pais[p][i]
        filhos.append(filho)

    print(filhos)
    


def caixeiroViajante(qtdGeracoes,qtdPopulacao,taxaCrossover, taxaMutacao):
    #Criar população inicial
    populacao = criarPopulacao(qtdPopulacao)

    for geracao in range(qtdGeracoes):
        #Realizar avaliações de fitness 
        fitness = calcularFitness(populacao) ##Não precisa estar dentro do for uma vez que forem salvas as avaliações de fitness

        #Gerar nova população através do método da roleta
        for i in range( int(qtdPopulacao/2) ):
            paisSelecionados = roleta(populacao,fitness)

            crossoverOrdem(paisSelecionados)

            ##Verificar a necessidade de crossover
            if rd.random() < taxaCrossover:
                ##Realizar crossover
                print("Realizou crossover")
                filhos = paisSelecionados
            else:
                print("Não Realizou crossover")
                filhos = paisSelecionados

            ##Verificar a necessidade de mutação
            if rd.random() < taxaMutacao:
                ##Realizar mutacao
                print("Realizou mutacao")
            else:
                novosFilhos = filhos
                print("Não realizou mutacao")
        
        #Ordenar pais e filhos por fitness


def main():

    qtdGeracoes = 1
    qtdPopulacao = 10
    taxaCrossover = 0.93
    taxaMutacao = 0.01

    caixeiroViajante(qtdGeracoes,qtdPopulacao,taxaCrossover,taxaMutacao)


main()