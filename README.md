# caixeiro-viajante

O presente repositório trás a abordagem utilizando algoritmo genético para o problema do caixeiro viajante. O problema visa determinar a menor rota que passem por todas as cidades.
As coordenadas X e Y das cidades encontram-se nos arquivos de texto nomeados de "coordenadaX.txt" e "coordenadaY.txt".

Para o problema foram utilizados os seguintes parâmetros:
Método de seleção: Roleta;
Operador de crossover: Ordem;
Método de mutação: Duas trocas;
Formação da nova população: Maiores avaliações de fitness entre pais e filhos.

Ao final do programa são gerados gráficos do histórico da melhor avaliação de fitness por geração e o gráfico da melhor rota.
A função caixeiroViajante() retorna a melhor rota encontrada, sua avaliação de fitness e sua geração.
