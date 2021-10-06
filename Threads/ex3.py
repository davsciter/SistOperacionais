import threading, random, os, unicodedata

'''
Parte do codigo desenvolvido
em parceria com a dupla Thayllor dos Santos e Vinícius Ferreira, e a partir
de certo ponto cada um finalizou da melhor forma que pode
'''

class thread(threading.Thread):
    def __init__(self,texto,tipo, nome, mutex):
        self.texto = texto
        self.tipo = tipo
        self.mutex = mutex
        self.nome = nome
        self.resposta=[]
        threading.Thread.__init__(self)

    def run(self):
            with self.mutex:
                if(self.tipo=="palavras"):
                    quebra=False
                    palavras=[]
                    n_de_palavras=len(self.texto)
                    mais_numerosa='a'
                    vezes=1
                    for i in range(0, len(self.texto)):
                        add=True
                        for j in palavras:
                            if(self.texto[i] == str(j[0])):
                                j[1]+=1
                                if(j[1]>vezes):
                                    mais_numerosa=j[0]
                                    vezes=int(j[1])
                                add=False
                        if(add):
                            x = [self.texto[i], 1]
                            palavras.append(x)
                    self.resposta.append(mais_numerosa)
                    self.resposta.append(vezes)
                    self.resposta.append(n_de_palavras)

                elif(self.tipo== "letras"):
                    vogais = [["a", 0], ["e", 0], ["i", 0], ["o", 0], ["u", 0]]
                    consoantes=[]
                    consoanteM=""
                    vezes=0
                    for i in range(0, len(self.texto)):#for texto i =palavras
                        for j in self.texto[i]: #for palavra j = letras
                            add = True
                            if(j=="a" or j=="A"):
                                vogais[0][1]+=1
                            elif(j=="e" or j=="E"):
                                vogais[1][1]+=1
                            elif(j=="i" or j=="I"):
                                vogais[2][1]+=1
                            elif(j=="o" or j=="O"):
                                vogais[3][1]+=1
                            elif(j=="u" or j=="U"):
                                vogais[4][1]+=1
                            else:
                                for k in consoantes:
                                    if(j == k[0]):
                                        k[1]+=1
                                        if(k[1]>vezes):
                                            consoanteM=k[0]
                                            vezes=int(k[1])
                                        add=False
                                if(add):
                                    x = [j, 1]
                                    consoantes.append(x)
                    self.resposta.append(vogais)
                    self.resposta.append(len(consoantes))
                    self.resposta.append(consoanteM)
                    self.resposta.append(vezes)
                    self.resposta.append(consoantes)

                elif(self.tipo=="arquivo2"):
                    arquivo2 = open(("upper_"+ self.nome) , "w")
                    antigo = open(arquivo, "r")
                    for i in antigo:
                        arquivo2.write(i)
                    arquivo2.close()
                    antigo.close()
                    arquivo2 = open(("upper_"+ self.nome) , "r")
                    b = arquivo2.read()
                    b = unicodedata.normalize("NFD", b).encode("ascii", "ignore").decode("utf-8")
                    arquivo2.close()
                    arquivo2 = open(("upper_" + self.nome) , "w")
                    arquivo2.write(b.upper())
                else:
                    self.resposta="Nenhum arquivo"

caminhos = [os.path.join("arquivo", nome) for nome in os.listdir("arquivo")]
arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
stdoutmutex = threading.Lock()
nomes_arquivos = os.listdir("arquivo")

for i in range(0,len(arquivos)):
    arquivo=arquivos[i]
    texto=open(arquivo, "r")
    texto1=texto.read()
    texto1 = unicodedata.normalize("NFD", texto1).encode("ascii", "ignore").decode("utf-8")
    texto1= texto1.lower()
    texto_dividido= texto1.split()

    print("\nAnalise do arquivo: " + arquivo + "...")

    thread_n=thread(texto,"arquivo2",nomes_arquivos[i],stdoutmutex)
    thread_n.start()
    thread_n.join()

    tipos = ["palavras", "letras"]

    thread_p=thread(texto_dividido,tipos[0],"",stdoutmutex)
    thread_p.start()

    thread_l=thread(texto_dividido,tipos[1],"",stdoutmutex)
    thread_l.start()

    thread_p.join()
    print("\nO arquivo possui " + str(thread_p.resposta[2]) +" palavras e a palavra mais repetida é '" + str(thread_p.resposta[0]) + "', que se repete "+ str(thread_p.resposta[1]) + " vezes.")

    thread_l.join()
    vog="a"
    num_vogais = 0
    n=0
    mais=0
    for i in thread_l.resposta[0]:
        num_vogais+=i[1]
        if(i[1]>mais):
            mais=i[1]
            vog=i[0]
    for i in thread_l.resposta[4]:
        n+=i[1]
    print("\nO arquivo possui "+ str(num_vogais) + " vogais, sendo que '" + str(vog) + "' foi repetida "+ str(mais) +" vezes")
    print("\nO arquivo possui "+ str(thread_l.resposta[1]) + " consoantes diferentes e um total de " + str(n) +" consoantes.\nA consoante mais frequente foi '"+ str(thread_l.resposta[2]).lower() + "', "+ str(thread_l.resposta[3]) +" vezes." )