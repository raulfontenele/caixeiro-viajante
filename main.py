import numpy as np
import math
import random as rd
import matplotlib.pyplot as plt

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

    coord = []
    for row in coorX:
        coorXY = [int(row),int(coorY.readline())]
        coord.append(coorXY)

    return coord

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

    qtdCidades = tamanho

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
    roulette = fitness/np.sum(fitness) # ver a questão da quantidade de casas numérica

    novosPais = []

    for i in range(2):

        #sortear número
        num = rd.random()

        acc = 0
        for index in range(len(fitness)):
            acc += roulette[index]
            if num < acc:
                novosPais.append(populacao[index])
                break

    return novosPais

def crossoverOrdem(pais):
    # Verificar quantos elementos serão selecionados
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
                        break
                else:
                    if pais[1][i] == pais[0][ind]:
                        ordem[0][idx] = pais[0][ind]
                        idx += 1
                        break

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

    return filhos
    
def mutacaoDuasTroca(filho):

    # Selecionar elementos índices a serem trocados

    values = np.zeros(2,dtype=int)

    indices = []
    
    for index in range(len(filho)):
        indices.append(index)

    for i in range(2):
        idc = rd.randint(0,len(indices)-1)
        values[i] =  idc
        indices.pop(idc)
    
    # Realizar a troca
    varAux = filho[values[0]]
    filho[values[0]] = filho[values[1]]
    filho[values[1]] = varAux

    return filho

def novaPopulacao(pais,fitnessPais,filhos,fitnessFilhos,tamanhoPop):

    fitnessAux = np.concatenate((fitnessPais,fitnessFilhos))
    vetorAux = pais + filhos

    # Obtendo chave de ordenamento
    chaves = np.argsort(fitnessAux)

    # Criando nova populacao e novo vetor de fitness
    novaPopulacao = []

    for chave in chaves[len(vetorAux):len(pais)-1:-1]:
        novaPopulacao.append(vetorAux[chave])

    fitness = fitnessAux[chaves[len(vetorAux):len(pais)-1:-1]]

    return novaPopulacao,fitness

def plotCaminhoHistorico(rota,hist):
    coordenadas = criarMatrizCoordenadas()

    coorXY = np.zeros( (len(rota), 2) )

    for ind in range( len(rota) ):
        for eixo in range(2):
           coorXY[ind][eixo] =  coordenadas[int(rota[ind])][eixo]

    plt.subplot(211)

    for cid in range( len(rota) ):
        plt.text(coorXY[cid,0],coorXY[cid,1],chr(int(rota[cid]) + 65) )
        
    plt.plot(coorXY[:,0],coorXY[:,1],coorXY[:,0],coorXY[:,1],'bo')
    plt.title("Melhor rota por geração")

    plt.subplot(212)
    plt.plot(hist[1],hist[0])
    plt.title("Histórico de fitness por geração")
    plt.show()
    




def caixeiroViajante(qtdGeracoes,qtdPopulacao,taxaCrossover, taxaMutacao):
    #Criar população inicial
    populacao = criarPopulacao(qtdPopulacao)

    #Realizar avaliações de fitness 
    fitness = calcularFitness(populacao)
    
    histFit = [[],[]]

    # Inicializar o melhor global e sua respectiva geração

    for geracao in range(qtdGeracoes):
        
        novosFilhos = []

        #Gerar nova população através do método da roleta
        for i in range( int(qtdPopulacao/2) ):
            
            paisSelecionados = roleta(populacao,fitness)

            ##Verificar a necessidade de crossover
            if rd.random() < taxaCrossover:
                # Realizar crossover
                filhos = crossoverOrdem(paisSelecionados)
                #print("Realizou o crossOver")
            else:

                filhos = paisSelecionados

            ##Verificar a necessidade de mutação

            for filho in filhos:
                if rd.random() < taxaMutacao:
                    #Realizar mutacao
                    novosFilhos.append( mutacaoDuasTroca(filho) )
                else:
                    novosFilhos.append(filho)

        # Calcular fitness dos novos filhos
        fitnessFilhos = calcularFitness(novosFilhos)

        #Ordenar pais e filhos por fitness
        populacao,fitness = novaPopulacao(populacao,fitness,novosFilhos,fitnessFilhos,qtdPopulacao)

        # Guardar o melhor indivíduo 
        if geracao == 0:
            best = [[],[],[]]
            best[0] = populacao[0]
            best[1] = fitness[0]
            best[2] = geracao
        else:
            if fitness[0] > best[1]:
                best[0] = populacao[0]
                best[1] = fitness[0]
                best[2] = geracao

        # Gravar histórico de fitness por geração
        histFit[0].append(fitness[0])
        histFit[1].append(geracao+1)
    
    plotCaminhoHistorico(best[0],histFit)

    return best,histFit



def main():

    qtdGeracoes = 100
    qtdPopulacao = 10
    taxaCrossover = 0.95
    taxaMutacao = 0.35

    caixeiroViajante(qtdGeracoes,qtdPopulacao,taxaCrossover,taxaMutacao)
    




main()