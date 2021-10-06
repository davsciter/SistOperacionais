import threading, numpy as np

linha, coluna = [1,1]
matriz_R = []

class minhathread(threading.Thread):
    def __init__(self, id, A, B, mutex):
        self.id = id
        self.A = A
        self.B = B
        self.mutex = mutex
        threading.Thread.__init__(self)

    def run(self):
        with self.mutex:
            x=0
    """
    tentei por muito tempo criar uma função que multiplicasse matrizes MxN, de diferentes formas
    mas nao consegui chegar ao resultado sem apresentar erros ou crashar
    até consegui fazer pra matrizes NxN, mas na tentativa de refazer o código
    acabei perdendo o metodo antigo e me desmotivando
    """
threads = []
stdoutnutex = threading.Lock()

def main():
    global stdoutnutex, threads, matriz_R, linha, coluna

    min, max = 0,100

    lin_A = int(input("\nDigite o numero de linhas da matriz A: "))
    col_A = lin_B = int(input("\nDigite o numero de colunas da matriz A: "))
    print("\n##[O numero linhas da matriz B foi definido para o mesmo numero de colunas da matriz A]##")
    col_B = int(input("\nDigite o numero de colunas da matriz B: "))
    num_threads = int(input("\nDigite o numero desejado de threads: "))

    matriz_A = np.random.randint(min,max+1, size = (lin_A, col_A))
    matriz_B = np.random.randint(min,max+1, size = (lin_B, col_B))
    matriz_R = np.random.randint(0,1, size = (lin_A, col_B))

    print("\nMatriz A:\n %s" % matriz_A)
    print("\nMatriz B:\n %s" % matriz_B)

    i=0
    while i < num_threads:
        thread = minhathread(i, matriz_A, matriz_B, stdoutnutex)
        thread.start()
        threads.append(thread)
        i+=1

    for thread in threads:
        thread.join()
    print()

    matriz_X = np.dot(matriz_A, matriz_B)
    print("\nMatriz Esperada:\n %s" % matriz_X)
    print("\nMatriz Obtida:\n %s" % matriz_R)
main()