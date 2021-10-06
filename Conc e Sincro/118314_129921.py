"""
Objetivo:
1) Criar n contas, criar n threads, fazer n operações.
2) Cada thread vai puxar uma operação aleatoria pra fazer numa conta aleatória Operações: credito, debito, saldo.
3) Saldo so pode ser feito em determinada conta se nenhuma thread estiver fazendo credito/debito sobre ela.
4) Os locks servirão para que as threads realizem somente 1 operação cada uma, sem que uma thread execute uma operação que outra thread já iria fazer.
5) Os semaphores limitarão o numero de threads que podem ocorrer em determinada conta. Semaphores tem por padrão valor 1.

Bibliotecas utilizadas: threading, random
"""

from threading import Thread, Lock, Semaphore
from random import randint, choice

N_OPER = 0

class Worker(Thread):
    def __init__(self, nome: str):
        super().__init__()
        self.nome = nome
        self.stoped = False

    def run(self):
        global N_OPER
        with Lock():
            if(N_OPER>0):
                N_OPER -= 1
                account = choice(contas)
                func = randint(1,3)
                if(func == 1):
                        print("\nConta %d\n\tDebito: $ %.2f\t\tThread: %s" % (account.cid, account.Debito(), self.nome))

                elif(func == 2):
                        print("\nConta %d\n\tCredito: $ %.2f\t\tThread: %s" % (account.cid, account.Credito(), self.nome))
                else:
                        print("\nConta %d\n\tSaldo: $ %.2f\t\tThread: %s" % (account.cid, account.Saldo(), self.nome))
                self.run()


class Conta(object):
    def __init__(self, cid: str):
        self.cid = cid
        self.saldo = 0

    def Credito(self):
        with Semaphore():
            valor = randint(1,200)
            self.saldo += valor
        return valor

    def Debito(self):
        with Semaphore():
            valor = randint(1,200)
            self.saldo -= valor
        return valor

    def Saldo(self):
        return self.saldo

def LerContas(array):
    print('\n\n')
    for i in array:
        result = ("\n[Conta %d] Saldo: $ %.2f" % (i.cid, i.Saldo()))
        print(result)

def CriarContas(array, n_contas):
    for i in range(n_contas):
        acc = Conta(i+1)
        array.append(acc)

def CriarThreads(array, n_threads):
    for i in range(n_threads):
        thrs = Worker(i+1)
        array.append(thrs)

def ExecutarThreads(array):
    [i.start() for i in array]
    [i.join() for i in array]

if __name__ == "__main__":
    contas = []
    threads = []
    inputs = [2,20,3]
    inpstr = ['Contas', 'Operações', 'Threads']
    print("\n####\tDefina o número desejado de contas, operações e threads\t\t####\n")

    for i in range(len(inputs)):
        try:
            inputs[i] = int(input("\n%s:\t" % inpstr[i]))
        except ValueError as e:
            print("Error: %s\t\t%s set as %d" % (str(e), inpstr[i], inputs[i]))

    n_cnt = inputs[0]
    N_OPER = inputs[1]
    N_THREADS = inputs[2]
    CriarContas(contas, n_cnt)
    CriarThreads(threads, N_THREADS)
    ExecutarThreads(threads)
    #LerContas(contas)