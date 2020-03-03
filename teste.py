import numpy as np
import matplotlib.pyplot as plt
'''
array = np.array([1,7,3,4])
print(array)
array.itemset(3,8)
print(array)
array.sort()
print(array)

array1 = np.zeros(100)
print(array1)'''


'''
array1 = np.array([0,1,2,3,4,5,10])
array2 = np.array([7,3,6,1,8,2,0])

retorno = np.lexsort((array1,array2))
print(retorno)
print("-----------------------")
'''
array = np.array([7,3,6,1,8,2,0])
print(array)

retorno = np.argsort(array)
print(retorno)
'''
lista = [[1,2,3,4],[0],[10]]
print(lista[0])
print(lista[1])
print(lista[2])
'''
'''
#plt.ion()
lista = [[],[]]
array1 = np.array([0,1,2,3,4,5,10])
array2 = np.array([7,3,6,1,8,2,0])

for ele in range(len(array1)):
    lista[0].append(array1[ele])
    lista[1].append(array2[ele])

plt.plot(lista[0],lista[1])
plt.show()

    #plt.plot(ele,2,'bo')
    #plt.draw()
#plt.show()             #this plots correctly, but blocks execution.
    #plt.show(block = False)   #this creates an empty frozen window.
#plt.ioff()
#plt.show()'''