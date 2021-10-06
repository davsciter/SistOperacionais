'''
Para adicionar novos processos, confimar a adição, executar o programa: pressionar [ENTER]
'''


import random, time, threading

tempo = 0.05
#global entrada, execucao, processos
entrada=0
execucao=0
processos = []

class Processo(object):
    def __init__(self, nome, pid, tempodeExe, prioridade, UID, qtdeMemoria):
        self.nome = nome
        self.pid = pid
        self.tempodeExe = tempodeExe
        self.prioridade = prioridade
        self.UID = UID
        self.qtdeMemoria = qtdeMemoria

    def UsandoCPU(self):
        global tempo
        self.tempodeExe -= 1
        print("\nEm execução: %s\t\t[%s passos restantes]\n" % (self.nome, self.tempodeExe))
        time.sleep(tempo)
        return 


def LerTxt(array):
    with open('entradaEscalonador.txt', 'r', encoding="utf8") as file:
        split = file.readline().split('|')
        algoritmoDeEscalonamento = split[0]
        fracaodeCPU = int(split[1])
        for line in file.readlines()[0:]:
            split = line.split('|')
            array.append(Processo(split[0], int(split[1]), int(split[2]), int(split[3]), int(split[4]), int(split[5])))
    return algoritmoDeEscalonamento, fracaodeCPU


def Escalonar(array, algoritmo, fracao):
    #O criterio de parada respeita o tempo de CPU de cada processo, sem prempção
    if (algoritmo == 'alternanciaCircular'):
        atual = processos[0]
        while (len(array) > 0):
            marcador = 0
            for i in range(fracao):
                    if (array[0].tempodeExe > 1):
                        array[0].UsandoCPU()
                    else:
                        array[0].UsandoCPU()
                        marcador = 1
                        break
            if(marcador == 1 and len(array) > 0):
                array.pop(0)
            elif(marcador == 0 and len(array)>0):
                array.append(array.pop(0))
            if (entrada == 1):
                break

    elif (algoritmo == 'prioridade'):
        array.sort(key=lambda processo: processo.prioridade, reverse=True)
        aux = []
        while(len(array) > 0):
            pr_atual = array[0].prioridade

            #Cria vetor auxiliar com processos de mesma prioridade.

            while(pr_atual == array[0].prioridade):
                aux.append(array[0])
                array.pop(array.index(array[0]))
                if(len(array) == 0):
                    break

            while(len(aux)>0):
                for processo in aux:
                    for i in range(fracao):
                        if(processo.tempodeExe > 1):
                            processo.UsandoCPU()
                        else:
                            processo.UsandoCPU()
                            aux.pop(aux.index(processo))
                            break
                    if (entrada == 1):
                        for processo in aux:
                            if (processo.tempodeExe >= 1):
                                array.append(processo)
                                aux.pop(aux.index(processo))
                        break
                if (entrada == 1):
                    break
            if (entrada == 1):
                break


    elif (algoritmo == 'loteria'):
        while (len(array) > 0):
            loteria = random.choice(array)
            for i in range(fracao):
                if (loteria.tempodeExe > 1):
                    loteria.UsandoCPU()
                else:
                    loteria.UsandoCPU()
                    array.pop(array.index(loteria))
                    break
                    
                if(entrada==1):
                    break
            if(entrada==1):
                break

    else:
        print('Algoritmo Invalido')

def cria_thread(algoritmoDeEscalonamento,fracaodeCPU):
    thread = threading.Thread(target=Escalonar, args=(processos,algoritmoDeEscalonamento,fracaodeCPU),)
    return thread

algoritmoDeEscalonamento, fracaodeCPU = LerTxt(processos)
threadProc = threading.Thread(target=Escalonar, args=(processos,algoritmoDeEscalonamento,fracaodeCPU),)



while True:
    x = input('##\t\tGERENCIADOR DE PROCESSOS\t\t##\n[1] Definir tempo de clock\n[2] Inserir novo processo\nOu Aperte qualquer tecla para executar\n\n')
    try:
        if(int(x)==1):
            tempo = float(input('\nClock: '))
            print('\n')
        elif(int(x)==2):
            print('\nAdicione quantos processos desejar, e ao final pressione qualquer tecla para iniciar.')
            while True:
                processo = input('\nFormato: nome|pid|tempodeExecucao|prioridade|UID|qtdeMemoria\nValores invalidos ou nulos serão desconsiderados\nProcesso: ')
                proc = processo.split('|')
                processos.append(Processo(proc[0], int(proc[1]), int(proc[2]), int(proc[3]), int(proc[4]), int(proc[5])))
        else:
            print('\nExecutando: %s processos\nAlgoritmo: %s\nFração de CPU: %s clocks\nClock: %s segundos\nPressione [Enter] para adicionar processos durante a execução\nAguarde...' % (len(processos), algoritmoDeEscalonamento, fracaodeCPU, tempo))
            time.sleep(5)
            threadProc.start()
            break
    except:
        print(
            '\nExecutando: %s processos\nAlgoritmo: %s\nFração de CPU: %s clocks\nClock: %s segundos\nPressione [Enter] para adicionar processos durante a execução\nAguarde...' % (
            len(processos), algoritmoDeEscalonamento, fracaodeCPU, tempo))
        time.sleep(5)
        threadProc.start()
        execucao=1
        while(execucao==1):
            input()
            entrada=1
            time.sleep(1)
            try:
                processo = input("\nFormato: nome|pid|tempodeExecucao|prioridade|UID|qtdeMemoria\nValores invalidos ou nulos serão desconsiderados\nProcesso: ")
                proc = processo.split('|')
                processos.append(Processo(proc[0], int(proc[1]), int(proc[2]), int(proc[3]), int(proc[4]), int(proc[5])))
                print("\nPressione [ENTER] para confirmar.")
            except:
                entrada=0
                print("\nReiniciando gerenciamento...\n")
                time.sleep(1)
                threadProc = cria_thread(algoritmoDeEscalonamento,fracaodeCPU);
                threadProc.start();
        break
