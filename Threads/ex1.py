import _thread as thread, random

indice_atual = 0     #Uma variável global que serve como guia para cada thread saber por onde começar na hora de inverter o vetor

def gerar_valores(id, array, n):
    while len(array) < n:
        random_num = random.randrange(0, 100)
        array.append(random_num)
        #print("\nThread [%s]: %s" % (id, array))       #Serve para analisar o vetor a partir de cada influencia das threads

def inverter_vetor(id, array, metade):
    global indice_atual
    while indice_atual < metade:
        aux = array[indice_atual]
        array[indice_atual] = array[len(array)-indice_atual-1]
        array[len(array)-indice_atual-1] = aux
        #print("\nThread [%s]: [%s]" % (id, array))
        indice_atual += 1


def main():
    array = []
    tam_array = int(input("\nDigite o tamanho do vetor:\0"))
    num_threads = int(input("\nDigite o numero de threads:\0"))

    conta_thread = 0
    while len(array) < tam_array:
        while conta_thread < num_threads:
            thread.start_new_thread(gerar_valores, (conta_thread+1, array, tam_array))   #Executa a função a partir da biblioteca _thread
            conta_thread+=1

    print("\nEntrada: "+str(array))

    metade_array = len(array) // 2                      #Só é necessário inverter até metade do vetor
    conta_thread = 0
    while indice_atual < metade_array:
        while conta_thread < num_threads:
            thread.start_new_thread(inverter_vetor, (conta_thread+1, array, metade_array))
            conta_thread += 1
    print("\nSaida: "+str(array))
main()
