# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''

''' Esta modulo tem o intuito de trabalhar em conjunto do sistema operacional, 
trabalhando com diretorios, arquivos(Nao seus conteudos) e partes do sistema'''
import os
import time
from collections import deque
import shutil
from .Error import Ambiente_erro
 
def _tratar_path(diretorio):
    '''Esta função trata um caminho de pastas, deixando ela sempre no mesmo padrão para o entendimento do sistema operacional'''
    if(type(diretorio)==list):
        #verificando se o diretorio veio como lista de varias path
        for arquivo in diretorio:
            arquivo=arquivo.replace("\\", "/")
        dir=diretorio
    else:
        #caso seja uma string ele simplismente retorna as barras como padrão
        dir=diretorio.replace("\\", "/")
    return dir

def irDiretorio(diretorio):
    r'''Esta função muda seu diretorio na sua linha de comando para outro diretorio
        Exemplo:
        irDiretorio("C:/User/cafe")
        irDiretorio(r"C:\User\cade")'''
    #os.chdir é nativo de python e vai ate o diretorio que voce indicar
    try:
        os.chdir(_tratar_path(diretorio))
    except:
        Erro='\nEste diretorio não existe!'
        raise Ambiente_erro(Erro)

def criarPasta(nomePasta):
    '''Esta função cria um diretorio
        Exemplo:
        criarPasta("C:/User/NovaPasta")
        criarPasta("NovaPasta")<- Não ha necessidade de passar o caminho, ou pode se criar outros diretorios dentro de diretorios'''
    #os.mkdir é nativo de python e cria uma pasta no diretorio atual caso nao exista
    try:
        os.mkdir('./'+nomePasta)
    except:
        Erro='\nEste diretorio já existe!'
        raise Ambiente_erro(Erro)
   

def abrirPrograma(programa):
    r'''Esta função execulta um programa(que for execultavel como permissao)
    Exemplo:
    abrirPrograma("C:\Program Files (x86)\Notepad++\notepad++.exe")'''
    #os.startfile abre um arquivo executavel sem precisar fazer uma chamada direto na linha de comando somente passando o caminho
    try:
        os.startfile(_tratar_path(programa))
    except:
        Erro='\nNão foi possivel encontrar ou não existe este programa!'
        raise Ambiente_erro(Erro)
   

def comandLine(command):
    '''Esta função executa uma instrução na linha de comando, dentro do seu ditorio atual
    Exemplo:
       comandLine("mkdir novaPasta") '''
    #os.system abre a parte interavel no seu sistema operacional e executa comandos proprios para cadas sistema que for passo
    os.system(command)

def dia_mes_ano():
    '''Esta função retorna o dia, mes e ano da sua maquina
    Exemplo:
    valor=dia_mes_ano()
    print(valor)
    >>>[16,7,2018]
    '''
    #retira data local do sistema
    line=time.localtime()
    #adiciona em uma lista todos os dados
    line=list(line)
    #Cria um objeto pilha
    lis=deque()
    for h in line:
        #faz a interação com a pilha
        lis.appendleft(int(h))
        #adiciona os tres primeiros valores da lista (dia, mes , ano), e no final discarta as outras informações
        if(line.index(h) == 2):
            break
    return list(lis)

def path_atual(Com_seu_diretorio=True):
    '''Esta função retorna o caminho ate o seu diretorio, por parametro você pode retirar 
    com False a sua pasta atual da path, retornando somente o caminho
    Exemplos:
    path=path_atual()
    print(path)
    >>>C:/User/administrador/[pastaAtual]/
    Ou
    path=path_atual(False)
    print(path)
    >>>C:/User/administrador/
    '''
    
    diretorio=None
    # se o parametro: Com_seu_diretorio for True, Ele pega sua path atual, caso seja false o valor será de somente o caminho ate o diretorio 
    if(Com_seu_diretorio):
        diretorio=_tratar_path(str(os.getcwd()))
    elif(not Com_seu_diretorio):
        diretorio=_tratar_path(str(os.path.dirname(os.getcwd())))
        
    return diretorio+"/"

def copiar_aquivos_diretorio(path_arquivo1:str,path_arquivo2:str):
    r'''Esta função copia o conteudo de um arquico para outro arquivo, passando o caminho conseguimos colocar em outro
    diretorio
    Exemplo::
    copiar_aquivos_diretorio(r"C:\Users\administrador\Desktop\Cenarios.txt", "Features/Cenario.txt")'''
    Erro=r'''
        Para copiar um arquivo de diretorio, passe uma String do arquivo que deseja copiar e uma String do arquivo alvo
        Exemplo:
        copiar_aquivos_diretorio(r"C:\Users\administrador\Desktop\Cenarios.txt", "Features/Cenario.txt")'''
    #ajustar a path
    path_arquivo1=_tratar_path(path_arquivo1)
    path_arquivo2=_tratar_path(path_arquivo2)
    #se o tipo do original e da copia for string ele copiara
    if(type(path_arquivo1) == str and type(path_arquivo2) == str):
        try:
            shutil.copyfile(path_arquivo1, path_arquivo2)
        except:
            raise Ambiente_erro(Erro)
    else:
        
        raise Ambiente_erro(Erro)
    
    
def mover_arquivos_diretorio(path_arquivo1:str,path_2:str):
    r'''Esta função mode o conteudo de um arquico para outro diretorio
    Exemplo::
    mover_arquivos_diretorio(r"C:\Users\administrador\Desktop\Cenarios.txt", "Features/")'''
    Erro=r'''
        Para mover um arquivo de diretorio, passe uma String do arquivo que deseja copiar e uma String do diretorio alvo
        Exemplo:
        mover_arquivos_diretorio(r"C:\Users\administrador\Desktop\Cenarios.txt", "Features/")'''
    #ajustar a path
    path_arquivo1=_tratar_path(path_arquivo1)
    path_arquivo2=_tratar_path(path_2)
    #se o tipo do original e do diretorio for string ele movera o arquivo
    if(type(path_arquivo1) == str and type(path_2) == str):
        try:
            shutil.move(path_arquivo1, path_arquivo2)
        except:
            raise Ambiente_erro(Erro)
    else:
        
        raise Ambiente_erro(Erro)
        
def remover_arquivo(NomeArquivo:str):
    '''Esta função exclui um arquivo
    Exemplo:
    remover_arquivo('arquivo.txt')
    remover_arquivo('base/arquivo.txt')
    '''
    #remove o arquivo caso o mesmo exista
    NomeArquivo=_tratar_path(NomeArquivo)
    try:
        os.remove(NomeArquivo)
    except:
        Erro='''Este arquivo ou diretorio não existe!!'''
        raise Ambiente_erro(Erro)